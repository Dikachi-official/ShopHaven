# Generated by Django 4.1.2 on 2022-11-21 23:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_delete_gadget_delete_game_alter_product_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
    ]
