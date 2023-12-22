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

    if sender.is_admin:
        course_id = request.POST.get('course_id')
    else:
        course_id = sender.current_course.id

    send_message(sender, [receiver_id], content, course_id, title)

    return JsonResponse({"message": "发送成功"}, status=200)


def send_message(sender_id, receiver_ids, content, course_id, title=""):
    course = Course.objects.get(pk=course_id)
    sender = User.objects.get(pk=sender_id)
    for receiver_id in receiver_ids:
        receiver = User.objects.get(pk=receiver_id)
        message = Message(sender=sender, receiver=receiver, title=title, content=content, course=course)
        message.save()


@jwt_auth()
@require_POST
def get_message(request):
    user = request.user

    if user.is_admin:
        messages = Message.objects.all()
        result = [
            {
                "sender": message.sender.name,
                "title": message.title,
                "content": message.content,
                "send_time": message.send_time,
                "course": message.course.name
            }
            for message in messages
        ]
    else:
        messages = Message.objects.filter(receiver=user, course=user.current_course)
        result = [
            {
                "sender": message.sender.name,
                "title": message.title,
                "content": message.content,
                "send_time": message.send_time
            }
            for message in messages
        ]

    return JsonResponse({"result": result}, status=200)
