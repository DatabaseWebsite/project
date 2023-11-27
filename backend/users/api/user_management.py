import json
import openpyxl

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from users.api.auth import jwt_auth, generate_token, generate_refresh_token, varify_captcha
from users.models import Course
from users.models.user import User


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
            {"msg": "Login successful.", 'access': token, 'refresh': refresh_token, 'userId': username, 'code': 200},
            status=200)
    elif User.objects.filter(username=username).exists():
        return JsonResponse({"error": "密码错误", 'code': 401}, status=201)
    else:
        return JsonResponse({"error": "用户不存在", 'code': 401}, status=201)


@require_POST
def signup_user(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    category = data.get('category')
    name = data.get('name')

    if username is None or password is None or email is None or category is None:
        return JsonResponse({"error": "内容未填写完整"}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "用户名已存在"}, status=400)
    if User.objects.filter(email=email).exists():
        return JsonResponse({"error": "邮箱已注册"}, status=400)
    if password == '':
        return JsonResponse({"error": "密码不能为空"}, status=400)

    # 使用 create_user 方法创建用户，它会处理密码的哈希存储
    User.objects.create_user(username=username, password=password, email=email, category=category, name=name)

    return JsonResponse({"message": "用户注册成功"}, status=200)


@jwt_auth()
@require_GET
def logout_user(request):
    # 登出用户
    logout(request)
    return JsonResponse({"message": "登出成功"})


@jwt_auth()
@require_POST
def update_avatar(request):
    user = request.user
    avatar = request.FILES.get('avatar')

    if avatar:
        if avatar.size > 1024 * 1024 * 2:
            return JsonResponse({"error": "图片大小不能超过2MB"}, status=400)
        if user.avatar.name != 'avatar/default.png':
            user.avatar.delete()
        avatar.name = user.username + '.png'
        user.avatar = avatar
    else:
        return JsonResponse({"error": "未上传头像"}, status=400)

    user.save()
    return JsonResponse({"message": "更新成功", "url": user.get_avatar_url()})


@jwt_auth()
@require_POST
def change_password(request):
    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')
    print(old_password, new_password)
    user = authenticate(username=request.user.username, password=old_password)
    if user is not None:
        user.password = make_password(new_password)
        user.save()
        return JsonResponse({"message": "密码修改成功"})
    else:
        return JsonResponse({"error": "旧密码错误"}, status=400)


@jwt_auth()
@require_POST
def update_selected_course(request):
    user = request.user
    data = json.loads(request.body.decode('utf-8'))
    new_course_id = int(data.get('course_id'))
    new_course = Course.objects.get(pk=new_course_id)
    if new_course is not None:
        if user.selected_course is not None:
            course_id = user.selected_course.id
            if course_id == new_course_id:
                return JsonResponse({"message": "您已选择该课程"}, status=200)
            else:
                user.selected_course = new_course
                user.save()
                return JsonResponse({"message": "修改课程成功，您现在的课程为{}".format(new_course.name)}, status=200)
        else:
            user.selected_course = new_course
            user.save()
            return JsonResponse({"message": "修改课程成功"}, status=200)
    else:
        return JsonResponse({"error": "未查询到此课程"}, status=400)


@jwt_auth()
@require_GET
def get_user_info(request):
    user = request.user
    course = ""
    if user.selected_course is None:
        course = "您还未选择课程"
    else:
        course = user.selected_course.name
    return JsonResponse({
        "personID": user.username,
        "username": user.name,
        "identity": user.category,
        "avatar": user.get_avatar_url(),
        "course": course
    }, status=200)


@jwt_auth()
@require_POST
def xlsx_create_user(request):
    xlsx_file = request.FILES.get('xlsxFile')
    workbook = openpyxl.load_workbook(xlsx_file)
    worksheet = workbook.active

    count = 0
    for row in worksheet.iter_rows():
        username = str(row[0].value).strip() if row[0].value else ''
        name = str(row[1].value).strip() if row[1].value else ''
        email = str(row[2].value).strip() if row[2].value else ''
        category = str(row[3].value).strip() if row[3].value else ''
        print(username, name, email, category)
        if username is None or email is None or category is None:
            return JsonResponse({"error": "内容未填写完整"}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "用户名%s已存在".format(username)}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "邮箱%s已注册".format(email)}, status=400)
        User.objects.create_user(username=username, name=name, password="123456", email=email, category=category)
        count = count + 1

    return JsonResponse({"message": "{}个用户已被成功创建".format(count)}, status=200)


@jwt_auth()
@require_GET
def user_list(request):
    all_users = User.objects.all()
    items_per_page = 3
    paginator = Paginator(all_users, items_per_page)
    page_number = request.GET.get('page', 1)

    try:
        current_page_data = paginator.page(page_number)
    except EmptyPage:
        return JsonResponse({'error': 'Page not found'}, status=404)

    serialized_data = [
        {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'category': user.category,
            'course': user.selected_course.name if user.selected_course else "未选择课程"
        }
        for user in current_page_data
    ]
    return JsonResponse({
        'results': serialized_data,
        'total_pages': paginator.num_pages,
        'current_page': current_page_data.number})
