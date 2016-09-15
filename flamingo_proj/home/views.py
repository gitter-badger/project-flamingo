from itertools import chain


from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


from forms import SignUpForm
from utils import get_query, get_key
from posts.models import Post
from profiles.models import Profile


MyUser = get_user_model()


def home(request):
    logged_user = request.user
    posts = Post.objects.filter(
                posted_by__in=[fol.user.id
                               for fol in logged_user.profile.follows.all()
                               ]).order_by('-created')
    if request.user.is_authenticated():
        context = {
            'user_name': logged_user.get_full_name(),
            'posts': Post.add_liked_by_user(posts, request.user)
        }
        return render(request, 'home/feed.html', context)
    else:
        return render(request, 'home/home.html', {})


@csrf_protect
def sign_up(request):
    registered = False
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            registered = True
    else:
        form = SignUpForm()
    return render(request, 'home/signup.html', {'form': form, 'registered': registered})


@login_required
def search(request):
    query_string = ''
    found_users = None
    results = []
    if('q' in request.GET) and request.GET.get('q').strip():
        query_string = request.GET.get('q')
        user_query = get_query(query_string, ['user__first_name', 'user__last_name', ])
        users  = Profile.objects.filter(user_query)
        posts_query = get_query(query_string, ['tag__tag'], tag=True)
        posts = Post.objects.filter(posts_query)
        results = list(chain(users, posts))
        results = sorted(chain(users, posts), key=lambda instance: get_key(instance), reverse=True)
    return render(request, 'search.html',
                  context={'search_results': results, 'search': query_string})
