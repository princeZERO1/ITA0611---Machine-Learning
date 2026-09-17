# Comparison of Classification Algorithms
# Using Iris Dataset

import pandas as pd

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


# --------------------------------------------------
# 1. Load Iris Dataset
# --------------------------------------------------

iris = load_iris()

X = iris.data
y = iris.target

print("Iris Dataset")
print("-------------")

print("Number of Samples:", X.shape[0])
print("Number of Features:", X.shape[1])
print("Classes:", iris.target_names)


# --------------------------------------------------
# 2. Split Dataset
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# --------------------------------------------------
# 3. Feature Scaling
# --------------------------------------------------

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# --------------------------------------------------
# 4. Create Classification Models
# --------------------------------------------------

models = {

    "Logistic Regression":
        LogisticRegression(max_iter=200),

    "KNN":
        KNeighborsClassifier(n_neighbors=5),

    "Decision Tree":
        DecisionTreeClassifier(random_state=42),

    "SVM":
        SVC(),

    "Random Forest":
        RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )
}


# --------------------------------------------------
# 5. Train and Evaluate Models
# --------------------------------------------------

results = []

print("\nClassification Results")
print("=" * 70)

for name, model in models.items():

    # Train model
    model.fit(X_train_scaled, y_train)

    # Predict test data
    y_pred = model.predict(X_test_scaled)

    # Calculate performance metrics
    accuracy = accuracy_score(y_test, y_pred)

    precision = precision_score(
        y_test,
        y_pred,
        average="weighted"
    )

    recall = recall_score(
        y_test,
        y_pred,
        average="weighted"
    )

    f1 = f1_score(
        y_test,
        y_pred,
        average="weighted"
    )

    # Store results
    results.append([
        name,
        accuracy,
        precision,
        recall,
        f1
    ])

    # Display results
    print("\nAlgorithm:", name)
    print("Accuracy :", round(accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall   :", round(recall, 4))
    print("F1 Score :", round(f1, 4))


# --------------------------------------------------
# 6. Results Comparison Table
# --------------------------------------------------

results_df = pd.DataFrame(
    results,
    columns=[
        "Algorithm",
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score"
    ]
)

print("\n\nFinal Comparison")
print("=" * 70)

print(results_df.to_string(index=False))


# --------------------------------------------------
# 7. Find Best Algorithm
# --------------------------------------------------

best_model = results_df.loc[
    results_df["Accuracy"].idxmax()
]

print("\nBest Performing Algorithm:")
print(best_model["Algorithm"])

print(
    "Best Accuracy:",
    round(best_model["Accuracy"], 4)
)


# --------------------------------------------------
# 8. Confusion Matrix for Best Model
# --------------------------------------------------

best_name = best_model["Algorithm"]

best_classifier = models[best_name]

best_predictions = best_classifier.predict(
    X_test_scaled
)

cm = confusion_matrix(
    y_test,
    best_predictions
)

print("\nConfusion Matrix of Best Model:")
print(cm)
