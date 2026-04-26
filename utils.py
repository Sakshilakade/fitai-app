"""
Utility functions for FitAI app
Includes BMI calculation, diet plans, and fitness tips
"""


def calculate_bmi(weight_kg: float, height_m: float) -> dict:
    """
    Calculate BMI and return results with category
    
    Args:
        weight_kg: Weight in kilograms
        height_m: Height in meters
        
    Returns:
        Dictionary with bmi value, category, and message
    """
    if height_m <= 0 or weight_kg <= 0:
        return {
            "bmi": 0,
            "category": "Invalid",
            "message": "Please enter valid weight and height values."
        }
    
    bmi = weight_kg / (height_m ** 2)
    bmi = round(bmi, 1)
    
    if bmi < 18.5:
        category = "Underweight"
        message = "Focus on nutrient-rich foods and strength training to build muscle mass."
    elif 18.5 <= bmi < 25:
        category = "Normal"
        message = "Great job! Maintain your healthy lifestyle with balanced nutrition and regular exercise."
    elif 25 <= bmi < 30:
        category = "Overweight"
        message = "Incorporate more cardio and reduce processed foods for optimal health."
    else:
        category = "Obese"
        message = "Consider consulting a healthcare provider for a personalized fitness plan."
    
    return {
        "bmi": bmi,
        "category": category,
        "message": message
    }


def get_meal_plan(goal: str) -> dict:
    """
    Get personalized meal plan based on fitness goal
    
    Args:
        goal: Fitness goal (weight_loss, muscle_gain, maintain)
        
    Returns:
        Dictionary with meal plan
    """
    meal_plans = {
        "weight_loss": {
            "breakfast": {
                "time": "8:00 AM",
                "meal": "Oatmeal with berries and Greek yogurt",
                "calories": "350 kcal"
            },
            "mid_morning": {
                "time": "11:00 AM",
                "meal": "Apple slices with almond butter",
                "calories": "200 kcal"
            },
            "lunch": {
                "time": "1:00 PM",
                "meal": "Grilled chicken salad with quinoa",
                "calories": "450 kcal"
            },
            "snack": {
                "time": "4:00 PM",
                "meal": "Carrot sticks with hummus",
                "calories": "150 kcal"
            },
            "dinner": {
                "time": "7:00 PM",
                "meal": "Baked salmon with steamed vegetables",
                "calories": "400 kcal"
            }
        },
        "muscle_gain": {
            "breakfast": {
                "time": "8:00 AM",
                "meal": "Scrambled eggs with whole grain toast and avocado",
                "calories": "550 kcal"
            },
            "mid_morning": {
                "time": "11:00 AM",
                "meal": "Protein shake with banana",
                "calories": "300 kcal"
            },
            "lunch": {
                "time": "1:00 PM",
                "meal": "Grilled chicken with brown rice and vegetables",
                "calories": "650 kcal"
            },
            "snack": {
                "time": "4:00 PM",
                "meal": "Greek yogurt with nuts and honey",
                "calories": "250 kcal"
            },
            "dinner": {
                "time": "7:00 PM",
                "meal": "Lean beef stir-fry with sweet potato",
                "calories": "600 kcal"
            }
        },
        "maintain": {
            "breakfast": {
                "time": "8:00 AM",
                "meal": "Whole grain cereal with milk and fruit",
                "calories": "400 kcal"
            },
            "mid_morning": {
                "time": "11:00 AM",
                "meal": "Mixed nuts and dried fruit",
                "calories": "200 kcal"
            },
            "lunch": {
                "time": "1:00 PM",
                "meal": "Turkey sandwich with salad",
                "calories": "500 kcal"
            },
            "snack": {
                "time": "4:00 PM",
                "meal": "Fresh fruit smoothie",
                "calories": "180 kcal"
            },
            "dinner": {
                "time": "7:00 PM",
                "meal": "Grilled fish with vegetables and quinoa",
                "calories": "450 kcal"
            }
        }
    }
    
    return meal_plans.get(goal, meal_plans["maintain"])


