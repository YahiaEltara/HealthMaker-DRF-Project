from django.contrib import admin
from .models import Client, Coach, Recommendation, Workout_Plan, Meal
from django.contrib.auth.models import User



class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'coach', 'created_at', 'goal', )
    list_filter = ('user', 'coach', 'goal',)
    search_fields = ['user__username', 'coach__user__username', 'goal',]
    ordering = ['-created_at']

    def get_form(self, request, obj=None, **kwargs):     # Admin users or Coach users cannot be a client.
        # Call the default form
        form = super().get_form(request, obj, **kwargs)
        # Customize the queryset for the 'user' field
        form.base_fields['user'].queryset = User.objects.filter(
            is_staff=False
        ).exclude(id__in=Coach.objects.values_list('user_id', flat=True))
        return form



class CoachAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    list_filter = ['user',]
    search_fields = ['user__username',]
    ordering = ['-created_at']



class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'coach', 'title','created_at')
    list_filter = ('client', 'coach',)
    search_fields = ['client__user__username', 'coach__user__username', 'title',]
    ordering = ['-created_at']



class Workout_PlanAdmin(admin.ModelAdmin):
    list_display = ('type', 'client', 'coach', 'created_at')
    list_filter = ('type', 'client', 'coach',)
    search_fields = ['client__user__username', 'coach__user__username', 'type',]
    ordering = ['-created_at']



class MealAdmin(admin.ModelAdmin):
    list_display = ('type', 'client', 'coach',)
    list_filter = ('type', 'client', 'coach',)
    search_fields = ['client__user__username', 'coach__user__username', 'type',]
    ordering = ['-created_at']



admin.site.register(Client, ClientAdmin)
admin.site.register(Coach, CoachAdmin)
admin.site.register(Recommendation, RecommendationAdmin)
admin.site.register(Workout_Plan, Workout_PlanAdmin)
admin.site.register(Meal, MealAdmin)