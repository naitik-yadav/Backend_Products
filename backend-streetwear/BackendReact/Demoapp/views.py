from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Nike, User
from .serializers import NikeSerializer, RegisterSerializer, LoginSerializer, LogoutSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login

class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
            )
            if user is not None:
                auth_login(request, user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            try:
                RefreshToken(serializer.validated_data['refresh']).blacklist()
                logout(request)
                return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
            except RefreshToken.DoesNotExist:
                return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NikeList(APIView):
    parser_classes = (MultiPartParser, FormParser)

    
    def get(self, request, format=None):
        nike = Nike.objects.all()
        serializer = NikeSerializer(nike, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NikeSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            instance.notify_consumers()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class NikeDetails(APIView):
    def get_object(self, pk):
        try:
            return Nike.objects.get(pk=pk)
        except Nike.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        nike = self.get_object(pk)
        serializer = NikeSerializer(nike)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        nike = self.get_object(pk)
        serializer = NikeSerializer(nike, data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            instance.notify_consumers()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        nike = self.get_object(pk)
        nike.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

