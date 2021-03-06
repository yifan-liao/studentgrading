# -*- coding: utf-8 -*-
"""
This file is almost a copy of https://github.com/fusionbox/django-authtools/blob/master/authtools/admin.py
"""
import copy

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from .models import User
from .forms import UserCreationForm, AdminUserChangeForm

USERNAME_FIELD = get_user_model().USERNAME_FIELD

REQUIRED_FIELDS = (USERNAME_FIELD,) + tuple(get_user_model().REQUIRED_FIELDS)

BASE_FIELDS = (None, {
    'fields': REQUIRED_FIELDS + ('password',),
})

SIMPLE_PERMISSION_FIELDS = (_('Permissions'), {
    'fields': ('is_active', 'is_staff', ),
})

ADVANCED_PERMISSION_FIELDS = copy.deepcopy(SIMPLE_PERMISSION_FIELDS)
ADVANCED_PERMISSION_FIELDS[1]['fields'] += ('groups', 'user_permissions',)

DATE_FIELDS = (_('Important dates'), {
    'fields': ('last_login', 'date_joined',),
})


class StrippedUserAdmin(DjangoUserAdmin):
    # The forms to add and change user instances
    add_form_template = None
    add_form = UserCreationForm
    form = AdminUserChangeForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('is_active', USERNAME_FIELD, 'is_staff',)
    list_display_links = (USERNAME_FIELD,)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        BASE_FIELDS,
        SIMPLE_PERMISSION_FIELDS,
    )
    add_fieldsets = (
        (None, {
            'fields': REQUIRED_FIELDS + (
                'password1',
                'password2',
            ),
        }),
    )
    search_fields = (USERNAME_FIELD,)
    ordering = None
    filter_horizontal = tuple()
    readonly_fields = ('last_login', 'date_joined')


class UserAdmin(StrippedUserAdmin):
    fieldsets = (
        BASE_FIELDS,
        ADVANCED_PERMISSION_FIELDS,
        DATE_FIELDS,
    )
    # filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, UserAdmin)
