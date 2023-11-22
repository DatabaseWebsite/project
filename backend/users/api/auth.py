from datetime import timedelta

from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone

from users.models.auth_record import AuthRecord
from users.models.email_captcha import EmailCaptcha
from users.models.user import User

import jwt


def varify_captcha(email, captcha):
    entrys = EmailCaptcha.objects.filter(email=email, captcha=captcha)
    varify = False
    for entry in entrys:
        if not entry.is_expired():
            varify = True
            break

    entrys.delete()
    return varify


def generate_token(user: User, access_token_delta: int = 1) -> str:
    current_time = timezone.now()
    access_token_payload = {
        "user_id": user.id,
        "exp": current_time + timedelta(hours=access_token_delta),
        "iat": current_time,
        "type": "access_token",
    }
    token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm="HS256")
    if type(token) is str:
        return token
    return token.decode('utf-8')


def generate_refresh_token(user: User, refresh_token_delta: int = 6 * 24) -> str:
    AuthRecord.objects.filter(user=user).delete()
    current_time = timezone.now()
    auth_record = AuthRecord(user=user, login_at=current_time,
                             expires_by=current_time + timedelta(hours=refresh_token_delta))
    auth_record.save()
    refresh_token_payload = {
        "user_id": user.id,
        "record_id": auth_record.id,
        "iat": current_time,
        "type": "refresh_token",
    }
    refresh_token = jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm="HS256")
    if type(refresh_token) is str:
        return refresh_token
    return refresh_token.decode('utf-8')


def get_user(request):
    header = request.META.get('HTTP_AUTHORIZATION')
    try:
        if header is None:
            raise jwt.InvalidTokenError

        # 解码token
        auth_info = header.split(' ')

        if len(auth_info) != 2:
            raise jwt.InvalidTokenError
        auth_type, auth_token = auth_info

        if auth_type != 'Bearer':
            raise jwt.InvalidTokenError

        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])

        if payload['type'] != 'access_token':
            raise jwt.InvalidTokenError
        user_id = payload['user_id']
        user = User.objects.filter(id=user_id).first()
        return user
    except jwt.InvalidTokenError:
        return None


def jwt_auth():
    def decorator(api):
        def wrapper(request, *args, **kwargs):
            user = get_user(request)
            request.user = user
            if user is None:
                return JsonResponse({'error': '请先登录'}, status=401)
            return api(request, *args, **kwargs)

        return wrapper

    return decorator
