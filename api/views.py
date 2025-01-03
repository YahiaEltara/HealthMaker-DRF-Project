from rest_framework import viewsets, status, filters
from .models import Client, Coach, Recommendation, Meal, Workout_Plan
from . serializers import UserRegistrationSerializer, ClientSerializer, CoachSerializer, RecommendationSerializer, MealSerializer, Workout_PlanSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .utils import CustomPagination, get_user_related_field
from drf_spectacular.utils import extend_schema
from .permissions import DefaultPermission, ClientPermission, CoachPermission, AdminPermission




class UserRegistrationViewSet(viewsets.ViewSet):
    """
    A ViewSet for handling user registration (clients and coaches).
    """
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully.",
                "username": user.username,
                "role": user.role}, status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [ClientPermission | AdminPermission]
    lookup_field = 'user__username'
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if user.is_staff:
            return queryset
        return ClientPermission.get_filtered_queryset(queryset, user)



class CoachViewSet(viewsets.ModelViewSet):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer
    permission_classes = [CoachPermission | AdminPermission]
    lookup_field = 'user__username'
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if user.is_staff:
            return queryset
        return CoachPermission.get_filtered_queryset(queryset, user)



class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = [DefaultPermission | AdminPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        get_user_related_field('client'),
        get_user_related_field('coach')]
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if user.is_staff:
            return queryset
        return DefaultPermission.get_filtered_queryset(queryset, user)



class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [DefaultPermission | AdminPermission]
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['type', 'workout_plan__type',]
    lookup_field = 'slug'

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if user.is_staff:
            return queryset
        return DefaultPermission.get_filtered_queryset(queryset, user)

    
    @extend_schema(
        description="This method allow partial updating",)
    def update(self, request, *args, **kwargs):
        """
        Override PUT method to allow partial updates.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)



class WorkoutplanViewSet(viewsets.ModelViewSet):
    queryset = Workout_Plan.objects.all()
    serializer_class = Workout_PlanSerializer
    lookup_field = 'slug'
    permission_classes = [DefaultPermission | AdminPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        get_user_related_field('client'),
        get_user_related_field('coach')]
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if user.is_staff:
            return queryset
        return DefaultPermission.get_filtered_queryset(queryset, user)

