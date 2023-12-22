import os
import time

import openpyxl

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q, F
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from rest_framework import status

from users.api.auth import jwt_auth, generate_token, generate_refresh_token, varify_captcha
from users.api.message import send_message
from users.models import Course
from users.models.course_selection_record import CourseSelectionRecord
from users.models.forum import Post, Reply
from users.models.like_record import PostLikeRecord, ReplyLikeRecord
from users.models.subsciption_record import SubscriptionRecord
from users.models.user import User
from users.settings import ITEMS_PER_PAGE, OFFICIAL_ID


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

    post = Post(poster=poster, title=title, content=content, course=course, top=False, likes=0, elite=False)
    post.save()

    return JsonResponse({"message": "成功创建"}, status=200)


@jwt_auth()
@require_GET
def post_list(request):
    user = request.user
    user_like_post_set = set(
        PostLikeRecord.objects.filter(user=user).values('post').values_list('post', flat=True))
    user_subscribe_post_set = set(
        SubscriptionRecord.objects.filter(user=user).values('post').values_list('post', flat=True))

    if user.is_admin:
        posts = Post.objects.all().order_by('-top', '-post_time')
        result = [
            {
                "sender": post.poster.id,
                "title": post.title,
                "content": post.content,
                "send_time": post.post_time,
                "course": post.course.id,
                "top": post.top,
                "like": post in user_like_post_set,
                "subscribe": post in user_subscribe_post_set
            }
            for post in posts
        ]
    else:
        posts = Post.objects.filter(course=user.current_course).order_by('-top', '-post_time')
        result = [
            {
                "sender": post.poster.id,
                "title": post.title,
                "content": post.content,
                "send_time": post.post_time,
                "top": post.top,
                "like": post in user_like_post_set,
                "subscribe": post in user_subscribe_post_set
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

    subscribe_list = SubscriptionRecord.objects.filter(post=post).values_list('user_id', flat=True)
    send_message(OFFICIAL_ID, subscribe_list, "您关注的帖子\"{}\"已更新".format(post.title), post.course.id,
                 title="帖子更新通知")

    return JsonResponse({"message": "成功创建"}, status=200)


@jwt_auth()
@require_GET
def get_post(request):
    user = request.user
    post_id = request.GET.get('post_id', 1)
    _post = Post.objects.get(pk=post_id)
    _replies = Reply.objects.filter(post=_post)

    user_like_post_set = set(
        PostLikeRecord.objects.filter(user=user).values_list('post', flat=True))
    user_subscribe_post_set = set(
        SubscriptionRecord.objects.filter(user=user).values_list('post', flat=True))
    user_like_reply_set = set(
        ReplyLikeRecord.objects.filter(user=user).values_list('reply', flat=True))

    result = {
        "post": {
            "url": _post.poster.get_avatar_url(),
            "sender": _post.poster.id,
            "title": _post.title,
            "content": _post.content,
            "send_time": _post.post_time,
            "top": _post.top,
            "like": _post in user_like_post_set,
            "subscribe": _post in user_subscribe_post_set
        },
        "replies": []
    }
    count = 0
    for reply in _replies:
        result["replies"].append(
            {
                "url": reply.replier.get_avatar_url(),
                "replier": reply.replier.id,
                "content": reply.content,
                "reply_time": reply.reply_time,
                "like": reply in user_like_reply_set
            }
        )
        if reply.reply_to is not None:
            result["replies"][count]["reply_to"] = reply.reply_to.replier.id
        else:
            result["replies"][count]["reply_to"] = reply.post.poster.id
        count = count + 1

    return JsonResponse({"result": result}, status=200)


@jwt_auth()
@require_POST
def topping_post(request):
    post_id = request.POST.get("post_id")
    post = Post.objects.get(pk=post_id)
    post.top = True
    return JsonResponse({"message": "置顶成功"}, status=200)


@jwt_auth()
@require_POST
def cancel_topping_post(request):
    post_id = request.POST.get("post_id")
    post = Post.objects.get(pk=post_id)
    post.top = False
    return JsonResponse({"message": "取消置顶成功"}, status=200)


@jwt_auth()
@require_POST
def subscribe_post(request):
    post_id = request.POST.get("post_id")
    post = Post.objects.get(pk=post_id)
    user = request.user

    if SubscriptionRecord.objects.filter(post=post, user=user).exists():
        return JsonResponse({"error": "您已订阅该帖子"}, status=405)
    else:
        subscriptionRecord = SubscriptionRecord(post=post, user=user)
        subscriptionRecord.save()
        return JsonResponse({"message": "订阅成功"}, status=200)


@jwt_auth()
@require_POST
def cancel_subscribe_post(request):
    post_id = request.POST.get("post_id")
    post = Post.objects.get(pk=post_id)
    user = request.user

    if SubscriptionRecord.objects.filter(post=post, user=user).exists():
        subscriptionRecord = SubscriptionRecord.objects.filter(post=post, user=user)
        subscriptionRecord.delete()

    return JsonResponse({"message": "成功解除订阅"}, status=200)


@jwt_auth()
@require_POST
def like_reply(request):
    reply_id = request.POST.get("reply_id")
    reply = Reply.objects.get(pk=reply_id)
    user = request.user

    if ReplyLikeRecord.objects.filter(reply=reply, user=user).exists():
        return JsonResponse({"error": "您已喜欢该评论"}, status=405)
    else:
        replyLikeRecord = ReplyLikeRecord(reply=reply, user=user)
        replyLikeRecord.save()
        return JsonResponse({"message": "喜欢评论成功"}, status=200)


@jwt_auth()
@require_POST
def dislike_reply(request):
    reply_id = request.POST.get("reply_id")
    reply = Reply.objects.get(pk=reply_id)
    user = request.user

    if ReplyLikeRecord.objects.filter(reply=reply, user=user).exists():
        replyLikeRecord = ReplyLikeRecord.objects.filter(reply=reply, user=user)
        replyLikeRecord.delete()

    return JsonResponse({"message": "成功取消喜欢"}, status=200)


@jwt_auth()
@require_POST
def like_post(request):
    post_id = request.POST.get("post_id")
    post = Post.objects.get(pk=post_id)
    user = request.user

    if PostLikeRecord.objects.filter(post=post, user=user).exists():
        return JsonResponse({"error": "您已喜欢该帖子"}, status=405)
    else:
        postLikeRecord = PostLikeRecord(post=post, user=user)
        postLikeRecord.save()
        return JsonResponse({"message": "喜欢帖子成功"}, status=200)


@jwt_auth()
@require_POST
def dislike_post(request):
    post_id = request.POST.get("post_id")
    post = Post.objects.get(pk=post_id)
    user = request.user

    if PostLikeRecord.objects.filter(post=post, user=user).exists():
        postLikeRecord = PostLikeRecord.objects.filter(post=post, user=user)
        postLikeRecord.delete()

    return JsonResponse({"message": "成功取消喜欢"}, status=200)


@jwt_auth()
@require_POST
def search_posts(request):
    query_string = request.POST.get("q")
    search_query = SearchQuery(query_string)

    user = request.user
    user_like_post_set = set(
        PostLikeRecord.objects.filter(user=user).values('post').values_list('post', flat=True))
    user_subscribe_post_set = set(
        SubscriptionRecord.objects.filter(user=user).values('post').values_list('post', flat=True))

    posts = Post.objects.annotate(
        rank=SearchRank(F('search_vector'), search_query)
    ).filter(search_vector=search_query).order_by('-rank', '-top', '-post_time')

    result = [
        {
            "sender": post.poster.id,
            "title": post.title,
            "content": post.content,
            "send_time": post.post_time,
            "top": post.top,
            "like": post in user_like_post_set,
            "subscribe": post in user_subscribe_post_set
        }
        for post in posts
    ]

    return JsonResponse({"result": result}, status=200)

