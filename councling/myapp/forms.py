from django import forms
from .models import CustomUserStudent,CustomUserStaff,StoreoverallData,PgStudentDetails
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth import authenticate


#add custom user form staff
class CustomUserStaffCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUserStaff
        fields = ('username','email','phone_number','department')


class CustomUserStaffChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUserStaff
        fields = ('username','email','phone_number','department', 'is_active', 'is_staff')

#for for student custom form
class CustomUserStudentCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUserStudent
        fields = ('username','email','phone_number',)


class CustomUserStudentChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUserStudent
        fields = ('username','email','phone_number', 'is_active', 'is_staff')



#student login forms

class customUserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Invalid login')
        
        return cleaned_data

#get data
class PgDataForm(forms.ModelForm):
    class Meta:
        model=PgStudentDetails
        exclude=('student','status','details_submited',)