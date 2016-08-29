from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, LoginForm


def login(request):
    title = 'Welcome '

    # Add a form
    form = LoginForm(request.POST)
    context = {
        'title': title,
        'form': form
    }

    if form.is_valid():
        instance = form.save()
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
        context = {
            'title': "Logged in user {}".format(email)
        }
    return render(request, 'home/login.html', context)


def sign_up(request):
    title = 'Welcome '
    if request.user.is_authenticated():
        title += str(request.user)

    # Add a form
    form = SignUpForm(request.POST)
    context = {
        'title': title,
        'form': form
    }

    if form.is_valid():
        form.save()
        context = {
            'title': "Welcome!"
        }
    return render(request, 'home/login.html', context)
