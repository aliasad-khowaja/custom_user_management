from django.urls import path

from .views.role import RoleView, RoleDetail
from .views.user import UserView, UserDetail
from .views.login import LoginView

app_name = "login"

urlpatterns = [
    path('login', LoginView.as_view()),
    path('roles', RoleView.as_view()),
    path('roles/<int:pk>', RoleDetail.as_view()),
    path('users', UserView.as_view()),
    path('users/<int:pk>', UserDetail.as_view()),
]