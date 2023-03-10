# Generated by Django 4.1.5 on 2023-03-09 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog_app', '0009_rename_user_blog_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='user_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
