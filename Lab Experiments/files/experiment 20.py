# Future Sales Prediction using Linear Regression

import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# --------------------------------------------------
# 1. Create Historical Sales Dataset
# --------------------------------------------------

data = {
    "Month": np.arange(1, 13),

    "Sales": [
        120, 135, 150, 160,
        175, 190, 210, 225,
        240, 255, 275, 290
    ]
}

df = pd.DataFrame(data)

print("Historical Sales Data")
print("---------------------")
print(df)


# --------------------------------------------------
# 2. Prepare Input and Target
# --------------------------------------------------

X = df[["Month"]]
y = df["Sales"]


# --------------------------------------------------
# 3. Create Linear Regression Model
# --------------------------------------------------

model = LinearRegression()


# --------------------------------------------------
# 4. Train the Model
# --------------------------------------------------

model.fit(X, y)


# --------------------------------------------------
# 5. Predict Historical Sales
# --------------------------------------------------

y_pred = model.predict(X)


# --------------------------------------------------
# 6. Display Model Parameters
# --------------------------------------------------

print("\nLinear Regression Model")
print("-----------------------")

print("Slope     :", model.coef_[0])
print("Intercept :", model.intercept_)


# --------------------------------------------------
# 7. Evaluate Model
# --------------------------------------------------

mae = mean_absolute_error(y, y_pred)

mse = mean_squared_error(y, y_pred)

r2 = r2_score(y, y_pred)

print("\nModel Performance")
print("-----------------")

print("Mean Absolute Error :", round(mae, 2))
print("Mean Squared Error  :", round(mse, 2))
print("R2 Score            :", round(r2, 4))


# --------------------------------------------------
# 8. Predict Future Sales
# --------------------------------------------------

future_months = np.array([
    [13],
    [14],
    [15],
    [16],
    [17],
    [18]
])

future_sales = model.predict(future_months)


# --------------------------------------------------
# 9. Display Future Predictions
# --------------------------------------------------

print("\nFuture Sales Prediction")
print("-----------------------")

for i in range(len(future_months)):

    print(
        "Month",
        future_months[i][0],
        "-> Predicted Sales:",
        round(future_sales[i], 2)
    )
