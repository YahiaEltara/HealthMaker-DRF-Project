from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, CoachViewSet, RecommendationViewSet, MealViewSet, WorkoutplanViewSet

router = DefaultRouter()
router.register('clients', ClientViewSet)
router.register('coaches', CoachViewSet)
router.register('recommendations', RecommendationViewSet)
router.register('workoutpalns', WorkoutplanViewSet)
router.register('meals', MealViewSet)

urlpatterns = [
    
    path('', include(router.urls)),
    
]
