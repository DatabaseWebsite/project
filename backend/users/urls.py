from django.urls import path

from . import api

urlpatterns = [
    path('user/login/', api.login_user),
    path('user/signup-admin/', api.signup_admin),
    # path('user/send-captcha/', api.send_mail),
    path('user/user-info/', api.get_user_info),
    path('user/refresh-token/', api.refresh_token),
    path('user/logout/', api.logout_user),
    path('user/change-password/', api.change_password),
    path('user/update-avatar/', api.update_avatar),
    path('user/update-current-course/', api.update_current_course),
    path('user/user-selected-course/', api.user_selected_course),

    path('userManage/xlsx-create-users/', api.xlsx_create_users),
    path('userManage/update-user-info/', api.update_user_info),
    path('userManage/del-user/', api.delete_user),
    path('userManage/del-users/', api.delete_users),
    path('userManage/create-single-user/', api.create_single_user),
    path('userManage/search-users/', api.search_users),
    path('userManage/user-list/', api.user_list),
    path('userManage/all-course-info/', api.all_course_info),

    path('course/create-course/', api.create_course),
    path('course/all-participants/', api.all_participants),

    path('homework/create-homework/', api.create_homework),
    path('homework/homework-list/', api.homework_list),
    path('homework/submit-homework/', api.submit_homework),
    path('homework/submit-score/', api.submit_score),

    path('material/upload-material/', api.upload_material),
    path('material/material-list/', api.material_list),
    # TODO: 没测没测没测！！！
    path('materail/download-multiple-materials/', api.download_multiple_materials),

]
