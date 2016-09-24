from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import JsonResponse
from models import Profile
from posts.models import Post


class ProfileView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = 'profiles/profile.html'

    def get_context_data(self, **kwargs):
        posts = Post.objects.filter(
            posted_by=self.object.user.id).order_by('-created')
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['posts'] = Post.add_liked_by_user(posts, self.request.user)
        Post.add_shared_property(context['posts'])
        return context


class GoToProfile(LoginRequiredMixin, generic.base.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        kwargs['pk'] = self.request.user.id
        self.url = '/profile/{}/'.format(kwargs['pk'])
        return super(GoToProfile, self).get_redirect_url(*args, **kwargs)


def follow_user(request, id):
    if request.method == 'GET':
        try:
            follows = Profile.objects.get(user_id=request.user).follows.all()
            to_follow = Profile.objects.get(user_id=id)
            if to_follow in follows:
                return JsonResponse({'followed_by_user': True})
            else:
                return JsonResponse({'followed_by_user': False})
        except Profile.DoesNotExist:
            return JsonResponse({'followed_by_user': 'Error! No such user!'})

    if request.method == 'POST':
        try:
            follows = Profile.objects.get(user_id=request.user).follows.all()
            to_follow = Profile.objects.get(user_id=id)
            if to_follow in follows:
                print "ALREADY FOLLOWING"
                request.user.profile.follows.remove(to_follow)
                return JsonResponse({'followed_by_user': False})
            else:
                print "FOLLOW!"
                request.user.profile.follows.add(to_follow)
                return JsonResponse({'followed_by_user': True})
        except:
            return JsonResponse({'followed_by_user': 'Error! No such user!'})
