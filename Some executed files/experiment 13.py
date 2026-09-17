# Car Price Prediction using Linear Regression

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# Create car dataset
data = {
    "Year": [2015, 2016, 2017, 2018, 2019,
             2020, 2021, 2017, 2018, 2019,
             2020, 2021, 2016, 2018, 2022],

    "Kilometers_Driven": [
        80000, 70000, 60000, 50000, 40000,
        30000, 20000, 65000, 55000, 45000,
        35000, 25000, 75000, 52000, 15000
    ],

    "Engine_CC": [
        1200, 1500, 1600, 1800, 1200,
        1500, 1600, 1400, 1800, 1500,
        1600, 2000, 1200, 1500, 2000
    ],

    "Mileage": [
        18, 17, 16, 15, 19,
        18, 17, 20, 15, 18,
        17, 14, 19, 18, 14
    ],

    "Price": [
        450000, 500000, 550000, 650000, 700000,
        800000, 900000, 520000, 620000, 750000,
        820000, 950000, 480000, 680000, 1100000
    ]
}


# Convert dataset into DataFrame
df = pd.DataFrame(data)

print("Car Price Dataset")
print("-----------------")
print(df)


# Separate input features and target
X = df[
    [
        "Year",
        "Kilometers_Driven",
        "Engine_CC",
        "Mileage"
    ]
]

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


# Predict prices for test data
y_pred = model.predict(X_test)


# Display actual and predicted prices
print("\nActual Prices:")
print(y_test.values)

print("\nPredicted Prices:")
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


# Predict price for a new car
new_car = pd.DataFrame({
    "Year": [2021],
    "Kilometers_Driven": [30000],
    "Engine_CC": [1500],
    "Mileage": [18]
})


predicted_price = model.predict(new_car)


print("\nNew Car Details")
print("----------------")
print(new_car)

print("\nPredicted Car Price: ₹",
      round(predicted_price[0], 2))
