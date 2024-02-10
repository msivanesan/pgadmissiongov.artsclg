import pyotp
from datetime import datetime,timedelta
from django.utils import timezone
#create otp

def otp_generate(request):
    otp_key = pyotp.random_base32()
    totp = pyotp.TOTP(otp_key, interval=60)
    generated_otp = totp.now()
    valid_date = (timezone.now() + timedelta(minutes=1)).isoformat()
    request.session['otp_key']=otp_key
    request.session['valid_date']=str(valid_date)
    print(f'The OTP is :  {generated_otp}')