# Generated by Django 4.1.5 on 2023-02-06 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0005_order_products'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name', 'price']},
        ),
        migrations.RenameField(
            model_name='product',
            old_name='discription',
            new_name='description',
        ),
    ]
