from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class MealList(generics.ListCreateAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]


class MealDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]


class SuggestionsList(generics.ListAPIView):
    serializer_class = MealSerializer

    def get_queryset(self):
        user = self.request.user
        return Meal.objects.filter(suggestions__user=user)
