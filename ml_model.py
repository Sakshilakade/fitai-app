"""
Machine Learning Model for FitAI
Predicts workout type using DecisionTreeClassifier
"""

import numpy as np
from sklearn.tree import DecisionTreeClassifier


# ------------------------------------------------------------
# 1. Create dataset
# ------------------------------------------------------------

def create_sample_data():

    X = []
    y = []

    for weight in range(45, 101, 5):
        for height in [1.50, 1.55, 1.60, 1.65, 1.70, 1.75, 1.80]:
            for age in range(15, 61, 5):
                for gender in [0, 1]:
                    for activity in [0, 1, 2]:
                        for diet in [0, 1, 2]:
                            for goal in [0, 1, 2]:

                                if goal == 0:
                                    workout = 0 if activity >= 1 else 2
                                elif goal == 1:
                                    workout = 1
                                else:
                                    workout = 2 if activity == 0 else 0

                                X.append([weight, height, age, gender, activity, diet, goal])
                                y.append(workout)

    return np.array(X), np.array(y)


# ------------------------------------------------------------
# 2. Train model
# ------------------------------------------------------------

def train_model():
    X, y = create_sample_data()
    model = DecisionTreeClassifier(max_depth=12, random_state=42)
    model.fit(X, y)
    return model


model = train_model()


# ------------------------------------------------------------
# 3. Workout Plans
# ------------------------------------------------------------
WORKOUT_PLANS = {

    0: {
        "workout_type": "HIIT (High-Intensity Interval Training)",
        "exercises": [
            {"name": "Jumping Jacks", "reps": "30 sec"},
            {"name": "Burpees", "reps": "15"},
            {"name": "Mountain Climbers", "reps": "30 sec"},
            {"name": "High Knees", "reps": "30 sec"},
            {"name": "Push-ups", "reps": "12"},
            {"name": "Squat Jumps", "reps": "12"},
            {"name": "Plank", "reps": "30 sec"}
        ]
    },

    1: {
        "workout_type": "Strength Training",
        "exercises": [
            {"name": "Squats", "reps": "12"},
            {"name": "Deadlifts", "reps": "10"},
            {"name": "Bench Press", "reps": "10"},
            {"name": "Shoulder Press", "reps": "12"},
            {"name": "Dumbbell Curls", "reps": "15"},
            {"name": "Lunges", "reps": "12 per leg"},
            {"name": "Plank", "reps": "30 sec"}
        ]
    },

    2: {
        "workout_type": "Cardio Training",
        "exercises": [
            {"name": "Running", "reps": "20 min"},
            {"name": "Cycling", "reps": "25 min"},
            {"name": "Skipping", "reps": "15 min"},
            {"name": "Brisk Walking", "reps": "30 min"},
            {"name": "Swimming", "reps": "20 min"},
            {"name": "Jump Rope", "reps": "10 min"}
        ]
    }

}
# ------------------------------------------------------------
# 4. FOOD PLANS
# ------------------------------------------------------------

