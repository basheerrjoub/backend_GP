from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status


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


class QuestionsView(generics.ListAPIView):
    serializer_class = QuestionsSerializer
    queryset = Questions.objects.all()
    permission_classes = [IsAuthenticated]


class AnswersView(generics.ListCreateAPIView):
    serializer_class = AnswersSerializer

    def get_queryset(self):
        user = self.request.user
        return Answers.objects.filter(user=user)

    def update(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        for item_data in request.data:
            question_id = item_data.get("question_id")
            answer_text = item_data.get("question_answer")

            answer, created = queryset.update_or_create(
                question_id=question_id, defaults={"question_answer": answer_text}
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "message": "User Created Successfully.  Now perform Login to get your token",
            }
        )


from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from .recommendations import (
    recommend_meals,
)  # Assuming recommend_meals function is in recommendations.py


class RecommendationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, type, format=None):
        user_id = request.user.id
        print(f"Recommend : {type}")
        try:
            recommended_meals = recommend_meals(user_id, mealType=type)
        except User.DoesNotExist:
            raise NotFound("User does not exist")

        serializer = MealSerializer(recommended_meals, many=True)
        return Response(serializer.data)
