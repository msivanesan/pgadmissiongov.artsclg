from django.urls import path
from . import views
urlpatterns = [
    path('login',views.Student_login,name="student_login"),
    path('logout',views.user_logout,name='logout'),
    path('opt-verfiy',views.otp_auth,name='otp_auth'),
    path('getdata',views.pgregister,name='register')
]