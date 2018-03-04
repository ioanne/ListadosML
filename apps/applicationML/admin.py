from django.contrib import admin
from .models import Application

# Register your models here.

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
	list_display = ('name', 'app_id', 'secret_key', 'user')
