# Create your views here.
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
import pyotp
from .models import CustomUserStudent,StoreoverallData
from datetime import datetime
from .utils import otp_generate

#user login 
def Student_login(request):
    error_message=None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            otp_generate(request)
            request.session['username']=username
            request.session['password']=password
            return redirect('otp_auth')
        else:
           error_message='invalid username or'
    return render(request,'login.html',{'error':error_message})

# authenticate user with opt
def otp_auth(request):
    error_message=None
    if request.method=='POST':
        otp =request.POST['opt']
        username=request.session['username']
        password=request.session['password']
        otp_key=request.session['otp_key']
        validy=request.session['valid_date']
        if otp_key and validy is not None:
            valid_until=datetime.fromisoformat(validy)
            if valid_until>datetime.now():
                totp=pyotp.TOTP(otp_key,interval=60)
                if otp==totp.now():
                    user=authenticate(request, username=username, password=password)
                    login(request,user)
                    del request.session['otp_key']
                    del request.session['valid_date']
                    del request.session['password']
                    return redirect('logout')
                else:
                    error_message='opt not valid'
            else:
                error_message='pot expried'
        else:
            error_message='somethig went wrong'

    return render(request,'otp_auth.html',{'errormessage':error_message})




def user_logout(request):
    logout(request)
    # Redirect to a success page, such as the home page.
    return HttpResponse('logout succs')




