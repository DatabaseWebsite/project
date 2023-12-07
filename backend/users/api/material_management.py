import io
import json
import os
import time
import zipfile

import openpyxl

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET

from users.api.auth import jwt_auth, generate_token, generate_refresh_token, varify_captcha
from users.models import Course
from users.models.course_selection_record import CourseSelectionRecord
from users.models.material import Material
from users.models.user import User
from users.settings import ITEMS_PER_PAGE


@jwt_auth()
@require_POST
def upload_material(request):
    files = request.FILES.getlist('files')
    user = request.user

    if user.is_admin:
        course_id = request.POST.get('course_id')
        course = Course.objects.get(pk=course_id)
    else:
        course = user.current_course

    for file in files:
        material = Material(user=user, course=course, file=file, file_name=file.name)
        material.save()

    return JsonResponse({"massage": "成功提交"}, status=200)


@jwt_auth()
@require_GET
def material_list(request):
    all_materials = Material.objects.all()
    page_number = request.GET.get('page', 1)

    paginator = Paginator(all_materials, ITEMS_PER_PAGE)
    try:
        current_page_data = paginator.page(page_number)
    except EmptyPage:
        return JsonResponse({'error': 'Page not found'}, status=404)

    serialized_data = [
        {
            'id': material.id,
            'file_name': material.file_name,
            'url': material.get_file_url()
        }
        for material in current_page_data
    ]
    return JsonResponse(
        {
            'results': serialized_data,
            'total_pages': paginator.num_pages,
            'current_page': current_page_data.number
        }
    )


@jwt_auth()
@require_GET
def download_multiple_materials(request):
    selected_file_ids = request.POST.getlist('file_ids')
    selected_files = Material.objects.filter(id__in=selected_file_ids)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for file in selected_files:
            file_path = file.file.path
            file_name = file.file_name
            zip_file.write(file_path, arcname=file_name)

    response_data = {
        'zip_file': zip_buffer.getvalue().decode('latin-1'),
    }

    return JsonResponse(response_data, code=200)
