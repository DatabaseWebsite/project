import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET

from users.api.auth import jwt_auth, generate_token, generate_refresh_token, varify_captcha
from users.models.user import User


@require_POST
def login_user(request):
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    username = data.get('username')
    password = data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        token = generate_token(user)
        refresh_token = generate_refresh_token(user)
        return JsonResponse({"msg": "Login successful.", 'access': token, 'refresh': refresh_token, 'userId':username},
                            status=200)
    elif User.objects.filter(username=username).exists():
        return JsonResponse({"error": "密码错误"},  status=401)
    else:
        return JsonResponse({"error": "用户不存在"}, status=401)


@require_POST
def signup_user(request):
    data = json.loads(request.body.decode('utf-8'))
    print(data)
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
    avatar = request.FILES.getlist('avatar')[0]

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
@require_GET
def get_user_info(request):
    user = request.user
    return JsonResponse({
        "personID": user.username,
        "username": user.name,
        "identity": user.category,
        "avatar": user.get_avatar_url(),
        "course": user.course
    }, status=200)

