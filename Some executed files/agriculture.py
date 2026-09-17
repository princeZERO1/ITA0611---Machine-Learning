import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load dataset
df = pd.read_csv("smart_agriculture_crop_yield_dataset.csv")

# Input and output
X = df.drop("Crop_Yield_ton_per_hectare", axis=1)
y = df["Crop_Yield_ton_per_hectare"]

# Columns
categorical = ["Season"]
numerical = [c for c in X.columns if c != "Season"]

# Preprocessing
preprocessor = ColumnTransformer([
    ("num", StandardScaler(), numerical),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical)
])

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

# Transform data
X_train = preprocessor.fit_transform(X_train)
X_test = preprocessor.transform(X_test)

# Convert to NumPy array if necessary
X_train = np.asarray(X_train)
X_test = np.asarray(X_test)

# Locally Weighted Regression
def lwr_predict(X_train, y_train, X_test, tau=3):

    predictions = []

    for x in X_test:

        # Calculate distance
        distance = np.sum((X_train - x) ** 2, axis=1)

        # Gaussian weights
        weights = np.exp(-distance / (2 * tau ** 2))

        # Add intercept
        A = np.column_stack((np.ones(len(X_train)), X_train))

        W = np.diag(weights)

        # Weighted regression
        beta = np.linalg.solve(
            A.T @ W @ A + 0.001 * np.eye(A.shape[1]),
            A.T @ W @ y_train.values
        )

        # Prediction
        x_new = np.insert(x, 0, 1)

        predictions.append(x_new @ beta)

    return np.array(predictions)


# Prediction
y_pred = lwr_predict(X_train, y_train, X_test)

# Evaluation
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\nCrop Yield Prediction using LWR")
print("--------------------------------")
print("MAE  :", round(mae, 2))
print("RMSE :", round(rmse, 2))
print("R2   :", round(r2, 3))

# Actual vs predicted
result = pd.DataFrame({
    "Actual Yield": y_test.values,
    "Predicted Yield": y_pred
})

print("\nActual vs Predicted:")
print(result.round(2))
