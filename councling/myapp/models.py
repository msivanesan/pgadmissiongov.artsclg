from django.db import models
from . helperfunctions import datafile_rename,Photo_rename,special_documents_rename,community_rename,validate_image_size,Marksheet_rename,aadhar_rename
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,Group,Permission
# Create your models here.

#department model
class Department(models.Model):
    name=models.CharField(max_length=30,null=False,unique=True)
    ug_couse=models.CharField(max_length=30,null=False)
    pg_course=models.CharField(max_length=30,null=False)
    pg_oc=models.IntegerField(default=0,null=False)
    pg_bc=models.IntegerField(default=0,null=False)
    pg_bcm=models.IntegerField(default=0,null=False)
    pg_sc=models.IntegerField(default=0,null=False)
    pg_sca=models.IntegerField(default=0,null=False)
    pg_st=models.IntegerField(default=0,null=False)
    pg_mbc=models.IntegerField(default=0,null=False)


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
    ROLE=[
        ('controler','CONTROLER'),
        ('department','DEPARTMENT'),
        ('principal','PRINCIPAL'),
        ('office','OFFICE')
    ]
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    phone_number=models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    role=models.CharField(max_length=10,null=True,choices=ROLE)
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
    role=models.CharField(max_length=10,default='student')
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
    BOOLOPT=[
        ('yes','YES'),
        ('no','NO')
    ]
    MAR_STATUS=[
        ('single','SINGLE'),
        ('married','MARRIED')
    ]
    RELIGION=[
        ('hindu','HINDU'),
        ('muslim','MUSLIM'),
        ('cristin','CRISTIN')
    ]
    STATUS=[
        ('applied','APPLIED'),
        ('controler','CONTROLER'),
        ('department','DEPARTMENT'),
        ('admited','ADMITED'),
        ('rejected','REJECTED')
    ]
    #PERSONAL DETAILS
    student=models.OneToOneField(CustomUserStudent,on_delete=models.CASCADE)
    name=models.CharField(max_length=30,null=False)
    fathername=models.CharField(max_length=30,null=True,blank=True)
    gender=models.CharField(max_length=10,choices=GENDER)
    dateofbirth=models.DateField(null=True,blank=True)
    community=models.CharField(max_length=5,choices=COMUNNITY)
    religion=models.CharField(max_length=20,choices=RELIGION,null=True,blank=True)
    maratail_status=models.CharField(max_length=10,null=True,blank=True,choices=MAR_STATUS)
    pysically_chalanged=models.CharField(max_length=5,choices=BOOLOPT,null=True,blank=True)
    sports=models.CharField(max_length=5,choices=BOOLOPT,null=True,blank=True)
    aadhar=models.CharField(max_length=30,null=True,blank=True)
    address=models.CharField(max_length=130,null=True,blank=True)
    distric=models.CharField(max_length=30,null=False)
    #educational details
    Department=models.ForeignKey(Department,on_delete=models.CASCADE)
    percentageoptained=models.CharField(max_length=5,null=False)
    instute_name=models.CharField(max_length=30,null=True,blank=True)
    degree=models.CharField(max_length=30,null=True,blank=True)
    mode_of_study=models.CharField(max_length=30,null=True,blank=True)
    medium=models.CharField(max_length=30,null=True,blank=True)
    acadamic_year=models.CharField(max_length=30,null=True,blank=True)
    
    #DOCUMENTS
    photo_doc=models.ImageField(upload_to=Photo_rename, validators=[validate_image_size],null=True,blank=True)
    aadhar_doc=models.ImageField(upload_to=aadhar_rename, validators=[validate_image_size],null=True,blank=True)
    marksheet_doc=models.ImageField(upload_to=Marksheet_rename, validators=[validate_image_size],null=True,blank=True)
    community_doc=models.ImageField(upload_to=community_rename, validators=[validate_image_size],null=True,blank=True)
    special_doc=models.ImageField(upload_to=special_documents_rename,null=True,blank=True, validators=[validate_image_size])
    
    #DEPARTMENT FIELDS
    details_submited=models.BooleanField(default=False)
    status=models.CharField(max_length=30,null=False, choices=STATUS)
    resevation=models.CharField(max_length=10, null=True,blank=True)
    remark=models.CharField(max_length=150,null=True,blank=True)
    fees=models.BooleanField(default=False)



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

