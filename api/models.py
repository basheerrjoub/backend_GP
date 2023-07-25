from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, staff=0):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        if staff:
            return user
        user.save(self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, password=password, username=username, staff=1)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(self._db)
        return user


class User(AbstractUser, PermissionsMixin):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.username


class Meal(models.Model):
    meal_id = models.IntegerField(primary_key=True)
    meal_name = models.CharField(max_length=50)
    meal_des = models.CharField(max_length=300)
    snack = models.IntegerField()
    breakfast = models.IntegerField()
    lunch = models.IntegerField()
    dinner = models.IntegerField()
    warm = models.IntegerField()
    hard = models.IntegerField()
    salty = models.IntegerField()
    sweety = models.IntegerField()
    spicy = models.IntegerField()
    image = models.ImageField(upload_to="meals/", blank=True, null=True)
    vegan = models.IntegerField()
    calories = models.IntegerField()

    class Meta:
        db_table = "meal"

    def __str__(self):
        return self.meal_name


class Questions(models.Model):
    question_id = models.IntegerField(primary_key=True)
    question_desc = models.CharField(max_length=1000)

    class Meta:
        db_table = "questions"
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.question_desc


class Suggestions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)

    suggestion_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "suggestions"

    def __str__(self):
        return f"Suggestion: {self.meal.meal_name} for User: {self.user.username}"


class Answers(models.Model):
    user_question_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    question_answer = models.CharField(max_length=100)

    class Meta:
        db_table = "user_question"
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        unique_together = (("user_id", "question_id"),)

    def __str__(self):
        return f"Question ID: {self.question_id} Answer: {self.question_answer}"


from django.utils import timezone


class DailyCalorieIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    total_recommended_calories = models.IntegerField(default=0)
    total_consumed_calories = models.IntegerField(default=0)

    class Meta:
        db_table = "daily_calorie_intake"
        unique_together = (("user", "date"),)

    def __str__(self):
        return f"Daily calorie intake for {self.user.username} on {self.date}"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        db_table = "rating"
        unique_together = (("user", "meal"),)

    def __str__(self):
        return f"Rating for {self.user.username} on Meal: {self.meal.meal_name}"


class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=100)
    item_desc = models.CharField(max_length=500)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    fat = models.DecimalField(max_digits=5, decimal_places=2)
    carbs = models.DecimalField(max_digits=5, decimal_places=2)
    cal = models.DecimalField(max_digits=5, decimal_places=2)
    sugar = models.DecimalField(max_digits=5, decimal_places=2)
    vegan = models.BooleanField(default=False)
    vegetarian = models.BooleanField(default=False)
    bread = models.BooleanField(default=False)
    rice = models.BooleanField(default=False)

    class Meta:
        db_table = "items"

    def __str__(self):
        return self.item_name


class MealItem(models.Model):
    id = models.AutoField(primary_key=True)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    weight = models.FloatField()

    class Meta:
        db_table = "meal_item"


class ConsumedMeal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    consumed = models.BooleanField(default=False)

    class Meta:
        db_table = "consumed_meal"

    def __str__(self):
        return f"{self.user.username} - {self.meal.meal_name}"
