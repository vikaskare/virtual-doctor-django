from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.decorators import (
    api_view,
    permission_classes,
    parser_classes)
from rest_framework import (status)
import pickle
from pathlib import Path
import os


@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, JSONParser])
def PredictDiseaseView(request, format=None):
    print(request.user)
    return Response({'disease': "your disease here", 'message': "Your message is message"})


@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, JSONParser])
def CheckForCoronaView(request):
    print(request.data)
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
