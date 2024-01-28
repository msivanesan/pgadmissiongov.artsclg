# Create your views here.
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse


def Student_login(request):
    if request.method == 'POST':
        name = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return  HttpResponse("login succes") # Redirect to a success page.
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    # Redirect to a success page, such as the home page.
    return HttpResponse('logout succs')

