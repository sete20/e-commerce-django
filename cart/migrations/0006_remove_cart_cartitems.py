# Generated by Django 4.0.5 on 2022-06-29 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_alter_cart_cartitems'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='cartItems',
        ),
    ]
