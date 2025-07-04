from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Profile

class Command(BaseCommand):
    help = 'Creates profiles for existing users'

    def handle(self, *args, **options):
        for user in User.objects.all():
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)
                self.stdout.write(f'Created profile for {user.username}')