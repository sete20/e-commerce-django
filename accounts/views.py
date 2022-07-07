from django.contrib import messages, auth
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator


def register(request):
    context = {
        'form': RegisterForm
    }
    return render(request, 'accounts/register.html', context)


def CreateUser(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        phone_number = form.cleaned_data['phone_number']
        password = form.cleaned_data['password']
        username = email.split('@')[0]
        user = Account.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password
        )
        user.phone_number = phone_number
        user.save()
        messages.success(request=request, message='registered successfully')
        return redirect('register')
    else:
        messages.error(request=request, message="Register failed!")
        return redirect('register')


def login(request):
    return render(request, 'accounts/login.html')


def loginPost(request):

    user = auth.authenticate(email=request.POST.get(
        'email'), password=request.POST.get(
        'password'))
    # return HttpResponse(user)
    # exit()
    if user != None:
        # if user.is_active == 1:
        #     messages.success(request=request, message="Login successful!")
        #     return redirect('login')
        # else:
        messages.error(
            request=request, message="Login successful but the user is inactive !")
        return redirect('login')
    else:
        messages.error(request=request,
                       message="Login field please try again!")
        return redirect('login')


@login_required  # middleware
def logout(request):
    auth.logout(request)
    messages.success(request=request, message="You are logged out!")
    return redirect('login')


def forgotPassword(request):
    pass
