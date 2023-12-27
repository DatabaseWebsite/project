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
from users.models.notice import Notice
from users.models.user import User
from users.settings import ITEMS_PER_PAGE


@jwt_auth()
@require_POST
def create_notice(request):
    title = request.POST.get('title')
    content = request.POST.get('content')

    notice = Notice(sender=request.user, title=title, content=content, course=request.user.current_course)
    notice.save()

    return JsonResponse({"message": "创建成功"}, status=200)


@jwt_auth()
@require_POST
def delete_notice(request):
    notice_id = int(request.POST.get('notice_id'))
    notice = Notice.objects.get(pk=notice_id)
    notice.delete()
    return JsonResponse({"message": "删除成功"}, status=200)


@jwt_auth()
@require_GET
def notice_list(request):
    user = request.user
    result = []
    course = user.current_course

    notices = Notice.objects.filter(course=course)

    for notice in notices:
        result.append(
            {
                'id': notice.id,
                "sender": notice.sender.name,
                "title": notice.title,
                "content": notice.content,
                "create_time": notice.create_time,
                "course": notice.course.name
            }
        )

    return JsonResponse({'result': result}, status=200)