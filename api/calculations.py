from .models import Answers, User, Questions, DailyCalorieIntake
from datetime import datetime


def calculateTDEE(user_id):
    currentUser = User.objects.get(id=user_id)
    questionExcersise = Questions.objects.get(
        question_desc="How often do you engage in physical activity or exercise?"
    )
    excersieAnswer = Answers.objects.get(user=currentUser, question=questionExcersise)
    exersise_answers_mapping = {"1": 1.2, "2": 1.375, "3": 1.55, "4": 1.725, "5": 1.9}
    multiplayer = exersise_answers_mapping[excersieAnswer.question_answer]

    # Calculate BMR\
    BMR = 0

    # Gender
    questionGender = Questions.objects.get(question_desc="What is your gender?")
    genderAnswer = Answers.objects.get(user=currentUser, question=questionGender)

    # weight
    questionWeight = Questions.objects.get(question_desc="Please provide your weight:")
    weightAnswer = Answers.objects.get(user=currentUser, question=questionWeight)

    weight = int(weightAnswer.question_answer)

    # height
    questionHeight = Questions.objects.get(question_desc="Please provide your height:")
    heightAnswer = Answers.objects.get(user=currentUser, question=questionHeight)

    height = int(heightAnswer.question_answer)

    # Age
    questionAge = Questions.objects.get(question_desc="Date of Birth")

    ageAnswer = Answers.objects.get(user=currentUser, question=questionAge)
    currentYear = datetime.now().year
    age = int(currentYear) - int(ageAnswer.question_answer)

    if str(genderAnswer.question_answer) == "female":
        BMR = 65.5 + (9.563 * weight) + (1.850 * height) - (4.676 * age)
    elif str(genderAnswer.question_answer) == "male":
        BMR = 66.5 + (13.76 * weight) + (5.003 * height) - (6.755 * age)

    tdee = BMR * multiplayer

    # Get today's date
    today = datetime.now().date()

    # Fetch or create a DailyCalorieIntake record for this user and today's date
    daily_calorie_intake, created = DailyCalorieIntake.objects.get_or_create(
        user=currentUser, date=today, defaults={"total_recommended_calories": tdee}
    )

    # If the record was not just created, update the total_recommended_calories
    if not created:
        daily_calorie_intake.total_recommended_calories = tdee
        daily_calorie_intake.save()

    print(f"TDEE: {tdee}")


def calculateBMI(user_id):
    currentUser = User.objects.get(id=user_id)

    # weight
    questionWeight = Questions.objects.get(question_desc="Please provide your weight:")
    weightAnswer = Answers.objects.get(user=currentUser, question=questionWeight)
    weight = int(weightAnswer.question_answer)

    # height
    questionHeight = Questions.objects.get(question_desc="Please provide your height:")
    heightAnswer = Answers.objects.get(user=currentUser, question=questionHeight)
    height = int(heightAnswer.question_answer) / 100  # Convert height to meters

    # Calculate BMI
    bmi = weight / (height * height)

    return bmi
