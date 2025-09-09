from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create default admin users for SDDM system'

    def handle(self, *args, **options):
        # Create Super Admin
        superadmin, created = User.objects.get_or_create(
            username='superadmin',
            defaults={
                'email': 'superadmin@ssdm.com',
                'first_name': 'Super',
                'last_name': 'Admin',
                'role': 'super_admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            superadmin.set_password('complex_password_123')
            superadmin.save()
            self.stdout.write(
                self.style.SUCCESS('Successfully created Super Admin user: superadmin')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Super Admin user already exists: superadmin')
            )

        # Create Security Admin
        securityadmin, created = User.objects.get_or_create(
            username='securityadmin',
            defaults={
                'email': 'securityadmin@ssdm.com',
                'first_name': 'Security',
                'last_name': 'Admin',
                'role': 'security_admin',
                'is_staff': True,
                'is_superuser': False,
            }
        )
        if created:
            securityadmin.set_password('secure_password_456')
            securityadmin.save()
            self.stdout.write(
                self.style.SUCCESS('Successfully created Security Admin user: securityadmin')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Security Admin user already exists: securityadmin')
            )

        # Create Admin
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@ssdm.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': False,
            }
        )
        if created:
            admin.set_password('admin_password_789')
            admin.save()
            self.stdout.write(
                self.style.SUCCESS('Successfully created Admin user: admin')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Admin user already exists: admin')
            )

        self.stdout.write(
            self.style.SUCCESS('Admin user creation completed!')
        )
        self.stdout.write(
            self.style.SUCCESS('\nDefault credentials:')
        )
        self.stdout.write(
            self.style.SUCCESS('Super Admin: superadmin / complex_password_123')
        )
        self.stdout.write(
            self.style.SUCCESS('Security Admin: securityadmin / secure_password_456')
        )
        self.stdout.write(
            self.style.SUCCESS('Admin: admin / admin_password_789')
        )
