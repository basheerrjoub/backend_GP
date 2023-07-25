from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import *

urlpatterns = [
    path("users/", UserList.as_view()),
    path("profile/", UserDetailView.as_view()),
    path("meals/", MealList.as_view()),
    path("meals/<int:pk>/", MealDetail.as_view()),
    path("suggestions/", SuggestionsList.as_view()),
    path("login/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register_new_user"),
    path("answers/", AnswersView.as_view(), name="add_questionaire"),
    path("answers/update/", AnswersUpdateView.as_view(), name="answers-update"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("questions/", QuestionsView.as_view(), name="view_questions"),
    path(
        "recommendations/<str:type>",
        RecommendationsView.as_view(),
        name="recommendations",
    ),
    path("consumed/", report_consumed_meal_view),
    path(
        "daily_calorie_intake/",
        DailyCalorieIntakeView.as_view(),
        name="daily_calorie_intake",
    ),
    path("rate/", RatingView.as_view(), name="rate-meal"),
    path("top-rated/", TopRatedMealsView.as_view(), name="top-rated"),
    path("average-rating/<int:meal_id>/", RatingView.as_view(), name="average-rating"),
    path("meal_items/<int:meal_id>/", MealItemsView.as_view(), name="meal_items"),
    path("consumed_meals/", get_consumed_meals_view),
    path(
        "consumed_meals/delete/",
        DeleteConsumedMealView.as_view(),
        name="delete_consumed_meal",
    ),
]