VEG_MEAL_PLANS = {

    0: {  # HIIT
        "food_type": "Veg HIIT",
        "meals": [
            "Oats with fruits",
            "Banana smoothie",
            "Peanut butter toast",
            "Paneer quinoa bowl",
            "Vegetable upma",
            "Sprouts salad",
            "Greek yogurt with nuts",
            "Protein shake (veg)",
            "Brown rice with dal",
            "Mixed veg curry + roti",
            "Moong dal chilla",
            "Vegetable poha",
            "Paneer tikka salad",
            "Fruit and nut lassi"
        ]
    },

    1: {  # Strength
        "food_type": "Veg Strength",
        "meals": [
            "Paneer bhurji",
            "Paneer paratha",
            "Rajma rice",
            "Chole with roti",
            "Tofu stir fry",
            "Boiled chickpeas",
            "Milk with almonds",
            "Protein shake",
            "Soy chunks curry",
            "Dal + rice + ghee",
            "Paneer tikka",
            "Spinach dal",
            "Chana masala",
            "Curd rice"
        ]
    },

    2: {  # Cardio
        "food_type": "Veg Cardio",
        "meals": [
            "Poha",
            "Vegetable upma",
            "Khichdi",
            "Fruit bowl",
            "Vegetable sandwich",
            "Idli with sambar",
            "Buttermilk",
            "Light dal soup",
            "Steamed vegetables",
            "Whole wheat roti + sabzi",
            "Cucumber salad",
            "Sprouts chaat",
            "Mint coriander chutney",
            "Vegetable dalia"
        ]
    }

}
NONVEG_MEAL_PLANS = {

    0: {  # HIIT
        "food_type": "Non-Veg HIIT",
        "meals": [
            "Boiled eggs",
            "Egg omelette",
            "Chicken wrap",
            "Grilled chicken breast",
            "Chicken salad",
            "Egg sandwich",
            "Protein shake",
            "Chicken quinoa bowl",
            "Boiled eggs + toast",
            "Chicken soup",
            "Egg bhurji",
            "Tandoori chicken skewers",
            "Fish tikka",
            "Masala omelette"
        ]
    },

    1: {  # Strength
        "food_type": "Non-Veg Strength",
        "meals": [
            "Grilled chicken",
            "Chicken curry + rice",
            "Fish (salmon/tuna)",
            "Eggs + peanut butter toast",
            "Chicken breast + sweet potato",
            "Tuna salad",
            "Boiled eggs",
            "Protein shake with milk",
            "Chicken biryani (controlled portion)",
            "Egg bhurji + roti",
            "Mutton stew",
            "Egg curry",
            "Tandoori fish",
            "Chicken kebab"
        ]
    },

    2: {  # Cardio
        "food_type": "Non-Veg Cardio",
        "meals": [
            "Boiled eggs",
            "Egg white omelette",
            "Tuna sandwich",
            "Grilled fish",
            "Chicken soup",
            "Egg salad",
            "Light chicken curry",
            "Fish + steamed vegetables",
            "Egg toast",
            "Chicken sandwich (light)",
            "Fish fry",
            "Tuna salad",
            "Chicken shawarma wrap",
            "Egg bhurji"
        ]
    }

}
VEGAN_MEAL_PLANS = {

    0: {  # HIIT
        "food_type": "Vegan HIIT",
        "meals": [
            "Oats with almond milk",
            "Banana smoothie",
            "Peanut butter toast",
            "Mixed nuts",
            "Tofu quinoa bowl",
            "Chickpea salad",
            "Vegan protein shake",
            "Brown rice + vegetables",
            "Fruit bowl",
            "Soy milk smoothie",
            "Sprouts salad",
            "Vegetable poha",
            "Moong dal chilla",
            "Coconut water"
        ]
    },

    1: {  # Strength
        "food_type": "Vegan Strength",
        "meals": [
            "Tofu scramble",
            "Lentil (dal) curry",
            "Chickpea (chana) bowl",
            "Soy chunks curry",
            "Peanut butter sandwich",
            "Vegan protein shake",
            "Kidney beans (rajma)",
            "Quinoa salad",
            "Oats + nuts",
            "Brown rice + dal",
            "Rajma masala",
            "Chole bhature (portion controlled)",
            "Vegetable khichdi",
            "Soya chaap curry"
        ]
    },

    2: {  # Cardio
        "food_type": "Vegan Cardio",
        "meals": [
            "Fruit smoothie",
            "Green salad",
            "Vegetable soup",
            "Steamed vegetables",
            "Brown rice + veggies",
            "Whole wheat toast + peanut butter",
            "Fruit bowl",
            "Lemon water + nuts",
            "Light dal soup",
            "Veg sandwich (no butter)",
            "Cucumber raita",
            "Moong dal salad",
            "Sprouts chaat",
            "Carrot-cucumber sticks"
        ]
    }

}

def _interleave_meals(veg_meals, nonveg_meals):
    """Return a mixed meal list with alternating veg and non-veg items."""
    mixed = []
    max_len = max(len(veg_meals), len(nonveg_meals))
    for i in range(max_len):
        if i < len(veg_meals):
            mixed.append(veg_meals[i])
        if i < len(nonveg_meals):
            mixed.append(nonveg_meals[i])
    return mixed


MIXED_MEAL_PLANS = {

    0: {  # HIIT
        "food_type": "Veg + Non-Veg HIIT",
        "meals": _interleave_meals(VEG_MEAL_PLANS[0]["meals"], NONVEG_MEAL_PLANS[0]["meals"])
    },

    1: {  # Strength
        "food_type": "Veg + Non-Veg Strength",
        "meals": _interleave_meals(VEG_MEAL_PLANS[1]["meals"], NONVEG_MEAL_PLANS[1]["meals"])
    },

    2: {  # Cardio
        "food_type": "Veg + Non-Veg Cardio",
        "meals": _interleave_meals(VEG_MEAL_PLANS[2]["meals"], NONVEG_MEAL_PLANS[2]["meals"])
    }

}


# ------------------------------------------------------------
# 5. FINAL FUNCTION (FIXED)
# ------------------------------------------------------------

def predict_workout(weight, height, age, gender, activity, diet, goal):

    # -------- ENCODING --------
    gender_map = {"Male": 0, "Female": 1}
    activity_map = {"Low": 0, "Moderate": 1, "High": 2}
    goal_map = {"weight_loss": 0, "muscle_gain": 1, "maintain": 2}

    gender_enc = gender_map.get(gender, 0)
    activity_enc = activity_map.get(activity, 1)
    goal_enc = goal_map.get(goal, 0)

    # -------- INPUT --------
    user_input = np.array([[weight, height, age, gender_enc, activity_enc, 0, goal_enc]])

    # -------- PREDICT --------
    predicted_id = int(model.predict(user_input)[0])

    workout_plan = WORKOUT_PLANS[predicted_id]

    # -------- DIET FIX --------
    diet_clean = diet.strip().lower().replace(" ", "").replace("-", "")

    if diet_clean == "veg":
        food_plan = VEG_MEAL_PLANS[predicted_id]

    elif diet_clean in ["non-veg", "nonveg"]:
        food_plan = NONVEG_MEAL_PLANS[predicted_id]

    elif diet_clean == "vegan":
        food_plan = VEGAN_MEAL_PLANS[predicted_id]

    elif diet_clean == "veg+nonveg":
        food_plan = MIXED_MEAL_PLANS[predicted_id]

    else:
        food_plan = VEG_MEAL_PLANS[predicted_id]

    # -------- RETURN --------
    return {
        "workout": workout_plan,
        "food_plan": food_plan
    }
