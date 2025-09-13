from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.forms import formset_factory
from django.db import transaction
from django.db.models import Count
from .models import User, EmployeeProfile, Dependent, Notification
from .forms import UserSignupForm, EmployeeProfileForm, DependentFormSet, UserLoginForm
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
import datetime as dt
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from zoneinfo import ZoneInfo

def is_security_admin(user):
    return user.is_authenticated and user.role == 'security_admin'

def is_super_admin(user):
    return user.is_authenticated and user.role == 'super_admin'

def is_admin_user(user):
    return user.is_authenticated and user.role in ['security_admin', 'super_admin']

def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Find user by email first
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
            
            if user is not None:
                # Enforce UNDP email domain for regular users only (not for security or super admins)
                if user.role == 'user' and not user.email.lower().endswith('@undp.org'):
                    messages.error(request, '⚠️ Access denied! This system is restricted to UNDP staff only. Please use your @undp.org email address to login.', extra_tags='undp_restriction')
                    return render(request, 'core/login.html', {'form': form})
                login(request, user)
                display_name = user.get_full_name() or user.username
                messages.success(request, f'Welcome back, {display_name}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'core/login.html', {'form': form})

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = UserSignupForm()
    
    return render(request, 'core/signup.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def dashboard_view(request):
    user = request.user
    
    if user.role == 'user':
        # Regular user dashboard - show their own profile
        try:
            profile = EmployeeProfile.objects.get(created_by=user)
            context = {
                'profile': profile,
                'user_role': user.role,
                'profile_status': profile.get_completion_status()
            }
        except EmployeeProfile.DoesNotExist:
            context = {
                'profile': None,
                'user_role': user.role,
                'profile_status': 'incomplete'
            }
    else:
        # Admin dashboard - show all profiles
        profiles = EmployeeProfile.objects.all().order_by('-created_at')
        
        context = {
            'profiles': profiles,
            'user_role': user.role
        }
    
    return render(request, 'core/dashboard.html', context)

@login_required
def profile_create_view(request):
    # Check if user already has a profile
    if hasattr(request.user, 'employee_profile'):
        messages.warning(request, 'You already have a profile. You can only edit your existing profile.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        print("POST request received")
        print("POST data:", request.POST)
        
        form = EmployeeProfileForm(request.POST, user_role=request.user.role)
        dependent_formset = DependentFormSet(request.POST, instance=None)
        
        print("Form is valid:", form.is_valid())
        if not form.is_valid():
            print("Form errors:", form.errors)
        
        print("Dependent formset is valid:", dependent_formset.is_valid())
        if not dependent_formset.is_valid():
            print("Dependent formset errors:", dependent_formset.errors)
        
        # Check if main form is valid
        if form.is_valid():
            # Try to validate dependent formset, but don't fail if it's not valid
            dependents_valid = dependent_formset.is_valid()
            
            with transaction.atomic():
                profile = form.save(commit=False)
                profile.created_by = request.user
                profile.save()
                
                # Only save dependents if the formset is valid
                if dependents_valid:
                    dependent_formset.instance = profile
                    dependent_formset.save()
                
                # Notify all security admins after the transaction commits
                def notify_security_admins(profile_id: int, created_by_id: int):
                    try:
                        created_by = User.objects.get(id=created_by_id)
                        security_admins = User.objects.filter(role='security_admin')
                        for admin in security_admins:
                            Notification.objects.create(
                                recipient=admin,
                                sender=created_by,
                                notification_type='profile_submitted',
                                title='New Profile Created',
                                message=f'{created_by.get_full_name() or created_by.username} created a new profile.',
                                profile=EmployeeProfile.objects.get(id=profile_id)
                            )
                    except Exception:
                        # Swallow notification errors to not block profile creation
                        pass
                transaction.on_commit(lambda: notify_security_admins(profile.id, request.user.id))
                
                messages.success(request, 'Profile created successfully!')
                return redirect('dashboard')
        else:
            # If main form is not valid, show errors
            if request.user.role == 'security_admin':
                # For security admins, show more specific error message
                messages.error(request, 'Please fill in the required security fields (26-38).')
            pass
    else:
        form = EmployeeProfileForm(user_role=request.user.role)
        dependent_formset = DependentFormSet(instance=None)
    
    context = {
        'form': form,
        'dependent_formset': dependent_formset,
        'user_role': request.user.role,
        'is_create': True,
        'profile_status': 'incomplete'
    }
    return render(request, 'core/profile_form.html', context)

@login_required
def profile_edit_view(request, pk):
    profile = get_object_or_404(EmployeeProfile, pk=pk)
    
    # Check permissions
    if request.user.role == 'user':
        # Users can only edit their own profile
        if profile.created_by != request.user:
            messages.error(request, 'You can only edit your own profile.')
            return redirect('dashboard')
    elif request.user.role == 'security_admin':
        # Security admins can only edit security fields of any profile
        pass  # Will be handled in the form
    elif request.user.role == 'super_admin':
        # Super admins can edit any field of any profile
        pass  # Will be handled in the form
    else:
        messages.error(request, 'You do not have permission to edit profiles.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST, instance=profile, user_role=request.user.role)
        dependent_formset = DependentFormSet(request.POST, instance=profile)
        
        # For security admins, be more lenient with validation
        if request.user.role == 'security_admin':
            # Security admins can save with just security fields
            if form.is_valid():
                with transaction.atomic():
                    updated_profile = form.save(commit=False)
                    
                    # No approval workflow needed
                    updated_profile.save()
                    
                    # Don't require dependent formset validation for security admins
                    try:
                        if dependent_formset.is_valid():
                            dependent_formset.save()
                    except:
                        pass  # Ignore dependent formset errors for security admins
                    # Notify employee that security information was updated
                    try:
                        # Do not notify super admins
                        if getattr(updated_profile.created_by, 'role', None) != 'super_admin':
                            Notification.objects.create(
                                recipient=updated_profile.created_by,
                                sender=request.user,
                                notification_type='security_update',
                                title='Security Information Updated',
                                message=f'Security-related fields for your profile ({updated_profile.name}) were updated by Security Admin.',
                                profile=updated_profile
                            )
                    except Exception:
                        pass
                    
                    messages.success(request, 'Security information updated successfully!')
                    return redirect('dashboard')
        else:
            # Regular validation for other roles
            if form.is_valid():
                with transaction.atomic():
                    updated_profile = form.save(commit=False)
                    
                    
                    
                    updated_profile.save()
                    
                    # Try to save dependent formset, but don't fail if it's not valid
                    try:
                        if dependent_formset.is_valid():
                            dependent_formset.save()
                    except:
                        pass  # Ignore dependent formset errors for regular users
                    # Notify all security admins that employee updated data
                    try:
                        security_admins = User.objects.filter(role='security_admin')
                        for admin in security_admins:
                            Notification.objects.create(
                                recipient=admin,
                                sender=request.user,
                                notification_type='profile_edited',
                                title='Employee Profile Updated',
                                message=f'{request.user.get_full_name()} updated their profile ({updated_profile.name}).',
                                profile=updated_profile
                            )
                    except Exception:
                        pass
                    
                    messages.success(request, 'Profile updated successfully!')
                    return redirect('dashboard')
    else:
        form = EmployeeProfileForm(instance=profile, user_role=request.user.role)
        dependent_formset = DependentFormSet(instance=profile)
    
    context = {
        'form': form,
        'dependent_formset': dependent_formset,
        'profile': profile,
        'user_role': request.user.role,
        'is_create': False,
        'profile_status': profile.get_completion_status()
    }
    return render(request, 'core/profile_form.html', context)

@login_required
@user_passes_test(is_super_admin)
def profile_delete_view(request, pk):
    profile = get_object_or_404(EmployeeProfile, pk=pk)
    
    if request.method == 'POST':
        profile.delete()
        messages.success(request, 'Profile deleted successfully!')
        return redirect('dashboard')
    
    return render(request, 'core/profile_confirm_delete.html', {'profile': profile})

@login_required
@user_passes_test(is_admin_user)
def profile_detail_view(request, pk):
    profile = get_object_or_404(EmployeeProfile, pk=pk)
    context = {
        'profile': profile,
        'user_role': request.user.role,
        'is_super_admin': request.user.role == 'super_admin'
    }
    return render(request, 'core/profile_detail.html', context)


@login_required
def notifications_view(request):
    """View to display notifications for the current user"""
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
        'user_role': request.user.role
    }
    return render(request, 'core/notifications.html', context)

@login_required
def mark_notification_read_view(request, notification_id):
    """AJAX view to mark a notification as read"""
    if request.method == 'POST':
        try:
            notification = Notification.objects.get(id=notification_id, recipient=request.user)
            notification.mark_as_read()
            return JsonResponse({'success': True})
        except Notification.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Notification not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def get_notification_count_view(request):
    """AJAX view to get unread notification count"""
    unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({'unread_count': unread_count})

@login_required
def get_notifications_list_view(request):
    """AJAX view to get recent notifications list for the navbar dropdown"""
    limit = int(request.GET.get('limit', 10))
    notifications_qs = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    notifications = notifications_qs[:limit]
    # Count all unread for accuracy (not only within the slice)
    unread_count = notifications_qs.filter(is_read=False).count()
    dhaka_tz = ZoneInfo('Asia/Dhaka')
    data = [
        {
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'type': n.notification_type,
            'is_read': n.is_read,
            'created_at': timezone.localtime(n.created_at, dhaka_tz).strftime('%b %d, %Y %I:%M %p')
        }
        for n in notifications
    ]
    return JsonResponse({'notifications': data, 'unread_count': unread_count})

def update_dependent_forms(request):
    """AJAX view to update the number of dependent forms"""
    if request.method == 'POST':
        num_dependents = int(request.POST.get('num_dependents', 0))
        profile_id = request.POST.get('profile_id')

        instance = None
        existing_count = 0
        if profile_id:
            try:
                instance = EmployeeProfile.objects.get(pk=profile_id)
                existing_count = instance.dependents.count()
            except EmployeeProfile.DoesNotExist:
                instance = None

        extra_forms = max(num_dependents - existing_count, 0)

        # Create a new formset with the specified number of extra forms and preserve existing ones when editing
        formset = DependentFormSet(instance=instance, extra=extra_forms)

        # Render the management form and each form's HTML
        management_form_html = formset.management_form.as_p()

        forms_html = ''
        for idx, form in enumerate(formset.forms, start=1):
            forms_html += f'''
            <div class="border border-gray-200 rounded-xl p-6 mb-6 bg-gray-50">
                <h4 class="text-lg font-medium text-gray-700 mb-4 flex items-center">
                    <span class="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                        <span class="text-blue-600 text-sm font-medium">{idx}</span>
                    </span>
                    Dependent {idx}
                </h4>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {form.as_p()}
                </div>
            </div>
            '''

        return JsonResponse({'management_form_html': management_form_html, 'forms_html': forms_html})
    
    return JsonResponse({'error': 'Invalid request'})

@login_required
@user_passes_test(is_super_admin)
def report_generation_view(request):
    """Report generation view for super admins"""
    profiles = EmployeeProfile.objects.all()
    total_profiles = profiles.count()
    
    # Initialize filters
    filters = {}
    
    if request.method == 'GET':
        # Apply filters based on GET parameters (restricted set)
        agency = request.GET.get('agency')                 # Project
        duty_station = request.GET.get('duty_station')     # District
        contact_type = request.GET.get('contact_type')     # Level
        zone = request.GET.get('zone')                     # Zone
        
        if agency:
            filters['agency'] = agency
            profiles = profiles.filter(agency_project_cluster_office__iexact=agency)
        
        if duty_station:
            filters['duty_station'] = duty_station
            profiles = profiles.filter(duty_station__iexact=duty_station)
        
        if contact_type:
            filters['contact_type'] = contact_type
            profiles = profiles.filter(contact_type__iexact=contact_type)
        if zone:
            filters['zone'] = zone
            # Handle case-insensitive zone filtering since we format zones with title case
            profiles = profiles.filter(zone__iexact=zone)
        
        # Apply ordering
        profiles = profiles.order_by('-created_at')
    
    # Get unique values for filter dropdowns (restricted to Project, District, Level, Zone)
    all_profiles = EmployeeProfile.objects.all()
    
    # Get unique agencies and sort them alphabetically (handle whitespace and case)
    agencies = sorted(set([agency.strip() for agency in 
                          all_profiles.values_list('agency_project_cluster_office', flat=True)
                          .exclude(agency_project_cluster_office__isnull=True)
                          .exclude(agency_project_cluster_office='') if agency.strip()]))
    
    # Get unique duty stations and sort them alphabetically (handle whitespace and case)
    duty_stations = sorted(set([station.strip() for station in 
                               all_profiles.values_list('duty_station', flat=True)
                               .exclude(duty_station__isnull=True)
                               .exclude(duty_station='') if station.strip()]))
    
    # Get unique contact types and sort them alphabetically (handle whitespace and case)
    contact_types = sorted(set([contact.strip() for contact in 
                               all_profiles.values_list('contact_type', flat=True)
                               .exclude(contact_type__isnull=True)
                               .exclude(contact_type='') if contact.strip()]))
    
    # Get unique zones, filter out empty/null values, and sort them alphabetically (handle whitespace and case)
    zones = sorted(set([zone.strip().title() for zone in 
                       all_profiles.values_list('zone', flat=True)
                       .exclude(zone__isnull=True)
                       .exclude(zone='') if zone.strip()]))
    
    # Generate statistics based on filtered profiles
    stats = {
        'total_profiles': total_profiles,
        'filtered_profiles': profiles.count(),
        'by_agency': profiles.values('agency_project_cluster_office').annotate(count=Count('id')),
        'by_duty_station': profiles.values('duty_station').annotate(count=Count('id')),
        'by_nationality': profiles.values('nationality').annotate(count=Count('id')),
        'by_contact_type': profiles.values('contact_type').annotate(count=Count('id')),
        'by_gender': profiles.values('gender').annotate(count=Count('id')),
        'by_role': profiles.values('created_by__role').annotate(count=Count('id')),
    }
    
    context = {
        'profiles': profiles,
        'stats': stats,
        'filters': filters,
        'filter_options': {
            'agencies': agencies,            # Project wise
            'duty_stations': duty_stations,  # District wise
            'contact_types': contact_types,  # Level wise
            'zones': zones,                  # Zone wise
        }
    }
    
    return render(request, 'core/report_generation.html', context)

@login_required
@user_passes_test(is_super_admin)
def export_pdf_view(request):
    """Export filtered profiles to PDF"""
    profiles = EmployeeProfile.objects.all()
    
    # Apply the same filters as the report generation view
    agency = request.GET.get('agency')                 # Project
    duty_station = request.GET.get('duty_station')     # District
    contact_type = request.GET.get('contact_type')     # Level
    zone = request.GET.get('zone')                     # Zone
    
    if agency:
        profiles = profiles.filter(agency_project_cluster_office=agency)
    if duty_station:
        profiles = profiles.filter(duty_station=duty_station)
    if contact_type:
        profiles = profiles.filter(contact_type=contact_type)
    if zone:
        profiles = profiles.filter(zone=zone)
    
    profiles = profiles.order_by('-created_at')
    
    # Create the HttpResponse object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="employee_profiles_{dt.datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
    
    # Create the PDF object using ReportLab
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # Center alignment
        textColor=colors.HexColor('#1e40af')  # UNDP blue
    )
    
    # Add title
    title = Paragraph("Employee Profiles Report", title_style)
    elements.append(title)
    
    # Add report metadata
    metadata_style = ParagraphStyle(
        'Metadata',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=20,
        textColor=colors.grey
    )
    
    # Build filter description (restricted filters)
    filter_descriptions = []
    if agency:
        filter_descriptions.append(f"Project: {agency}")
    if duty_station:
        filter_descriptions.append(f"District: {duty_station}")
    if contact_type:
        filter_descriptions.append(f"Level: {contact_type}")
    if zone:
        filter_descriptions.append(f"Zone: {zone}")
    
    filter_text = ', '.join(filter_descriptions) if filter_descriptions else 'None'
    
    # Use Bangladesh time for generation timestamp
    metadata = f"""
    Generated on: {timezone.localtime(timezone.now(), ZoneInfo('Asia/Dhaka')).strftime("%B %d, %Y at %I:%M %p")}<br/>
    Total Profiles: {profiles.count()}<br/>
    Filters Applied: {filter_text}
    """
    elements.append(Paragraph(metadata, metadata_style))
    elements.append(Spacer(1, 20))
    
    if profiles.exists():
        # Create table data
        table_data = [['Name', 'Employee ID', 'Agency', 'Duty Station', 'Contact Type', 'Created Date']]
        
        for profile in profiles:
            table_data.append([
                profile.name,
                profile.employee_id,
                profile.agency_project_cluster_office,
                profile.duty_station,
                profile.contact_type,
                profile.created_at.strftime("%b %d, %Y")
            ])
        
        # Create table
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),  # UNDP blue header
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(table)
    else:
        no_data_style = ParagraphStyle(
            'NoData',
            parent=styles['Normal'],
            fontSize=14,
            spaceAfter=20,
            textColor=colors.grey,
            alignment=1  # Center alignment
        )
        elements.append(Paragraph("No profiles found with the applied filters.", no_data_style))
    
    # Build PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    
    response.write(pdf)
    return response

def forget_password_view(request):
    """Forget password view - Step 1: Enter email address"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Create reset URL
            reset_url = request.build_absolute_uri(
                f'/reset-password/{uid}/{token}/'
            )
            
            # Send password reset email
            subject = 'Password Reset Request - SDDM System'
            message = render_to_string('core/emails/password_reset_email.html', {
                'user': user,
                'reset_url': reset_url,
            })
            
            # Send email
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
                html_message=message
            )
            
            messages.success(request, 'Password reset link has been sent to your email address. Please check your inbox and follow the instructions.')
            return redirect('login')
            
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email address.')
        except Exception as e:
            messages.error(request, 'An error occurred while sending the password reset email. Please try again.')
    
    return render(request, 'core/forget_password.html')

def reset_password_confirm_view(request, uidb64, token):
    """Password reset confirmation view - Step 4 & 5: Type new password and confirm"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been successfully reset. You can now login with your new password.')
                return redirect('login')
        else:
            form = SetPasswordForm(user)
        
        return render(request, 'core/reset_password_confirm.html', {'form': form})
    else:
        messages.error(request, 'The password reset link is invalid or has expired. Please request a new password reset.')
        return redirect('forget_password')
