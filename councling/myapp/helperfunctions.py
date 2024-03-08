import os
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from datetime import datetime

#rename photo
def Photo_rename(instance, filename):
    ext = filename.split('.')[-1]
    title_slug = instance.student.username
    new_filename = f"{title_slug}photo.{ext}"
    return os.path.join('uploads/photos/', new_filename)

def datafile_rename(instance, filename):
    ext = filename.split('.')[-1]
    if ext  != 'csv':
        raise ValueError("please uplode the csv file !:)")
    title_slug = slugify(datetime.now())
    new_filename = f"{title_slug}datafile.{ext}"
    return os.path.join('uploads/files/', new_filename)


#rename aadhar
def aadhar_rename(instance, filename):
    ext = filename.split('.')[-1]
    title_slug = slugify(instance.student.username)
    new_filename = f"{title_slug}aadhar.{ext}"
    return os.path.join('uploads/aadhars/', new_filename)


#remane marksheet
def Marksheet_rename(instance, filename):
    ext = filename.split('.')[-1]
    title_slug = slugify(instance.student.username)
    new_filename = f"{title_slug}marksheet.{ext}"
    return os.path.join('uploads/marksheets/', new_filename)


#rename community
def community_rename(instance, filename):
    ext = filename.split('.')[-1]
    title_slug = slugify(instance.student.username)
    new_filename = f"{title_slug}community.{ext}"
    return os.path.join('uploads/community/', new_filename)


#rename tc
def tc_rename(instance, filename):
    ext = filename.split('.')[-1]
    title_slug = slugify(instance.student.username)
    new_filename = f"{title_slug}tc.{ext}"
    return os.path.join('uploads/tc/', new_filename)

#rename special_documents
def special_documents_rename(instance, filename):
    ext = filename.split('.')[-1]
    title_slug = slugify(instance.student.username)
    new_filename = f"{title_slug}specialdoc.{ext}"
    return os.path.join('uploads/specialdocuments/', new_filename)



# validate files
def validate_image_size(file):
    max_size_kb = 250
    max_size = max_size_kb * 1024  

    if file.size > max_size:
        raise ValidationError(f"Maximum file size is {max_size_kb}KB")

