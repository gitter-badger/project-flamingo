from django.shortcuts import render
from django.views import generic
from django.views.decorators.csrf import csrf_protect


from .forms import SignUpForm


class HomePageView(generic.TemplateView):

    template_name = 'home/home.html'


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
