from django.shortcuts import render, get_object_or_404
from . models import Post, Like
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .forms import PostForm


# @login_required
# def feed(request):
#     logged_user = request.user
#     context = {
#         'user_name': logged_user.get_full_name(),
#         'own_posts': Post.objects.filter(posted_by=logged_user.id),
#         'posts_by_followed': Post.objects.filter(
#             posted_by__in=[fol.user.id
#                            for fol in logged_user.profile.follows.all()
#                            ])
#     }
#     return render(request, 'posts/feed.html', context)


def create_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.posted_by = request.user
        instance.save()
    context = {'form': form,
               'posted_by': request.user.id}
    return render(request, 'posts/create.html', context)


@login_required
@require_POST
def like(request):
    pass
