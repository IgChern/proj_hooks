from .forms import LoginUserForm
from django.contrib.auth.views import LoginView
from .forms import LoginUserForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'app_users/login.html'
