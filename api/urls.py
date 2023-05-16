from django.urls import path
from .views import *

urlpatterns = [
    path("users/", UserList.as_view()),
    path("users/<int:pk>/", UserDetail.as_view()),
    path("meals/", MealList.as_view()),
    path("meals/<int:pk>/", MealDetail.as_view()),
    path("suggestions/", SuggestionsList.as_view()),
]
