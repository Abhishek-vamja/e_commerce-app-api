# Generated by Django 4.2.5 on 2023-09-21 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_remove_cart_product_cart_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favorite',
            old_name='Product',
            new_name='product',
        ),
    ]
