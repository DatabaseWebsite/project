import json
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
from util.word_cloud_map import make_word_cloud_map
import matplotlib.pyplot as plt
import palettable


@jwt_auth()
@require_POST
def create_post(request):
    poster = request.user
    title = request.POST.get('title')
    content = request.POST.get('content')
    course = poster.current_course

    post = Post(poster=poster, title=title, content=content, course=course, top=False, likes=0, elite=False)
    post.save()
    posts = Post.objects.filter(course=poster.current_course)
    content = ""
    for post in posts:
        content += post.content
    make_word_cloud_map(content)
    return JsonResponse({"message": "成功创建"}, status=200)


@jwt_auth()
@require_GET
def post_list(request):
    user = request.user
    user_like_post_set = set(
        PostLikeRecord.objects.filter(user=user).values('post').values_list('post', flat=True))
    user_subscribe_post_set = set(
        SubscriptionRecord.objects.filter(user=user).values('post').values_list('post', flat=True))

    posts = Post.objects.filter(course=user.current_course).order_by('-top', '-post_time')
    result = [
        {
            "id": post.id,
            "authorAvatar": post.poster.get_avatar_url(),
            "author": post.poster.name,
            "title": post.title,
            "content": post.content,
            "timestamp": post.post_time.strftime("%Y-%m-%d %H:%M:%S"),
            "top": post.top,
            "elite": post.elite,
            "likes": post.likes,
            "like": post.id in user_like_post_set,
            "subscribe": post.id in user_subscribe_post_set
        }
        for post in posts
    ]
    print(result)
    return JsonResponse({"result": result}, status=200)


@jwt_auth()
@require_GET
def gen_word_cloud_map(request):
    return JsonResponse({"img_url": "http://127.0.0.1:8000/media/word_cloud_map.png"}, status=200)

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
    send_message(OFFICIAL_ID, subscribe_list, "您关注的帖子\"{}\"已更新".format(post.title), post.course.id
                 , "DISCUSSION", title="帖子更新通知")

    return JsonResponse({"message": "成功创建"}, status=200)


@jwt_auth()
@require_POST
def get_post(request):
    user = request.user
    post_id = request.POST.get('post_id')
    _post = Post.objects.get(pk=post_id)
    _replies = Reply.objects.filter(post=_post)
    print(post_id)
    user_like_post_set = set(
        PostLikeRecord.objects.filter(user=user).values_list('post', flat=True))
    user_subscribe_post_set = set(
        SubscriptionRecord.objects.filter(user=user).values_list('post', flat=True))
    user_like_reply_set = set(
        ReplyLikeRecord.objects.filter(user=user).values_list('reply', flat=True))

    result = {
        "post": {
            "id": _post.id,
            "authorAvatar": _post.poster.get_avatar_url(),
            "author": _post.poster.name,
            "title": _post.title,
            "content": _post.content,
            "timestamp": _post.post_time,
            "top": _post.top,
            "elite": _post.elite,
            "likes": _post.likes,
            "like": _post.id in user_like_post_set,
            "subscribe": _post.id in user_subscribe_post_set
        },
        "replies": []
    }
    print(result)
    count = 0
    for reply in _replies:
        result["replies"].append(
            {
                "id": reply.id,
                "authorAvatar": reply.replier.get_avatar_url(),
                "author": reply.replier.name,
                "content": reply.content,
                "timestamp": reply.reply_time,
                "likes": reply.likes,
                "like": reply.id in user_like_reply_set
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
    post.save()
    return JsonResponse({"message": "置顶成功"}, status=200)


@jwt_auth()
@require_POST
def cancel_topping_post(request):
    post_id = request.POST.get("post_id")
    post = Post.objects.get(pk=post_id)
    post.top = False
    post.save()
    return JsonResponse({"message": "取消置顶成功"}, status=200)


@jwt_auth()
@require_POST
def elite_post(request):
    post_id = request.POST.get("post_id")
    post = Post.objects.get(pk=post_id)
    post.elite = True
    post.save()
    return JsonResponse({"message": "加精成功"}, status=200)


@jwt_auth()
@require_POST
def cancel_elite_post(request):
    post_id = request.POST.get("post_id")
    post = Post.objects.get(pk=post_id)
    post.elite = False
    post.save()
    return JsonResponse({"message": "取消加精成功"}, status=200)


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
        reply.likes = reply.likes + 1
        reply.save()
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
        reply.likes = reply.likes - 1
        reply.save()

    return JsonResponse({"message": "成功取消喜欢"}, status=200)


@jwt_auth()
@require_POST
def like_post(request):
    post_id = request.POST.get("post_id")
    print(post_id)
    post = Post.objects.get(pk=post_id)
    user = request.user

    if PostLikeRecord.objects.filter(post=post, user=user).exists():
        return JsonResponse({"error": "您已喜欢该帖子"}, status=405)
    else:
        postLikeRecord = PostLikeRecord(post=post, user=user)
        postLikeRecord.save()
        post.likes = post.likes + 1
        post.save()
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
        post.likes = post.likes - 1
        post.save()

    return JsonResponse({"message": "成功取消喜欢"}, status=200)


@jwt_auth()
@require_POST
def search_posts(request):
    query_string = request.POST.get("q")

    user = request.user
    user_like_post_set = set(
        PostLikeRecord.objects.filter(user=user).values('post').values_list('post', flat=True))
    user_subscribe_post_set = set(
        SubscriptionRecord.objects.filter(user=user).values('post').values_list('post', flat=True))

    matching_posts = set(Post.objects.filter(
        Q(title__contains=query_string) | Q(content__contains=query_string)
    ))

    matching_replies = set(Reply.objects.filter(Q(content__contains=query_string)))

    for reply in matching_replies:
        matching_posts.add(reply.post)

    result = [
        {
            "author": post.poster.id,
            "title": post.title,
            "content": post.content,
            "timestamp": post.post_time,
            "top": post.top,
            "like": post in user_like_post_set,
            "likes": post.likes,
            "elite": post.elite,
            "subscribe": post in user_subscribe_post_set
        }
        for post in matching_posts
    ]

    return JsonResponse({"result": result}, status=200)


