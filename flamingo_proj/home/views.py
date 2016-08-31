from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.views import generic


from .forms import SignUpForm


class HomePageView(generic.TemplateView):
    template_name = 'home/home.html'


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('signup_success')
        else:
            return HttpResponseRedirect('signup')

    args = {}
    args['form'] = SignUpForm()
    return render(request, 'home/signup.html', args)

