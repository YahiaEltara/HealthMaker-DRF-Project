from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationViewSet, ClientViewSet, CoachViewSet, RecommendationViewSet, MealViewSet, WorkoutplanViewSet
from rest_framework_simplejwt.views import TokenRefreshView #, TokenObtainPairView
from .tokens import CustomTokenObtainPairView

router = DefaultRouter()
router.register('register', UserRegistrationViewSet, basename='user-registration')
router.register('clients', ClientViewSet)
router.register('coaches', CoachViewSet)
router.register('recommendations', RecommendationViewSet)
router.register('workoutplans', WorkoutplanViewSet)
router.register('meals', MealViewSet)

urlpatterns = [

    # Token Endpoints
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),


    # API endpoints
    path('', include(router.urls)),
    
]
