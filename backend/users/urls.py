from django.urls import path

from . import api

urlpatterns = [
    path('login/', api.login_user),
    path('signup/', api.signup_user),
    # path('send-captcha/', api.send_mail),
    path('user-info/', api.get_user_info),
    path('refresh-token/', api.refresh_token),
    path('logout/', api.logout_user),

    path('change-password/', api.change_password),
    path('update-avatar/', api.update_avatar),
    path('create-course/', api.create_course),
    path('all-course-info/', api.all_course_info),
    path('update-selected-course/', api.update_selected_course),
    path('xlsx-create-user/', api.xlsx_create_user),
    path('user-list/', api.user_list),

    # TODO：后续接口测试
    path('create-homework/', api.create_homework),
    path('submit-homework/', api.submit_homework),

]
