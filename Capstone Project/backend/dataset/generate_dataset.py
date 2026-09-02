import pandas as pd
import random
import os

def generate_realistic_meals(num_meals=2500):
    cuisines = ['Indian', 'Italian', 'American', 'Mexican', 'Asian', 'Mediterranean']
    meal_types = ['Breakfast', 'Lunch', 'Dinner', 'Snack']
    
    # Base foods to combine
    veg_proteins = ['Paneer', 'Tofu', 'Lentils', 'Chickpeas', 'Beans']
    non_veg_proteins = ['Chicken', 'Fish', 'Egg', 'Beef', 'Pork', 'Turkey']
    carbs = ['Rice', 'Pasta', 'Quinoa', 'Bread', 'Oats', 'Potato', 'Wrap']
    veg_extras = ['Broccoli', 'Spinach', 'Mixed Veggies', 'Mushroom', 'Salad']
    flavors = ['Spicy', 'Mild', 'Creamy', 'Grilled', 'Roasted', 'Fried', 'Baked']
    
    meals = []
    
    for i in range(1, num_meals + 1):
        is_veg = random.choice([True, False])
        meal_type = random.choice(meal_types)
        cuisine = random.choice(cuisines)
        
        # Name generation
        flavor = random.choice(flavors)
        carb = random.choice(carbs)
        protein = random.choice(veg_proteins) if is_veg else random.choice(non_veg_proteins)
        extra = random.choice(veg_extras)
        
        if meal_type == 'Breakfast':
            meal_name = f"{flavor} {protein} with {carb}" if not is_veg else f"{carb} with {extra}"
            if is_veg and random.random() < 0.5:
                meal_name = f"Oats with Fruits & Nuts"
        elif meal_type == 'Snack':
            meal_name = f"Roasted {protein}" if is_veg else f"Grilled {protein} Bites"
            if random.random() < 0.3:
                meal_name = f"Greek Yogurt with Honey"
        else:
            meal_name = f"{flavor} {protein} & {carb} Bowl with {extra}"

        # Nutritional logic
        # Base multipliers
        size_mult = 1.0
        if meal_type == 'Snack':
            size_mult = 0.4
        elif meal_type == 'Dinner':
            size_mult = 1.2
            
        calories = int(random.uniform(300, 700) * size_mult)
        
        # Macros in grams
        protein_g = int(random.uniform(10, 40) * size_mult)
        if not is_veg:
            protein_g += int(random.uniform(10, 20)) # Meat has more protein
            
        fat_g = int(random.uniform(5, 25) * size_mult)
        if flavor in ['Fried', 'Creamy']:
            fat_g += int(random.uniform(10, 15))
            calories += int(fat_g * 9)
            
        # Carbs = (Calories - (Protein*4 + Fat*9)) / 4
        rem_cal = calories - (protein_g * 4 + fat_g * 9)
        if rem_cal < 0:
            rem_cal = 50
            calories = int((protein_g * 4 + fat_g * 9) + rem_cal)
        carbs_g = int(rem_cal / 4)
        
        fiber_g = int(random.uniform(2, 12) * size_mult)
        if is_veg:
            fiber_g += int(random.uniform(2, 5))
            
        # Cost logic (INR)
        base_cost = random.uniform(40, 120) * size_mult
        if not is_veg:
            base_cost += random.uniform(20, 50)
        cost = int(base_cost)
        
        prep_time = int(random.uniform(5, 45))
        if meal_type == 'Snack':
            prep_time = int(random.uniform(2, 10))
            
        rating = round(random.uniform(3.5, 5.0), 1)
        
        meals.append({
            'Meal_ID': i,
            'Meal_Name': meal_name,
            'Cuisine': cuisine,
            'Calories': calories,
            'Protein': protein_g,
            'Carbohydrates': carbs_g,
            'Fat': fat_g,
            'Fiber': fiber_g,
            'Cost': cost,
            'Is_Vegetarian': 1 if is_veg else 0,
            'Meal_Type': meal_type,
            'Prep_Time': prep_time,
            'Base_Rating': rating
        })
        
    df = pd.DataFrame(meals)
    # Ensure dataset directory exists
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    df.to_csv(os.path.join(os.path.dirname(__file__), 'meals.csv'), index=False)
    print(f"Generated {num_meals} meals in meals.csv")

if __name__ == '__main__':
    generate_realistic_meals()
