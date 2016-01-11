from django.contrib import admin

from .models import Track


class TrackAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('user', 'date', 'time', 'distance')
    list_filter = ('date',)


admin.site.register(Track, TrackAdmin)
