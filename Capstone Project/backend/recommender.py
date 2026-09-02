def calculate_suitability_score(meal, user_req):
    """
    Calculates how well a meal fits the user's requirements.
    Score out of 100.
    """
    score = 100.0
    
    # Hard filter: Vegetarian mismatch
    if user_req.get('Is_Vegetarian') and meal['Is_Vegetarian'] == 0:
        return 0.0 # Completely unsuited
        
    # Budget Penalty
    daily_budget = user_req.get('Daily_Budget', 500)
    # A single meal should roughly be ~35% of daily budget
    if meal['Cost'] > daily_budget * 0.4: 
        score -= 20
    elif meal['Cost'] > daily_budget * 0.35:
        score -= 10
        
    # BMI and Fitness Goal Logic
    bmi = user_req.get('BMI', 22.0)
    fitness_goal = user_req.get('Fitness_Goal', 'Maintain')
    
    # Penalize high calories/fat if cutting or high BMI
    if fitness_goal == 'Cut' or (bmi > 25 and fitness_goal != 'Bulk'):
        if meal['Calories'] > 600: score -= 15
        if meal['Fat'] > 20: score -= 10
    
    # Penalize low calories/protein if bulking
    if fitness_goal == 'Bulk':
        if meal['Calories'] < 400: score -= 15
        if meal['Protein'] < 25: score -= 10
        
    # Nutrition Penalty
    target_cal = user_req.get('Daily_Calories', 2000) / 3.0
    target_pro = user_req.get('Daily_Protein', 100) / 3.0
    
    cal_diff_pct = abs(meal['Calories'] - target_cal) / max(1, target_cal)
    if cal_diff_pct > 0.15:
        score -= min(30, cal_diff_pct * 50)
        
    pro_diff_pct = abs(meal['Protein'] - target_pro) / max(1, target_pro)
    if pro_diff_pct > 0.2:
        score -= min(20, pro_diff_pct * 40)

    # Prep time penalty
    max_prep = user_req.get('Max_Prep_Time', 0)
    if max_prep > 0 and meal['Prep_Time'] > max_prep:
        score -= 20
        
    # Preference match boosts
    pref_cuisine = user_req.get('Cuisine_Preference', 'Any')
    if pref_cuisine != 'Any' and meal['Cuisine'] == pref_cuisine:
        score += 15
        
    req_meal_type = user_req.get('Meal_Type', 'Any')
    if req_meal_type != 'Any' and meal['Meal_Type'] == req_meal_type:
        score += 20
        
    # Add base rating bonus
    score += meal['Base_Rating'] * 2
    
    return max(0.0, min(100.0, score))
