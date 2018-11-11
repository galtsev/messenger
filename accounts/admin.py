from django.contrib import admin

from accounts import models

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.CustomUser, CustomUserAdmin)
