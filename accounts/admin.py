from django.contrib import admin
from .models import Adress, Profile, ContactNumber

# Register your models here.

admin.site.register(Adress)
admin.site.register(Profile)
admin.site.register(ContactNumber)
