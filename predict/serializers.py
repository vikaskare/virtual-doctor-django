from rest_framework import serializers
from .models import DiseaseHistory


class SymptomsSerializer(serializers.Serializer):
    symptoms = serializers.ListField(
        child=serializers.CharField(max_length=255)
    )
