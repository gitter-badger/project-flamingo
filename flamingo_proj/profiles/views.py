import operator


from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import render


from models import Profile
from posts.models import Post
from utils import get_query


MyUser = get_user_model()


class ProfileView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = 'profiles/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        return context


class GoToProfile(LoginRequiredMixin, generic.base.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        kwargs['pk'] = self.request.user.id
        self.url = '/profile/{}/'.format(kwargs['pk'])
        return super(GoToProfile, self).get_redirect_url(*args, **kwargs)


@login_required
def search_users(request):
    query_string = ''
    found_users = None
    if('q' in request.GET) and request.GET.get('q').strip():
        query_string = request.GET.get('q')
        user_query = get_query(query_string, ['first_name', 'last_name', ])
        found_users = MyUser.objects.filter(user_query)
    return render(request, 'profiles/search.html',
                  context={'search_results': found_users, 'search': query_string})
