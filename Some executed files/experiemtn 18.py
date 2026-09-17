# Perceptron Based IRIS Classification

import numpy as np

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score, confusion_matrix


# --------------------------------------------------
# 1. Load Iris Dataset
# --------------------------------------------------

iris = load_iris()

X = iris.data
y = iris.target

print("IRIS Flower Classification")
print("--------------------------")

print("Features:")
print(iris.feature_names)

print("\nClasses:")
print(iris.target_names)


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

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# --------------------------------------------------
# 4. Create Perceptron Model
# --------------------------------------------------

model = Perceptron(
    max_iter=1000,
    eta0=0.1,
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


print("\nActual Values:")
print(y_test)

print("\nPredicted Values:")
print(y_pred)


# --------------------------------------------------
# 7. Calculate Accuracy
# --------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", accuracy)


# --------------------------------------------------
# 8. Display Confusion Matrix
# --------------------------------------------------

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# --------------------------------------------------
# 9. Predict a New Iris Flower
# --------------------------------------------------

# Features:
# Sepal Length, Sepal Width,
# Petal Length, Petal Width

new_flower = np.array([
    [5.1, 3.5, 1.4, 0.2]
])

# Scale new data
new_flower_scaled = scaler.transform(new_flower)

# Predict class
prediction = model.predict(new_flower_scaled)

print("\nNew Flower:")
print(new_flower)

print(
    "\nPredicted Species:",
    iris.target_names[prediction[0]]
)
