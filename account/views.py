from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import (generics, status)
from .serializers import (
    RegisterSerializer,
    UserProfileSerializer,
    CustomTokenObtainPairSerializer,
    UserDiseaseHistorySerializer)
from .models import (
    Profile,
    DiseaseHistory)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework.decorators import (api_view, permission_classes)
from rest_framework.response import Response


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserProfileDetail(request):
    if request.user.id:
        users = User.objects.get(id=request.user.id)
        profiles = Profile.objects.get(id=request.user.id)
        user = RegisterSerializer(users, many=False)
        profile = UserProfileSerializer(profiles, many=False)
        return Response({"user": user.data, "profile": profile.data})
    else:
        data = {
            "data": "Unathorized access"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
def UserProfileUpdate(request):
    if request.user.id:
        request.data['user'] = request.user.id
        profile = Profile.objects.get(user=request.user.id)
        serializer = UserProfileSerializer(
            instance=profile, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data)
    else:
        data = {
            "data": "Unathorized access"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserDiseaseHistory(request):
    if request.user.id:
        diseases = DiseaseHistory.objects.filter(user=request.user.id)
        serializer = UserDiseaseHistorySerializer(diseases, many=True)
        return Response(serializer.data)
    else:
        data = {
            "data": "Unathorized access"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
