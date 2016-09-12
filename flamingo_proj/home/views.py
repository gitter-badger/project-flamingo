from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from .forms import SignUpForm
from posts.models import Post


def home(request):
    logged_user = request.user
    if request.user.is_authenticated():
        context = {
            'user_name': logged_user.get_full_name(),
            'posts_by_followed': Post.objects.filter(
                posted_by__in=[fol.user.id
                               for fol in logged_user.profile.follows.all()
                               ]).order_by('-created')
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
