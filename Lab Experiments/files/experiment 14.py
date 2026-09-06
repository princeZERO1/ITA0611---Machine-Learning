# House Price Prediction using Linear Regression

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# Create sample house dataset
data = {
    "Area_sqft": [
        800, 1000, 1200, 1400, 1600,
        1800, 2000, 2200, 2400, 2600,
        2800, 3000, 1500, 1900, 2500
    ],

    "Bedrooms": [
        2, 2, 3, 3, 3,
        3, 4, 4, 4, 4,
        5, 5, 3, 4, 4
    ],

    "Bathrooms": [
        1, 2, 2, 2, 3,
        3, 3, 3, 4, 4,
        4, 5, 2, 3, 4
    ],

    "Age": [
        20, 15, 12, 10, 8,
        6, 5, 4, 3, 2,
        1, 1, 10, 7, 3
    ],

    "Parking": [
        0, 1, 1, 1, 2,
        2, 2, 2, 2, 2,
        3, 3, 1, 2, 2
    ],

    # House price in lakhs
    "Price": [
        35, 45, 55, 65, 75,
        85, 100, 115, 130, 145,
        160, 175, 70, 95, 135
    ]
}


# Convert data into DataFrame
df = pd.DataFrame(data)

print("House Price Dataset")
print("-------------------")
print(df)


# Select input features
X = df[
    [
        "Area_sqft",
        "Bedrooms",
        "Bathrooms",
        "Age",
        "Parking"
    ]
]

# Select target variable
y = df["Price"]


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


# Predict house prices
y_pred = model.predict(X_test)


# Display actual and predicted values
print("\nActual House Prices:")
print(y_test.values)

print("\nPredicted House Prices:")
print(y_pred)


# Calculate performance metrics
mae = mean_absolute_error(y_test, y_pred)

mse = mean_squared_error(y_test, y_pred)

r2 = r2_score(y_test, y_pred)


print("\nModel Performance")
print("-----------------")
print("Mean Absolute Error :", mae)
print("Mean Squared Error  :", mse)
print("R2 Score            :", r2)


# Predict price of a new house
new_house = pd.DataFrame({
    "Area_sqft": [1800],
    "Bedrooms": [3],
    "Bathrooms": [3],
    "Age": [5],
    "Parking": [2]
})


predicted_price = model.predict(new_house)


print("\nNew House Details")
print("-----------------")
print(new_house)

print(
    "\nPredicted House Price: ₹",
    round(predicted_price[0], 2),
    "lakhs"
)
