from django.contrib import admin

# Register your models here.
# forms.py
from django import forms
from .models import Erp_User

admin.site.register(Erp_User)
