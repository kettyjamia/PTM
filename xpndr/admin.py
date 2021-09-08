from django.contrib import admin

# Register your models here.
from .models import Satellite,Transponder,Comment

admin.site.register(Satellite)
admin.site.register(Transponder)
admin.site.register(Comment)