from django.db import models
from datetime import datetime, date
from user.models import User


class Citation(models.Model):
    ONL_T = [
        ("EDL", "Enhanced Driver's License"),
        ("DPC", "Driver Privilege Card"),
        ("CDL", "Commercial Driver's License"),
        ("NDR", "Non-Driver Identification"),
    ]

    YES_NO = [(False, 'No'), (True, 'Yes')]
    M_F = [("M", "Male"), ("F", "Female")]

    COLOR = [
        ("BR", "Brown"),
        ("BL", "Black"),
        ("AU", "Auburn"),
        ("RE", "Red"),
        ("BL", "Blonde"),
        ("GR", "Gray"),
        ("WH", "White"),
    ]

    ST = [
        ('AL', 'Alabama'),
        ('AK', 'Alaska'),
        ('AS', 'American Samoa'),
        ('AZ', 'Arizona'),
        ('AR', 'Arkansas'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DE', 'Delaware'),
        ('DC', 'District of Columbia'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('GU', 'Guam'),
        ('HI', 'Hawaii'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('IA', 'Iowa'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('ME', 'Maine'),
        ('MD', 'Maryland'),
        ('MA', 'Massachusetts'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MS', 'Mississippi'),
        ('MO', 'Missouri'),
        ('MT', 'Montana'),
        ('NE', 'Nebraska'),
        ('NV', 'Nevada'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NY', 'New York'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('MP', 'Northern Mariana Islands'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('PR', 'Puerto Rico'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VT', 'Vermont'),
        ('VI', 'Virgin Islands'),
        ('VA', 'Virginia'),
        ('WA', 'Washington'),
        ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'),
        ('WY', 'Wyoming')
    ]

    V_L = [
        ("FTA", "Failed to aid"),
        ("UNSF", "Unsafe start from parked, stopped, standing"),
    ]

    violation_datetime = models.DateTimeField(default=datetime.today)
    violation_route = models.CharField(max_length=255)
    violation_county = models.CharField(max_length=255)
    violation_city = models.CharField(max_length=255)
    contact_type = models.CharField(max_length=255)
    oln_state = models.CharField(max_length=255, choices=ST, default="AL")
    oln = models.IntegerField(null=False, blank=False, default=0)
    oln_class = models.CharField(max_length=3, choices=ONL_T, default="EDL")
    cdl = models.BooleanField(choices=YES_NO, default=False)
    violator_name = models.CharField(max_length=255)
    violator_dob = models.DateField(default=date.today)
    violator_gender = models.CharField(max_length=1, choices=M_F, default="M")
    violator_hair = models.CharField(max_length=2, choices=COLOR, default="BR")
    violator_eyes = models.CharField(max_length=2, choices=COLOR, default="BR")
    violator_height = models.CharField(max_length=255)
    violator_address = models.CharField(max_length=255)
    violator_city = models.CharField(max_length=255)
    violator_state = models.CharField(max_length=2, choices=ST, default="AL")
    violator_phone = models.IntegerField(null=False)
    violator_email = models.EmailField(max_length=255, blank=False)
    vehicle_type = models.CharField(max_length=255)
    vehicle_vin = models.CharField(max_length=255)
    vehicle_color = models.CharField(max_length=255)
    vehicle_year = models.IntegerField(null=False)
    vehicle_make = models.CharField(max_length=255)
    vehicle_model = models.CharField(max_length=255)
    factor_crash = models.BooleanField(choices=YES_NO, default=False)
    factor_passenger = models.BooleanField(choices=YES_NO, default=False)
    factor_spanish = models.BooleanField(choices=YES_NO, default=False)
    factor_car_cam = models.BooleanField(choices=YES_NO, default=False)
    factor_body_cam = models.BooleanField(choices=YES_NO, default=False)
    factor_school_zone = models.BooleanField(choices=YES_NO, default=False)
    factor_construction = models.BooleanField(choices=YES_NO, default=False)
    factor_workers = models.BooleanField(choices=YES_NO, default=False)
    violation_0 = models.CharField(max_length=255, choices=V_L, default="FTA")
    violation_1 = models.CharField(max_length=255, choices=V_L, default="FTA")
    violation_2 = models.CharField(max_length=255, choices=V_L, default="FTA")
    violation_3 = models.CharField(max_length=255, choices=V_L, default="FTA")
    violation_4 = models.CharField(max_length=255, choices=V_L, default="FTA")
    issued_by = models.CharField(max_length=255)
    officer = models.ForeignKey(User, on_delete=models.CASCADE)
    issued_datetime = models.DateTimeField(default=datetime.today)
    court = models.CharField(max_length=255)
    court_appearance_date = models.DateTimeField(default=datetime.today)
    violator_signature = models.ImageField(upload_to="static/")

    def __str__(self):
        return self.violator_name
