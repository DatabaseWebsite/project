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
    path('userManage/add-user-to-course/', api.add_user_to_course),
    path('userMange/del-user-from-course/', api.del_user_from_course),

    path('course/create-course/', api.create_course),
    path('course/course-list/', api.course_list),
    path('course/all-participants/', api.all_participants),

    path('homework/create-homework/', api.create_homework),
    path('homework/modify-work/', api.modify_work),
    path('homework/remove-work/', api.delete_work),
    path('homework/works-info/', api.works_info),
    path('homework/work-detail/', api.work_detail),
    path('homework/work-submissions/', api.work_submissions),
    path('homework/work-submissions-detail/', api.work_submissions_detail),
    path('homework/submit-work-score/', api.submit_score),
    path('homework/student-work-detail/', api.student_work_detail),
    path('homework/student-submit-work/', api.student_submit_work),
    path('homework/get-pie/', api.get_pie),
    path('homework/get-avg/', api.get_avg),

    path('material/upload-materials/', api.upload_material),
    path('material/material-list/', api.material_list),
    # TODO: 没测没测没测！！！
    path('materail/download-multiple-materials/', api.download_multiple_materials),

    path('material/del-material/', api.delete_material),
    path('upload-image/', api.upload_image),
    path('userManage/reset-user-password/', api.reset_user_password),

    path('log/login-log/', api.login_log),
    path('log/search-login-log/', api.search_login_log),
    path('log/record-login-log/', api.record_login_log),
    path('log/operation-log/', api.operation_log),
    path('log/search-operation-log/', api.search_operation_log),
    path('log/record-operation-log/', api.record_operation_log),

    path('notice/create-notice/', api.create_notice),
    path('notice/edit-notice/', api.create_notice),
    path('notice/delete-notice/', api.delete_notice),
    path('notice/notice-list/', api.notice_list),

    path('message/send-message/', api.send_message_),
    path('message/message-list/', api.get_message),
    path('message/read-message/', api.read_message),
    path('message/unread-messages-count/', api.message_number),

    path('forum/create-post/', api.create_post),
    path('forum/post-list/', api.post_list),
    path('forum/delete-post/', api.delete_post),
    path('forum/create-reply/', api.create_reply),
    path('forum/get-post/', api.get_post),
    path('forum/topping-post/', api.topping_post),
    path('forum/cancel-topping-post/', api.cancel_topping_post),
    path('forum/subscribe-post/', api.subscribe_post),
    path('forum/cancel-subscribe-post/', api.cancel_subscribe_post),
    path('forum/elite-post/', api.elite_post),
    path('forum/cancel-elite-post/', api.cancel_elite_post),
    path('forum/like-reply/', api.like_reply),
    path('forum/dislike-reply/', api.dislike_reply),
    path('forum/like-post/', api.like_post),
    path('forum/dislike-post/', api.dislike_post),
    path('forum/search-posts/', api.search_posts),
    path('forum/word-cloud-map/', api.gen_word_cloud_map),

    path('courseManage/modify-identity/', api.modify_identity),

]
