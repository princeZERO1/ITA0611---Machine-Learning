# Implementation of Linear Regression (LR) Algorithm in Python

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Dataset
# X = Study Hours
# y = Marks

X = np.array([
    [1],
    [2],
    [3],
    [4],
    [5],
    [6],
    [7],
    [8],
    [9],
    [10]
])

y = np.array([
    35,
    40,
    45,
    50,
    55,
    60,
    65,
    70,
    75,
    80
])

# Split dataset into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create Linear Regression model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Predict test data
y_pred = model.predict(X_test)

# Display actual and predicted values
print("Actual Values    :", y_test)
print("Predicted Values :", y_pred)

# Display coefficient and intercept
print("\nSlope (Coefficient) :", model.coef_[0])
print("Intercept           :", model.intercept_)

# Calculate Mean Squared Error
mse = mean_squared_error(y_test, y_pred)

# Calculate R2 Score
r2 = r2_score(y_test, y_pred)

print("\nMean Squared Error :", mse)
print("R2 Score           :", r2)

# Predict marks for a new student
new_data = np.array([[7]])

prediction = model.predict(new_data)

print("\nStudy Hours :", new_data[0][0])
print("Predicted Marks :", prediction[0])
