from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import os
import random
import json
from datetime import datetime
from model import preprocess_and_train
from recommender import calculate_suitability_score

app = FastAPI(title="AI Meal Recommender")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load dataset
DATASET_PATH = os.path.join(os.path.dirname(__file__), "dataset", "meals.csv")
USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")

try:
    meals_df = pd.read_csv(DATASET_PATH)
except Exception as e:
    print(f"Error loading dataset: {e}")
    meals_df = pd.DataFrame()

# Global variable to store latest model metrics
latest_metrics = {}
latest_importances = []
latest_predictions = []

class UserInput(BaseModel):
    Name: str
    Gender: str
    Age: int
    Height: float
    Weight: float
    BMI: float
    Fitness_Goal: str
    Daily_Calories: int
    Daily_Protein: int
    Daily_Carbs: int
    Daily_Fat: int
    Daily_Fiber: int
    Daily_Budget: float
    Weekly_Budget: float
    Is_Vegetarian: bool
    Cuisine_Preference: str
    Meal_Type: str
    Max_Prep_Time: int
    Goal: str

@app.post("/predict")
def predict_meals(user_input: UserInput):
    if meals_df.empty:
        raise HTTPException(status_code=500, detail="Dataset not found")
        
    req_dict = user_input.dict()
    
    # 1. Generate target scores based on user inputs
    df = meals_df.copy()
    df['Suitability_Score'] = df.apply(lambda row: calculate_suitability_score(row, req_dict), axis=1)
    
    # 2. Train Random Forest dynamically
    try:
        model, features, top_features, metrics, actual_vs_predicted = preprocess_and_train(df, target_col='Suitability_Score')
        global latest_metrics, latest_importances, latest_predictions
        latest_metrics = metrics
        latest_importances = top_features
        latest_predictions = actual_vs_predicted
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model training failed: {str(e)}")
        
    # 3. Rank meals
    df_sorted = df.sort_values(by='Suitability_Score', ascending=False)
    
    # Get top 10 recommended
    top_meals = df_sorted.head(10).to_dict(orient="records")
    
    # 4. Generate Daily Plan (1 Breakfast, 1 Lunch, 1 Snack, 1 Dinner)
    def get_best_meal(m_type, used_ids):
        pool = df_sorted[(df_sorted['Meal_Type'] == m_type) & (~df_sorted['Meal_ID'].isin(used_ids))]
        if not pool.empty:
            return pool.iloc[0].to_dict()
        return None

    used = set()
    daily_plan = {}
    total_daily = {"Calories": 0, "Protein": 0, "Carbs": 0, "Fat": 0, "Fiber": 0, "Cost": 0}
    # Map response keys to CSV column names where they differ
    key_to_col = {"Carbs": "Carbohydrates"}
    
    for mt in ["Breakfast", "Lunch", "Snack", "Dinner"]:
        m = get_best_meal(mt, used)
        if m:
            used.add(m["Meal_ID"])
            daily_plan[mt] = m
            for k in total_daily.keys():
                col = key_to_col.get(k, k)
                total_daily[k] += m[col]

    # Generate Weekly Plan (Mocking by rotating top 20 suitable meals)
    weekly_plan = []
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekly_total = {"Calories": 0, "Protein": 0, "Cost": 0}
    
    for day in days:
        day_plan = {}
        day_totals = {"Calories": 0, "Protein": 0, "Cost": 0}
        for mt in ["Breakfast", "Lunch", "Snack", "Dinner"]:
            # Pick a somewhat random top suitable meal for variety
            pool = df_sorted[(df_sorted['Meal_Type'] == mt) & (df_sorted['Suitability_Score'] > 50)]
            if not pool.empty:
                m = pool.sample(n=1).iloc[0].to_dict()
                day_plan[mt] = m
                day_totals["Calories"] += m["Calories"]
                day_totals["Protein"] += m["Protein"]
                day_totals["Cost"] += m["Cost"]
                
        weekly_plan.append({
            "Day": day,
            "Meals": day_plan,
            "Totals": day_totals
        })
        for k in weekly_total.keys():
            weekly_total[k] += day_totals[k]

    # Save to users.json
    if req_dict.get("Name") and req_dict.get("Name") != "Demo User":
        try:
            users = []
            if os.path.exists(USERS_FILE):
                with open(USERS_FILE, "r") as f:
                    try:
                        users = json.load(f)
                    except json.JSONDecodeError:
                        pass
            
            # check if user already exists
            user_exists = next((u for u in users if u["Name"] == req_dict["Name"]), None)
            user_record = {
                "Name": req_dict["Name"],
                "Gender": req_dict["Gender"],
                "Age": req_dict["Age"],
                "BMI": req_dict["BMI"],
                "Fitness_Goal": req_dict["Fitness_Goal"],
                "Goal": req_dict["Goal"],
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Daily_Plan": daily_plan
            }
            if user_exists:
                # Update existing user
                user_exists.update(user_record)
            else:
                users.append(user_record)
                
            with open(USERS_FILE, "w") as f:
                json.dump(users, f, indent=4)
        except Exception as e:
            print(f"Failed to save user: {e}")

    return {
        "top_recommendations": top_meals,
        "daily_plan": daily_plan,
        "daily_totals": total_daily,
        "weekly_plan": weekly_plan,
        "weekly_totals": weekly_total
    }

@app.get("/meals")
def get_dataset(page: int = 1, limit: int = 20, search: str = ""):
    df = meals_df.copy()
    if search:
        df = df[df['Meal_Name'].str.contains(search, case=False) | df['Cuisine'].str.contains(search, case=False)]
    
    total = len(df)
    start = (page - 1) * limit
    end = start + limit
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": df.iloc[start:end].to_dict(orient="records")
    }

@app.get("/model-metrics")
def get_metrics():
    return {
        "metrics": latest_metrics,
        "feature_importances": latest_importances,
        "actual_vs_predicted": latest_predictions,
        "model_params": {
            "n_estimators": 100,
            "test_size": 0.2,
            "random_state": 42,
            "algorithm": "Random Forest Regressor",
            "criterion": "squared_error",
            "max_depth": "None (Auto)",
            "min_samples_split": 2,
            "min_samples_leaf": 1
        }
    }

@app.get("/users")
def get_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            try:
                users = json.load(f)
                return {"users": users}
            except json.JSONDecodeError:
                return {"users": []}
    return {"users": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
