from django.contrib import admin
from .models import Collect


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'reason', 'planned_amount')
    search_fields = ('title',)
    list_filter = ('author', 'title',)
    empty_value_display = '-empty-'
