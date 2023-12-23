import json
import os
import time
from datetime import datetime
import pytz
from django.core.paginator import Paginator, EmptyPage

from django.http import JsonResponse
from django.utils import timezone
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
        end_time = pytz.utc.localize(datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M:%S.%fZ'))
        title = request.POST.get('title')
        content = request.POST.get('description')
        total_score = request.POST.get('totalScore')
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
            file=file,
            totalScore=total_score
        )
        normalHomework.save()
        return JsonResponse({"massage": "作业成功创建"}, status=200)
    else:
        return JsonResponse({"error": "您无此权限"}, status=405)


@jwt_auth()
@require_POST
def modify_work(request):
    homework_id = request.POST.get('id')
    homework = NormalHomework.objects.get(pk=homework_id)
    end_time_str = request.POST.get('deadline')
    end_time = pytz.utc.localize(datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M:%S.%fZ'))
    title = request.POST.get('title')
    content = request.POST.get('description')
    total_score = request.POST.get('totalScore')
    op = int(request.POST.get('op'))
    file = request.FILES.get('file')

    homework.end_time = end_time
    homework.title = title
    homework.content = content
    homework.totalScore = total_score
    if op == 0:
        homework.file = file
    elif op == 1:
        homework.file.delete()
        homework.file = file
    elif op == 2:
        homework.file.delete()

    homework.save()
    return JsonResponse({"message": "修改成功"}, status=200)


@jwt_auth()
@require_POST
def delete_work(request):
    homework_id = request.POST.get('id')
    homework = NormalHomework.objects.get(pk=homework_id)
    if homework.file is not None:
        homework.file.delete()
    homework.delete()
    return JsonResponse({"message": "成功删除"}, status=200)


@jwt_auth()
@require_GET
def works_info(request):
    flag = False
    if request.user.is_admin:
        flag = True
    else:
        my_type = CourseSelectionRecord.objects.filter(user=request.user,
                                                       selected_course=request.user.current_course).first().type
        if my_type == "TEACHER" or my_type == "ASSISTANT":
            flag = True

    if request.user.is_admin:
        all_homeworks = NormalHomework.objects.all()
    else:
        all_homeworks = NormalHomework.objects.filter(belong_to_course=request.user.current_course)

    count = 0
    result = []
    for homework in all_homeworks:
        result.append(
            {
                'id': homework.id,
                'title': homework.title,
                'deadline': homework.end_time.strftime('%Y-%m-%d %H:%M:%S.%fZ'),
                'totalScore': homework.totalScore
            }
        )

        if not flag:
            if timezone.now() < homework.end_time:
                if not NormalHomeworkSubmit.objects.filter(user=request.user, homework=homework).exists():
                    result[count]['status'] = 0
                else:
                    result[count]['status'] = 1
            else:
                if not NormalHomeworkSubmit.objects.filter(user=request.user, homework=homework).exists():
                    result[count]['status'] = 2
                else:
                    result[count]['status'] = 3

            if NormalHomeworkSubmit.objects.filter(user=request.user, homework=homework).exists():
                score = NormalHomeworkSubmit.objects.filter(user=request.user, homework=homework).first().score
                if score is None:
                    result[count]['score'] = "未批阅"
                else:
                    result[count]['score'] = str(score)
        count = count + 1

    print(result)
    return JsonResponse({'result': result}, status=200)


@jwt_auth()
@require_POST
def work_detail(request):
    homework_id = request.POST.get('id')
    homework = NormalHomework.objects.get(pk=homework_id)

    result = {
        "id": homework.id,
        "title": homework.title,
        "totalScore": homework.totalScore,
        "deadline": homework.end_time.strftime('%Y-%m-%d %H:%M:%S.%fZ'),
        "description": homework.content
    }

    total_people = CourseSelectionRecord.objects.filter(selected_course=homework.belong_to_course,
                                                        type="STUDENT").count()
    submit_people = NormalHomeworkSubmit.objects.filter(homework=homework).count()
    result['submitPeople'] = submit_people
    result['totalPeople'] = total_people

    if homework.file is not None:
        result['file'] = {
            "name": homework.file.name,
            "url": homework.get_file_url()
        }

    if timezone.now() > homework.end_time:
        result['status'] = '已截止'
    else:
        result['status'] = '进行中'

    return JsonResponse({"result": result}, status=200)


@jwt_auth()
@require_POST
def student_submit_work(request):
    user = request.user
    file = request.FILES.get('file')
    content = request.POST.get('context')

    homework_id = request.POST.get('id')
    homework = NormalHomework.objects.get(pk=homework_id)

    if file is not None:
        timestamp = str(int(time.time()))
        _, extension = os.path.splitext(file.name)
        file.name = f"{user.username}_{homework_id}_{timestamp}{extension}"

    if NormalHomeworkSubmit.objects.filter(user=user, homework=homework).exists():
        submit = NormalHomeworkSubmit.objects.filter(user=user, homework=homework).first()
        submit.file.delete()
        submit.file = file
        submit.content = content
    else:
        submit = NormalHomeworkSubmit(user=user, homework=homework, file=file, content=content)
    submit.save()

    return JsonResponse({
        "massage": "作业已成功提交",
        "url": submit.get_file_url()}, status=200)


@jwt_auth()
@require_POST
def work_submissions(request):
    homework_id = request.POST.get('id')
    homework = NormalHomework.objects.get(pk=homework_id)
    submits = NormalHomeworkSubmit.objects.filter(homework=homework)

    result = []
    count = 0
    for submit in submits:
        result.append(
            {
                "id": submit.id,
                "studentId": submit.user.username,
                "studentName": submit.user.name,
                "submitTime": submit.submit_time.strftime('%Y-%m-%d %H:%M:%S.%fZ')
            }
        )
        if submit.score is None:
            result[count]['score'] = ""
            result[count]['markingPerson'] = ""
        else:
            result[count]['score'] = submit.score
            result[count]['markingPerson'] = submit.markingPerson

    return JsonResponse({"result": result}, status=200)


@jwt_auth()
@require_POST
def work_submissions_detail(request):
    submit_id = request.POST.get('id')
    submit = NormalHomeworkSubmit.objects.get(pk=submit_id)

    result = {
        "id": submit.id,
        "score": submit.score,
        "submit_time": submit.submit_time.strftime('%Y-%m-%d %H:%M:%S.%fZ')
    }

    if submit.content is not None:
        result['context'] = submit.content
    if submit.file is not None:
        result['file'] = {
            'name': submit.file.name,
            'url': submit.get_file_url()
        }
    if submit.markingPerson is not None:
        result['markingPerson'] = submit.markingPerson.username

    return JsonResponse({"result": result}, status=200)


@jwt_auth()
@require_POST
def student_work_detail(request):
    print("??????????????????????")
    homework_id = int(request.POST.get('id'))

    print(request.POST.get('id'))

    homework = NormalHomework.objects.get(pk=homework_id)

    result = {
        "id": homework.id,
        "title": homework.title,
        "totalScore": homework.totalScore,
        "deadline": homework.end_time.strftime('%Y-%m-%d %H:%M:%S.%fZ'),
        "description": homework.content
    }

    if homework.file is not None:
        result["file"] = {
            "name": homework.file.name,
            "url": homework.get_file_url()
        }

    if NormalHomeworkSubmit.objects.filter(user=request.user, homework=homework).exists():
        submit = NormalHomeworkSubmit.objects.filter(user=request.user, homework=homework).first()
        result['submitTime'] = submit.submit_time
        if submit.content is not None:
            result['submitContext'] = submit.content
        if submit.file is not None:
            result['submitFile'] = {
                'name': submit.file.name,
                'url': submit.get_file_url()
            }
        result['status'] = 1
        if submit.score is not None:
            result['score'] = submit.score
    else:
        result['status'] = 0

    return JsonResponse({"result": result}, status=200)


@jwt_auth()
@require_POST
def submit_score(request):
    user = request.user
    score = request.POST.get('score')
    submit_id = request.POST.get('id')

    submit = NormalHomeworkSubmit.objects.get(pk=submit_id)
    submit.score = score
    submit.markingPerson = user
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
