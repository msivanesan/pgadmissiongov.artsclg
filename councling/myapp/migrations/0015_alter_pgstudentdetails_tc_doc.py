# Generated by Django 5.0.1 on 2024-02-13 04:13

import myapp.helperfunctions
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_pgstudentdetails_tc_doc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pgstudentdetails',
            name='tc_doc',
            field=models.ImageField(blank=True, null=True, upload_to=myapp.helperfunctions.tc_rename, validators=[myapp.helperfunctions.validate_image_size]),
        ),
    ]
