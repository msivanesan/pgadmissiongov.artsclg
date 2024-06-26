# Generated by Django 5.0.1 on 2024-01-31 14:24

import django.db.models.deletion
import myapp.helperfunctions
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('ug_couse', models.CharField(max_length=30)),
                ('pg_course', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='StoreoverallData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datafile', models.FileField(upload_to=myapp.helperfunctions.datafile_rename)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUserStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('phone_number', models.CharField(max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('password_created', models.CharField(max_length=15)),
                ('groups', models.ManyToManyField(related_name='customuserstudent_groups', to='auth.group')),
                ('user_permissions', models.ManyToManyField(related_name='customuserstudent_permissions', to='auth.permission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomUserStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('phone_number', models.CharField(max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(related_name='customuserstaff_groups', to='auth.group')),
                ('user_permissions', models.ManyToManyField(related_name='customuserstaff_permissions', to='auth.permission')),
                ('department', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.department')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PgStudentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('gender', models.CharField(choices=[('male', 'MALE'), ('female', 'FEMALE'), ('others', 'OTHERS')], max_length=10)),
                ('distric', models.CharField(max_length=30)),
                ('community', models.CharField(choices=[('oc', 'OC'), ('bc', 'BC'), ('bcm', 'BCM'), ('sc', 'SC'), ('sca', 'SCA'), ('st', 'ST'), ('mbc', 'MBC')], max_length=5)),
                ('percentageoptained', models.CharField(max_length=3)),
                ('address', models.CharField(blank=True, max_length=130, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=myapp.helperfunctions.Photo_rename, validators=[myapp.helperfunctions.validate_image_size])),
                ('aadhar', models.ImageField(blank=True, null=True, upload_to=myapp.helperfunctions.aadhar_rename, validators=[myapp.helperfunctions.validate_image_size])),
                ('marksheet', models.ImageField(blank=True, null=True, upload_to=myapp.helperfunctions.Marksheet_rename, validators=[myapp.helperfunctions.validate_image_size])),
                ('community_doc', models.ImageField(blank=True, null=True, upload_to=myapp.helperfunctions.community_rename, validators=[myapp.helperfunctions.validate_image_size])),
                ('special_doc', models.ImageField(blank=True, null=True, upload_to=myapp.helperfunctions.special_documents_rename, validators=[myapp.helperfunctions.validate_image_size])),
                ('details_submited', models.BooleanField(default=False)),
                ('status', models.CharField(max_length=30)),
                ('Department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.department')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myapp.customuserstudent')),
            ],
        ),
    ]
