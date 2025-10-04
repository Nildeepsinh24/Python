from django.contrib import admin
from .models import *

# Register your models here.
class studData(admin.ModelAdmin):
    ordering=["id"]
    list_display=["id","firstname","lastname","email","city","mobile"]

admin.site.register(Studinfo,studData)