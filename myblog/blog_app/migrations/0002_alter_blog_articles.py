# Generated by Django 4.1.5 on 2023-02-25 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='articles',
            field=models.TextField(max_length=10000),
        ),
    ]