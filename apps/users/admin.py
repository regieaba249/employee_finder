from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.users.models import (
    CustomUser,
    Applicant,
    ApplicantAttachment,
    ApplicantSkill,
    ApplicantEducation,
    ApplicantExperience,
    Region,
    Province,
    Municipality,
    Barangay
)


@admin.register(CustomUser)
class MyUserAdmin(AuthUserAdmin):
    exclude = ('username',)

    fieldsets = (
        (None, {'fields': ( 'email', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name',
            'last_name',
            'middle_name',
            'address',
            'region',
            'province',
            'municipality',
            'barangay',
            'phone_number',
            'mobile_number',
            'extension',
            'headline',
            'birthdate',
            'user_avatar',
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

    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(Applicant)
class Applicant(admin.ModelAdmin):
    search_fields = ('__all__',)


@admin.register(ApplicantAttachment)
class ApplicantAttachment(admin.ModelAdmin):
    search_fields = ('__all__',)


@admin.register(ApplicantSkill)
class ApplicantSkill(admin.ModelAdmin):
    search_fields = ('__all__',)


@admin.register(ApplicantExperience)
class ApplicantExperience(admin.ModelAdmin):
    search_fields = ('__all__',)


@admin.register(ApplicantEducation)
class ApplicantEducation(admin.ModelAdmin):
    search_fields = ('__all__',)


@admin.register(Region)
class Region(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Province)
class Province(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Municipality)
class Municipality(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Barangay)
class Barangay(admin.ModelAdmin):
    search_fields = ['name']
