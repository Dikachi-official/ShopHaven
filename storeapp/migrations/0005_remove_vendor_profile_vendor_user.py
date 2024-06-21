# Generated by Django 4.1.2 on 2023-06-21 19:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('storeapp', '0004_remove_vendor_user_vendor_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='profile',
        ),
        migrations.AddField(
            model_name='vendor',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
