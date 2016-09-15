from django.utils.crypto import get_random_string


import models


allowed_chars='abcdefghtuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'


def generate_random_username(length=10, allowed_chars=allowed_chars):
    username = get_random_string(length, allowed_chars)

    try:
        models.MyUser.objects.get(username=username)
        return generate_random_username(length, allowed_chars)
    except models.MyUser.DoesNotExist:
        return username
