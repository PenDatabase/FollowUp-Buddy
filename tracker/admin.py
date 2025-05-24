from django.contrib import admin
from django.db.models import Count, F
from .models import Evangelism, FollowUp

@admin.register(Evangelism)
class EvangelismAdmin(admin.ModelAdmin):
    list_display = ['person_name', 'date', 'location', 'no_followups', 'completed']
    exclude = ['relevance']
    search_fields = ['person_name', 'location']

    @admin.display(ordering='followup_count')
    def no_followups(self, evangelism):
        return evangelism.followup_count
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            followup_count = Count('followups')
        )

    
@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    list_display = ['person_name', 'met_first_on', 'date']
    search_fields = ['person_name']

    @admin.display(ordering='evangelism')
    def person_name(self, followup):
        return followup.person_name
    
    @admin.display(ordering='evangelism__date')
    def met_first_on(self, followup):
        return followup.evangelism.date
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            person_name = F('evangelism__person_name')
        )
        