from django.contrib import admin

from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color_code', 'slug')
    list_editable = ('name', 'color_code', 'slug')


admin.site.register(Tag, TagAdmin)
