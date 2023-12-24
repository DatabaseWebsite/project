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
from users.models.message import Message
from users.models.notice import Notice
from users.models.user import User
from users.settings import ITEMS_PER_PAGE


@jwt_auth()
@require_POST
def send_message_(request):
    sender = request.user.id
    title = request.POST.get('title')
    content = request.POST.get('content')
    receiver_id = request.POST.get('receiver_id')
    course_id = sender.current_course.id

    send_message(sender, [receiver_id], content, course_id, "OTHER", title)

    return JsonResponse({"message": "发送成功"}, status=200)


def send_message(sender_id, receiver_ids, content, course_id, m_type, title=""):
    course = Course.objects.get(pk=course_id)
    sender = User.objects.get(pk=sender_id)
    for receiver_id in receiver_ids:
        receiver = User.objects.get(pk=receiver_id)
        message = Message(sender=sender, receiver=receiver, title=title, content=content, course=course, type=m_type)
        message.save()


@jwt_auth()
@require_POST
def get_message(request):
    user = request.user
    message_type = request.POST.get('type')
    if message_type is None:
        messages = Message.objects.filter(receiver=user, course=user.current_course)
    else:
        messages = Message.objects.filter(receiver=user, course=user.current_course, type=message_type)

    result = [
        {
            "id": message.id,
            "sender": message.sender.name,
            "title": message.title,
            "content": message.content,
            "time": message.send_time,
            "type": message.type,
            "unread": ~message.read
        }
        for message in messages
    ]

    return JsonResponse({"result": result}, status=200)


@jwt_auth()
@require_POST
def read_message(request):
    message_id = request.POST.get('id')
    message = Message.objects.get(pk=message_id)
    message.read = True
    message.save()
    return JsonResponse({"message": "已阅读"}, status=200)


@jwt_auth()
@require_GET
def message_number(request):
    user = request.user
    course = user.current_course
    total = Message.objects.filter(receiver=user, course=course, read=False).count()
    CLASS = Message.objects.filter(receiver=user, course=course, read=False, type="class").count()
    WORK = Message.objects.filter(receiver=user, course=course, read=False, type="work").count()
    DISCUSSION = Message.objects.filter(receiver=user, course=course, read=False, type="discussion").count()
    return JsonResponse(
        {
            "result": {"total": total,
                       "class": CLASS,
                       "work": WORK,
                       "discussion": DISCUSSION}
        }, status=200
    )
