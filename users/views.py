"""users app"""

from django.core.exceptions import NON_FIELD_ERRORS
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from users.forms import RegistrationForm, LoginForm, ProfileForm

REGIS_PAGE = 'users/register.html'
REGIS_DONE_PAGE = 'users/register_success.html'
VERIF_DONE_PAGE = 'users/email_verified.html'
LOGIN_PAGE = 'users/login.html'
USER_PROF_PAGE = 'users/profile.html'


def register(request):
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, REGIS_PAGE, context={"form": form})
    elif request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.send_verification_email()
            login(request, user)
            return render(request, REGIS_DONE_PAGE)
        else:
            return render(request, REGIS_PAGE, context={"form": form})


def verify(request):
    user = request.user
    data = request.GET
    if user.is_token_correct(data['token']):
        user.verify_email()
        return render(request, VERIF_DONE_PAGE)
    else:
        return Http404("NOT FOUND")


def login_user(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, LOGIN_PAGE, context={
            'form': form
        })
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        form.is_valid()
        user = form.get_user(request)
        if user and user.is_email_verified:
            login(request, user)
            return redirect("/")
        else:
            form.errors[NON_FIELD_ERRORS] = 'Cannot perform login with this credentials'
            return render(request, LOGIN_PAGE, context={
                'form': form,
            })


@login_required
def logout_user(request):
    logout(request)
    return redirect("/")


@login_required
def user_profile(request):
    user = request.user
    if request.method == 'GET':
        form = ProfileForm(instance=user)
        return render(request, USER_PROF_PAGE, context={"form": form})
    elif request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = form.save()

            return render(request, USER_PROF_PAGE)
        else:
            return render(request, USER_PROF_PAGE, context={"form": form})
