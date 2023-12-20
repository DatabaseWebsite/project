import os
import time

import openpyxl

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from rest_framework import status

from users.api.auth import jwt_auth, generate_token, generate_refresh_token, varify_captcha
from users.models import Course
from users.models.course_selection_record import CourseSelectionRecord
from users.models.user import User
from users.settings import ITEMS_PER_PAGE


@require_POST
def login_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        token = generate_token(user)
        refresh_token = generate_refresh_token(user)
        return JsonResponse(
            {"msg": "Login successful.", 'access': token, 'refresh': refresh_token, 'userId': username, 'username': user.name,  'code': 200},
            status=200)
    elif User.objects.filter(username=username).exists():
        return JsonResponse({"error": "密码错误", 'code': 401, "personId": username}, status=201)
    else:
        return JsonResponse({"error": "用户不存在", 'code': 401, "personId": username}, status=201)


@require_POST
def signup_admin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    name = request.POST.get('name')

    if username is None or password is None or email is None:
        return JsonResponse({"error": "内容未填写完整"}, status=405)
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "用户名已存在"}, status=405)
    if User.objects.filter(email=email).exists():
        return JsonResponse({"error": "邮箱已注册"}, status=405)
    if password == '':
        return JsonResponse({"error": "密码不能为空"}, status=405)

    # 使用 create_user 方法创建用户，它会处理密码的哈希存储
    User.objects.create_user(username=username, password=password, email=email, name=name, is_admin=True)

    return JsonResponse({"message": "管理员用户注册成功"}, status=200)


@jwt_auth()
@require_POST
def create_single_user(request):
    new_user_username = request.POST.get('person_id')
    new_user_email = request.POST.get('email')
    new_user_category = request.POST.get('identity')
    new_user_name = request.POST.get('username')

    request_user = request.user

    if not request_user.is_admin:
        course = request_user.current_course
        current_user_type = CourseSelectionRecord.objects.filter(user=request_user,
                                                                 selected_course=course).first().type
        if current_user_type == "STUDENT":
            return JsonResponse({"error": "您无此权限"}, status=405)
    else:
        course_id = request.POST.get('course_id')
        course = Course.objects.filter(pk=course_id).first()

    print(">>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<")
    print(course.name)
    if User.objects.filter(username=new_user_username).exists():
        registered_user = User.objects.filter(username=new_user_username).first()
        if CourseSelectionRecord.objects.filter(user=registered_user, selected_course=course).exists():
            return JsonResponse({"message": "用户{}({})已加入过课程{}".format(
                new_user_username,
                CourseSelectionRecord.objects.filter(user=registered_user, selected_course=course).first().type,
                course.name)}, status=405)
        else:
            courseSelectedRecord = CourseSelectionRecord(
                user=registered_user,
                selected_course=course,
                type=new_user_category
            )
            courseSelectedRecord.save()
            return JsonResponse({"message": "成功将用户{}加入课程{}".format(new_user_username, course.name)},
                                status=200)
    else:
        new_user = User.objects.create_user(
            username=new_user_username,
            password=new_user_username,
            email=new_user_email,
            name=new_user_name,
            current_course=course,
            is_admin=False
        )
        courseSelectedRecord = CourseSelectionRecord(
            user=new_user,
            selected_course=course,
            type=new_user_category
        )
        courseSelectedRecord.save()
        print("((((((((((()))))))))))))")
        return JsonResponse({"message": "成功创建用户{}，并加入课程{}".format(new_user_username, course.name)},
                            status=200)


@jwt_auth()
@require_GET
def logout_user(request):
    logout(request)
    return JsonResponse({"message": "登出成功"})


@jwt_auth()
@require_POST
def delete_user(request):
    user = request.user
    current_user_type = CourseSelectionRecord.objects.filter(user=user,
                                                             selected_course=user.current_course).first().type
    if user.is_admin or current_user_type == "TEACHER" or current_user_type == "ASSISTANT":
        deleted_user_id = request.POST.get('id')
        deleted_user = User.objects.get(pk=deleted_user_id)

        if deleted_user.avatar.name != 'avatar/default.jpg':
            deleted_user.avatar.delete()

        deleted_user.delete()
        return JsonResponse({"message": "注销成功"}, status=200)
    else:
        return JsonResponse({"error": "您无此权限"}, status=405)


@jwt_auth()
@require_POST
def delete_users(request):
    user = request.user
    current_user_type = CourseSelectionRecord.objects.filter(user=user,
                                                             selected_course=user.current_course).first().type
    if user.is_admin or current_user_type == "TEACHER" or current_user_type == "ASSISTANT":
        id_str = str(request.POST.get('ids'))
        deleted_ids = id_str.split(",")
        count = 0
        for deleted_id in deleted_ids:
            if not User.objects.filter(pk=deleted_id).exists():
                continue

            deleted_user = User.objects.get(pk=deleted_id)

            if deleted_user.avatar.name != 'avatar/default.jpg':
                deleted_user.avatar.delete()

            deleted_user.delete()
            count = count + 1
        return JsonResponse({"massage": "总计{}个用户已被删除".format(count)}, status=200)
    else:
        return JsonResponse({"error": "您无此权限"}, status=405)


