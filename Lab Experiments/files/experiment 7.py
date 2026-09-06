# Implementation of Logistic Regression (LR) in Python

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

# Dataset
X = np.array([
    [1, 20],
    [2, 25],
    [3, 30],
    [4, 35],
    [5, 40],
    [6, 45],
    [7, 50],
    [8, 55],
    [9, 60],
    [10, 65]
])

# Target values
# 0 = Fail
# 1 = Pass
y = np.array([
    0, 0, 0, 0, 1,
    1, 1, 1, 1, 1
])

# Split the dataset into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create Logistic Regression model
model = LogisticRegression()

# Train the model
model.fit(X_train, y_train)

# Predict the test data
y_pred = model.predict(X_test)

# Display predictions
print("Actual Values    :", y_test)
print("Predicted Values :", y_pred)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy :", accuracy)

# Display confusion matrix
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Predict a new data point
new_data = np.array([[7, 52]])

prediction = model.predict(new_data)

if prediction[0] == 1:
    print("\nNew Data: Pass")
else:
    print("\nNew Data: Fail")
