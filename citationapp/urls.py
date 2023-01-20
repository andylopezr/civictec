from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI, Schema
from ninja.security import HttpBearer
from user.models import User
from jwt import encode, PyJWTError, decode
from django.conf import settings
from django.shortcuts import get_object_or_404
from datetime import timedelta, datetime
from pydantic import SecretStr
from django.db.utils import IntegrityError

from citation.models import Citation
from user.models import User, Clerk

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


class UserSchema(Schema):
    agency: str
    email: str
    password: str
    name: str
    badge: int

class getUserSchema(Schema):
    id: int
    agency: str
    email: str
    name: str
    badge: int

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
    vehicle_year = int
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
    vehicle_year = int
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

# User creation
@api.post('/create-user', auth=None)
def create_user_api(request, payload: UserSchema):
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
            'badge': payload.badge,
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
        "type": "officer",
        "id": user.id,
        "email": user.email,
        }


# Clerk creation
@api.post('/create-clerk', auth=None)
def create_clerk_api(request, payload: ClerkSchema):
    """
        Create a new Clerk using email and password.

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

        clerk = Clerk.objects.create_clerk(
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
        "type": "clerk",
        "id": clerk.id,
        "email": clerk.email,
        }

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]