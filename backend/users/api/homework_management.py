import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from rest_framework import status

from users.api.auth import jwt_auth
from users.models import Course
from users.models.normal_homework import NormalHomework


@jwt_auth()
@require_POST
def create_homework(request):
    user = request.user
    if user.category == 'TEACHER' or user.category == 'STUDENT':
        data = json.loads(request.body.decode('utf-8'))
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        content = data.get('content')
        belong_to_course_id = data.get('belong_to_course_id')
        belong_to_course = Course.objects.filter(pk=belong_to_course_id)
        normalHomework = NormalHomework(
            start_time=start_time,
            end_time=end_time,
            content=content,
            belong_to_course=belong_to_course)
        normalHomework.save()
        return JsonResponse({"massage": "作业成功创建"}, status=200)
    else:
        return JsonResponse({"error": "您无此权限"}, status=400)


@jwt_auth()
@require_POST
def submit_homework(request):
    return JsonResponse({"massage": "接口正在编写中…"}, status=200)