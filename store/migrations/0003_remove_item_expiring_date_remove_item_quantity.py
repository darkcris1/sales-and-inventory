# Generated by Django 4.2.6 on 2024-05-22 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_remove_item_vendor_delete_delivery'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='expiring_date',
        ),
        migrations.RemoveField(
            model_name='item',
            name='quantity',
        ),
    ]
