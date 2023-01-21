"""
Django admin customization.
"""
from django.contrib import admin
from user.models import User, Clerk, Officer
from citation.models import Citation


admin.site.register(User)
admin.site.register(Clerk)
admin.site.register(Officer)
admin.site.register(Citation)
