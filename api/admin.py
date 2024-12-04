from django.contrib import admin
from .models import Client, Coach, Recommendation, Workout_Plan, Meal, User
# from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin



class CustomUserAdmin(UserAdmin):
    model = User
    # Customize the fields to display in the admin panel
    fieldsets = (
        (None, {'fields': ('username', 'password', 'age', 'gender', 'role')}),
    )
    # Customize the fields for the add user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'gender', 'age', 'role'),
        }),
    )
    list_display = ('username', 'is_staff', 'gender', 'age', 'role')
    list_filter = ('is_staff', 'is_active', 'groups', 'gender', 'role')
    search_fields = ('username', 'role')
    ordering = ('username',)
    def save_model(self, request, obj, form, change):
        # Hash the password if it is being updated
        if form.cleaned_data.get('password1'):
            obj.set_password(form.cleaned_data['password1'])
        super().save_model(request, obj, form, change)

    def save_form(self, request, form, change):
        obj = super().save_form(request, form, change)
        if not change:  # If it's a new user
            obj.set_password(form.cleaned_data['password1'])
        return obj



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
admin.site.register(User, CustomUserAdmin)