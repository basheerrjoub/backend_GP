from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import *

urlpatterns = [
    path("users/", UserList.as_view()),
    path("users/<int:pk>/", UserDetail.as_view()),
    path("meals/", MealList.as_view()),
    path("meals/<int:pk>/", MealDetail.as_view()),
    path("suggestions/", SuggestionsList.as_view()),
    path("login/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register_new_user"),
    path("answers/", AnswersView.as_view(), name="add_questionaire"),
    path("questions/", QuestionsView.as_view(), name="view_questions"),
    path("recommendations/", RecommendationsView.as_view(), name="recommendations"),
]
