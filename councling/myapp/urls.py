from django.urls import path
from . import views
from . import extendedviews as view
urlpatterns = [
    path('login',views.user_login,name="login"),
    path('logout',views.user_logout,name='logout'),
    path('opt-verfiy',views.otp_auth,name='otp_auth'),
    path('getpgdata',views.pgregister,name='pgregister'),
    path('controler/<str:department>/',view.controller,name='controler'),
    path('controler/<str:department>/<str:userid>',view.constudent,name="constudent"),
    path('department/<str:department>/',view.department,name='department'),
    path('department/<str:department>/<str:userid>',view.depstudent,name="depstudent"),
    path('principal/',view.principal,name='principal'),
    path('principal/<str:userid>',view.pplstudent,name="pplstudent"),

]