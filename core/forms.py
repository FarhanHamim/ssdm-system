from django import forms
from django.forms import inlineformset_factory
from .models import EmployeeProfile, Dependent, User

class UserSignupForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        exclude = ['created_at', 'updated_at', 'created_by']
        widgets = {
            # Basic Information (Fields 1-25) - Users can edit these
            'agency_project_cluster_office': forms.Select(attrs={
                'class': 'form-select'
            }),
            'r_ser': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter R/Ser number',
                'min': '0'
            }),
            'sl': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter SL number',
                'min': '0'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your full name'
            }),
            'post_title_designation': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your post title/designation'
            }),
            'nationality': forms.Select(attrs={
                'class': 'form-select'
            }),
            'employee_id': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your employee ID'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input'
            }),
            'contact_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'duty_station': forms.Select(attrs={
                'class': 'form-select'
            }),
            'number_of_dependents': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter number of dependents',
                'min': '0',
                'max': '10'
            }),
            'residential_address': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-textarea',
                'placeholder': 'Enter your residential address at duty station'
            }),
            'zone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your zone'
            }),
            'police_station_thana': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter police station/thana (sub zone)'
            }),
            'cell_phone_whatsapp': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter cell phone and WhatsApp number'
            }),
            'emergency_contact_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter emergency contact number'
            }),
            'emergency_contact_relation': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter emergency contact relation'
            }),
            'passport_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter passport number (optional)'
            }),
            'unlp_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter UNLP number (optional)'
            }),
            'blood_group': forms.Select(attrs={
                'class': 'form-select'
            }),
            'email_official': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your official email'
            }),
            'email_personal': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your personal email'
            }),
            
            # Security Information (Fields 26-38) - Only Security Admin can edit these
            'radio_call_sign': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter radio call sign'
            }),
            'radio_serial_id': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter radio serial ID'
            }),
            'zone_name_with_appointment': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter zone name with appointment'
            }),
            'office_location_address': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-textarea',
                'placeholder': 'Enter office location address'
            }),
            'appointment_unit_based_warden': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter appointment - unit based warden'
            }),
            'unid_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter UNID number'
            }),
            'rfid_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter RFID number'
            }),
            'unid_issue_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input'
            }),
            'id_contact_expiry': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input'
            }),
            'id_deposit_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input'
            }),
            'bsafe': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input'
            }),
            'sat': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input'
            }),
            'sbfat': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        user_role = kwargs.pop('user_role', 'user')
        super().__init__(*args, **kwargs)
        
        # Define field groups
        basic_fields = [
            'agency_project_cluster_office', 'r_ser', 'sl', 'name', 'post_title_designation',
            'nationality', 'employee_id', 'gender', 'date_of_birth', 'contact_type',
            'duty_station', 'number_of_dependents', 'residential_address', 'zone',
            'police_station_thana', 'cell_phone_whatsapp', 'emergency_contact_number',
            'emergency_contact_relation', 'passport_number', 'unlp_number', 'blood_group',
            'email_official', 'email_personal'
        ]
        
        security_fields = [
            'radio_call_sign', 'radio_serial_id', 'zone_name_with_appointment',
            'office_location_address', 'appointment_unit_based_warden', 'unid_number',
            'rfid_number', 'unid_issue_date', 'id_contact_expiry', 'id_deposit_date',
            'bsafe', 'sat', 'sbfat'
        ]
        
        # Approval workflow fields that should be hidden from all users except super admin
        approval_fields = ['status', 'submitted_at', 'approved_at', 'approved_by', 'rejection_reason']
        
        if user_role == 'user':
            # Users cannot see security fields (26-38) - completely hide them
            for field_name in security_fields:
                if field_name in self.fields:
                    del self.fields[field_name]
            
            # Users cannot see approval workflow fields
            for field_name in approval_fields:
                if field_name in self.fields:
                    del self.fields[field_name]
        
        elif user_role == 'security_admin':
            # Security admins can only see security fields (26-38) - hide basic fields
            for field_name in basic_fields:
                if field_name in self.fields:
                    del self.fields[field_name]
            
            # Security admins cannot see approval workflow fields
            for field_name in approval_fields:
                if field_name in self.fields:
                    del self.fields[field_name]
        
        # Super admins can edit all fields (no restrictions)
        
        # Store user_role for validation
        self.user_role = user_role
    
    def clean(self):
        cleaned_data = super().clean()
        
        # If user is security admin, only validate security fields
        if hasattr(self, 'user_role') and self.user_role == 'security_admin':
            # Get the fields that should be validated for security admin
            security_fields = [
                'radio_call_sign', 'radio_serial_id', 'zone_name_with_appointment',
                'office_location_address', 'appointment_unit_based_warden', 'unid_number',
                'rfid_number', 'unid_issue_date', 'id_contact_expiry', 'id_deposit_date',
                'bsafe', 'sat', 'sbfat'
            ]
            
            # Clear validation errors for non-security fields
            # Create a copy of error keys to avoid "dictionary changed size during iteration"
            error_fields = list(self.errors.keys())
            for field_name in error_fields:
                if field_name not in security_fields:
                    del self.errors[field_name]
            
            # Clear field errors for non-security fields
            # Create a copy of field keys to avoid iteration issues
            field_names = list(self.fields.keys())
            for field_name in field_names:
                if field_name not in security_fields and field_name in self.errors:
                    del self.errors[field_name]
        
        return cleaned_data
    
    def clean_agency_project_cluster_office(self):
        if hasattr(self, 'user_role') and self.user_role == 'security_admin':
            return self.cleaned_data.get('agency_project_cluster_office', '')
        return self.cleaned_data.get('agency_project_cluster_office')
    
    def clean_r_ser(self):
        if hasattr(self, 'user_role') and self.user_role == 'security_admin':
            return self.cleaned_data.get('r_ser', 0)
        return self.cleaned_data.get('r_ser')
    
    def clean_sl(self):
        if hasattr(self, 'user_role') and self.user_role == 'security_admin':
            return self.cleaned_data.get('sl', 0)
        return self.cleaned_data.get('sl')
    
    def clean_name(self):
        if hasattr(self, 'user_role') and self.user_role == 'security_admin':
            return self.cleaned_data.get('name', '')
        return self.cleaned_data.get('name')
    
    def clean_post_title_designation(self):
        if hasattr(self, 'user_role') and self.user_role == 'security_admin':
            return self.cleaned_data.get('post_title_designation', '')
        return self.cleaned_data.get('post_title_designation')
    
    def clean_nationality(self):
        if hasattr(self, 'user_role') and self.user_role == 'security_admin':
            return self.cleaned_data.get('nationality', 'bangladesh')
        return self.cleaned_data.get('nationality')
    
    def clean_employee_id(self):
        if hasattr(self, 'user_role') and self.user_role == 'security_admin':
            return self.cleaned_data.get('employee_id', '')
        return self.cleaned_data.get('employee_id')
    
    def clean_gender(self):
        if hasattr(self, 'user_role') and self.user_role == 'security_admin':
            return self.cleaned_data.get('gender', 'male')
        return self.cleaned_data.get('gender')
    
    def clean_date_of_birth(self):
        if hasattr(self, 'user_role') and self.user_role == 'security_admin':
            return self.cleaned_data.get('date_of_birth')
        return self.cleaned_data.get('date_of_birth')
    
    def clean_contact_type(self):
        if hasattr(self, 'user_role') and self.user_role == 'security_admin':
            return self.cleaned_data.get('contact_type', 'PA')
        return self.cleaned_data.get('contact_type')
    
    def clean_duty_station(self):
        if hasattr(self, 'user_role') and self.user_role == 'security_admin':
            return self.cleaned_data.get('duty_station', 'dhaka')
        return self.cleaned_data.get('duty_station')
    
    def clean_number_of_dependents(self):
        if hasattr(self, 'user_role') and self.user_role == 'security_admin':
            return self.cleaned_data.get('number_of_dependents', 0)
        return self.cleaned_data.get('number_of_dependents')
    
    def clean_residential_address(self):
        if hasattr(self, 'user_role') and self.user_role == 'security_admin':
            return self.cleaned_data.get('residential_address', '')
        return self.cleaned_data.get('residential_address')
    
    def clean_zone(self):
        if hasattr(self, 'user_role') and self.user_role == 'security_admin':
            return self.cleaned_data.get('zone', '')
        return self.cleaned_data.get('zone')
    
    def clean_police_station_thana(self):
        if hasattr(self, 'user_role') and self.user_role == 'security_admin':
            return self.cleaned_data.get('police_station_thana', '')
        return self.cleaned_data.get('police_station_thana')
    
    def clean_cell_phone_whatsapp(self):
        if hasattr(self, 'user_role') and self.user_role == 'security_admin':
            return self.cleaned_data.get('cell_phone_whatsapp', '')
        return self.cleaned_data.get('cell_phone_whatsapp')
    
    def clean_emergency_contact_number(self):
        if hasattr(self, 'user_role') and self.user_role == 'security_admin':
            return self.cleaned_data.get('emergency_contact_number', '')
        return self.cleaned_data.get('emergency_contact_number')
    
    def clean_emergency_contact_relation(self):
        if hasattr(self, 'user_role') and self.user_role == 'security_admin':
            return self.cleaned_data.get('emergency_contact_relation', '')
        return self.cleaned_data.get('emergency_contact_relation')
    
    def clean_passport_number(self):
        if hasattr(self, 'user_role') and self.user_role == 'security_admin':
            return self.cleaned_data.get('passport_number', '')
        return self.cleaned_data.get('passport_number')
    
    def clean_unlp_number(self):
        if hasattr(self, 'user_role') and self.user_role == 'security_admin':
            return self.cleaned_data.get('unlp_number', '')
        return self.cleaned_data.get('unlp_number')
    
    def clean_blood_group(self):
        if hasattr(self, 'user_role') and self.user_role == 'security_admin':
            return self.cleaned_data.get('blood_group', 'A+')
        return self.cleaned_data.get('blood_group')
    
    def clean_email_official(self):
        if hasattr(self, 'user_role') and self.user_role == 'security_admin':
            return self.cleaned_data.get('email_official', '')
        return self.cleaned_data.get('email_official')
    
    def clean_email_personal(self):
        if hasattr(self, 'user_role') and self.user_role == 'security_admin':
            return self.cleaned_data.get('email_personal', '')
        return self.cleaned_data.get('email_personal')

class DependentForm(forms.ModelForm):
    class Meta:
        model = Dependent
        fields = ['name', 'relationship', 'date_of_birth', 'residential_address']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter dependent name'
            }),
            'relationship': forms.Select(attrs={
                'class': 'form-select'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input'
            }),
            'residential_address': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-textarea',
                'placeholder': 'Enter dependent\'s residential address (optional)'
            }),
        }

# Create formset for dependents
DependentFormSet = inlineformset_factory(
    EmployeeProfile,
    Dependent,
    form=DependentForm,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=True
)

class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Password'
        })
    )
