from utils.vaptcha.fields import VaptchaField
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView


class CustomAuthenticationForm(AuthenticationForm):
    vaptcha = VaptchaField()


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'admin/login.html'
