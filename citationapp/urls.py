from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI, Schema
from ninja.security import HttpBearer
from django.contrib.auth.hashers import check_password
from jwt import encode, PyJWTError, decode
from django.conf import settings
from django.shortcuts import get_object_or_404
from datetime import timedelta, datetime
from pydantic import SecretStr
from django.db.utils import IntegrityError

from citation.models import Citation
from user.models import User, Officer

class TokenPayload(Schema):
    user_id: int = None


class AuthBearer(HttpBearer):
    def authenticate(self, request, token: str) -> User:
        user = self.get_current_user(token)
        if user:
            return user

    @staticmethod
    def get_current_user(token: str) -> User | None:
        """Check auth user"""
        try:
            payload = decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256'])

        except PyJWTError:
            return None
        user = get_object_or_404(User, email=payload['sub'])
        return user

# Django Ninja AccessToken --------------------------------------------------

class AccessToken:
    @staticmethod
    def create(user: User) -> dict:
        email = user.email
        access_token_expires = timedelta(minutes=999999)
        token = AccessToken.create_token(
            data={"sub": email},
            expires_delta=access_token_expires,
        )
        user.save()
        return {
            "email": email,
            "access_token": token,
        }

    @staticmethod
    def create_token(data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = encode(
            to_encode, settings.SECRET_KEY, algorithm="HS256"
        )
        return encoded_jwt


api = NinjaAPI(
    auth=AuthBearer(),
    title='Citation',
    version="0.1.0",
)


# Django Ninja schemas ------------------------------------------------------

class ClerkSchema(Schema):
    agency: str
    email: str
    password: str
    name: str

class getClerkSchema(Schema):
    id: int
    agency: str
    email: str
    name: str

class OfficerSchema(Schema):
    agency: str
    email: str
    password: str
    name: str
    badge: int

class getOfficerSchema(Schema):
    id: int
    agency: str
    email: str
    name: str
    badge: int

class LoginSchema(Schema):
    email: str
    password: SecretStr

class CitationSchema(Schema):
    violation_datetime: datetime
    violation_route: str
    violation_county: str
    violation_city: str
    contact_type: str
    oln_state: str
    oln: int
    oln_class: str
    cdl: bool
    violator_name: str
    violator_dob: datetime
    violator_gender: str
    violator_hair: str
    violator_eyes: str
    violator_height: str
    violator_address: str
    violator_city: str
    violator_state: str
    violator_phone: int
    violator_email: str
    vehicle_type: str
    vehicle_vin: str
    vehicle_color: str
    vehicle_year: int
    vehicle_make: str
    vehicle_model: str
    factor_crash: bool
    factor_passenger: bool
    factor_spanish: bool
    factor_car_cam: bool
    factor_body_cam: bool
    factor_school_zone: bool
    factor_construction: bool
    factor_workers: bool
    violation_0: str
    violation_1: str
    violation_2: str
    violation_3: str
    violation_4: str
    issued_by: str
    issued_datetime: datetime
    court: str
    court_appearance_date: datetime
    violator_signature: str

class getCitationSchema(Schema):
    id: int
    violation_datetime: datetime
    violation_route: str
    violation_county: str
    violation_city: str
    contact_type: str
    oln_state: str
    oln: int
    oln_class: str
    cdl: bool
    violator_name: str
    violator_dob: datetime
    violator_gender: str
    violator_hair: str
    violator_eyes: str
    violator_height: str
    violator_address: str
    violator_city: str
    violator_state: str
    violator_phone: int
    violator_email: str
    vehicle_type: str
    vehicle_vin: str
    vehicle_color: str
    vehicle_year: int
    vehicle_make: str
    vehicle_model: str
    factor_crash: bool
    factor_passenger: bool
    factor_spanish: bool
    factor_car_cam: bool
    factor_body_cam: bool
    factor_school_zone: bool
    factor_construction: bool
    factor_workers: bool
    violation_0: str
    violation_1: str
    violation_2: str
    violation_3: str
    violation_4: str
    issued_by: str
    issued_datetime: datetime
    court: str
    court_appearance_date: datetime
    violator_signature: str

# User routes ---------------------------------------------------------------

# Clerk creation
@api.post('/create-clerk/', auth=None)
def create_clerk_api(request, payload: ClerkSchema):
    """
        Create a new user using email and password.

        Password constrains:

            - At least 10 characters long.

            - Should include one lowercase letter.

            - Should include one UPPERCASE letter.

            - Should include one of these special characters: ! @ # ? ]

    """
    try:
        extrafields = {
            'agency': payload.agency,
            'name': payload.name,
        }

        user = User.objects.create_user(
            payload.email,
            payload.password,
            **extrafields,
        )

    except IntegrityError:
        return api.create_response(
            request,
            {"error": "Email already exists"},
            status=409,
        )

    return {
        "type": "clerk",
        "id": user.id,
        "email": user.email,
        }


# Officer creation
@api.post('/create-officer/', auth=None)
def create_officer_api(request, payload: OfficerSchema):
    """
        Create a new Officer using email and password.

        Password constrains:

            - At least 10 characters long.

            - Should include one lowercase letter.

            - Should include one UPPERCASE letter.

            - Should include one of these special characters: ! @ # ? ]

    """
    try:
        extrafields = {
            'agency': payload.agency,
            'name': payload.name,
            'badge': payload.badge,
        }

        officer = Officer.objects.create(
            payload.email,
            payload.password,
        )

    except IntegrityError:
        return api.create_response(
            request,
            {"error": "Email already exists"},
            status=409,
        )

    return {
        "type": "officer",
        "id": officer.id,
        "email": officer.email,
        }

# Login
@api.post('/login', auth=None)
def user_login(request, payload: LoginSchema):
    """Login using email and password"""
    try:
        user = User.objects.get(email=payload.email)

    except Exception:
        return api.create_response(
            request,
            {"error": "User not found"},
            status=404)

    if check_password(payload.password.get_secret_value(), user.password):
        return AccessToken.create(user)

# Citation creation
@api.post("/citation/")
def create(request, payload:CitationSchema):
    """Create a citation form"""
    citation_form = {
        'clerk': request.auth,
        'violation_datetime': payload.violation_datetime,
        'violation_route': payload.violation_route,
        'violation_county': payload.violation_county,
        'violation_city': payload.violation_city,
        'contact_type': payload.contact_type,
        'oln_state': payload.oln_state,
        'oln': payload.oln,
        'oln_class': payload.oln_class,
        'cdl': payload.cdl,
        'violator_name': payload.violator_name,
        'violator_dob': payload.violator_dob,
        'violator_gender': payload.violator_gender,
        'violator_hair': payload.violator_hair,
        'violator_eyes': payload.violator_eyes,
        'violator_height': payload.violator_height,
        'violator_address': payload.violator_address,
        'violator_city': payload.violator_city,
        'violator_state': payload.violator_state,
        'violator_phone': payload.violator_phone,
        'violator_email': payload.violator_email,
        'vehicle_type': payload.vehicle_type,
        'vehicle_vin': payload.vehicle_vin,
        'vehicle_color': payload.vehicle_color,
        'vehicle_year': payload.vehicle_year,
        'vehicle_make': payload.vehicle_make,
        'vehicle_model': payload.vehicle_model,
        'factor_crash': payload.factor_crash,
        'factor_passenger': payload.factor_passenger,
        'factor_spanish': payload.factor_spanish,
        'factor_car_cam': payload.factor_car_cam,
        'factor_body_cam': payload.factor_body_cam,
        'factor_school_zone': payload.factor_school_zone,
        'factor_construction': payload.factor_construction,
        'factor_workers': payload.factor_workers,
        'violation_0': payload.violation_0,
        'violation_1': payload.violation_1,
        'violation_2': payload.violation_2,
        'violation_3': payload.violation_3,
        'violation_4': payload.violation_4,
        'issued_by': payload.issued_by,
        'issued_datetime': payload.issued_datetime,
        'court': payload.court,
        'court_appearance_date': payload.court_appearance_date,
        'violator_signature': payload.violator_signature,
    }
    citation = Citation.objects.create(**citation_form)
    return {
        "item": "citation",
        "id": citation.id
    }

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]