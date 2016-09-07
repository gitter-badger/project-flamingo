from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin


from models import Profile


class ProfileView(LoginRequiredMixin, generic.DetailView):
    model =  Profile
    template_name = 'profiles/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        return context


class CurrentProfile(generic.base.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        kwargs['pk'] = self.request.user.id
        self.url = '/profile/{}/'.format(kwargs['pk'])
        return super(CurrentProfile, self).get_redirect_url(*args, **kwargs)

