import logging
import sys
from urllib.error import HTTPError

from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.utils.translation import gettext_lazy as _
from utils.vaptcha import tools

# from captcha import client
# from captcha.constants import TEST_PRIVATE_KEY, TEST_PUBLIC_KEY
# from captcha.widgets import ReCaptchaBase, ReCaptchaV2Checkbox
# from utils.vaptcha.widgets import VaptchaBase

logger = logging.getLogger(__name__)


class VaptchaField(forms.CharField):
    # widget = VaptchaV3
    default_error_messages = {
        "captcha_invalid": _("Error verifying VAPTCHA, please try again."),
        "captcha_error": _("Error verifying VAPTCHA, please try again."),
    }

    def __init__(self, public_key=None, private_key=None, *args, **kwargs):
        """
        ReCaptchaField can accepts attributes which is a dictionary of
        attributes to be passed to the ReCaptcha widget class. The widget will
        loop over any options added and create the RecaptchaOptions
        JavaScript variables as specified in
        https://developers.google.com/recaptcha/docs/display#render_param
        """
        super().__init__(*args, **kwargs)
        self.required = True

    def validate(self, value):
        super().validate(value)

        remote_ip = tools.get_remote_ip()

        try:
            vaptcha_result = tools.valid_shield(value, remote_ip=remote_ip)
            # {'msg': 'success', 'success': 1, 'score': 90}
        except HTTPError:  # Catch timeouts, etc
            raise ValidationError(
                self.error_messages["captcha_error"], code="captcha_error"
            )

        if not vaptcha_result.get("success") == 1:
            logger.warning(
                "VAPTCHA validation failed!"
            )
            raise ValidationError(
                self.error_messages["captcha_invalid"], code="captcha_invalid"
            )
        # print("*" * 100)
        # required_score = self.widget.attrs.get("required_score")
        # if not required_score:
        required_score = getattr(
            settings, "VAPTCHA_REQUIRED_SCORE", None
        )
        # Our score values need to be floats, as that is the expected
        # response from the Google endpoint. Rather than ensure that on
        # the widget, we do it on the field to better support user
        # subclassing of the widgets.
        required_score = float(required_score)

        # If a score was expected but non was returned, default to a 0,
        # which is the lowest score that it can return. This is to do our
        # best to assure a failure here, we can not assume that a form
        # that needed the threshold should be valid if we didn't get a
        # value back.
        score = float(vaptcha_result.get("score", 0))

        if required_score > score:
            logger.warning(
                "VAPTCHA validation failed due to its score of %s"
                " being lower than the required amount." % score
            )
            raise ValidationError(
                self.error_messages["captcha_invalid"], code="captcha_invalid"
            )
