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
    course = user.current_course

    for file in files:
        print(file.name)
        material = Material(user=user, course=course, file=file, file_name=file.name)
        material.save()

    return JsonResponse({"massage": "成功提交"}, status=200)


@jwt_auth()
@require_GET
def material_list(request):
    all_materials = Material.objects.all()

    result = [
        {
            'id': material.id,
            'name': os.path.splitext(material.file_name)[0],
            'fileName': material.file_name,
            'url': material.get_file_url(),
            'uploadTime': material.created_at
        }
        for material in all_materials
    ]

    return JsonResponse({'result': result}, status=200)


@jwt_auth()
@require_POST
def delete_material(request):
    material_id = request.POST.get("material_id")
    material = Material.objects.get(pk=material_id)
    material.delete()
    return JsonResponse({"message": "成功删除"}, status=200)


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
