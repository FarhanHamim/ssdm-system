from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, EmployeeProfile, Dependent

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'name', 'agency_project_cluster_office', 'duty_station', 'created_by', 'created_at')
    list_filter = ('agency_project_cluster_office', 'duty_station', 'contact_type', 'blood_group', 'created_at')
    search_fields = ('employee_id', 'name', 'email_official', 'cell_phone_whatsapp')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('agency_project_cluster_office', 'r_ser', 'sl', 'name', 'post_title_designation', 'nationality', 'employee_id', 'gender', 'date_of_birth', 'contact_type', 'duty_station')
        }),
        ('Contact Information', {
            'fields': ('cell_phone_whatsapp', 'emergency_contact_number', 'emergency_contact_relation', 'email_official', 'email_personal')
        }),
        ('Address Information', {
            'fields': ('residential_address', 'zone', 'police_station_thana')
        }),
        ('Personal Information', {
            'fields': ('passport_number', 'unlp_number', 'blood_group', 'number_of_dependents')
        }),
        ('Security Information', {
            'fields': ('radio_call_sign', 'radio_serial_id', 'zone_name_with_appointment', 'office_location_address', 'appointment_unit_based_warden', 'unid_number', 'rfid_number', 'unid_issue_date', 'id_contact_expiry', 'id_deposit_date', 'bsafe', 'sat', 'sbfat')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Dependent)
class DependentAdmin(admin.ModelAdmin):
    list_display = ('name', 'relationship', 'date_of_birth', 'employee_profile')
    list_filter = ('relationship', 'date_of_birth')
    search_fields = ('name', 'employee_profile__name')
    ordering = ('name',)
