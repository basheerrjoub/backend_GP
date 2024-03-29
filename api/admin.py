from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "username", "is_staff")
    search_fields = ("email", "username")
    ordering = ("email",)


class MealAdmin(admin.ModelAdmin):
    list_display = (
        "meal_id",
        "meal_name",
        "meal_des",
        "snack",
        "breakfast",
        "lunch",
        "dinner",
        "warm",
        "hard",
        "salty",
        "sweety",
        "spicy",
        "image",
        "vegan",
        "calories",
    )
    search_fields = ("meal_name",)


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ("question_id", "question_desc")
    search_fields = ("question_desc",)


class AnswersAdmin(admin.ModelAdmin):
    list_display = ("user_question_id", "user", "question", "question_answer")
    search_fields = ("user__username", "question__question_desc", "question_answer")


class DailyCalorieIntakeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "date",
        "total_recommended_calories",
        "total_consumed_calories",
    )

    search_fields = ("user_id",)


class RatingAdmin(admin.ModelAdmin):
    list_display = ("user", "meal", "rating")
    list_filter = ("user", "meal")
    search_fields = ("user__username", "meal__meal_name")


admin.site.register(Rating, RatingAdmin)

admin.site.register(DailyCalorieIntake, DailyCalorieIntakeAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Questions, QuestionsAdmin)
admin.site.register(Answers, AnswersAdmin)
admin.site.site_header = "AI Diabetes Management System"
admin.site.site_title = " Management System"
admin.site.index_title = "Management System"
