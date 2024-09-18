from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, TemplateView, ListView
from users.forms import UserRegisterForm, UserProfilaForm, RecoveryForm
from users.models import User
from django.urls import reverse_lazy, reverse
import secrets
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER


class RegisterView(CreateView):
    """Контроллер для регистрации пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}'
        send_mail(
            subject='Подтверждение почты',
            message=f'Привет, перейди по ссылке для подтверждения почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    """Контроллер для просмотра профиля пользователя"""
    model = User
    form_class = UserProfilaForm
    success_url = reverse_lazy('main:home_view')

    def get_object(self, queryset=None):
        return self.request.user


class PasswordRecovery(TemplateView):
    """Контроллер для восстановления пароля"""
    model = User
    template_name = 'users/password_recovery_form.html'
    form_class = RecoveryForm

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return HttpResponse('Пользователя с таким email не существует!')
        new_pass = User.objects.make_random_password()
        user.set_password(new_pass)
        user.save()

        send_mail(
            subject='Вы запросили сброс пароля',
            message=f'Ваш новый пароль {new_pass}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return HttpResponseRedirect(reverse('users:login'))


def email_verification(request, token):
    """Контроллер для верификации пользователя"""
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


def toggle_activity_user(request, pk):
    """Контроллер для изменения статуса пользователя"""
    user_activity = get_object_or_404(User, pk=pk)
    if user_activity.is_active:
        user_activity.is_active = False
    else:
        user_activity.is_active = True
    user_activity.save()
    return redirect(reverse('users:manager'))


class ManagerListView(UserPassesTestMixin, ListView):
    """Контроллер для просмотра списка пользователей менеджером с возможностью их деактивации"""
    model = User
    template_name = 'users/manager.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.is_superuser:
            queryset = queryset
        else:
            queryset = queryset.filter(is_staff=False)
        return queryset
