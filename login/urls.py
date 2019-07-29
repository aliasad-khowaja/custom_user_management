from django.urls import path

from .views import RoleView, RoleDetail, UserView, UserDetail

app_name = "login"

urlpatterns = [
    path('roles', RoleView.as_view()),
    path('roles/<int:pk>', RoleDetail.as_view()),
    path('users', UserView.as_view()),
    path('users/<int:pk>', UserDetail.as_view()),
]