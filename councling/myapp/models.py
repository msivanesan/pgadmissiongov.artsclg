from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,Group,Permission
# Create your models here.


#department model
class Department(models.Model):
    name=models.CharField(max_length=30,null=False,unique=True)
    ug_couse=models.CharField(max_length=30,null=False)
    pg_course=models.CharField(max_length=30,null=False)


# custom user magement
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

# custom user model for staff
class CustomUserStaff(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    phone_number=models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    department=models.OneToOneField(Department,on_delete=models.CASCADE,null=True,blank=True)
    groups = models.ManyToManyField(
        Group,
        related_name="customuserstaff_groups",
        # other arguments...
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuserstaff_permissions",
        # other arguments...
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','phone_number']

    def __str__(self):
        return self.username
    


#custom user model student
class CustomUserStudent(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    phone_number=models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group,
        related_name="customuserstudent_groups",
        # other arguments...
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuserstudent_permissions",
        # other arguments...
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','phone_number']

    def __str__(self):
        return self.username
    
