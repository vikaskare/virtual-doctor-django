
from django.urls import path
from .views import PredictDiseaseView
urlpatterns = [
    path('', PredictDiseaseView, name='predict_disease'),
]
