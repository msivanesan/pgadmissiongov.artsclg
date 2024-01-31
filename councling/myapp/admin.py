from django.contrib import admin
from django.urls import path
from django.utils.crypto import get_random_string
import csv
from django.shortcuts import render, redirect,get_object_or_404
from django.urls.resolvers import URLPattern
from . models import CustomUserStaff,CustomUserStudent,Department,PgStudentDetails,StoreoverallData,StoreFileOFUser
from django.contrib.auth.admin import UserAdmin
from . forms import CustomUserStaffCreationForm, CustomUserStaffChangeForm
from django.http import HttpResponse


# staff admin register
class CustomUserStaffAdmin(UserAdmin):
    add_form = CustomUserStaffCreationForm
    form = CustomUserStaffChangeForm
    model = CustomUserStaff
    list_display = ['email', 'username','phone_number','department' ,'is_active', 'is_staff']

    # Customize fieldsets
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email','phone_number','department')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'username','email','phone_number', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

admin.site.register(CustomUserStaff, CustomUserStaffAdmin)


#student admi9n register
class CustomUserStudentAdmin(UserAdmin):
    add_form = CustomUserStaffCreationForm
    form = CustomUserStaffChangeForm
    model = CustomUserStudent
    list_display = ['email', 'username','phone_number','password_created' ,'is_active', 'is_staff']

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
    

    def get_urls(self) :
        urls=super().get_urls()
        my_urls=[
             path('uploade/', self.admin_site.admin_view(self.upload_data), name='upload_data'),
        ]
        return my_urls+urls
    
    def upload_data(self,request):
        if request.method=='POST' and 'datafile' in request.FILES:
            try:
                data_file=request.FILES['datafile']
                decoded_file = data_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                for row in reader:
                   username=row['App_No']
                   email=row['Email']
                   phonenumber=row['Mobile']
                   password = get_random_string(10)
                   user, created = CustomUserStudent.objects.get_or_create(email=email,defaults={'username': username, 'phone_number': phonenumber} )
                   print()
                   if user:
                        de=row['Department'].lower()
                        dept=Department.objects.get(name=de)
                        if not dept:
                            print("no department")
                        else:
                            user.set_password(password)
                            user.password_created = password  # Store the raw password if necessary
                            user.save()
                            data,crt=PgStudentDetails.objects.get_or_create(student=user,name=row['Name'],gender=row['Gender'].lower(),distric=row['District'],community=row['Community'].lower(),percentageoptained=row['Percentage_mark'],Department=dept)
                            if data:
                                print("details already exsit ",user)
                            else:
                                print("error in detail :",user)

                   else:
                        print("User data failed !:")
                StoreoverallData.objects.create(datafile=data_file)
                return HttpResponse("CSV file processed successfully.")
            except ValueError as e:
                return HttpResponse(e)
        else:
            return render(request,'upload_csv.html')


admin.site.register(CustomUserStudent, CustomUserStudentAdmin)
admin.site.register(Department)
admin.site.register(PgStudentDetails,PgStudentDetailsadmin)
admin.site.register(StoreoverallData)
admin.site.register(StoreFileOFUser)

