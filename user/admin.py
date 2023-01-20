# """
# Django admin customization.
# """
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.utils.translation import gettext_lazy as _

# from user import models


# class UserAdmin(BaseUserAdmin):
#     """Define the admin pages for users."""
#     ordering = ['id']
#     list_filter = ('is_staff', 'agency')
#     list_display = [
#         'agency',
#         'email', 'name',
#         'badge',
#         'is_active',
#         'is_staff']
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         (_('Personal Info'), {'fields': ('name', 'badge')}),
#         (
#             _('Permissions'),
#             {
#                 'fields': (
#                     'is_active',
#                     'is_staff',
#                     'is_superuser',
#                 )
#             }
#         ),
#         (_('Important dates'), {'fields': ('last_login',)}),
#     )
#     readonly_fields = ['last_login']
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': (
#                 'agency',
#                 'email',
#                 'password1',
#                 'password2',
#                 'name',
#                 'badge',
#                 'is_active',
#                 'is_staff',
#             ),
#         }),
#     )


# admin.site.register(models.User, UserAdmin)
