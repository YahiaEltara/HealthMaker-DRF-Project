from rest_framework import viewsets, status, filters
from .models import Client, Coach, Recommendation, Meal, Workoutplan
from . serializers import ClientSerializer, CoachSerializer, RecommendationSerializer, MealSerializer, WorkoutplanSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .utils import CustomPagination
from drf_spectacular.utils import extend_schema






class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]




class CoachViewSet(viewsets.ModelViewSet):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]



class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]



class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = CustomPagination
    search_fields = ['client__name', 'coach__name']
    lookup_field = 'slug'
    @extend_schema(
        description="This endpoint allow updating a specific meal attributes or totally",)
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
    queryset = Workoutplan.objects.all()
    serializer_class = WorkoutplanSerializer
    lookup_field = 'slug'
