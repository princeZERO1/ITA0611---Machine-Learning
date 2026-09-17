import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_csv("smart_agriculture_crop_yield_dataset.csv")

df["Season"] = df["Season"].map({
    "Kharif": 0,
    "Rabi": 1,
    "Zaid": 2
})

X = df.drop("Crop_Yield_ton_per_hectare", axis=1).values
y = df["Crop_Yield_ton_per_hectare"].values

scaler = StandardScaler()
X = scaler.fit_transform(X)

def locally_weighted_regression(X_train, y_train, X_test, tau=1.0):
    predictions = []

    for x in X_test:
        distances = np.sum((X_train - x) ** 2, axis=1)

        weights = np.exp(-distances / (2 * tau ** 2))

        X_bias = np.c_[np.ones(X_train.shape[0]), X_train]
        theta = np.linalg.pinv(
            X_bias.T @ np.diag(weights) @ X_bias
        ) @ (X_bias.T @ np.diag(weights) @ y_train)

        x_bias = np.r_[1, x]
        prediction = x_bias @ theta

        predictions.append(prediction)

    return np.array(predictions)

split = int(0.8 * len(X))

X_train = X[:split]
X_test = X[split:]
y_train = y[:split]
y_test = y[split:]

y_pred = locally_weighted_regression(
    X_train,
    y_train,
    X_test,
    tau=1.0
)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("SMART AGRICULTURE - CROP YIELD PREDICTION")
print("------------------------------------------")

print("Actual Yield     Predicted Yield")

for actual, predicted in zip(y_test, y_pred):
    print(f"{actual:.2f}            {predicted:.2f}")

print("\nMean Squared Error:", round(mse, 3))
print("Root Mean Squared Error:", round(rmse, 3))
print("R2 Score:", round(r2, 3))

plt.scatter(y_test, y_pred)

plt.xlabel("Actual Crop Yield")
plt.ylabel("Predicted Crop Yield")
plt.title("Locally Weighted Regression - Crop Yield Prediction")

plt.plot(
    [min(y_test), max(y_test)],
    [min(y_test), max(y_test)]
)

plt.show()
print("\nDATASET INFORMATION")
print("-------------------")
df.info()

df["Season"] = df["Season"].map({
    "Kharif": 0,
    "Rabi": 1,
    "Zaid": 2
})
# Example: Using loc to select specific columns by name
print("\nFirst 5 rows with Season and Crop_Yield:")
print(df.loc[:4, ["Season", "Crop_Yield_ton_per_hectare"]])

# Example: Using iloc to select rows/columns by position
print("\nFirst 5 rows (all columns) using iloc:")
print(df.iloc[:5, :])

# Example: Select a single value
print("\nValue at row 2, column 'Crop_Yield_ton_per_hectare':")
print(df.loc[2, "Crop_Yield_ton_per_hectare"])

# Replace NaN values in Season with a default category (e.g., 0 for Kharif)
df["Season"] = df["Season"].fillna(0)

# Or, if you want to use a string label instead of numbers:
df["Season"] = df["Season"].fillna("Unknown")

print("\nSeason Distribution After fillna:")
print(df["Season"].value_counts())


