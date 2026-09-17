# Comparison of Linear and Polynomial Regression using Python

import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score


# Dataset
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
    2,
    5,
    10,
    17,
    26,
    37,
    50,
    65,
    82,
    101
])


# -------------------------------------------------
# Linear Regression
# -------------------------------------------------

linear_model = LinearRegression()

linear_model.fit(X, y)

y_linear = linear_model.predict(X)


# -------------------------------------------------
# Polynomial Regression
# -------------------------------------------------

# Convert input into polynomial features
poly = PolynomialFeatures(degree=2)

X_poly = poly.fit_transform(X)

# Create and train polynomial regression model
poly_model = LinearRegression()

poly_model.fit(X_poly, y)

y_poly = poly_model.predict(X_poly)


# -------------------------------------------------
# Calculate Performance
# -------------------------------------------------

linear_mse = mean_squared_error(y, y_linear)
linear_r2 = r2_score(y, y_linear)

poly_mse = mean_squared_error(y, y_poly)
poly_r2 = r2_score(y, y_poly)


# -------------------------------------------------
# Display Results
# -------------------------------------------------

print("LINEAR REGRESSION")
print("-----------------")
print("Slope      :", linear_model.coef_[0])
print("Intercept  :", linear_model.intercept_)
print("MSE        :", linear_mse)
print("R2 Score   :", linear_r2)

print("\nPOLYNOMIAL REGRESSION")
print("--------------------")
print("Coefficients :", poly_model.coef_)
print("Intercept    :", poly_model.intercept_)
print("MSE          :", poly_mse)
print("R2 Score     :", poly_r2)


# -------------------------------------------------
# Compare Predictions
# -------------------------------------------------

print("\nActual and Predicted Values")
print("---------------------------------------------")
print("X\tActual\tLinear\tPolynomial")

for i in range(len(X)):
    print(
        f"{X[i][0]}\t"
        f"{y[i]}\t"
        f"{y_linear[i]:.2f}\t"
        f"{y_poly[i]:.2f}"
    )


# -------------------------------------------------
# Visualization
# -------------------------------------------------

X_plot = np.linspace(1, 10, 100).reshape(-1, 1)

# Linear prediction
y_linear_plot = linear_model.predict(X_plot)

# Polynomial prediction
X_plot_poly = poly.transform(X_plot)
y_poly_plot = poly_model.predict(X_plot_poly)


plt.scatter(X, y, label="Actual Data")

plt.plot(
    X_plot,
    y_linear_plot,
    label="Linear Regression"
)

plt.plot(
    X_plot,
    y_poly_plot,
    label="Polynomial Regression"
)

plt.xlabel("X")
plt.ylabel("Y")
plt.title("Linear vs Polynomial Regression")

plt.legend()
plt.grid()

plt.show()
