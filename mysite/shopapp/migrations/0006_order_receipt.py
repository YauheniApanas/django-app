# Generated by Django 4.1.7 on 2023-06-19 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0005_alter_order_user_alter_product_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='receipt',
            field=models.FileField(null=True, upload_to='orders/receipts'),
        ),
    ]