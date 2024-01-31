from django.db import models
from . helperfunctions import datafile_rename,Photo_rename,special_documents_rename,community_rename,validate_image_size,Marksheet_rename,aadhar_rename
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,Group,Permission
# Create your models here.

#department model
class Department(models.Model):
    name=models.CharField(max_length=30,null=False,unique=True)
    ug_couse=models.CharField(max_length=30,null=False)
    pg_course=models.CharField(max_length=30,null=False)

    def __str__(self):
        return self.name



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
    password_created=models.CharField(max_length=15,null=False,blank=False)
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
    
#details of pg studentr data
class PgStudentDetails(models.Model):
    GENDER=[
    ('male','MALE'),
    ('female','FEMALE'),
    ('others','OTHERS')
    ]
    COMUNNITY=[
        ('oc','OC'),
        ('bc','BC'),
        ('bcm','BCM'),
        ('sc','SC'),
        ('sca','SCA'),
        ('st','ST'),
        ('mbc','MBC')
    ]
    student=models.OneToOneField(CustomUserStudent,on_delete=models.CASCADE)
    name=models.CharField(max_length=30,null=False)
    gender=models.CharField(max_length=10,choices=GENDER)
    distric=models.CharField(max_length=30,null=False)
    community=models.CharField(max_length=5,choices=COMUNNITY)
    Department=models.ForeignKey(Department,on_delete=models.CASCADE)
    percentageoptained=models.CharField(max_length=3,null=False)

    @property
    def username(self):
        return "%s"%(self.student.username)

    def __str__(self):
        return self.name
    
# store datafiles uploded
class StoreoverallData(models.Model):
    datafile=models.FileField(null=False,upload_to=datafile_rename)

    def __str__(self):
        return str(self.datafile)


class StoreFileOFUser(models.Model):
    student=models.OneToOneField(CustomUserStudent,on_delete=models.CASCADE)
    photo=models.ImageField(null=False,upload_to=Photo_rename, validators=[validate_image_size])
    aadhar=models.ImageField(null=False,upload_to=aadhar_rename, validators=[validate_image_size])
    marksheet=models.ImageField(null=False,upload_to=Marksheet_rename, validators=[validate_image_size])
    community_doc=models.ImageField(null=False,upload_to=community_rename, validators=[validate_image_size])
    special_doc=models.ImageField(upload_to=special_documents_rename,null=True,blank=True, validators=[validate_image_size])

    def __str__(self):
        return self.student.username