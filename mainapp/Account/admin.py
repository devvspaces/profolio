from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis.admin import OSMGeoAdmin
from .forms import UserRegisterForm

from .models import AuthActivityLog, Profile, User


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserRegisterForm

    list_display = ("username", "is_active", "is_staff", "is_active")
    list_filter = ('active', 'staff', 'admin',)
    search_fields = ("username",)
    ordering = ("username",)

    fieldsets = (
        ('User', {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('admin', 'staff', 'active',)}),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('created',)
        }),
    )

    # add_fieldsets = (
    #     (None, {
    #             'classes': ('wide',),
    #             'fields': ("username", "password", "confirm_password",)
    #         }
    #     ),
    # )

    filter_horizontal = ()


@admin.register(Profile)
class ProfileAdmin(OSMGeoAdmin):
    list_display = ('name', 'location', 'phone', 'address')
    search_fields = ('name', 'phone', 'address')
    list_filter = ('created',)
    readonly_fields = ('created',)
    fieldsets = (
        (None, {
            'fields': ('name', 'phone', 'address', 'location')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('created',)
        }),
    )


@admin.register(AuthActivityLog)
class AuthActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'created')
    search_fields = ('user__username',)
    list_filter = ('action', 'created')
    readonly_fields = ('created',)
    fieldsets = (
        (None, {
            'fields': ('user', 'action',)
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('created',)
        }),
    )
