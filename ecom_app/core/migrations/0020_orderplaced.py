# Generated by Django 4.2.5 on 2023-09-27 08:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_alter_checkout_address_delete_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderPlaced',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Order Pending', 'Order Pending'), ('Confirmed', 'Confirmed'), ('Packed', 'Packed'), ('Shipped', 'Shipped'), ('Outer Delivery', 'Outer Delivery'), ('Delivered', 'Delivered'), ('Favorite', 'Favorite')], default='Order Pending', max_length=50)),
                ('product', models.ManyToManyField(to='core.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]