@jwt_auth()
@require_POST
def change_password(request):
    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')

    user = authenticate(username=request.user.username, password=old_password)
    if user is not None:
        user.password = make_password(new_password)
        user.save()
        return JsonResponse({"message": "密码修改成功"})
    else:
        return JsonResponse({"error": "旧密码错误"}, status=405)


@jwt_auth()
@require_POST
def update_avatar(request):
    user = request.user
    avatar = request.FILES.get('avatar')

    if avatar:
        if avatar.size > 1024 * 1024 * 2:
            return JsonResponse({"error": "图片大小不能超过2MB"}, status=405)
        if user.avatar.name != 'avatar/default.png':
            user.avatar.delete()

        timestamp = str(int(time.time()))
        _, extension = os.path.splitext(avatar.name)
        avatar.name = f"{user.username}_{timestamp}{extension}"

        user.avatar = avatar
    else:
        return JsonResponse({"error": "未上传头像"}, status=405)

    user.save()
    return JsonResponse({"message": "更新成功", "url": user.get_avatar_url()})


@jwt_auth()
@require_POST
def update_user_info(request):
    update_user_id = request.POST.get('id')
    update_user_username = request.POST.get('person_id')
    update_user_name = request.POST.get('username')
    update_user_grade = request.POST.get('grade')

    update_user = User.objects.get(pk=update_user_id)
    update_user.username = update_user_username
    update_user.name = update_user_name
    update_user.grade = update_user_grade

    update_user.save()
    return JsonResponse({"message": "修改成功"}, status=200)


@jwt_auth()
@require_POST
def update_current_course(request):
    user = request.user
    new_course_id = int(request.POST.get('course_id'))
    new_course = Course.objects.get(pk=new_course_id)
    if new_course is not None:
        if not CourseSelectionRecord.objects.filter(user=user, selected_course=new_course).exists():
            return JsonResponse({"error": "您未加入该课程"}, status=405)

        if user.current_course is not None:
            course_id = user.current_course.id
            if course_id == new_course_id:
                return JsonResponse({"message": "您已正在浏览该课程"}, status=200)
            else:
                user.current_course = new_course
                user.save()
                return JsonResponse({
                    "message": "修改课程成功，您当前浏览的课程为{}".format(new_course.name),
                    "identity": str(
                        CourseSelectionRecord.objects.filter(user=user, selected_course=new_course).first().type)
                }, status=200)
        else:
            user.current_course = new_course
            user.save()
            return JsonResponse({
                "message": "修改课程成功",
                "identity": str(
                    CourseSelectionRecord.objects.filter(user=user, selected_course=new_course).first().type)
            }, status=200)
    else:
        return JsonResponse({"error": "未查询到此课程"}, status=405)


@jwt_auth()
@require_GET
def get_user_info(request):
    user = request.user
    if user.current_course is None:
        if user.is_admin:
            course_name = "管理员无课程"
            identity = "ADMIN"
        else:
            course_name = ""
            identity = ""
    else:
        course_name = user.current_course.name
        identity = CourseSelectionRecord.objects.filter(user=user, selected_course=user.current_course).first().type

    return JsonResponse({
        "personID": user.username,
        "username": user.name,
        "identity": identity,
        "avatar": user.get_avatar_url(),
        "course": course_name,
        "is_admin": user.is_admin,
        "grade": user.grade,
        "college": user.college,
        "major": user.major
    }, status=200)


@jwt_auth()
@require_GET
def user_selected_course(request):
    user = request.user
    if user.is_admin:
        return JsonResponse({"error": "您为网站管理员"}, status=405)
    else:
        courseSelectionRecords = CourseSelectionRecord.objects.filter(user=user).all()
        data = [
            {
                "course_id": record.selected_course.id,
                "name": record.selected_course.name
            }
            for record in courseSelectionRecords
        ]
        return JsonResponse({"result": data}, status=status.HTTP_200_OK)


