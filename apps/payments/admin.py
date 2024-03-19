from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class CollectAdmin(admin.ModelAdmin):
    list_display = ('id', 'collect', 'donor', 'amount',)
    search_fields = ('collect',)
    list_filter = ('donor', 'collect',)
    empty_value_display = '-empty-'
