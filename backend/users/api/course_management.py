import json

from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from rest_framework import status

from users.api.auth import jwt_auth
from users.models import Course
from users.models.course_selection_record import CourseSelectionRecord
from users.settings import ITEMS_PER_PAGE


@jwt_auth()
@require_POST
def create_course(request):
    course_name = request.POST.get('course_name')
    user = request.user
    if user.is_admin:
        course = Course(name=course_name)
        course.save()
        return JsonResponse({"message": "创建成功"}, status=200)
    else:
        user_category = CourseSelectionRecord.objects.filter(user=user,
                                                             selected_course=user.current_course).first().type

        if user_category != 'TEACHER':
            return JsonResponse({"error": "您没有此权限"}, status=405)
        else:
            course = Course(name=course_name)
            course.save()
            return JsonResponse({"message": "创建成功"}, status=200)


@jwt_auth()
@require_GET
def all_course_info(request):
    user = request.user
    if user.is_admin:
        user_category = "ADMIN"
    else:
        user_category = CourseSelectionRecord.objects.filter(user=user,
                                                             selected_course=user.current_course).first().type
    if user.is_admin or user_category == "TEACHER" or user_category == "ASSISTANT":
        courses = Course.objects.all()
        data = [{'course_id': course.id, 'name': course.name} for course in courses]
        return JsonResponse({"result": data}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"error": "您没有此权限"}, status=405)


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
            "username": record.user.username,
            "name": record.user.name,
            "type": record.type
        }
        for record in courseSelectionRecords
    ]

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
