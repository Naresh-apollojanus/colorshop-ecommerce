from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Banner)
admin.site.register(Blog)
admin.site.register(ContactUs)
admin.site.register(Newsletter)


