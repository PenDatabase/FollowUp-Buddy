from django.contrib import admin
from .models import Evangelism, FollowUp

@admin.register(Evangelism)
class EvangelismAdmin(admin.ModelAdmin):
    list_display = ['person_name', 'location']


admin.site.register(FollowUp)
