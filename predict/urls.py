
from django.urls import path
from .views import (PredictDiseaseView,
                    CheckForCoronaView)
urlpatterns = [
    path('', PredictDiseaseView, name='predict_disease'),
    path('corona/', CheckForCoronaView, name='predict_corona'),
]
