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
from users.models.forum import Post, Reply
from users.models.user import User
from users.settings import ITEMS_PER_PAGE


@jwt_auth()
@require_POST
def create_post(request):
    poster = request.user
    title = request.POST.get('title')
    content = request.POST.get('content')

    if poster.is_admin:
        course_id = request.POST.get('course_id')
        course = Course.objects.get(pk=course_id)
    else:
        course = poster.current_course

    post = Post(poster=poster, title=title, content=content, course=course)
    post.save()

    return JsonResponse({"message": "成功创建"}, status=200)


@jwt_auth()
@require_GET
def post_list(request):
    user = request.user

    if user.is_admin:
        posts = Post.objects.all()
        result = [
            {
                "sender": post.poster.id,
                "title": post.title,
                "content": post.content,
                "send_time": post.post_time,
                "course": post.course.id
            }
            for post in posts
        ]
    else:
        posts = Post.objects.filter(course=user.current_course)
        result = [
            {
                "sender": post.poster.id,
                "title": post.title,
                "content": post.content,
                "send_time": post.post_time
            }
            for post in posts
        ]

    return JsonResponse({"result": result}, status=200)


@jwt_auth()
@require_POST
def delete_post(request):
    post_id = request.POST.get('post_id')
    post = Post.objects.get(pk=post_id)

    post.delete()
    return JsonResponse({"message": "成功删除"}, status=200)


@jwt_auth()
@require_POST
def create_reply(request):
    replier = request.user
    content = request.POST.get('content')
    post_id = request.POST.get('post_id')
    post = Post.objects.get(pk=post_id)
    reply_to_id = request.POST.get('reply_id')
    reply_to = None
    if reply_to_id is not None:
        reply_to = Reply.objects.get(pk=reply_to_id)

    if reply_to is not None:
        reply = Reply(replier=replier, content=content, post=post, reply_to=reply_to)
    else:
        reply = Reply(replier=replier, content=content, post=post)
    reply.save()

    return JsonResponse({"message": "成功创建"}, status=200)


@jwt_auth()
@require_GET
def get_post(request):
    post_id = request.GET.get('post_id', 1)
    _post = Post.objects.get(pk=post_id)
    _replies = Reply.objects.filter(post=_post)
    result = {
        "post": {
            "url"
            "sender": _post.poster.id,
            "title": _post.title,
            "content": _post.content,
            "send_time": _post.post_time
        },
        "replies": []
    }
    count = 0
    for reply in _replies:
        result["replies"].append(
            {
                "replier": reply.replier.id,
                "content": reply.content,
                "reply_time": reply.reply_time,
            }
        )
        if reply.reply_to is not None:
            result["replies"][count]["reply_to"] = reply.reply_to.replier.id
        else:
            result["replies"][count]["reply_to"] = reply.post.poster.id
        count = count + 1

    return JsonResponse({"result": result}, status=200)






















