from django.contrib import admin

from dialogs import models

# Register your models here.

class ThreadAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Thread, ThreadAdmin)


class MessageAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Message, MessageAdmin)
