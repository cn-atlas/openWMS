import threading
import time
from functools import partial
from django.db.models.signals import pre_save
from django.apps import apps
from django.conf import settings
from auditlog.models import LogEntry
from django.utils.deprecation import MiddlewareMixin
from auditlog.middleware import AuditlogMiddleware
from rest_framework_simplejwt.authentication import JWTAuthentication

threadlocal = threading.local()
METHOD_OVERRIDE_HEADER = 'HTTP_X_HTTP_METHOD_OVERRIDE'


class MethodOverrideMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and METHOD_OVERRIDE_HEADER in request.META:
            request.method = request.META[METHOD_OVERRIDE_HEADER]
        return self.get_response(request)


class GetUserAnywhereMiddleware:
    """
    from https://gist.github.com/rbtsolis/1db34b7d5a2ce9594f226cae414f9f12

    USAGE:
    # models.py or signals.py file
    from middlewares.middlewares import RequestMiddleware

    # First we need create an instance of that and later get the current_request assigned
    request = RequestMiddleware(get_response=None)
    request = request.thread_local.current_request
    """

    def __init__(self, get_response, thread_local=threading.local()):
        self.get_response = get_response
        self.thread_local = thread_local
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        self.thread_local.current_request = request
        # response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return self.get_response(request)


class XAuditlogMiddleware(AuditlogMiddleware):
    """
    Middleware to couple the request's user to log items. This is accomplished by currying the signal receiver with the
    user from the request (or None if the user is not authenticated).

    不知道跟直接使用 AuditlogMiddleware 有什么区别，但是加了这个修改人就对了，否则一直是 "system"
    """

    def process_request(self, request):
        """
        Gets the current user from the request and prepares and connects a signal receiver with the user already
        attached to it.
        """
        # Initialize thread local storage
        threadlocal.auditlog = {
            'signal_duid': (self.__class__, time.time()),
            'remote_addr': request.META.get('REMOTE_ADDR'),
        }

        # In case of proxy, set 'original' address
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            threadlocal.auditlog['remote_addr'] = request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0]
        # Connect signal for automatic logging
        if hasattr(request, 'user') and getattr(request.user, 'is_authenticated', False):
            set_actor = partial(self.set_actor, user=request.user, signal_duid=threadlocal.auditlog['signal_duid'])
            pre_save.connect(set_actor, sender=LogEntry, dispatch_uid=threadlocal.auditlog['signal_duid'], weak=False)

    @staticmethod
    def set_actor(user, sender, instance, signal_duid, **kwargs):
        """
        Signal receiver with an extra, required 'user' kwarg. This method becomes a real (valid) signal receiver when
        it is curried with the actor.
        """
        if hasattr(threadlocal, 'auditlog'):
            if signal_duid != threadlocal.auditlog['signal_duid']:
                return
            try:
                app_label, model_name = settings.AUTH_USER_MODEL.split('.')
                auth_user_model = apps.get_model(app_label, model_name)
            except ValueError:
                auth_user_model = apps.get_model('auth', 'user')
            if sender == LogEntry and isinstance(user, auth_user_model) and instance.actor is None:
                instance.actor = user

            instance.remote_addr = threadlocal.auditlog['remote_addr']


class JWTAuthMiddleware(MiddlewareMixin):
    """
    Convenience middleware for users of django-rest-framework-jwt.
    Fixes issue https://github.com/GetBlimp/django-rest-framework-jwt/issues/45
    """

    def get_user_jwt(self, request):
        from rest_framework.request import Request
        from rest_framework.exceptions import AuthenticationFailed
        from django.contrib.auth.middleware import get_user
        # from rest_framework_jwt.authentication import JSONWebTokenAuthentication

        user = get_user(request)
        if user.is_authenticated:
            return user
        try:
            user_jwt = JWTAuthentication().authenticate(Request(request))
            if user_jwt is not None:
                return user_jwt[0]
        except AuthenticationFailed:
            pass
        return user

    def process_request(self, request):
        from django.utils.functional import SimpleLazyObject
        assert hasattr(request, 'session'), \
            """The Django authentication middleware requires session middleware to be installed.
             Edit your MIDDLEWARE setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."""

        request.user = SimpleLazyObject(lambda: self.get_user_jwt(request))
