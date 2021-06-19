from account.models import DiseaseHistory
from .serializers import PrescriptionSerializer
import os
import pickle
from pathlib import Path

from django.shortcuts import render
from prescription.models import Prescription
from rest_framework import status
from rest_framework.decorators import (api_view, parser_classes,
                                       permission_classes)
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


def map_symptoms(symptoms):
    all_symptoms = ['itching', 'skin_rash', 'chills', 'joint_pain', 'stomach_pain', 'vomiting', 'fatigue', 'cough', 'high_fever', 'headache', 'yellowish_skin', 'nausea', 'loss_of_appetite', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellowing_of_eyes',
                    'malaise', 'chest_pain', 'dizziness', 'slurred_speech', 'muscle_weakness', 'movement_stiffness', 'loss_of_balance', 'loss_of_smell', 'bladder_discomfort', 'irritability', 'muscle_pain', 'polyuria', 'coma', 'painful_walking', 'red_sore_around_nose']
    mapped_symptoms = [0] * len(all_symptoms)

    for index, symptom in enumerate(all_symptoms):
        if symptom in symptoms:
            mapped_symptoms[index] = 1

    return [mapped_symptoms]


@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, JSONParser])
def PredictDiseaseView(request, format=None):
    try:
        # print(request.data['data'])
        symptoms = request.data['data']
        path = os.path.join(
            Path(__file__).resolve().parent.parent, 'predict\\general-disease.pkl')
        file = open(path, 'rb')
        classifierDT = pickle.load(file)
        file.close()
        symptoms_data = map_symptoms(symptoms)
        predicted_disease = classifierDT.predict(symptoms_data)[0]
        print(predicted_disease)
        prescription = Prescription.objects.filter(
            title=predicted_disease).first()

        if prescription:
            prescription_serialized = PrescriptionSerializer(
                prescription, many=False)
            message = prescription_serialized.data['description']
        else:
            message = "No prescriptions available"

        if request.user.id:
            # print(request.user.id)
            user = request.user
            history = DiseaseHistory()
            history.user = user
            history.disease = predicted_disease
            history.prescription = prescription
            history.save()
        return Response({'disease': predicted_disease, 'message': message})

    except Exception as e:
        print(e)
        return Response({'data': "invalid data/ insufficient data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, JSONParser])
def CheckForCoronaView(request):
    # print(request.data)
    try:
        inputFeatures = [
            int(request.data['fever']),
            int(request.data['age']),
            int(request.data['bodyPain']),
            int(request.data['runnyNose']),
            int(request.data['breathingProblem']),
        ]
        path = os.path.join(
            Path(__file__).resolve().parent.parent, 'predict\\corona.pkl')
        file = open(path, 'rb')
        clf = pickle.load(file)
        file.close()
        infectionProbability = clf.predict_proba([inputFeatures])[0][1]
        probability = round(infectionProbability*100)
        return Response({'probability': probability})
    except:
        return Response({'data': "invalid data/ insufficient data"}, status=status.HTTP_400_BAD_REQUEST)
