from django.http import JsonResponse

from users.models import User


def reset_avatar(request):
    users = User.objects.all()
    for user in users:
        user.avatar = "avatars/default.png"
        user.save()
        print(user.get_avatar_url())

    return JsonResponse({"message": "成功了"}, status=200)
