from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import (generics, status)
from .serializers import (
    RegisterSerializer,
    UserProfileSerializer,
    CustomTokenObtainPairSerializer,
    UserDiseaseHistorySerializer,
    UpdateUserSerializer)
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
        # try:
        request.data['user'] = request.user.id
        profile = Profile.objects.get(user=request.user.id)
        profileData = {}
        profileData['user'] = request.data['user']
        profileData['mobile'] = request.data['mobile']
        profileData['age'] = request.data['age']
        profileData['bp_problem'] = request.data['bpProblem']
        profileData['blood_group'] = request.data['bloodGroup']
        profileData['major_health_problem'] = request.data['majorHealthIssue']
        profileData['city'] = request.data['city']
        profileData['any_operation'] = request.data['anyOperation']
        serializer = UserProfileSerializer(
            instance=profile, data=profileData)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        userData = {}
        userData['id'] = request.user.id
        userData['username'] = request.user.username
        userData['first_name'] = request.data['firstName']
        userData['last_name'] = request.data['lastName']
        userData['email'] = request.data['email']

        userSerilizer = UpdateUserSerializer(
            instance=request.user, data=userData)
        if userSerilizer.is_valid(raise_exception=True):
            userSerilizer.save()
            return Response(userSerilizer.data)
        return Response(serializer.data)
        # except:
        #     data = {
        #         "data": "Insuffient/incorrect data"
        #     }
        #     return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
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
