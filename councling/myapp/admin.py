from django.contrib import admin
from django.urls import path
from django.utils.crypto import get_random_string
import csv
from django.shortcuts import render, redirect,get_object_or_404
from django.urls.resolvers import URLPattern
from . models import CustomUserStaff,CustomUserStudent,Department,PgStudentDetails,StoreoverallData
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from . forms import CustomUserStaffCreationForm, CustomUserStaffChangeForm
from django.http import HttpResponse


class customadminarea(admin.AdminSite):
    site_header="Online Counsling"

cusadmin=customadminarea(name="admin area")

# staff admin register
class CustomUserStaffAdmin(UserAdmin):
    add_form = CustomUserStaffCreationForm
    form = CustomUserStaffChangeForm
    model = CustomUserStaff
    search_fields=['username','email']
    list_display = ['email', 'username','phone_number','department' ,'is_active']

    # Customize fieldsets
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email','phone_number','department','role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'username','email','phone_number', 'password1', 'password2', 'is_active','department','role','groups')}
        ),
    )




#student admi9n register
class CustomUserStudentAdmin(UserAdmin):
    add_form = CustomUserStaffCreationForm
    form = CustomUserStaffChangeForm
    model = CustomUserStudent
    search_fields=['username','email']
    list_display = ['email', 'username','phone_number','password_created' ]

    # Customize fieldsets
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email','phone_number','password_created')}),
        ('Permissions', {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'username','email','phone_number', 'password1', 'password2','password_created','is_active')}
        ),
    )


#dstudent detail register

class PgStudentDetailsadmin(admin.ModelAdmin):
    list_display = ['username','name']
    search_fields=['student__username','name']

    def get_urls(self) :
        urls=super().get_urls()
        my_urls=[
             path('uploade/', self.admin_site.admin_view(self.upload_data), name='upload_data'),
        ]
        return my_urls+urls
    
    def upload_data(self,request):
        reportList=[]
        if request.method=='POST' and 'datafile' in request.FILES:
            try:
                data_file=request.FILES['datafile']
                decoded_file = data_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                for row in reader:
                   ls=[]
                   username=row['App_No']
                   email=row['Email']
                   phonenumber=row['Mobile']
                   password = get_random_string(10)
                   user, created = CustomUserStudent.objects.get_or_create(email=email,defaults={'username': username, 'phone_number': phonenumber} )
                   if user:
                        de=row['Department'].lower()
                        try:
                            dept=Department.objects.get(name=de)
                            user.set_password(password)
                            user.password_created = password  # Store the raw password if necessary
                            user.save()
                            data,crt=PgStudentDetails.objects.get_or_create(student=user,name=row['Name'],gender=row['Gender'].lower(),distric=row['District'],community=row['Community'].lower(),percentageoptained=row['Percentage_mark'],Department=dept,status='applied')
                            if data:
                                ls=[username,'data updated succesfully']
                                reportList.append(ls)
                            else:
                                ls=[username,'data not updated !error in data']
                                reportList.append(ls)
                        except  Exception as e:
                             ls=[username,'has no department']
                             reportList.append(ls)
                   else:
                        ls=[username,'user not created']
                        reportList.append(ls)
                StoreoverallData.objects.create(datafile=data_file)
                return HttpResponse(str(reportList))
            except ValueError as e:
                return HttpResponse(e)
        else:
            return render(request,'upload_csv.html')

# admin.site.register(CustomUserStaff, CustomUserStaffAdmin)
# admin.site.register(CustomUserStudent, CustomUserStudentAdmin)
# admin.site.register(Department)
# admin.site.register(PgStudentDetails,PgStudentDetailsadmin)
# admin.site.register(StoreoverallData)

cusadmin.register(CustomUserStaff, CustomUserStaffAdmin)
cusadmin.register(CustomUserStudent, CustomUserStudentAdmin)
cusadmin.register(Department)
cusadmin.register(PgStudentDetails,PgStudentDetailsadmin)
cusadmin.register(StoreoverallData)




