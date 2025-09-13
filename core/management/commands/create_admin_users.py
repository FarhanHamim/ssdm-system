from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

User = get_user_model()

@csrf_exempt
def create_admin_users(request):
    """Simple view to create admin users - for deployment only"""
    if request.method == 'POST':
        try:
            # Create Super Admin
            superadmin, created = User.objects.get_or_create(
                username='superadmin',
                defaults={
                    'email': 'superadmin.test@demo.com',
                    'first_name': 'Super',
                    'last_name': 'Admin',
                    'role': 'super_admin',
                    'is_staff': True,
                    'is_superuser': True,
                }
            )
            if created:
                superadmin.set_password('complexpass123')
                superadmin.save()

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

            return HttpResponse(json.dumps({
                'success': True,
                'message': 'Admin users created successfully!',
                'credentials': {
                    'superadmin': 'superadmin.test@demo.com / complexpass123',
                    'securityadmin': 'securityadmin@ssdm.com / secure_password_456',
                    'admin': 'admin@ssdm.com / admin_password_789'
                }
            }), content_type='application/json')
            
        except Exception as e:
            return HttpResponse(json.dumps({
                'success': False,
                'message': f'Error: {str(e)}'
            }), content_type='application/json')
    
    return HttpResponse("""
    <html>
    <body>
        <h1>Create Admin Users</h1>
        <p>Click the button below to create admin users for your SSDM system:</p>
        <button onclick="createUsers()">Create Admin Users</button>
        <div id="result"></div>
        
        <script>
        function createUsers() {
            fetch('/create-admin-users/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('result').innerHTML = 
                    '<h3>Success!</h3>' +
                    '<p>Admin users created:</p>' +
                    '<ul>' +
                    '<li>Super Admin: superadmin.test@demo.com / complexpass123</li>' +
                    '<li>Security Admin: securityadmin@ssdm.com / secure_password_456</li>' +
                    '<li>Admin: admin@ssdm.com / admin_password_789</li>' +
                    '</ul>';
            })
            .catch(error => {
                document.getElementById('result').innerHTML = 
                    '<h3>Error:</h3><p>' + error + '</p>';
            });
        }
        </script>
    </body>
    </html>
    """)
