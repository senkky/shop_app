from django.contrib import admin
from .models import News, Housing, TypeRoom


class HousingAdmin(admin.ModelAdmin):
    list_display = ['address', 'number_rooms', 'total_area']


class NewsAdmin(admin.ModelAdmin):
    list_display = ['heading', 'text', 'published']


class TypeRoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


admin.site.register(Housing, HousingAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(TypeRoom, TypeRoomAdmin)

