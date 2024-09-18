from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, email_verification, PasswordRecovery, toggle_activity_user, \
    ManagerListView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('email-confirm/<str:token>', email_verification, name='email-confirm'),
    path('recovery-password/', PasswordRecovery.as_view(), name='recovery_password'),
    path('user_activity/<int:pk>/', toggle_activity_user, name='user_activity'),
    path('manager/', ManagerListView.as_view(), name='manager'),
]
