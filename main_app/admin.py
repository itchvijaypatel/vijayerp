from django.contrib import admin

from .models import *

# Register your models here.
admin.site.site_header = 'VIJAY ERP'
admin.site.register(BusinessCategory)
admin.site.register(BusinessSubCategory)

