from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('security_admin', 'Security Admin'),
        ('super_admin', 'Super Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class EmployeeProfile(models.Model):
    # Basic Information (Fields 1-25) - Users can edit these
    agency_project_cluster_office = models.CharField(
        max_length=200, 
        verbose_name="Name of Agency/Project/Cluster/Office",
        default='undp',
        choices=[
            ('undp', 'UNDP - United Nations Development Programme'),
            ('unicef', 'UNICEF - United Nations Children\'s Fund'),
            ('who', 'WHO - World Health Organization'),
            ('unhcr', 'UNHCR - UN Refugee Agency'),
            ('sdg', 'SDG Integration'),
            ('climate', 'Climate Change Adaptation'),
            ('governance', 'Democratic Governance'),
            ('crisis', 'Crisis Prevention & Recovery'),
            ('health', 'Health Cluster'),
            ('education', 'Education Cluster'),
            ('protection', 'Protection Cluster'),
            ('shelter', 'Shelter Cluster'),
            ('co', 'Country Office'),
            ('ro', 'Regional Office'),
            ('hq', 'Headquarters'),
            ('liaison', 'Liaison Office'),
        ]
    )
    r_ser = models.PositiveIntegerField(verbose_name="R/Ser", default=0)
    sl = models.PositiveIntegerField(verbose_name="SL", default=0)
    name = models.CharField(max_length=200, verbose_name="Name", default="")
    post_title_designation = models.CharField(max_length=200, verbose_name="Post Title/Designation", default="", blank=True)
    nationality = models.CharField(
        max_length=100, 
        verbose_name="Nationality",
        default='bangladesh',
        choices=[
            ('afghanistan', 'Afghanistan'), ('albania', 'Albania'), ('algeria', 'Algeria'),
            ('andorra', 'Andorra'), ('angola', 'Angola'), ('antigua_and_barbuda', 'Antigua and Barbuda'),
            ('argentina', 'Argentina'), ('armenia', 'Armenia'), ('australia', 'Australia'),
            ('austria', 'Austria'), ('azerbaijan', 'Azerbaijan'), ('bahamas', 'Bahamas'),
            ('bahrain', 'Bahrain'), ('bangladesh', 'Bangladesh'), ('barbados', 'Barbados'),
            ('belarus', 'Belarus'), ('belgium', 'Belgium'), ('belize', 'Belize'),
            ('benin', 'Benin'), ('bhutan', 'Bhutan'), ('bolivia', 'Bolivia'),
            ('bosnia_and_herzegovina', 'Bosnia and Herzegovina'), ('botswana', 'Botswana'),
            ('brazil', 'Brazil'), ('brunei', 'Brunei'), ('bulgaria', 'Bulgaria'),
            ('burkina_faso', 'Burkina Faso'), ('burundi', 'Burundi'), ('cambodia', 'Cambodia'),
            ('cameroon', 'Cameroon'), ('canada', 'Canada'), ('cape_verde', 'Cape Verde'),
            ('central_african_republic', 'Central African Republic'), ('chad', 'Chad'),
            ('chile', 'Chile'), ('china', 'China'), ('colombia', 'Colombia'),
            ('comoros', 'Comoros'), ('congo', 'Congo'), ('costa_rica', 'Costa Rica'),
            ('croatia', 'Croatia'), ('cuba', 'Cuba'), ('cyprus', 'Cyprus'),
            ('czech_republic', 'Czech Republic'), ('denmark', 'Denmark'), ('djibouti', 'Djibouti'),
            ('dominica', 'Dominica'), ('dominican_republic', 'Dominican Republic'),
            ('east_timor', 'East Timor'), ('ecuador', 'Ecuador'), ('egypt', 'Egypt'),
            ('el_salvador', 'El Salvador'), ('equatorial_guinea', 'Equatorial Guinea'),
            ('eritrea', 'Eritrea'), ('estonia', 'Estonia'), ('eswatini', 'Eswatini'),
            ('ethiopia', 'Ethiopia'), ('fiji', 'Fiji'), ('finland', 'Finland'),
            ('france', 'France'), ('gabon', 'Gabon'), ('gambia', 'Gambia'),
            ('georgia', 'Georgia'), ('germany', 'Germany'), ('ghana', 'Ghana'),
            ('greece', 'Greece'), ('grenada', 'Grenada'), ('guatemala', 'Guatemala'),
            ('guinea', 'Guinea'), ('guinea_bissau', 'Guinea-Bissau'), ('guyana', 'Guyana'),
            ('haiti', 'Haiti'), ('honduras', 'Honduras'), ('hungary', 'Hungary'),
            ('iceland', 'Iceland'), ('india', 'India'), ('indonesia', 'Indonesia'),
            ('iran', 'Iran'), ('iraq', 'Iraq'), ('ireland', 'Ireland'),
            ('israel', 'Israel'), ('italy', 'Italy'), ('ivory_coast', 'Ivory Coast'),
            ('jamaica', 'Jamaica'), ('japan', 'Japan'), ('jordan', 'Jordan'),
            ('kazakhstan', 'Kazakhstan'), ('kenya', 'Kenya'), ('kiribati', 'Kiribati'),
            ('kuwait', 'Kuwait'), ('kyrgyzstan', 'Kyrgyzstan'), ('laos', 'Laos'),
            ('latvia', 'Latvia'), ('lebanon', 'Lebanon'), ('lesotho', 'Lesotho'),
            ('liberia', 'Liberia'), ('libya', 'Libya'), ('liechtenstein', 'Liechtenstein'),
            ('lithuania', 'Lithuania'), ('luxembourg', 'Luxembourg'), ('madagascar', 'Madagascar'),
            ('malawi', 'Malawi'), ('malaysia', 'Malaysia'), ('maldives', 'Maldives'),
            ('mali', 'Mali'), ('malta', 'Malta'), ('marshall_islands', 'Marshall Islands'),
            ('mauritania', 'Mauritania'), ('mauritius', 'Mauritius'), ('mexico', 'Mexico'),
            ('micronesia', 'Micronesia'), ('moldova', 'Moldova'), ('monaco', 'Monaco'),
            ('mongolia', 'Mongolia'), ('montenegro', 'Montenegro'), ('morocco', 'Morocco'),
            ('mozambique', 'Mozambique'), ('myanmar', 'Myanmar'), ('namibia', 'Namibia'),
            ('nauru', 'Nauru'), ('nepal', 'Nepal'), ('netherlands', 'Netherlands'),
            ('new_zealand', 'New Zealand'), ('nicaragua', 'Nicaragua'), ('niger', 'Niger'),
            ('nigeria', 'Nigeria'), ('north_korea', 'North Korea'), ('north_macedonia', 'North Macedonia'),
            ('norway', 'Norway'), ('oman', 'Oman'), ('pakistan', 'Pakistan'),
            ('palau', 'Palau'), ('panama', 'Panama'), ('papua_new_guinea', 'Papua New Guinea'),
            ('paraguay', 'Paraguay'), ('peru', 'Peru'), ('philippines', 'Philippines'),
            ('poland', 'Poland'), ('portugal', 'Portugal'), ('qatar', 'Qatar'),
            ('romania', 'Romania'), ('russia', 'Russia'), ('rwanda', 'Rwanda'),
            ('saint_kitts_and_nevis', 'Saint Kitts and Nevis'), ('saint_lucia', 'Saint Lucia'),
            ('saint_vincent_and_the_grenadines', 'Saint Vincent and the Grenadines'),
            ('samoa', 'Samoa'), ('san_marino', 'San Marino'), ('sao_tome_and_principe', 'Sao Tome and Principe'),
            ('saudi_arabia', 'Saudi Arabia'), ('senegal', 'Senegal'), ('serbia', 'Serbia'),
            ('seychelles', 'Seychelles'), ('sierra_leone', 'Sierra Leone'), ('singapore', 'Singapore'),
            ('slovakia', 'Slovakia'), ('slovenia', 'Slovenia'), ('solomon_islands', 'Solomon Islands'),
            ('somalia', 'Somalia'), ('south_africa', 'South Africa'), ('south_korea', 'South Korea'),
            ('south_sudan', 'South Sudan'), ('spain', 'Spain'), ('sri_lanka', 'Sri Lanka'),
            ('sudan', 'Sudan'), ('suriname', 'Suriname'), ('sweden', 'Sweden'),
            ('switzerland', 'Switzerland'), ('syria', 'Syria'), ('taiwan', 'Taiwan'),
            ('tajikistan', 'Tajikistan'), ('tanzania', 'Tanzania'), ('thailand', 'Thailand'),
            ('togo', 'Togo'), ('tonga', 'Tonga'), ('trinidad_and_tobago', 'Trinidad and Tobago'),
            ('tunisia', 'Tunisia'), ('turkey', 'Turkey'), ('turkmenistan', 'Turkmenistan'),
            ('tuvalu', 'Tuvalu'), ('uganda', 'Uganda'), ('ukraine', 'Ukraine'),
            ('united_arab_emirates', 'United Arab Emirates'), ('united_kingdom', 'United Kingdom'),
            ('united_states', 'United States'), ('uruguay', 'Uruguay'), ('uzbekistan', 'Uzbekistan'),
            ('vanuatu', 'Vanuatu'), ('vatican_city', 'Vatican City'), ('venezuela', 'Venezuela'),
            ('vietnam', 'Vietnam'), ('yemen', 'Yemen'), ('zambia', 'Zambia'),
            ('zimbabwe', 'Zimbabwe'),
        ]
    )
    employee_id = models.CharField(max_length=20, unique=True, verbose_name="Employee ID", default="")
    gender = models.CharField(
        max_length=10, 
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        verbose_name="Gender",
        default='male'
    )
    date_of_birth = models.DateField(verbose_name="Date of Birth", default='2000-01-01')
    contact_type = models.CharField(
        max_length=10,
        choices=[
            ('PA', 'PA'), ('CA', 'CA'), ('FTA', 'FTA'), ('TA', 'TA'),
            ('SC', 'SC'), ('IC', 'IC'), ('UNV', 'UNV')
        ],
        verbose_name="Contact Type",
        default='PA'
    )
    duty_station = models.CharField(
        max_length=200,
        verbose_name="Duty Station",
        default='dhaka',
        choices=[
            ('dhaka', 'Dhaka'), ('chittagong', 'Chittagong'), ('sylhet', 'Sylhet'),
            ('rajshahi', 'Rajshahi'), ('khulna', 'Khulna'), ('barisal', 'Barisal'),
            ('rangpur', 'Rangpur'), ('mymensingh', 'Mymensingh'), ('other', 'Other')
        ]
    )
    number_of_dependents = models.PositiveIntegerField(
        verbose_name="Number of Dependents",
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        default=0
    )
    residential_address = models.TextField(verbose_name="Residential Address (at Duty Station)", default="")
    zone = models.CharField(max_length=100, verbose_name="Zone", default="", blank=True)
    police_station_thana = models.CharField(max_length=100, verbose_name="Police Station/Thana (Sub Zone)", default="", blank=True)
    cell_phone_whatsapp = models.CharField(max_length=20, verbose_name="Cell Phone and WhatsApp Number", default="")
    emergency_contact_number = models.CharField(max_length=20, verbose_name="Emergency Contact Number", default="")
    emergency_contact_relation = models.CharField(max_length=100, verbose_name="Emergency Contact (Relation)", default="")
    passport_number = models.CharField(max_length=50, verbose_name="Passport Number", blank=True, default="")
    unlp_number = models.CharField(max_length=50, verbose_name="UNLP Number", blank=True, default="")
    blood_group = models.CharField(
        max_length=5,
        choices=[
            ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
            ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
        ],
        verbose_name="Blood Group",
        default='A+'
    )
    email_official = models.EmailField(verbose_name="Email (Official)", default="")
    email_personal = models.EmailField(verbose_name="Email (Personal)", default="", blank=True)
    
    # Security Information (Fields 26-38) - Only Security Admin can edit these
    radio_call_sign = models.CharField(max_length=50, verbose_name="Radio Call Sign", blank=True, default="")
    radio_serial_id = models.CharField(max_length=50, verbose_name="Radio Serial ID", blank=True, default="")
    zone_name_with_appointment = models.CharField(max_length=200, verbose_name="Zone Name with Appointment", blank=True, default="")
    office_location_address = models.TextField(verbose_name="Office Location Address", blank=True, default="")
    appointment_unit_based_warden = models.CharField(max_length=200, verbose_name="Appointment- Unit Based Warden", blank=True, default="")
    unid_number = models.CharField(max_length=50, verbose_name="UNID #", blank=True, default="")
    rfid_number = models.CharField(max_length=50, verbose_name="RFID Number", blank=True, default="")
    unid_issue_date = models.DateField(verbose_name="UNID Issue Date", blank=True, null=True)
    id_contact_expiry = models.DateField(verbose_name="ID/Contact Expiry", blank=True, null=True)
    id_deposit_date = models.DateField(verbose_name="ID Deposit Date", blank=True, null=True)
    bsafe = models.DateField(verbose_name="BSAFE", blank=True, null=True)
    sat = models.DateField(verbose_name="SAT", blank=True, null=True)
    sbfat = models.DateField(verbose_name="SBFAT", blank=True, null=True)
    
    # Approval Workflow
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('pending_approval', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    submitted_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_profiles')
    rejection_reason = models.TextField(blank=True, default="")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_profiles')
    
    class Meta:
        verbose_name = "Employee Profile"
        verbose_name_plural = "Employee Profiles"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.employee_id} - {self.name}"
    
    def get_full_name(self):
        return self.name

    # Completion helpers
    def is_basic_section_complete(self):
        required_basic_fields = [
            'agency_project_cluster_office', 'r_ser', 'sl', 'name', 'post_title_designation',
            'nationality', 'employee_id', 'gender', 'date_of_birth', 'contact_type',
            'duty_station', 'residential_address', 'cell_phone_whatsapp',
            'emergency_contact_number', 'emergency_contact_relation', 'email_official'
        ]
        for field_name in required_basic_fields:
            value = getattr(self, field_name)
            if value in [None, '', 0]:
                return False
        return True

    def is_security_section_complete(self):
        security_fields = [
            'radio_call_sign', 'radio_serial_id', 'zone_name_with_appointment',
            'office_location_address', 'appointment_unit_based_warden', 'unid_number',
            'rfid_number', 'unid_issue_date', 'id_contact_expiry', 'id_deposit_date',
            'bsafe', 'sat', 'sbfat'
        ]
        for field_name in security_fields:
            value = getattr(self, field_name)
            if value in [None, '']:
                return False
        return True

    def get_completion_status(self):
        if self.is_basic_section_complete() and self.is_security_section_complete():
            return 'complete'
        if self.is_basic_section_complete():
            return 'partially_completed'
        return 'incomplete'

class Dependent(models.Model):
    RELATIONSHIP_CHOICES = [
        ('spouse', 'Spouse'),
        ('son', 'Son'),
        ('daughter', 'Daughter'),
    ]
    
    employee_profile = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='dependents')
    name = models.CharField(max_length=100, verbose_name="Dependent Name")
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES, verbose_name="Relationship")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    residential_address = models.TextField(verbose_name="Residential Address (Dependent)", blank=True, default="")
    
    class Meta:
        verbose_name = "Dependent"
        verbose_name_plural = "Dependents"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_relationship_display()}) - {self.employee_profile.get_full_name()}"

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('profile_submitted', 'Profile Submitted'),
        ('profile_approved', 'Profile Approved'),
        ('profile_rejected', 'Profile Rejected'),
        ('security_update', 'Security Information Updated'),
        ('profile_edited', 'Profile Edited'),
    )
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications', null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    profile = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
    
    def __str__(self):
        return f"{self.title} - {self.recipient.username}"
    
    def mark_as_read(self):
        self.is_read = True
        self.save()
