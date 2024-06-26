
from django.contrib import admin
from django.urls import path
from django.utils.crypto import get_random_string
import csv
from django.shortcuts import render, redirect
from django.urls.resolvers import URLPattern
from . models import CustomUserStaff,CustomUserStudent,Department,PgStudentDetails,StoreoverallData
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.conf import settings
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
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'username','email','phone_number', 'password1', 'password2', 'is_active','department','role')}
        ),
    )

#student admin register
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


def export_as_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta}.csv'
    writer = csv.writer(response)
    
    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])
    
    return response

export_as_csv.short_description = "Export Selected to CSV"

#dstudent detail register
class PgStudentDetailsadmin(admin.ModelAdmin):
    list_display = ['username','name']
    search_fields=['student__username','name']
    list_filter=['Department','status']
    actions = [export_as_csv]


    def get_urls(self) :
        urls=super().get_urls()
        my_urls=[
            path('uploade/', self.admin_site.admin_view(self.upload_data), name='upload_data'),
        ]
        return my_urls+urls
    

    def upload_data(self, request):
        reportList = [['Application ID','depatment','Status']]  # Adjust the header for CSV output
        if request.method == 'POST' and 'datafile' in request.FILES:
            try:
                data_file = request.FILES['datafile']
                decoded_file = data_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                for row in reader:
                    username = row['App_No']
                    email = row['Email']
                    phonenumber = row['Mobile']
                    password = get_random_string(10)
                    user = CustomUserStudent.objects.filter(username=username).first()
                    if user:
                        # If user exists, no need to create a new one, just update the necessary fields
                        user.username = username  # Assuming you want to update the username
                        user.phone_number = phonenumber
                        # User's password and other fields can be updated here as needed
                        user.save()
                        user_created = False
                    else:
                        try:
                            user = CustomUserStudent.objects.create(email=email, username=username, phone_number=phonenumber)
                            user.set_password(password)
                            user.password_created = password  # Store the raw password if necessary
                            user.save()
                            user_created = True
                        except Exception as e:
                            reportList.append([username, '', e])
                            continue 
                    if user_created:
                        user.set_password(password)
                        user.password_created = password  # Store the raw password if necessary
                        user.save()
                    
                    de = row['Department'].lower()
                    try:
                        dept = Department.objects.get(name=de)
                        # Check if PgStudentDetails already exists for the user
                        pg_student_details, pg_created = PgStudentDetails.objects.update_or_create(
                            student=user,
                            defaults={
                                'name': row['Name'],
                                'gender': row['Gender'].lower(),
                                'distric': row['District'],
                                'community': row['Community'].lower(),
                                'percentageoptained': row['Percentage_mark'],
                                'Department': dept,
                                'status': 'applied'
                            }
                        )
                        if pg_created:
                            reportList.append([username,dept, 'Data created successfully'])
                                # send the user their user name and data\
                            send_mail(
                                    'USER NAME AND PASSWORD FOR YOUR ACCOUNT',
                                    'USERNAME : '+username +'PASSWORD :' + password,
                                    'settings.EMAIL_HOST_USER',
                                    ['msivanesan2003@gmail.com'],
                                    fail_silently=False,
                                )
                        else:
                            reportList.append([username, dept,'Data already exist'])
                    except Department.DoesNotExist:
                        reportList.append([username, de,'Has no department'])

                StoreoverallData.objects.create(datafile=data_file)
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="report_list.csv"'
                writer = csv.writer(response)
                writer.writerows(reportList)  # Use writerows to write all entries in reportList
                return response
            except Exception as e:  # Catch broader exceptions if necessary
                return HttpResponse(f"Error processing the file: {e}")
        else:
            return render(request, 'upload_csv.html')


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
