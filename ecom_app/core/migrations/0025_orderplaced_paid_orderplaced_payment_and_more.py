# Generated by Django 4.2.5 on 2023-10-02 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_rename_product_orderplaced_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderplaced',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderplaced',
            name='payment',
            field=models.CharField(choices=[('Online', 'Online'), ('COD', 'COD')], default='COD', max_length=255),
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('Order Pending', 'Order Pending'), ('Confirmed', 'Confirmed'), ('Packed', 'Packed'), ('Shipped', 'Shipped'), ('Outer Delivery', 'Outer Delivery'), ('Delivered', 'Delivered'), ('Favorite', 'Favorite')], default='Confirmed', max_length=50),
        ),
    ]
