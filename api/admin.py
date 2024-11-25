from django.contrib import admin
from .models import Client, Coach, Recommendation, Workoutplan, Meal




class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'coach', 'created_at')
    list_filter = ('user', 'coach',)
    search_fields = ['user__username', 'coach__user__username',]







admin.site.register(Client, ClientAdmin)
admin.site.register(Coach)
admin.site.register(Recommendation)
admin.site.register(Workoutplan)
admin.site.register(Meal)