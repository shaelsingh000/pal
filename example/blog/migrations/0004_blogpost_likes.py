# Generated by Django 3.1.4 on 2021-06-13 16:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0003_auto_20210113_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='likes',
            field=models.ManyToManyField(related_name='blogpost_like', to=settings.AUTH_USER_MODEL),
        ),
    ]