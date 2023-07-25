from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.db.models import Avg
from django.contrib.auth.hashers import make_password
from django.views import View
from django.http import JsonResponse


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.filter(id=self.request.user.id).first()
        if obj is None:
            raise Http404("No User matches the given query.")
        return obj


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


class AnswersUpdateView(generics.UpdateAPIView):
    queryset = Answers.objects.all()
    serializer_class = AnswersSerializer

    def get_queryset(self):
        user = self.request.user
        return Answers.objects.filter(user=user)

    def partial_update(self, request, *args, **kwargs):
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


from rest_framework import status
from rest_framework.decorators import api_view, permission_classes


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def report_consumed_meal_view(request):
    meal_id = request.data.get("meal_id")
    if not meal_id:
        return Response(
            {"error": "Meal id is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        meal = Meal.objects.get(meal_id=meal_id)
        report_consumed_meal(request.user.id, meal_id)
        consumed_meal = ConsumedMeal(user=request.user, meal=meal, consumed=True)
        consumed_meal.save()
    except Meal.DoesNotExist:
        return Response(
            {"error": "Meal does not exist"}, status=status.HTTP_400_BAD_REQUEST
        )

    return Response({"message": "Meal consumption reported successfully"})


def report_consumed_meal(user_id, meal_id):
    meal = Meal.objects.get(meal_id=meal_id)
    today = timezone.localtime().date()
    daily_intake, created = DailyCalorieIntake.objects.get_or_create(
        user_id=user_id, date=today
    )
    if created:
        daily_intake.date = today
    daily_intake.total_consumed_calories += meal.calories
    daily_intake.save()


class DailyCalorieIntakeView(generics.GenericAPIView):
    serializer_class = DailyCalorieIntakeSerializer

    def get(self, request, format=None):
        try:
            user_id = request.user.id
            user = User.objects.get(id=user_id)

            today = datetime.today()

            daily_calorie_intake = DailyCalorieIntake.objects.get(user=user, date=today)

            serializer = self.get_serializer(daily_calorie_intake)

            return Response(serializer.data)

        except DailyCalorieIntake.DoesNotExist:
            return Response(
                {"message": "No daily calorie intake record found for today."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except User.DoesNotExist:
            return Response(
                {"message": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )


class TopRatedMealsView(APIView):
    def get(self, request):
        top_rated_meals = Meal.objects.annotate(
            average_rating=Avg("rating__rating")
        ).order_by("-average_rating")[:5]

        serializer = MealSerializer(top_rated_meals, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RatingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            rating = serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, meal_id):
        ratings = Rating.objects.filter(meal__meal_id=meal_id)
        average_rating = ratings.aggregate(Avg("rating"))["rating__avg"]
        return Response({"average_rating": average_rating}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    def put(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        new_password = data.get("new_password")

        if new_password:
            user.password = make_password(new_password)
            user.save()
            return Response(
                {"status": "Password updated successfully."}, status=status.HTTP_200_OK
            )

        else:
            return Response(
                {"error": "New password not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class MealItemsView(View):
    def get(self, request, meal_id):
        meal = Meal.objects.get(meal_id=meal_id)
        meal_items = MealItem.objects.filter(meal=meal)
        result = []
        for mi in meal_items:
            item = Item.objects.get(item_id=mi.item.item_id)
            result.append(
                {
                    "item_name": item.item_name,
                    "item_desc": item.item_desc,
                    "weight": mi.weight,
                }
            )
        return JsonResponse(result, safe=False)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_consumed_meals_view(request):
    consumed_meals = ConsumedMeal.objects.filter(user=request.user, consumed=True)
    consumed_meals_list = [meal.meal_id for meal in consumed_meals]
    return Response({"consumed_meals": consumed_meals_list})


from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import ConsumedMealSerializer
from django.shortcuts import get_object_or_404


class DeleteConsumedMealView(generics.DestroyAPIView):
    queryset = ConsumedMeal.objects.all()
    serializer_class = ConsumedMealSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        meal_id = request.data.get("meal_id")  # get meal id from the request data
        user_id = request.user.id  # get the user id from the request

        # check for user and meal id
        if not meal_id:
            return Response(
                {"error": "Meal id is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        consumed_meals = ConsumedMeal.objects.filter(user=user_id, meal=meal_id)

        if not consumed_meals:
            return Response(
                {"error": "No record of this user consuming this meal was found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        for consumed_meal in consumed_meals:
            consumed_meal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
