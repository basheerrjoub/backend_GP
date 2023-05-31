from sklearn.metrics.pairwise import cosine_similarity
from .models import *


def get_user_vector(user_id):
    # Get all the answers for a user
    user_answers = Answers.objects.filter(user__id=user_id)

    # Map questions to meal attributes
    question_mapping = {11: "spicy", 12: "warm", 17: "sweety", 18: "salty", 21: "hard"}

    # Make a list of meal attributes in the same order as the question mapping
    user_vector = [0] * len(question_mapping)

    # Map binary responses to numerical scores, and add some specific textual responses
    binary_response_mapping = {"yes": 1, "no": 0, "easy to chew": 1, "hard": 0}

    for answer in user_answers:
        if answer.question_id in question_mapping:
            # Map the binary response to a numerical score
            # Use the 'get' method with default as 0 to handle any unexpected answers
            score = binary_response_mapping.get(answer.question_answer.lower(), 0)

            index = list(question_mapping.keys()).index(answer.question_id)
            user_vector[index] = score

    return user_vector


def get_meal_vector(meal_id):
    # Get the meal by id
    meal = Meal.objects.get(meal_id=meal_id)

    # Make a vector from meal attributes
    meal_vector = [
        meal.spicy,
        meal.warm,
        meal.sweety,
        meal.salty,
        meal.hard,
    ]

    return meal_vector


def recommend_meals(user_id):
    # Get the user's answer vector
    user_vector = get_user_vector(user_id)

    # Calculate cosine similarity with all meals
    similarities = []
    all_meals = Meal.objects.all()
    for meal in all_meals:
        meal_vector = get_meal_vector(meal.meal_id)
        similarity = cosine_similarity([user_vector], [meal_vector])[0][0]
        similarities.append((meal, similarity))

    # Sort by similarity and return the top 5 most similar meals
    sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    recommended_meals = [meal[0] for meal in sorted_similarities[:5]]

    return recommended_meals
