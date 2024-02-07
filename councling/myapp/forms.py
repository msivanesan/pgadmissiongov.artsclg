from django import forms
from django.contrib.auth.models import Group
from .models import CustomUserStudent,CustomUserStaff,StoreoverallData,PgStudentDetails
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth import authenticate


#add custom user form staff
class CustomUserStaffCreationForm(UserCreationForm):
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False, widget=forms.SelectMultiple)
    class Meta(UserCreationForm.Meta):
        model = CustomUserStaff
        fields = ('username','email','phone_number','department','groups')

class CustomUserStaffChangeForm(UserChangeForm):
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False, widget=forms.SelectMultiple)
    class Meta(UserChangeForm.Meta):
        model = CustomUserStaff
        fields = ('username','email','phone_number','department', 'groups','is_active', 'is_staff')

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
        model = PgStudentDetails
        exclude = ('student', 'status', 'details_submited', 'resevation', 'fees','rejectedBy','remark','resevation','percentageoptained','Department','distric','community')

    def __init__(self, *args, **kwargs):
        super(PgDataForm, self).__init__(*args, **kwargs)
        self.fields['fathername'].required = True
        self.fields['gender'].required = True
        self.fields['dateofbirth'].required = True
        self.fields['religion'].required = True
        self.fields['maratail_status'].required = True
        self.fields['pysically_chalanged'].required = True
        self.fields['sports'].required = True
        self.fields['aadhar'].required = True
        self.fields['address'].required = True
        self.fields['instute_name'].required = True
        self.fields['degree'].required = True
        self.fields['mode_of_study'].required = True
        self.fields['medium'].required = True
        self.fields['acadamic_year'].required = True
        self.fields['photo_doc'].required = True
        self.fields['aadhar_doc'].required = True
        self.fields['marksheet_doc'].required = True
        self.fields['community_doc'].required = True

        self.fields['special_doc'].required = False

    def clean(self):
        cleaned_data = super().clean()
        # Corrected field name to match the model's field
        physicaly_challenged = cleaned_data.get("pysically_chalanged")
        sports = cleaned_data.get("sports")
        special_doc = cleaned_data.get("special_doc")

        # If physically challenged or sports is 'yes', 'special_doc' is required
        if (physicaly_challenged == 'yes' or sports == 'yes') and not special_doc:
            self.add_error('special_doc', "This field is required if physically challenged or sports is 'YES'.")

        return cleaned_data