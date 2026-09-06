# Iris Flower Classification using KNN

import pandas as pd

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix


# Load Iris dataset
iris = load_iris()

X = iris.data
y = iris.target

# Display feature names
print("Features:")
print(iris.feature_names)

print("\nTarget Classes:")
print(iris.target_names)


# Split dataset into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Feature scaling
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# Create KNN classifier
k = 5

model = KNeighborsClassifier(n_neighbors=k)

# Train the model
model.fit(X_train, y_train)


# Predict test data
y_pred = model.predict(X_test)


# Display actual and predicted values
print("\nActual Values:")
print(y_test)

print("\nPredicted Values:")
print(y_pred)


# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", accuracy)


# Display confusion matrix
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# Predict a new Iris flower
# [Sepal Length, Sepal Width, Petal Length, Petal Width]

new_flower = [[5.1, 3.5, 1.4, 0.2]]

new_flower_scaled = scaler.transform(new_flower)

prediction = model.predict(new_flower_scaled)

print("\nNew Flower:")
print(new_flower)

print("\nPredicted Species:",
      iris.target_names[prediction[0]])
