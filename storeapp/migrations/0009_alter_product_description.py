# Generated by Django 4.1.2 on 2023-08-15 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0008_alter_product_vendor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(default='This is a quality product', null=True),
        ),
    ]
