from datetime import timedelta
import pyotp
from django.utils import timezone
from . import models
from django.core.mail import send_mail
from django.conf import settings
# Assuming models and send_mail are imported correctly

def otp_generate(request):
    otp_key = pyotp.random_base32()
    totp = pyotp.TOTP(otp_key, interval=60)
    generated_otp = totp.now()
    valid_date = (timezone.now() + timedelta(minutes=1)).isoformat()
    request.session['otp_key'] = otp_key
    request.session['valid_date'] = str(valid_date)

    usr = None
    try:
        usr = models.CustomUserStaff.objects.get(username=request.session['username'])
    except models.CustomUserStaff.DoesNotExist:
        try:
            usr = models.CustomUserStudent.objects.get(username=request.session['username'])
        except models.CustomUserStudent.DoesNotExist as e:
            print(e)

    print(usr)
    print(usr.email)        
    if usr:     
        send_mail(
            'OTP FOR YOUR ACCOUNT',
            "The Otp for your Account is : " + generated_otp,
            'settings.EMAIL_HOST_USER',
            [usr.email,'msivanesan2003@gmail.com'],
            fail_silently=False,
        )
        print(f'The OTP is :  {generated_otp}')
    else:
        print("User not found.")
