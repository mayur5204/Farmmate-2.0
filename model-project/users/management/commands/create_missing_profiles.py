from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import UserProfile

class Command(BaseCommand):
    help = 'Create user profiles for all users that do not have one'

    def handle(self, *args, **kwargs):
        users_without_profile = []
        
        # Get all users
        users = User.objects.all()
        self.stdout.write(f"Found {len(users)} users in the database")
        
        # Check which users don't have profiles
        for user in users:
            try:
                # Try to access the profile
                profile = user.profile
            except UserProfile.DoesNotExist:
                users_without_profile.append(user)
            except Exception as e:
                self.stdout.write(f"Error checking profile for user {user.username}: {str(e)}")
                users_without_profile.append(user)
        
        self.stdout.write(f"Found {len(users_without_profile)} users without profiles")
        
        # Create profiles for users that don't have one
        for user in users_without_profile:
            UserProfile.objects.create(user=user)
            self.stdout.write(f"Created profile for user: {user.username}")
        
        self.stdout.write(self.style.SUCCESS(f"Successfully created {len(users_without_profile)} user profiles"))