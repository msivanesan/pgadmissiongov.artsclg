# Generated by Django 5.0.1 on 2024-02-06 04:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_pgstudentdetails_acceptorrejectedby'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pgstudentdetails',
            old_name='acceptorrejectedBy',
            new_name='rejectedBy',
        ),
    ]