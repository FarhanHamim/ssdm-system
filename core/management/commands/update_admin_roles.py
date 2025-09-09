from django.core.management.base import BaseCommand
from core.models import User

class Command(BaseCommand):
    help = 'Update existing users with admin role to super_admin role'

    def handle(self, *args, **options):
        # Find users with 'admin' role
        admin_users = User.objects.filter(role='admin')
        
        if admin_users.exists():
            # Update them to 'super_admin'
            admin_users.update(role='super_admin')
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully updated {admin_users.count()} users from admin to super_admin role'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING('No users with admin role found')
            )
