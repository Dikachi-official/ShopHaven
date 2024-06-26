# Generated by Django 4.1.2 on 2023-08-14 02:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0006_vendor_default'),
        ('userapp', '0003_remove_profile_is_vendor_user_is_vendor'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='review',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='storeapp.productreview'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
