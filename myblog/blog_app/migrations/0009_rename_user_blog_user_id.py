# Generated by Django 4.1.5 on 2023-03-09 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0008_alter_blog_gallery'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='user',
            new_name='user_id',
        ),
    ]