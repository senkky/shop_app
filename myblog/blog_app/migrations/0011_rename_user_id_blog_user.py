# Generated by Django 4.1.5 on 2023-03-09 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0010_alter_blog_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='user_id',
            new_name='user',
        ),
    ]
