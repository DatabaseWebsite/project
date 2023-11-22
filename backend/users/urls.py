from django.urls import path

from . import api

urlpatterns = [
    path('login/', api.login_user),
    path('signup/', api.signup_user),
    path('send-captcha/', api.send_mail),
    path('update-avatar/', api.update_avatar),
    path('user-info/', api.get_user_info),

]
