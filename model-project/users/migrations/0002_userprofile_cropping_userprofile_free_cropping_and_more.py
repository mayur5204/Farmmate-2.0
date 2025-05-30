# Generated by Django 5.2 on 2025-04-24 04:20

import django.core.validators
import image_cropping.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('profile_picture', '300x300', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text='Select the area to crop for your profile picture', hide_image_field=False, size_warning=True, verbose_name='cropping'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='free_cropping',
            field=image_cropping.fields.ImageRatioField('profile_picture', '300x300', adapt_rotation=False, allow_fullsize=False, free_crop=True, help_text='Free cropping for mobile devices', hide_image_field=False, size_warning=True, verbose_name='free cropping'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='name',
            field=models.CharField(blank=True, help_text='Your full name', max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, help_text='Tell us about yourself and your farm', max_length=500),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='farmer_type',
            field=models.CharField(choices=[('small', 'Small Scale Farmer'), ('medium', 'Medium Scale Farmer'), ('large', 'Large Scale Farmer'), ('hobbyist', 'Hobbyist/Gardener'), ('commercial', 'Commercial Farmer'), ('other', 'Other')], default='small', help_text='What type of farming do you practice?', max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='farming_experience',
            field=models.CharField(choices=[('beginner', 'Beginner (0-2 years)'), ('intermediate', 'Intermediate (3-5 years)'), ('experienced', 'Experienced (6-10 years)'), ('expert', 'Expert (10+ years)')], default='beginner', help_text='How long have you been farming?', max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='location',
            field=models.CharField(blank=True, help_text='Your general location or region', max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, help_text='Contact number with country code (e.g., +91XXXXXXXXXX)', max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='preferred_crops',
            field=models.CharField(blank=True, help_text='Comma-separated list of crops you typically grow', max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(default='profile_pics/default.png', help_text='Profile picture - will be cropped to a square', upload_to='profile_pics'),
        ),
    ]
