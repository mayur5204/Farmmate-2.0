from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator

class UserProfile(models.Model):
    FARMER_TYPE_CHOICES = [
        ('small', 'Small Scale Farmer'),
        ('medium', 'Medium Scale Farmer'),
        ('large', 'Large Scale Farmer'),
        ('hobbyist', 'Hobbyist/Gardener'),
        ('commercial', 'Commercial Farmer'),
        ('other', 'Other'),
    ]
    
    EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner (0-2 years)'),
        ('intermediate', 'Intermediate (3-5 years)'),
        ('experienced', 'Experienced (6-10 years)'),
        ('expert', 'Expert (10+ years)'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pics', default='profile_pics/default.png')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', 
                                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    farmer_type = models.CharField(max_length=20, choices=FARMER_TYPE_CHOICES, default='small')
    farming_experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='beginner')
    preferred_crops = models.CharField(max_length=255, blank=True)
    farm_size = models.FloatField(blank=True, null=True, help_text="Farm size in acres")
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        if hasattr(instance, 'profile'):
            instance.profile.save()
    except UserProfile.DoesNotExist:
        # Create a profile for users that don't have one
        UserProfile.objects.create(user=instance)