@jwt_auth()
@require_POST
def xlsx_create_users(request):
    xlsx_file = request.FILES.get('xlsxFile')
    workbook = openpyxl.load_workbook(xlsx_file)
    worksheet = workbook.active
    new_users_category = request.POST.get('type')

    # 确定课程
    request_user = request.user
    if request_user.is_admin:
        course_id = request.POST.get('course_id')
        course = Course.objects.get(pk=course_id)
    else:
        request_user_type = CourseSelectionRecord.objects.filter(user=request_user,
                                                                 selected_course=request_user.current_course).first().type
        if request_user_type == 'STUDENT':
            return JsonResponse({"error": "抱歉，您无此权限"}, status=200)
        else:
            course = request_user.current_course

    # 新建用户
    count = 0
    error_massage_list = []
    success_massage_list = []
    for row in worksheet.iter_rows():
        new_user_username = str(row[0].value).strip() if row[0].value else ''
        new_user_name = str(row[1].value).strip() if row[1].value else ''
        if User.objects.filter(username=new_user_username).exists():
            registered_user = User.objects.filter(username=new_user_username).first()
            if CourseSelectionRecord.objects.filter(user=registered_user, selected_course=course).exists():
                error_massage_list.append("用户{}({})已加入过课程{}".format(
                    new_user_username,
                    CourseSelectionRecord.objects.filter(user=registered_user, selected_course=course).first().type,
                    course.name))
            else:
                courseSelectedRecord = CourseSelectionRecord(
                    user=registered_user,
                    selected_course=course,
                    type=new_users_category
                )
                courseSelectedRecord.save()
                success_massage_list.append("成功将用户{}加入课程{}".format(new_user_username, course.name))
        else:
            new_user = User.objects.create_user(
                username=new_user_username,
                password=new_user_username,
                name=new_user_name,
                current_course=course,
                is_admin=False
            )
            courseSelectedRecord = CourseSelectionRecord(
                user=new_user,
                selected_course=course,
                type=new_users_category
            )
            courseSelectedRecord.save()
            success_massage_list.append("成功创建用户{}，并加入课程{}".format(new_user_username, course.name))
        count = count + 1

    return JsonResponse({
        "message": "{}个用户已被添加到课程{}".format(count, course.name),
        "error_list": error_massage_list,
        "success_list": success_massage_list}, status=200)


@jwt_auth()
@require_GET
def user_list(request):
    all_users = User.objects.filter(is_admin=False)
    items_per_page = ITEMS_PER_PAGE
    page_number = request.GET.get('page', 1)

    if page_number == "":
        items_per_page = all_users.count()
        page_number = 1

    paginator = Paginator(all_users, items_per_page)
    try:
        current_page_data = paginator.page(page_number)
    except EmptyPage:
        return JsonResponse({'error': 'Page not found'}, status=404)

    courses = {}
    for user in all_users:
        records = CourseSelectionRecord.objects.filter(user=user)
        course = ""
        for record in records:
            course = course + str(record.selected_course.name) + "(" + str(record.type) + "),"
        courses[user] = course[:-1]

    serialized_data = [
        {
            'id': user.id,
            'person_id': user.username,
            'username': user.name,
            'courses': courses[user]
        }
        for user in current_page_data
    ]

    return JsonResponse({
        'result': serialized_data,
        'total_pages': paginator.num_pages,
        'current_page': current_page_data.number}, status=200)


@jwt_auth()
@require_POST
def search_users(request):
    search_username = request.POST.get('person_id')
    search_name = request.POST.get('username')
    search_grade = request.POST.get('grade')
    search_course = request.POST.get('course')
    search_identity = request.POST.get('identity')
    page = request.POST.get('page')

    query_user = Q()
    if search_username:
        query_user &= Q(username=search_username)
    if search_name:
        query_user &= Q(name=search_name)
    if search_grade:
        query_user &= Q(grade=search_grade)

    filtered_users = User.objects.filter(query_user)

    query_course_select_record = Q()
    if search_course:
        query_course_select_record &= Q(selected_course=search_course)
    if search_identity:
        query_course_select_record &= Q(type=search_identity)

    filtered_course_select_records = CourseSelectionRecord.objects.filter(query_course_select_record)

    user_ids_filtered_course_select_records = filtered_course_select_records.values_list('user__id', flat=True)
    filtered_users = filtered_users.filter(id__in=user_ids_filtered_course_select_records)

    result_ = {
        filtered_user:
            {
                "id": filtered_user.id,
                "person_id": filtered_user.username,
                "username": filtered_user.name,
                "grade": filtered_user.grade,
                "courses": ''
            }
        for filtered_user in filtered_users
    }

    for filtered_user in filtered_users:
        selected_courses_records = CourseSelectionRecord.objects.filter(user=filtered_user)
        for record in selected_courses_records:
            result_[filtered_user]['courses'] = (result_[filtered_user]['courses'] +
                                                 str(record.selected_course.name) + '(' + str(record.type) + '),')
        result_[filtered_user]['courses'] = result_[filtered_user]['courses'][:-1]

    paginator = Paginator(list(result_.values()), ITEMS_PER_PAGE)

    try:
        current_page_data = paginator.page(page)
    except EmptyPage:
        return JsonResponse({'error': 'Page not found'}, status=404)

    result = [item for item in current_page_data]

    return JsonResponse(
        {
            'result': result,
            'total_pages': paginator.num_pages,
            'current_page': current_page_data.number
        }, status=200
    )


@jwt_auth()
@require_POST
def reset_user_password(request):
    user_id = request.POST.get('id')
    user = User.objects.get(pk=user_id)
    username = user.username
    new_password = make_password(username)
    user.password = new_password
    user.save()
    return JsonResponse({"massage": "密码成功重置为学号"}, status=200)
