from django.core.management.base import BaseCommand
from users.models import UserProfile
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Clears fake or placeholder information from your user profile'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the profile to clear')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        
        try:
            user = User.objects.get(username=username)
            profile = user.profile
            
            # Clear profile information
            profile.bio = ""
            profile.location = ""
            profile.phone_number = ""
            profile.preferred_crops = ""
            profile.farm_size = None
            
            # Don't reset profile picture as it has a default
            # Don't reset farmer_type and farming_experience as they have defaults
            
            profile.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully cleared fake information from {username}\'s profile'))
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} does not exist'))
        except UserProfile.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Profile for user {username} does not exist'))