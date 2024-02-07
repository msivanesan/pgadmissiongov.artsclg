# Create your views here.
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import pyotp
from . import forms
from .models import CustomUserStudent,StoreoverallData,PgStudentDetails
from datetime import datetime
from .utils import otp_generate

#user login 
def user_login(request):
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
            error_message='invalid username or password'
            return render(request,'login.html',{'error':error_message})
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
                    if user.role=='department':
                        return redirect('department',department=user.department.name, list='selected')
                    elif user.role=='controler':
                        return redirect('deptcontrol')
                    elif user.role=='principal':
                        return redirect('principal',list='admited')
                    elif user.role=='student':
                        return redirect('pgregister')
                    else:
                        return HttpResponse("error")
                else:
                    error_message='opt not valid'
            else:
                error_message='pot expried'
        else:
            error_message='somethig went wrong'
            return render(request,'otp_auth.html',{'error':error_message})
    return render(request,'otp_auth.html',{'error':error_message})


#user logout
def user_logout(request):
    logout(request)
    # Redirect to a success page, such as the home page.
    return HttpResponse('logout succs')


#to view the register the pg data
@login_required(login_url="login")
def pgregister(request):
    try:
        data = PgStudentDetails.objects.get(student=request.user)
    except PgStudentDetails.DoesNotExist:
        return HttpResponse("You have no data. Please contact the administrator.")
    if data.details_submited ==True :
        return HttpResponse("you have uploded the data ")
    else:
        if request.method == 'POST':
            form = forms.PgDataForm(request.POST, request.FILES, instance=data)
            if form.is_valid():
                data = form.save(commit=False)
                data.student = request.user
                data.details_submited=True
                data.status = "controler"
                data.save()
                return HttpResponse("Data uploaded successfully")
        else:
            form = forms.PgDataForm(instance=data)

        return render(request, 'pg/components/pgregister.html', {'forms': form})

