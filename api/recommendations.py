from sklearn.metrics.pairwise import cosine_similarity
from .models import *
from .models import DailyCalorieIntake
from .calculations import calculateTDEE


def get_user_vector(user_id):
    user_answers = Answers.objects.filter(user__id=user_id)

    question_mapping = {11: "spicy", 12: "warm", 17: "sweety", 18: "salty", 21: "hard"}

    user_vector = [0] * len(question_mapping)

    binary_response_mapping = {"yes": 1, "no": 0, "easy to chew": 1, "hard": 0}

    for answer in user_answers:
        if answer.question_id in question_mapping:
            score = binary_response_mapping.get(answer.question_answer.lower(), 0)

            index = list(question_mapping.keys()).index(answer.question_id)
            user_vector[index] = score

    return user_vector


meal_vectors_cache = {}


def get_meal_vector(meal_id):
    if meal_id in meal_vectors_cache:
        return meal_vectors_cache[meal_id]

    meal = Meal.objects.get(meal_id=meal_id)

    meal_vector = [
        meal.spicy,
        meal.warm,
        meal.sweety,
        meal.salty,
        meal.hard,
    ]

    meal_vectors_cache[meal_id] = meal_vector

    return meal_vector


def recommend_meals(user_id, mealType):
    calculateTDEE(user_id)
    # How much the user should have calories
    today = timezone.now().date()
    daily_intake = DailyCalorieIntake.objects.filter(
        user_id=user_id, date=today
    ).first()
    calories_already_consumed = 0
    daily_calorie_limit = 3000000
    if daily_intake:
        calories_already_consumed = daily_intake.total_consumed_calories
        daily_calorie_limit = daily_intake.total_recommended_calories

    remaining_calories = daily_calorie_limit - calories_already_consumed

    user_vector = get_user_vector(user_id)
    # Filter if the user is vegan or not:
    currentUser = User.objects.get(id=user_id)
    questionVegan = Questions.objects.get(question_desc="Are you vegan?")
    answer = Answers.objects.get(user=currentUser, question=questionVegan)
    vegan = 0
    if answer.question_answer.lower() == "yes":
        vegan = 1

    # @Todo
    # use the vegan indicator to filter for vegan users,
    # But First add the Vegan attribute to the meal table
    #
    # Filter For the meal's type:
    all_meals = None
    if mealType == "dinner":
        all_meals = Meal.objects.filter(dinner=1, vegan=vegan)
    elif mealType == "lunch":
        all_meals = Meal.objects.filter(lunch=1, vegan=vegan)
    elif mealType == "breakfast":
        all_meals = Meal.objects.filter(breakfast=1, vegan=vegan)
    elif mealType == "snack":
        all_meals = Meal.objects.filter(snack=1, vegan=vegan)
    else:  # Get all the meals without specification
        all_meals = Meal.objects.all()

    similarities = []
    for meal in all_meals:
        if meal.calories <= remaining_calories:
            meal_vector = get_meal_vector(meal.meal_id)
            similarity = cosine_similarity([user_vector], [meal_vector])[0][0]
            similarities.append((meal, similarity))

    sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

    recommended_meals = []
    total_calories = 0
    for meal, similarity in sorted_similarities:
        if total_calories + meal.calories <= remaining_calories:
            recommended_meals.append(meal)
            total_calories += meal.calories

    return recommended_meals
