from django.shortcuts import render, redirect

from django.template import loader

from administration.models import Log

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

from account.models import Profile, Patient

from .forms import UserLoginForm, UserRegisterForm

# Create your views here.


def login_view(request):

    # if a user goes to the login screen while authenticated
    # they will be redirected to their profile
    if request.user.is_authenticated():
        return redirect('/profile')

    form = UserLoginForm(request.POST or None)
    title = "Login"
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request,user)

        if request.user.is_superuser:
            return redirect('/ad')
        else:
            return redirect('/profile')

    return render(request,"login/login.html",{"form":form,"title":title})


def logout_view(request):
    logout(request)
    return redirect('/login')


def register_view(request):

    # if a user goes to the login screen while authenticated
    # they will be redirected to their profile
    if request.user.is_authenticated():
        return redirect('/profile')


    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        profile = Profile()
        profile.user = user
        profile.save()

        patient = Patient()
        patient.profile = profile
        patient.save()

        log = Log(username=user.username, action=" registered as a patient")
        log.save()


        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect('/profile')

    context = {
        "form":form,
        "title":title
    }
    return render(request,"login/register.html",context)
