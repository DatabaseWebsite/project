import random

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from users.models.email_captcha import EmailCaptcha


@require_POST
def send_captcha(request):
    email = request.POST.get('email')
    captcha = '%06d' % random.randint(0, 999999)
    email_title = 'CourseConnect 验证码'
    email_body = '您的验证码为：' + captcha + '，请在5分钟内输入。'
    send_status = send_mail(email_title, email_body, settings.EMAIL_HOST_USER, [email])
    if send_status:
        entry = EmailCaptcha(email=email, captcha=captcha)
        entry.save()
        return JsonResponse({"message": "邮件发送成功，可能存在一定的延迟，请耐心等待。"})
    else:
        return JsonResponse({"error": "邮件发送失败"}, status=400)

