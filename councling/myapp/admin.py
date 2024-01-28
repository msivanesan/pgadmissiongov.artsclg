from django.contrib import admin
from . models import CustomUserStaff,CustomUserStudent,Department
from django.contrib.auth.admin import UserAdmin
from . forms import CustomUserStaffCreationForm, CustomUserStaffChangeForm


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

class CustomUserStudentAdmin(UserAdmin):
    add_form = CustomUserStaffCreationForm
    form = CustomUserStaffChangeForm
    model = CustomUserStudent
    list_display = ['email', 'username','phone_number', 'is_active', 'is_staff']

    # Customize fieldsets
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email','phone_number')}),
        ('Permissions', {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'username','email','phone_number', 'password1', 'password2', 'is_active')}
        ),
    )

admin.site.register(CustomUserStudent, CustomUserStudentAdmin)
admin.site.register(Department)