def get_fitness_tips(goal: str) -> list:
    """
    Get fitness tips based on goal
    
    Args:
        goal: Fitness goal
        
    Returns:
        List of fitness tips
    """
    base_tips = [
        "Stay hydrated - drink at least 8 glasses of water daily",
        "Get 7-9 hours of quality sleep each night",
        "Warm up before every workout and cool down after",
        "Track your progress to stay motivated"
    ]
    
    goal_specific_tips = {
        "weight_loss": [
            "Create a caloric deficit of 300-500 calories daily",
            "Incorporate HIIT workouts 3-4 times per week",
            "Focus on compound exercises for maximum calorie burn",
            "Eat protein-rich foods to preserve muscle mass",
            "Avoid sugary drinks and processed foods"
        ],
        "muscle_gain": [
            "Consume 1.6-2g of protein per kg of body weight",
            "Train each muscle group 2-3 times per week",
            "Progressive overload is key - increase weights gradually",
            "Rest at least 48 hours between intense workouts",
            "Consider creatine supplementation for better performance"
        ],
        "maintain": [
            "Mix cardio and strength training weekly",
            "Aim for 150 minutes of moderate exercise per week",
            "Practice portion control with meals",
            "Include flexibility exercises in your routine",
            "Listen to your body and adjust as needed"
        ]
    }
    
    return base_tips + goal_specific_tips.get(goal, goal_specific_tips["maintain"])


import datetime
from typing import Dict, List
try:
    import pandas as pd
except ImportError:
    pd = None


def calculate_streak(profile: dict) -> int:
    """
    Calculate current workout streak days.
    """
    log = profile.get('workouts_log', [])
    if not log:
        return 0
    
    today = datetime.date.today()
    streak = 0
    
    for workout in reversed(log):
        workout_date = datetime.datetime.fromisoformat(workout['date']).date()
        if (today - workout_date).days == streak:
            streak += 1
        else:
            break
    
    return streak


def log_workout(profile: dict, workout_type: str, completed_exercises: list) -> dict:
    """
    Log a completed workout and update stats.
    """
    today_str = datetime.date.today().isoformat()
    
    new_log_entry = {
        'date': today_str,
        'workout_type': workout_type,
        'completed_exercises': completed_exercises,
        'completion_rate': len(completed_exercises) / len(completed_exercises) if completed_exercises else 0
    }
    
    profile['workouts_log'].append(new_log_entry)
    profile['total_workouts'] += 1
    profile['streak_days'] = calculate_streak(profile)
    
    return profile


def get_progress_stats(profile: dict) -> dict:
    """
    Get summary stats for dashboard.
    """
    log = profile.get('workouts_log', [])
    weights = profile.get('weight_history', [])
    
    stats = {
        'total_workouts': profile.get('total_workouts', 0),
        'current_streak': calculate_streak(profile),
        'avg_completion': sum(entry.get('completion_rate', 0) for entry in log) / len(log) if log else 0,
        'weight_change': weights[-1] - weights[0] if len(weights) >= 2 else (0 if weights else None)
    }
    
    return stats


def get_weight_chart_data(profile: dict) -> dict:
    """
    Prepare weight history data for Streamlit line chart.
    
    Args:
        profile: User profile dict
        
    Returns:
        Dict with 'labels' (dates) and 'values' (weights) or None if empty
    """
    weights = profile.get('weight_history', [])
    if not weights:
        return None
    
    # Assume weight_history is list of dicts like [{'date': '2024-01-01', 'weight': 70.0}, ...]
    # For compatibility, if simple list of numbers, use sequential dates
    if isinstance(weights[0], (int, float)):
        # Backward compat: simple list → generate dates
        base_date = datetime.date.today() - datetime.timedelta(days=len(weights))
        labels = [(base_date + datetime.timedelta(days=i)).isoformat() for i in range(len(weights))]
        values = weights
    else:
        # Structured: extract date/weight
        labels = [w.get('date', '') for w in weights]
        values = [w.get('weight', 0.0) for w in weights]
    
    return {
        "labels": labels,
        "values": values
    }