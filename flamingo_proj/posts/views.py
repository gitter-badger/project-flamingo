from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse


from .forms import PostForm
from .models import Tag, Post, Like


class PostView(LoginRequiredMixin, generic.DetailView):
    model = Post
    template_name = 'posts/post_detail.html'


def create_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.posted_by = request.user
        instance.save()
        messages.success(request, "You posted successfully!")
        return redirect('profiles:go-to-profile')
    context = {'form': form,
               'posted_by': request.user.id}
    return render(request, 'posts/post_form.html', context)


@login_required
def like(request, id):
    if request.method == 'GET':
        try:
            Like.objects.get(
                liked_by=request.user,
                post=Post.objects.get(id=id))
            return JsonResponse({'liked_by_user': True})
        except Like.DoesNotExist:
            return JsonResponse({'liked_by_user': False})

    elif request.method == 'POST':
        obj, created = Like.objects.get_or_create(
            liked_by=request.user,
            post=Post.objects.get(id=id),
        )
        if not created:
            obj.delete()
            return JsonResponse({'liked_by_user': False})
        else:
            return JsonResponse({'liked_by_user': True})


@login_required
def posts_by_tag(request, tag):
    requested_tag = Tag.objects.get(tag='#' + tag)
    posts = Post.objects.filter(tag=requested_tag).order_by('-created')
    context = {
        "tag": tag,
        # "posts": Tag.objects.get(tag='#' + tag).posts.order_by('-created')
        "posts": Post.add_liked_by_user(posts, request.user)
    }
    return render(request, 'posts/tag.html', context)


@login_required
def post_edit(request, id):
    instance = get_object_or_404(Post, id=id)
    if request.user.id == instance.posted_by.id:
        form = PostForm(request.POST or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "You have successfully edited this post!")
            return redirect('profiles:go-to-profile')
        context = {
            'instance': instance,
            'form': form
        }
        return render(request, 'posts/post_form.html', context)
    else:
        raise Http404("You can only edit your own posts!")


def post_delete(request, id):
    instance = get_object_or_404(Post, id=id)
    if request.user.id == instance.posted_by.id:
        instance.delete()
        messages.success(request, "You have successfully deleted this post!")
        return redirect('profiles:go-to-profile')
    else:
        raise Http404("You can only delete your own posts")
