import json
import os
import time
from datetime import datetime
import pytz
from django.core.paginator import Paginator, EmptyPage

from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET

from users.api.auth import jwt_auth
from users.api.message import send_message
from users.models import Course
from users.models.course_selection_record import CourseSelectionRecord
from users.models.normal_homework import NormalHomework
from users.models.normal_homework_submit import NormalHomeworkSubmit
from users.models.picture import Picture
from users.settings import ITEMS_PER_PAGE


@jwt_auth()
@require_POST
def create_homework(request):
    user = request.user
    if user.is_admin:
        user_category = "ADMIN"
    else:
        user_category = CourseSelectionRecord.objects.filter(user=user,
                                                             selected_course=user.current_course).first().type

    if user.is_admin or user_category == 'TEACHER' or user_category == 'ASSISTANT':
        end_time_str = request.POST.get('deadline')
        print(end_time_str)
        end_time = pytz.utc.localize(datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M:%S.%fZ'))
        title = request.POST.get('title')
        content = request.POST.get('description')
        if user.is_admin:
            belong_to_course_id = request.POST.get('course_id')
            belong_to_course = Course.objects.get(pk=belong_to_course_id)
        else:
            belong_to_course = user.current_course
        file = request.FILES.get('file')
        normalHomework = NormalHomework(
            end_time=end_time,
            title=title,
            content=content,
            belong_to_course=belong_to_course,
            file=file
        )
        normalHomework.save()
        return JsonResponse({"massage": "作业成功创建"}, status=200)
    else:
        return JsonResponse({"error": "您无此权限"}, status=405)


@jwt_auth()
@require_GET
def homework_list(request):
    all_homeworks = NormalHomework.objects.all()
    page_number = request.GET.get('page', 1)

    paginator = Paginator(all_homeworks, ITEMS_PER_PAGE)
    try:
        current_page_data = paginator.page(page_number)
    except EmptyPage:
        return JsonResponse({'error': 'Page not found'}, status=404)

    serialized_data = [
        {
            'id': homework.id,
            'title': homework.title,
            'content': homework.content,
            'start_time': homework.start_time,
            'end_time': homework.end_time,
            'belong_to_course': homework.belong_to_course.name
        }
        for homework in current_page_data
    ]
    return JsonResponse(
        {
            'results': serialized_data,
            'total_pages': paginator.num_pages,
            'current_page': current_page_data.number
        }
    )


@jwt_auth()
@require_POST
def submit_homework(request):
    user = request.user
    file = request.FILES.get('file')

    homework_id = request.POST.get('homework_id')
    homework = NormalHomework.objects.get(pk=homework_id)

    timestamp = str(int(time.time()))
    _, extension = os.path.splitext(file.name)
    file.name = f"{user.username}_{homework_id}_{timestamp}{extension}"

    if NormalHomeworkSubmit.objects.filter(user=user, homework=homework).exists():
        submit = NormalHomeworkSubmit.objects.filter(user=user, homework=homework).first()
        submit.file.delete()
        submit.file = file
    else:
        submit = NormalHomeworkSubmit(user=user, homework=homework, file=file)
    submit.save()

    return JsonResponse({
        "massage": "作业已成功提交",
        "url": submit.get_file_url()}, status=200)


@jwt_auth()
@require_POST
def submit_score(request):
    user = request.user
    score = request.POST.get('score')
    submit_id = request.POST.get('submit_id')

    submit = NormalHomeworkSubmit.objects.get(pk=submit_id)
    submit.score = score
    submit.save()

    send_message(user.id, submit.user.id, "{}作业老师批改已完成，请查看作答情况".format(submit.homework.title),
                 user.current_course.id, "作业批改通知")
    return JsonResponse({"massage": "成功批改"}, status=200)


@jwt_auth()
@require_POST
def upload_image(request):
    image = request.FILES.get("image")
    timestamp = str(int(time.time()))
    _, extension = os.path.splitext(image.name)
    image.name = f"{image.username}_{timestamp}{extension}"
    picture = Picture(picture=image)
    picture.save()
    return JsonResponse({"url": picture.get_pic_url()}, status=200)