from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import(
    CustomTokenObtainPairView,
    RegisterView,
    UserProfileDetail,
    UserProfileUpdate,
    UserDiseaseHistory
)

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='user_register'),
    path('profile/', UserProfileDetail, name='user_profile'),
    path('profile/update/', UserProfileUpdate, name='user_profile_update'),
    path('disease-history/', UserDiseaseHistory, name='user_disease_history'),

]
