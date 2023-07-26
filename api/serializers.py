from rest_framework import serializers
from .models import *
from rest_framework.exceptions import APIException
from django.db import IntegrityError
from rest_framework import status


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = "__all__"


class SuggestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestions
        fields = "__all__"


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = "__all__"


class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ["user_question_id", "question", "question_answer"]
        read_only_fields = ("user_question_id",)

    def create(self, validated_data):
        try:
            # Get the user from the request
            user = self.context["request"].user.id

            # Create a new Answer object
            answer = Answers.objects.create(user_id=user, **validated_data)

            return answer

        except IntegrityError:
            raise APIException("Duplicate entry", code=status.HTTP_400_BAD_REQUEST)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        return user


class DailyCalorieIntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyCalorieIntake
        fields = ["date", "total_recommended_calories", "total_consumed_calories"]


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["meal", "rating"]


class ConsumedMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumedMeal
        fields = ["user", "meal", "consumed"]


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("item_id", "item_name", "weight", "cal")


class HeightWeightSerializer(serializers.ModelSerializer):
    height = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()

    class Meta:
        model = Answers
        fields = ["height", "weight"]

    def get_height(self, obj):
        try:
            return Answers.objects.get(
                user=self.context["request"].user, question_id=4
            ).question_answer
        except Answers.DoesNotExist:
            return None

    def get_weight(self, obj):
        try:
            return Answers.objects.get(
                user=self.context["request"].user, question_id=5
            ).question_answer
        except Answers.DoesNotExist:
            return None
