from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .forms import PostForm


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
