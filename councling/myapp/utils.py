import pyotp
from datetime import datetime,timedelta

#create otp

def otp_generate(request):
    totp=pyotp.TOTP(pyotp.random_base32(),interval=60)
    otp=totp.now()
    request.session['otp_key']=totp.secret
    valid_date=datetime.now() + timedelta(minutes=1)
    request.session['valid_date']=str(valid_date)

    print(f'The OTP is :  {otp}')