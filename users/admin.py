"""
Register models editable by admin CRUD
"""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    # model = CustomUser
    list_display = ['email', 'username']
    exclude = ('allergic_food',)
    
    # readonly_fields = ['allergic_food']
    # def get_readonly_fields(self, request, obj=None):
    #     if obj:
    #         return ['allergic_food']
    #     else:
    #         return []

admin.site.register(CustomUser, CustomUserAdmin)
