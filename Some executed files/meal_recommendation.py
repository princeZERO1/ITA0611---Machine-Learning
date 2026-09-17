import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier


DATASET = "meal_dataset.csv"


def load_dataset():

    if not os.path.exists(DATASET):
        print("ERROR: meal_dataset.csv not found!")
        print("Keep the CSV file in the same folder as this Python file.")
        exit()

    df = pd.read_csv(DATASET)

    print("\nDataset loaded successfully!")
    print("Total meals:", len(df))

    return df


def get_input():

    print("\n==============================================")
    print("     AI-DRIVEN MEAL RECOMMENDATION SYSTEM")
    print("==============================================")

    calories = float(
        input("\nEnter daily calorie requirement (kcal): ")
    )

    protein = float(
        input("Enter daily protein requirement (g): ")
    )

    carbs = float(
        input("Enter daily carbohydrate requirement (g): ")
    )

    fat = float(
        input("Enter daily fat requirement (g): ")
    )

    budget = float(
        input("Enter daily food budget (Rs): ")
    )

    print("\nSelect your goal")
    print("1. Weight Loss")
    print("2. Healthy Maintenance")
    print("3. Weight Gain")

    goal_choice = input("Enter choice: ")

    if goal_choice == "1":
        goal = "Weight Loss"
    elif goal_choice == "2":
        goal = "Healthy Maintenance"
    else:
        goal = "Weight Gain"

    print("\nSelect meal category")
    print("1. Breakfast")
    print("2. Lunch")
    print("3. Snack")
    print("4. Dinner")
    print("5. All")

    category_choice = input("Enter choice: ")

    categories = {
        "1": "Breakfast",
        "2": "Lunch",
        "3": "Snack",
        "4": "Dinner",
        "5": "All"
    }

    category = categories.get(category_choice, "All")

    return {
        "Calories": calories,
        "Protein": protein,
        "Carbs": carbs,
        "Fat": fat,
        "Budget": budget,
        "Goal": goal,
        "Category": category
    }


def prepare_knn(df):

    features = [
        "Calories",
        "Protein_g",
        "Carbs_g",
        "Fat_g",
        "Cost_Rs"
    ]

    scaler = StandardScaler()

    data_scaled = scaler.fit_transform(
        df[features]
    )

    knn = NearestNeighbors(
        n_neighbors=min(5, len(df)),
        metric="euclidean"
    )

    knn.fit(data_scaled)

    return knn, scaler, features


def get_knn_recommendations(
    df,
    knn,
    scaler,
    features,
    user
):

    target = np.array([[
        user["Calories"],
        user["Protein"],
        user["Carbs"],
        user["Fat"],
        user["Budget"]
    ]])

    target_scaled = scaler.transform(target)

    distances, indexes = knn.kneighbors(
        target_scaled
    )

    recommendations = df.iloc[
        indexes[0]
    ].copy()

    recommendations["Distance"] = distances[0]

    return recommendations


def create_random_forest(df):

    X = []
    y = []

    for _, meal in df.iterrows():

        for _ in range(10):

            calorie_target = np.random.uniform(
                meal["Calories"] * 0.8,
                meal["Calories"] * 1.2
            )

            protein_target = np.random.uniform(
                meal["Protein_g"] * 0.8,
                meal["Protein_g"] * 1.2
            )

            carbs_target = np.random.uniform(
                meal["Carbs_g"] * 0.8,
                meal["Carbs_g"] * 1.2
            )

            fat_target = np.random.uniform(
                meal["Fat_g"] * 0.8,
                meal["Fat_g"] * 1.2
            )

            budget_target = np.random.uniform(
                meal["Cost_Rs"] * 0.8,
                meal["Cost_Rs"] * 1.5
            )

            calorie_difference = abs(
                meal["Calories"] - calorie_target
            ) / calorie_target

            protein_difference = abs(
                meal["Protein_g"] - protein_target
            ) / protein_target

            carbs_difference = abs(
                meal["Carbs_g"] - carbs_target
            ) / carbs_target

            fat_difference = abs(
                meal["Fat_g"] - fat_target
            ) / fat_target

            budget_difference = max(
                0,
                meal["Cost_Rs"] - budget_target
            ) / budget_target

            score = (
                calorie_difference +
                protein_difference +
                carbs_difference +
                fat_difference +
                budget_difference
            )

            if score < 0.8:
                label = 1
            else:
                label = 0

            X.append([
                calorie_target,
                protein_target,
                carbs_target,
                fat_target,
                budget_target,
                meal["Calories"],
                meal["Protein_g"],
                meal["Carbs_g"],
                meal["Fat_g"],
                meal["Cost_Rs"]
            ])

            y.append(label)

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    return model


def calculate_scores(
    recommendations,
    model,
    user
):

    scores = []

    for _, meal in recommendations.iterrows():

        input_data = [[
            user["Calories"],
            user["Protein"],
            user["Carbs"],
            user["Fat"],
            user["Budget"],
            meal["Calories"],
            meal["Protein_g"],
            meal["Carbs_g"],
            meal["Fat_g"],
            meal["Cost_Rs"]
        ]]

        probability = model.predict_proba(
            input_data
        )[0][1]

        rf_score = probability * 100

        distance_score = (
            100 / (1 + meal["Distance"])
        )

        final_score = (
            0.7 * rf_score +
            0.3 * distance_score
        )

        scores.append(final_score)

    recommendations[
        "AI_Score"
    ] = scores

    recommendations = recommendations.sort_values(
        "AI_Score",
        ascending=False
    )

    return recommendations


