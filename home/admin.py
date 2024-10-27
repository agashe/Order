from django.contrib import admin
from .models import *

class SettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'val')

class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

admin.site.register(Setting, SettingAdmin)
admin.site.register(NewsletterSubscriber)
admin.site.register(ContactUsMessage)
admin.site.register(Page, PageAdmin)

