import re


from django.db.models import Q


from profiles.models import Profile


def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields, tag=False):
    query = None
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None
        if tag:
            term = "#" + term
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

def get_key(obj):
    if isinstance(obj, Profile):
        return obj.user.date_joined
    return obj.created
