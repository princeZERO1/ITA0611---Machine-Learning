# Mobile Price Prediction using Random Forest Classifier

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix


# --------------------------------------------------
# 1. Create Mobile Dataset
# --------------------------------------------------

data = {
    "RAM": [2, 2, 3, 3, 4, 4, 6, 6, 8, 8,
            12, 12, 4, 6, 8],

    "Storage": [32, 64, 32, 64, 64, 128, 128, 256, 128, 256,
                256, 512, 128, 256, 512],

    "Battery": [3000, 3500, 4000, 4500, 4000, 4500, 5000, 5000,
                4500, 5000, 5000, 6000, 4500, 5000, 5500],

    "Camera": [8, 12, 12, 16, 16, 20, 24, 32, 32, 48,
               48, 64, 20, 32, 64],

    "Screen_Size": [5.0, 5.5, 5.5, 6.0, 6.0, 6.2, 6.4, 6.5,
                    6.5, 6.7, 6.7, 6.8, 6.3, 6.5, 6.8],

    # Price Range:
    # 0 = Low
    # 1 = Medium
    # 2 = High
    # 3 = Very High

    "Price_Range": [
        0, 0, 0, 1, 1,
        1, 2, 2, 2, 3,
        3, 3, 1, 2, 3
    ]
}


# Convert data into DataFrame
df = pd.DataFrame(data)

print("Mobile Price Dataset")
print("--------------------")
print(df)


# --------------------------------------------------
# 2. Separate Features and Target
# --------------------------------------------------

X = df[
    [
        "RAM",
        "Storage",
        "Battery",
        "Camera",
        "Screen_Size"
    ]
]

y = df["Price_Range"]


# --------------------------------------------------
# 3. Split Dataset
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# --------------------------------------------------
# 4. Create Random Forest Classifier
# --------------------------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# --------------------------------------------------
# 5. Train the Model
# --------------------------------------------------

model.fit(X_train, y_train)


# --------------------------------------------------
# 6. Predict Test Data
# --------------------------------------------------

y_pred = model.predict(X_test)


print("\nActual Price Ranges:")
print(y_test.values)

print("\nPredicted Price Ranges:")
print(y_pred)


# --------------------------------------------------
# 7. Calculate Accuracy
# --------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy)


# --------------------------------------------------
# 8. Display Confusion Matrix
# --------------------------------------------------

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# --------------------------------------------------
# 9. Predict Price Range of a New Mobile
# --------------------------------------------------

new_mobile = pd.DataFrame({
    "RAM": [8],
    "Storage": [256],
    "Battery": [5000],
    "Camera": [48],
    "Screen_Size": [6.5]
})


prediction = model.predict(new_mobile)


# Convert numerical class into price range
price_ranges = {
    0: "Low",
    1: "Medium",
    2: "High",
    3: "Very High"
}


print("\nNew Mobile Details")
print("------------------")
print(new_mobile)

print(
    "\nPredicted Mobile Price Range:",
    price_ranges[prediction[0]]
)
