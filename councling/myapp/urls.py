from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from . import extendedviews as view
urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.user_login,name="login"),
    path('logout',views.user_logout,name='logout'),
    path('opt-verfiy',views.otp_auth,name='otp_auth'),  
    path('getpgdata',views.pgregister,name='pgregister'),
    path('resend',views.resendusr,name='resend_user'),
    path('controler/<str:department>/',view.setchange,name='setchange'),
    path('controler/<str:department>/<str:list>/',view.controller,name='depcontroler'),
    path('controler/<str:department>/<str:list>/<str:userid>',view.constudent,name="constudent"),
    path('department/<str:department>/<str:list>/',view.department,name='department'),
    path('department/<str:department>/<str:list>/<str:userid>',view.depstudent,name="depstudent"),
    path('principal/<str:list>/',view.principal,name='principal'),
    path('principal/<str:list>/<str:userid>',view.pplstudent,name="pplstudent"),
    path('office/',view.office,name='office'),
    path('office/<str:userid>',view.stdoffice,name='stdoffice')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)