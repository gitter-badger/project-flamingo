import re


from django.utils.crypto import get_random_string
from django.db.models import Q


import models


allowed_chars='abcdefghtuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'


def generate_random_username(length=10, allowed_chars=allowed_chars):
    username = get_random_string(length, allowed_chars)

    try:
        models.MyUser.objects.get(username=username)
        return generate_random_username(length, allowed_chars)
    except models.MyUser.DoesNotExist:
        return username


def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    query = None
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{"{}__icontains".format(field_name): term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
