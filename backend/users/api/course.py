import json
from datetime import datetime

import pytz
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from rest_framework import status

from users.api.auth import jwt_auth
from users.models import Course, User
from users.models.course_selection_record import CourseSelectionRecord
from users.settings import ITEMS_PER_PAGE


@jwt_auth()
@require_POST
def create_course(request):
    course_name = request.POST.get('course_name')
    start_time_str = request.POST.get('start_time')
    start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time_str = request.POST.get('end_time')
    end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
    description = request.POST.get('course_description')
    course = Course(name=course_name, startTime=start_time, endTime=end_time, description=description)
    course.save()

    all_admins = User.objects.filter(is_admin=True)
    for admin in all_admins:
        record = CourseSelectionRecord(user=admin, selected_course=course, type="ADMIN")
        record.save()
        if admin.current_course is None:
            admin.current_course = course
            admin.save()

    return JsonResponse({"message": "新建成功"}, status=200)


@jwt_auth()
@require_GET
def all_course_info(request):
    courses = Course.objects.all()
    data = [
        {
            'course_id': course.id,
            'name': course.name
        } for course in courses]
    return JsonResponse({"result": data}, status=200)


@jwt_auth()
def course_list(request):
    user = request.user
    if user.is_admin:
        courses = Course.objects.all()
        data = [{
            'course_id': course.id,
            'name': course.name,
            'duration': course.startTime.strftime("%Y-%m-%d %H:%M:%S") + " 至 " + course.endTime.strftime("%Y-%m-%d %H:%M:%S"),
            'description': course.description,
        } for course in courses]
        return JsonResponse({"result": data}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"error": "权限不足"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@jwt_auth()
@require_POST
def all_participants(request):
    user = request.user
    page = request.POST.get('page')

    if user.is_admin:
        course_id = request.POST.get('course_id')
        course = Course.objects.get(pk=course_id)
    else:
        course = user.current_course

    courseSelectionRecords = CourseSelectionRecord.objects.filter(selected_course=course)

    result_ = [
        {
            "id": record.user.id,
            "personId": record.user.username,
            "name": record.user.name,
            "identity": record.type
        }
        for record in courseSelectionRecords
    ]
    print(result_)
    paginator = Paginator(result_, ITEMS_PER_PAGE)

    try:
        current_page_data = paginator.page(page)
    except EmptyPage:
        return JsonResponse({'error': 'Page not found'}, status=404)

    result = [item for item in current_page_data]

    return JsonResponse(
        {
            'result': result,
            'total_pages': paginator.num_pages,
            'current_page': current_page_data.number
        }, status=200
    )
