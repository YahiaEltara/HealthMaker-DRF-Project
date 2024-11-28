from django.contrib import admin
from .models import Client, Coach, Recommendation, Workoutplan, Meal




class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'coach', 'created_at')
    list_filter = ('user', 'coach',)
    search_fields = ['user__username', 'coach__user__username',]
    ordering = ['-created_at']



class CoachAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    list_filter = ['user',]
    search_fields = ['user__username',]
    ordering = ['-created_at']



class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('client', 'coach', 'created_at')
    list_filter = ('client', 'coach',)
    search_fields = ['client__user__username', 'coach__user__username',]
    ordering = ['-created_at']



class WorkoutplanAdmin(admin.ModelAdmin):
    list_display = ('client', 'coach', 'name', 'created_at')
    list_filter = ('client', 'coach',)
    search_fields = ['client__user__username', 'coach__user__username',]
    ordering = ['-created_at']



class MealAdmin(admin.ModelAdmin):
    list_display = ('meal_type', 'workout_plan', 'created_at')
    list_filter = ('meal_type', 'workout_plan__client',)
    search_fields = ['meal_type', 'workout_plan__client__user__username',]
    ordering = ['-created_at']



admin.site.register(Client, ClientAdmin)
admin.site.register(Coach, CoachAdmin)
admin.site.register(Recommendation, RecommendationAdmin)
admin.site.register(Workoutplan, WorkoutplanAdmin)
admin.site.register(Meal, MealAdmin)