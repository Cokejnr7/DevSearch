# Generated by Django 3.2.4 on 2022-05-10 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='profiles/user-default.png', null=True, upload_to='profiles/'),
        ),
    ]
