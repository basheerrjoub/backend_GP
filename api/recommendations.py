from sklearn.metrics.pairwise import cosine_similarity
from .models import *


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


def get_meal_vector(meal_id):
    meal = Meal.objects.get(meal_id=meal_id)

    meal_vector = [
        meal.spicy,
        meal.warm,
        meal.sweety,
        meal.salty,
        meal.hard,
    ]

    return meal_vector


def recommend_meals(user_id, mealType):
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
        meal_vector = get_meal_vector(meal.meal_id)
        similarity = cosine_similarity([user_vector], [meal_vector])[0][0]
        similarities.append((meal, similarity))

    # return the top 5 most similar meals
    sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    recommended_meals = [meal[0] for meal in sorted_similarities[:5]]

    return recommended_meals
