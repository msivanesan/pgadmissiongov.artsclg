# Create your views here.
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import pyotp
from . import forms
from .models import CustomUserStudent,StoreoverallData,PgStudentDetails
from datetime import datetime
from .utils import otp_generate
from django.utils import timezone  
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    return render(request,'home.html')
#user login 
def user_login(request):
    if request.user.is_authenticated:
        if request.user.role=='department':
            return redirect('department',department=user.department.name, list='selected')
        elif request.user.role=='controler':
            return redirect('depcontroler',department=request.user.department.name,list='truned up')
        elif request.user.role=='principal':
            return redirect('principal',list='admited')
        elif request.user.role=='student':
            return redirect('pgregister')
        else:
            return HttpResponse("you have no user role")
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
    error_message = None
    if request.method == 'POST':
        if 'resend' in request.POST:
            otp_generate(request)
        else:
            otp = request.POST['otp'].strip()  # Ensure no leading/trailing spaces
            username = request.session.get('username')
            password = request.session.get('password')
            otp_key = request.session.get('otp_key')
            validy = request.session.get('valid_date')
            
            if otp_key and validy:
                valid_until = datetime.fromisoformat(validy)
                if valid_until > timezone.now():  # Use timezone-aware comparison
                    totp = pyotp.TOTP(otp_key, interval=60)
                    if otp == totp.now():
                        user=authenticate(request, username=username, password=password)
                        login(request,user)
                        del request.session['otp_key']
                        del request.session['valid_date']
                        del request.session['password']
                        if user.role=='department':
                            return redirect('department',department=user.department.name, list='selected')
                        elif user.role=='controler':
                            return redirect('depcontroler',department=user.department.name,list='truned up')
                        elif user.role=='principal':
                            return redirect('principal',list='admited')
                        elif user.role=='student':
                            return redirect('pgregister')
                        else:
                            return HttpResponse("you have no user role")
                    else:
                        error_message = 'OTP not valid'
                else:
                    error_message = 'OTP expired'
            else:
                error_message = 'Something went wrong'
    ...
    return render(request, 'otp_auth.html', {'error': error_message})


#user logout
def user_logout(request):
    logout(request)
    # Redirect to a success page, such as the home page.
    return redirect("home")


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

        return render(request,'pg/components/pgregister.html', {'forms': form})
    
# user send email to user
def resendusr(request):
    error_message=None
    if request.method=='POST':
        username = request.POST.get('username')
        try:
            user=PgStudentDetails.objects.get(student__username=username)
            error_message=user
            print(user.student.email)
            send_mail(
                                    'USER NAME AND PASSWORD FOR YOUR ACCOUNT',
                                    'USERNAME : '+user.student.username +'  PASSWORD : ' + user.student.password_created,
                                    'settings.EMAIL_HOST_USER',
                                    [user.student.email],
                                    fail_silently=False,
                                )
            redirect('login')
        except Exception as e:
            error_message=e
    return render(request,'resend.html',{'error':error_message})