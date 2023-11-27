import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from rest_framework import status

from users.api.auth import jwt_auth
from users.models import Course


@jwt_auth()
@require_POST
def create_course(request):
    data = json.loads(request.body.decode('utf-8'))
    course_name = data.get('course_name')
    user = request.user
    if user.category != 'TEACHER':
        return JsonResponse({"error": "您没有此权限"}, status=400)
    else:
        course = Course(name=course_name)
        course.save()
        return JsonResponse({"message": "创建成功"}, status=200)


@jwt_auth()
@require_GET
def all_course_info(request):
    user = request.user
    if user.category == "TEACHER" or user.category == "ASSISTANT":
        courses = Course.objects.all()
        data = [{'course_id': course.id, 'name': course.name} for course in courses]
        return JsonResponse({"result": data}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"error": "您没有此权限"}, status=400)

