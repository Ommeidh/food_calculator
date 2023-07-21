#nutritionix_module.py
import os
import requests
import json
import config

def get_food_info(food_name, quantity):
    url = f"https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": config.NUTRITIONIX_APP_ID,
        "x-app-key": config.NUTRITIONIX_APP_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "query": f"{quantity} {food_name}"
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"Error: Unable to get food information (Status Code: {response.status_code})")
        return None

    response_data = response.json()

    if 'foods' not in response_data or len(response_data['foods']) == 0:
        print(f"Error: No food data found for {food_name}")
        return None

    # Return only the most relevant food item's information
    food = response_data['foods'][0]
    food_info = {
        "Food Name": food['food_name'],
        "Calories": food['nf_calories'],
        "Total Fat": food['nf_total_fat'],
        "Carbohydrates": food['nf_total_carbohydrate'],
        "Protein": food['nf_protein'],
        "Dietary Fiber": food['nf_dietary_fiber']
    }
    
    return food_info
