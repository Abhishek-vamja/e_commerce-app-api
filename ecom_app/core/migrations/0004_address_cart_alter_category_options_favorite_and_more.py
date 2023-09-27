# Generated by Django 4.2.5 on 2023-09-20 10:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_category_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.address')),
                ('product', models.ManyToManyField(to='core.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-created_at'], 'verbose_name': 'Categorie'},
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Order Pending', 'Order Pending'), ('Confirmed', 'Confirmed'), ('Packed', 'Packed'), ('Shipped', 'Shipped'), ('Outer Delivery', 'Outer Delivery'), ('Delivered', 'Delivered'), ('Favorite', 'Favorite')], default='Favorite', max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CheckOut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Order Pending', 'Order Pending'), ('Confirmed', 'Confirmed'), ('Packed', 'Packed'), ('Shipped', 'Shipped'), ('Outer Delivery', 'Outer Delivery'), ('Delivered', 'Delivered'), ('Favorite', 'Favorite')], default='Confirmed', max_length=255)),
                ('date_checkout', models.DateField(auto_now_add=True)),
                ('date_delivered', models.DateField()),
                ('cart', models.ManyToManyField(to='core.cart')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