def display_results(
    recommendations,
    user
):

    print("\n")
    print("=" * 65)
    print("              AI RECOMMENDATIONS")
    print("=" * 65)

    for i, (_, meal) in enumerate(
        recommendations.iterrows(),
        start=1
    ):

        print(f"\n{i}. {meal['Meal']}")

        print(
            f"   Category   : {meal['Category']}"
        )

        print(
            f"   Calories   : {meal['Calories']:.0f} kcal"
        )

        print(
            f"   Protein    : {meal['Protein_g']:.0f} g"
        )

        print(
            f"   Carbs      : {meal['Carbs_g']:.0f} g"
        )

        print(
            f"   Fat        : {meal['Fat_g']:.0f} g"
        )

        print(
            f"   Cost       : Rs.{meal['Cost_Rs']:.0f}"
        )

        print(
            f"   AI Score   : {meal['AI_Score']:.1f}/100"
        )

    best = recommendations.iloc[0]

    print("\n")
    print("=" * 65)
    print("              BEST RECOMMENDATION")
    print("=" * 65)

    print(
        f"\nMeal          : {best['Meal']}"
    )

    print(
        f"Calories      : {best['Calories']:.0f} kcal"
    )

    print(
        f"Protein       : {best['Protein_g']:.0f} g"
    )

    print(
        f"Carbohydrates : {best['Carbs_g']:.0f} g"
    )

    print(
        f"Fat           : {best['Fat_g']:.0f} g"
    )

    print(
        f"Cost          : Rs.{best['Cost_Rs']:.0f}"
    )

    print(
        f"AI Score      : {best['AI_Score']:.1f}/100"
    )

    if best["Cost_Rs"] <= user["Budget"]:

        print("Budget Status : WITHIN BUDGET")

    else:

        print("Budget Status : ABOVE BUDGET")

    return best


def nutrition_bar_chart(
    best,
    user
):

    labels = [
        "Calories",
        "Protein",
        "Carbs",
        "Fat"
    ]

    target = [
        user["Calories"],
        user["Protein"],
        user["Carbs"],
        user["Fat"]
    ]

    recommended = [
        best["Calories"],
        best["Protein_g"],
        best["Carbs_g"],
        best["Fat_g"]
    ]

    x = np.arange(len(labels))

    width = 0.35

    plt.figure(figsize=(10, 6))

    plt.bar(
        x - width / 2,
        target,
        width,
        label="User Requirement"
    )

    plt.bar(
        x + width / 2,
        recommended,
        width,
        label="Recommended Meal"
    )

    plt.xticks(x, labels)

    plt.ylabel("Amount")

    plt.title(
        "Nutrition Requirement vs Recommended Meal"
    )

    plt.legend()

    plt.tight_layout()

    plt.show()


def macro_pie_chart(best):

    protein = best["Protein_g"] * 4
    carbs = best["Carbs_g"] * 4
    fat = best["Fat_g"] * 9

    values = [
        protein,
        carbs,
        fat
    ]

    labels = [
        "Protein",
        "Carbohydrates",
        "Fat"
    ]

    plt.figure(figsize=(7, 7))

    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title(
        "Macronutrient Distribution"
    )

    plt.tight_layout()

    plt.show()


def cost_bar_chart(
    recommendations
):

    plt.figure(figsize=(10, 6))

    plt.bar(
        recommendations["Meal"],
        recommendations["Cost_Rs"]
    )

    plt.xlabel("Meal")

    plt.ylabel("Cost (Rs)")

    plt.title(
        "Cost Comparison of Recommended Meals"
    )

    plt.xticks(
        rotation=25,
        ha="right"
    )

    plt.tight_layout()

    plt.show()


def budget_pie_chart(
    best,
    budget
):

    spent = best["Cost_Rs"]

    remaining = max(
        0,
        budget - spent
    )

    plt.figure(figsize=(7, 7))

    plt.pie(
        [spent, remaining],
        labels=[
            "Spent",
            "Remaining"
        ],
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title(
        f"Budget Usage - Rs.{budget:.0f}"
    )

    plt.tight_layout()

    plt.show()


def score_bar_chart(
    recommendations
):

    plt.figure(figsize=(10, 6))

    plt.bar(
        recommendations["Meal"],
        recommendations["AI_Score"]
    )

    plt.xlabel("Meal")

    plt.ylabel("AI Score")

    plt.title(
        "AI Meal Recommendation Score"
    )

    plt.ylim(0, 100)

    plt.xticks(
        rotation=25,
        ha="right"
    )

    plt.tight_layout()

    plt.show()


def main():

    df = load_dataset()

    user = get_input()

    print("\nTraining Random Forest...")

    random_forest = create_random_forest(df)

    print("Random Forest training completed.")

    print("\nPreparing KNN model...")

    knn, scaler, features = prepare_knn(df)

    print("KNN model ready.")

    recommendations = get_knn_recommendations(
        df,
        knn,
        scaler,
        features,
        user
    )

    # Filter category after finding neighbors.
    if user["Category"] != "All":

        filtered = recommendations[
            recommendations["Category"]
            == user["Category"]
        ]

        if len(filtered) > 0:

            recommendations = filtered

    recommendations = calculate_scores(
        recommendations,
        random_forest,
        user
    )

    best = display_results(
        recommendations,
        user
    )

    print("\nGenerating graphs...")

    nutrition_bar_chart(
        best,
        user
    )

    macro_pie_chart(
        best
    )

    cost_bar_chart(
        recommendations
    )

    budget_pie_chart(
        best,
        user["Budget"]
    )

    score_bar_chart(
        recommendations
    )

    print("\n==============================================")
    print("              DEMO COMPLETED")
    print("==============================================")


if __name__ == "__main__":
    main()
