# SDDM - Staff and Dependent Data Management System

A secure, multi-user form submission web application built with Django that features distinct user roles with specific permissions, dynamic forms, and a modern user interface.

## Features

- **Multi-Role User System**: User, Admin, Security Admin, and Super Admin roles with specific permissions
- **Comprehensive Staff Profiles**: 38 fields covering personal, contact, employment, and security information
- **Dynamic Dependent Management**: Add/remove dependents based on staff input
- **Role-Based Field Access**: Different user roles can access different staff profile fields
- **Modern UI/UX**: Built with Tailwind CSS and Alpine.js for responsive design
- **Secure Authentication**: Django's built-in authentication system with custom user model
- **Responsive Dashboard**: Different views based on staff role and permissions

## Technology Stack

- **Backend**: Python 3.8+ with Django 5.2+
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML, CSS, JavaScript with Tailwind CSS and Alpine.js
- **Authentication**: Django's built-in authentication system
- **Forms**: Django ModelForms with dynamic formsets

## User Roles & Permissions

### User Role
- Can create and edit their own profile (fields 1-25)
- Cannot access security information (fields 26-38)
- View-only access to their profile data

### Admin Role
- Can view, edit, and delete all user profiles
- Can edit all profile fields except security fields (26-38)
- Full administrative access to user management

### Security Admin Role
- Can only edit security-related fields (26-38)
- Cannot modify personal or employment information
- Specialized access for security clearance management

### Super Admin Role
- Full access to all fields and functions
- Can manage all user roles and permissions
- Complete system administration capabilities

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd form_project
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Admin Users
```bash
python manage.py create_admin_users
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Default Admin Credentials

After running the `create_admin_users` command, you can log in with:

- **Super Admin**: `superadmin` / `complex_password_123`
- **Security Admin**: `securityadmin` / `secure_password_456`
- **Admin**: `admin` / `admin_password_789`

## Project Structure

```
form_project/
├── form_project/          # Main project settings
│   ├── settings.py       # Django settings
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI configuration
├── core/                 # Main application
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── forms.py         # Form definitions
│   ├── admin.py         # Admin interface
│   └── urls.py          # App URL configuration
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   └── core/            # App-specific templates
├── static/               # Static files (CSS, JS)
├── manage.py            # Django management script
└── requirements.txt      # Python dependencies
```

## Database Models

### User Model
- Custom user model extending Django's AbstractUser
- Role-based permissions system
- Authentication and authorization

### EmployeeProfile Model
- 38 fields covering all staff information
- Organized into logical sections:
  - Basic Information (fields 1-25)
  - Security Information (fields 26-38)
- Foreign key relationship to User model

### Dependent Model
- Related to EmployeeProfile
- Stores dependent information (name, relationship, date of birth)
- Dynamic formset management

## Key Features

### Dynamic Dependent Forms
- JavaScript-based dynamic form generation
- Add/remove dependent forms based on user input
- Form validation and error handling

### Role-Based Field Access
- Template logic for field visibility
- Form-level field restrictions
- Security-focused access control

### Modern UI Components
- Responsive design with Tailwind CSS
- Interactive elements with Alpine.js
- Clean, professional appearance
- UNDP-inspired color scheme

## API Endpoints

- `/` - Home/Login redirect
- `/login/` - User authentication
- `/signup/` - User registration
- `/dashboard/` - Main dashboard (role-based)
- `/profile/create/` - Create new profile
- `/profile/edit/<id>/` - Edit existing profile
- `/profile/<id>/` - View profile details
- `/profile/delete/<id>/` - Delete profile (admin only)

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
```

### Applying Migrations
```bash
python manage.py migrate
```

### Creating Superuser
```bash
python manage.py createsuperuser
```

## Production Deployment

### Database
- Use PostgreSQL for production
- Configure environment variables for database credentials
- Set `DEBUG = False` in production settings

### Static Files
- Configure `STATIC_ROOT` and `MEDIA_ROOT`
- Use a web server like Nginx to serve static files
- Consider using a CDN for static assets

### Security
- Change default admin passwords
- Use environment variables for sensitive settings
- Enable HTTPS in production
- Configure proper CORS settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please contact the development team or create an issue in the repository.

## Changelog

### Version 1.0.0
- Initial release
- Multi-role user system
- Complete staff profile management
- Dynamic dependent forms
- Modern UI with Tailwind CSS
- Role-based field access control
