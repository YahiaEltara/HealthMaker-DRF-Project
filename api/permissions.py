from rest_framework.permissions import BasePermission, SAFE_METHODS
from jsonschema import ValidationError
from rest_framework import viewsets
from .models import Coach, Client, Workout_Plan
from rest_framework.response import Response





class DefaultPermission(BasePermission):
    """
    Allow authenticated clients to use GET methods for their objects only,
    and allow authenticated coaches full access to their objects only.
    """
    def has_permission(self, request, view):
        user = request.user
        print(f"Authenticated user: {user}")

        if hasattr(user, 'client') and request.method == 'GET':
            return True
        if hasattr(user, 'coach'):
            if request.method in ['POST', 'PUT', 'DELETE']:
                # Restrict coaches to interacting with their own clients only
                client_username = request.data.get('client')
                coach_assigned = request.data.get('coach')
                workout_plan = request.data.get('workout_plan')

                if workout_plan:
                    try:
                        # Ensure workout_plan belongs to the provided client
                        workout_plan = Workout_Plan.objects.get(type=workout_plan)
                        client = Client.objects.get(user__username=client_username)
                        if workout_plan.client != client:
                            return False
                    except (Workout_Plan.DoesNotExist, Client.DoesNotExist):
                        return False
                
                if coach_assigned != str(user.coach):  # Compare the username
                    return False
                if_existed_user = user.coach.clients.filter(user__username=client_username).exists()
                if if_existed_user:
                    return True
                return False
            return True  # Allow other methods like GET for coaches
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if hasattr(user, 'client') and request.method == 'GET':
            return obj.client == user.client
        if hasattr(user, 'coach'):
            return obj.coach == user.coach
        return False
    @staticmethod
    def get_filtered_queryset(queryset, user):
        """
        Filters the queryset to include only objects belonging to the authenticated client.
        """
        if hasattr(user, 'client'):
            return queryset.filter(client=user.client)
        elif hasattr(user, 'coach'):
            return queryset.filter(coach=user.coach)
        return queryset.none()
    

class ClientPermission (BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if hasattr(user, 'client'):
            return True
        
        elif hasattr(user, 'coach') and request.method == 'GET':
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        user = request.user

        if hasattr(user, 'client'):
            return obj.user.username == user.username
        
        elif hasattr(user, 'coach') and request.method == 'GET':
            return obj.coach == user.coach
        
        return False
    @staticmethod
    def get_filtered_queryset(queryset, user):
        """
        Filters the queryset to include only objects belonging to the authenticated client.
        """
        if hasattr(user, 'client'):
            return queryset.filter(user__username=user.username)
        
        elif hasattr(user, 'coach'):
            return queryset.filter(coach=user.coach)
        
        return queryset.none()
        
# class CoachPermission (BasePermission):
#     def has_permission(self, request, view):
#         user = request.user

#         if hasattr(user, 'coach'):
#             return True
        
#         elif hasattr(user, 'client') and request.method == 'GET':
#             return True
#         return False
    
#     def has_object_permission(self, request, view, obj):
#         user = request.user

#         if hasattr(user, 'client') and request.method == 'GET':
#             return obj.client == user.client
        
#         elif hasattr(user, 'coach'):
#             return obj.coach == user.coach
        
#         return False
    
#     @staticmethod
#     def get_filtered_queryset(queryset, user):
#         """
#         Filters the queryset to include only objects belonging to the authenticated client.
#         """
#         if hasattr(user, 'client'):
#             return queryset.filter(client=user.client)
        
#         elif hasattr(user, 'coach'):
#             return queryset.filter(coach=user.coach)
        
#         return queryset.none()
    
# class AdminPermission (BasePermission):
#     def has_permission(self, request, view):
#         user = request.user
#         return user.is_staff
        
#     def has_object_permission(self, request, view, obj):
#         user = request.user
#         return user.is_staff