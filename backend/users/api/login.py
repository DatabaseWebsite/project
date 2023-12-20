import json
import os
import time
from datetime import datetime
import pytz
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q

from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET

from users.api.auth import jwt_auth
from users.models import Course
from users.models.course_selection_record import CourseSelectionRecord
from users.models.log import LoginLog, OperationLog
from users.models.normal_homework import NormalHomework
from users.models.normal_homework_submit import NormalHomeworkSubmit
from users.models.picture import Picture
from users.settings import ITEMS_PER_PAGE


@require_POST
def record_login_log(request):
    ip = request.POST.get('ip')
    address = request.POST.get('address')
    browser = request.POST.get('browser')
    log_time_str = str(request.POST.get('time'))
    log_time = pytz.utc.localize(datetime.strptime(log_time_str, '%Y-%m-%dA%H:%M:%S'))
    username = request.POST.get('username')

    _login_log = LoginLog(ip=ip, address=address, browser=browser, time=log_time, username=username)
    _login_log.save()

    return JsonResponse({"message": "success"}, status=200)


@require_POST
def record_operation_log(request):
    request_module = request.POST.get('request_module')
    api = request.POST.get('api')
    operation = request.POST.get('operation')
    ip = request.POST.get('ip')
    browser = request.POST.get('browser')
    operation_status = request.POST.get('status')
    code = request.POST.get('code')
    operation_time_str = str(request.POST.get('time'))
    operation_time = pytz.utc.localize(datetime.strptime(operation_time_str, '%Y-%m-%dA%H:%M:%S'))
    username = request.POST.get('username')

    _operation_log = OperationLog(request_module=request_module, api=api, operation=operation, ip=ip, browser=browser,
                                 status=operation_status, code=code, time=operation_time, username=username)
    _operation_log.save()

    return JsonResponse({"message": "success"}, status=200)


@require_GET
def login_log(request):
    all_login_log = LoginLog.objects.all()
    items_per_page = ITEMS_PER_PAGE
    page_number = request.GET.get("page", 1)
    if page_number == "":
        items_per_page = all_login_log.count()
        page_number = 1

    paginator = Paginator(all_login_log, items_per_page)
    try:
        current_page_data = paginator.page(page_number)
    except EmptyPage:
        return JsonResponse({'error': 'Page not found'}, status=404)

    serialized_data = [
        {
            "ip": log.ip,
            "address": log.address,
            "browser": log.browser,
            "time": log.time,
            "username": log.username
        }
        for log in current_page_data
    ]

    return JsonResponse({
        'result': serialized_data,
        'total_pages': paginator.num_pages,
        'current_page': current_page_data.number}, status=200)


@require_GET
def operation_log(request):
    all_operation_log = OperationLog.objects.all()
    items_per_page = ITEMS_PER_PAGE
    page_number = request.GET.get("page", 1)
    if page_number == "":
        items_per_page = all_operation_log.count()
        page_number = 1
    paginator = Paginator(all_operation_log, items_per_page)
    try:
        current_page_data = paginator.page(page_number)
    except EmptyPage:
        return JsonResponse({'error': 'Page not found'}, status=404)
    print(all_operation_log.count())
    serialized_data = [
        {
            "request_module": log.request_module,
            "api": log.api,
            "operation": log.operation,
            "ip": log.ip,
            "browser": log.browser,
            "time": log.time,
            "username": log.username,
            "status": log.status,
            "code": log.code
        }
        for log in current_page_data
    ]
    return JsonResponse({
        'result': serialized_data,
        'total_pages': paginator.num_pages,
        'current_page': current_page_data.number}, status=200)


@require_POST
def search_login_log(request):
    ip = request.POST.get('ip')
    address = request.POST.get('address')
    start_time_str = str(request.POST.get('start_time'))
    end_time_str = str(request.POST.get('end_time'))
    start_time = pytz.utc.localize(datetime.strptime(start_time_str, '%Y-%m-%dA%H:%M:%S'))
    end_time = pytz.utc.localize(datetime.strptime(end_time_str, '%Y-%m-%dA%H:%M:%S'))
    username = request.POST.get('username')
    page = int(request.POST.get('page'))

    query_login_log = Q()
    if ip:
        query_login_log &= Q(ip=ip)
    if address:
        query_login_log &= Q(address=address)
    if username:
        query_login_log &= Q(username=username)

    if start_time and end_time:
        query_login_log &= Q(time__range=(start_time, end_time))
    elif start_time and not end_time:
        query_login_log &= Q(time__gte=start_time)
    elif end_time and not start_time:
        query_login_log &= Q(time__lte=end_time)

    filtered_login_log = LoginLog.objects.filter(query_login_log)

    paginator = Paginator(filtered_login_log, ITEMS_PER_PAGE)
    try:
        current_page_data = paginator.page(page)
    except EmptyPage:
        return JsonResponse({'error': 'Page not found'}, status=404)

    serialized_data = [
        {
            "ip": log.ip,
            "address": log.address,
            "browser": log.browser,
            "time": log.time,
            "username": log.username
        }
        for log in current_page_data
    ]

    return JsonResponse({
        'result': serialized_data,
        'total_pages': paginator.num_pages,
        'current_page': current_page_data.number}, status=200)


@require_POST
def search_operation_log(request):
    request_module = request.POST.get('request_module')
    ip = request.POST.get('ip')
    operation = request.POST.get('operation')
    username = request.POST.get('username')
    api = request.POST.get('api')

    start_time_str = str(request.POST.get('start_time'))
    end_time_str = str(request.POST.get('end_time'))
    start_time = pytz.utc.localize(datetime.strptime(start_time_str, '%Y-%m-%dA%H:%M:%S'))
    end_time = pytz.utc.localize(datetime.strptime(end_time_str, '%Y-%m-%dA%H:%M:%S'))

    page = int(request.POST.get('page'))

    query_operation_log = Q()
    if ip:
        query_operation_log &= Q(ip=ip)
    if request_module:
        query_operation_log &= Q(request_module=request_module)
    if operation:
        query_operation_log &= Q(operation=operation)
    if username:
        query_operation_log &= Q(username=username)
    if api:
        query_operation_log &= Q(api=api)

    if start_time and end_time:
        query_operation_log &= Q(time__range=(start_time, end_time))
    elif start_time and not end_time:
        query_operation_log &= Q(time__gte=start_time)
    elif end_time and not start_time:
        query_operation_log &= Q(time__lte=end_time)

    filtered_operation_log = OperationLog.objects.filter(query_operation_log)

    paginator = Paginator(filtered_operation_log, ITEMS_PER_PAGE)
    try:
        current_page_data = paginator.page(page)
    except EmptyPage:
        return JsonResponse({'error': 'Page not found'}, status=404)

    serialized_data = [
        {
            "request_module": log.request_module,
            "api": log.api,
            "operation": log.operation,
            "ip": log.ip,
            "browser": log.browser,
            "time": log.time,
            "username": log.username,
            "status": log.status,
            "code": log.code
        }
        for log in current_page_data
    ]

    return JsonResponse({
        'result': serialized_data,
        'total_pages': paginator.num_pages,
        'current_page': current_page_data.number}, status=200)