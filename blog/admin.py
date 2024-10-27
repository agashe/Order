from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
