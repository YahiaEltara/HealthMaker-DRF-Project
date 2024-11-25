from django.contrib import admin
from .models import Client, Coach, Recommendation, Workoutplan, Meal


admin.site.register(Client)
admin.site.register(Coach)
admin.site.register(Recommendation)
admin.site.register(Workoutplan)
admin.site.register(Meal)