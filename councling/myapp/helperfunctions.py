import os
from django.core.exceptions import ValidationError
from django.utils.text import slugify

#rename photo
def Photo_rename(instance, filename):
    ext = filename.split('.')[-1]
    title_slug = slugify(instance.application_id)
    new_filename = f"{title_slug}photo.{ext}"
    return os.path.join('uploads/photos/', new_filename)


#rename aadhar
def aadhar_rename(instance, filename):
    ext = filename.split('.')[-1]
    title_slug = slugify(instance.application_id)
    new_filename = f"{title_slug}aadhar.{ext}"
    return os.path.join('uploads/aadhars/', new_filename)


#remane marksheet
def Marksheet_rename(instance, filename):
    ext = filename.split('.')[-1]
    title_slug = slugify(instance.application_id)
    new_filename = f"{title_slug}marksheet.{ext}"
    return os.path.join('uploads/marksheets/', new_filename)


#rename community
def community_rename(instance, filename):
    ext = filename.split('.')[-1]
    title_slug = slugify(instance.application_id)
    new_filename = f"{title_slug}community.{ext}"
    return os.path.join('uploads/community/', new_filename)

#rename special_documents
def special_documents_rename(instance, filename):
    ext = filename.split('.')[-1]
    title_slug = slugify(instance.application_id)
    new_filename = f"{title_slug}specialdoc.{ext}"
    return os.path.join('uploads/specialdocuments/', new_filename)



# validate files
def validate_image_size(image):
    max_size_kb = 250
    max_size = max_size_kb * 1024  

    if image.size > max_size:
        raise ValidationError(f"Maximum file size is {max_size_kb}KB")

