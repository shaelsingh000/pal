# Generated by Django 3.1.4 on 2022-08-09 11:29

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0005_comments'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='comments',
            new_name='comment',
        ),
    ]
