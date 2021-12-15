from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.users.forms import UserForm
from apps.users.models import (
    CustomUser,
    Applicant,
    ApplicantAttachments,
    ApplicantSkills,
    ApplicantEducation
)


@admin.register(CustomUser)
class MyUserAdmin(AuthUserAdmin):
    # form = UserForm
    exclude = ('username',)

    fieldsets = (
        (None, {'fields': ( 'email', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name',
            'last_name',
            'middle_name',
            'address',
            'phone_number',
            'mobile_number',
            'extension',
            'headline',
            'birthdate',
            'user_avatar',
            'overview',
            'gender',
            'user_type',
        )}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'token',
            'groups',
            'user_permissions')
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    add_filedsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2')}
        ),
    )

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(Applicant)
class Applicant(admin.ModelAdmin):
    search_fields = ('__all__',)


@admin.register(ApplicantAttachments)
class ApplicantAttachments(admin.ModelAdmin):
    search_fields = ('__all_',)


@admin.register(ApplicantSkills)
class ApplicantSkills(admin.ModelAdmin):
    search_fields = ('__all_',)


# @admin.register(ApplicantSkills)
# class ApplicantSkills(admin.ModelAdmin):
#     search_fields = ('__all_',)


# @admin.register(ApplicantEducation)
# class ApplicantEducation(admin.ModelAdmin):
#     search_fields = ('__all_',)
