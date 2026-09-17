import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ucimlrepo import fetch_ucirepo
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score


# ==========================================================
# 1. LOAD REAL UCI DATASET
# ==========================================================

dataset = fetch_ucirepo(id=294)

X = dataset.data.features
y = dataset.data.targets

print("Dataset loaded successfully")
print("Number of samples:", len(X))
print("Features:")
print(X.columns.tolist())
print("Target:")
print(y.columns.tolist())


# ==========================================================
# 2. SELECT ONE FEATURE FOR FUNCTION APPROXIMATION
# ==========================================================

data = pd.DataFrame()

data["AT"] = X["AT"]
data["PE"] = y["PE"]

data = data.sort_values("AT")

print("\nSelected data:")
print(data.head())


# ==========================================================
# 3. PREPARE DATA
# ==========================================================

X_data = data[["AT"]].values
y_data = data["PE"].values


X_train, X_test, y_train, y_test = train_test_split(
    X_data,
    y_data,
    test_size=0.20,
    random_state=42
)


# ==========================================================
# 4. STANDARDIZE INPUT
# ==========================================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# ==========================================================
# 5. LOCALLY WEIGHTED REGRESSION
# ==========================================================

def locally_weighted_regression(
    X_train,
    y_train,
    X_query,
    bandwidth=0.5
):

    predictions = []

    for xq in X_query:

        distances = np.sum(
            (X_train - xq) ** 2,
            axis=1
        )

        weights = np.exp(
            -distances / (2 * bandwidth ** 2)
        )

        X_design = np.column_stack(
            (
                np.ones(len(X_train)),
                X_train
            )
        )

        W = np.diag(weights)

        theta = np.linalg.pinv(
            X_design.T @ W @ X_design
        ) @ (
            X_design.T @ W @ y_train
        )

        x_design = np.array([1, xq[0]])

        prediction = x_design @ theta

        predictions.append(prediction)

    return np.array(predictions)


# ==========================================================
# 6. TRAIN / PREDICT USING LWR
# ==========================================================

lwr_predictions = locally_weighted_regression(
    X_train_scaled,
    y_train,
    X_test_scaled,
    bandwidth=0.5
)


# ==========================================================
# 7. RADIAL BASIS FUNCTION NETWORK
# ==========================================================

number_of_centers = 25

kmeans = KMeans(
    n_clusters=number_of_centers,
    random_state=42,
    n_init=10
)

kmeans.fit(X_train_scaled)

centers = kmeans.cluster_centers_


# ==========================================================
# 8. CALCULATE RBF FEATURES
# ==========================================================

def rbf_transform(X, centers, sigma):

    distances = np.sum(
        (X[:, np.newaxis, :] - centers[np.newaxis, :, :]) ** 2,
        axis=2
    )

    R = np.exp(
        -distances / (2 * sigma ** 2)
    )

    return R


sigma = 0.5

R_train = rbf_transform(
    X_train_scaled,
    centers,
    sigma
)

R_test = rbf_transform(
    X_test_scaled,
    centers,
    sigma
)


# ==========================================================
# 9. TRAIN OUTPUT LAYER
# ==========================================================

rbf_model = Ridge(alpha=0.001)

rbf_model.fit(
    R_train,
    y_train
)


# ==========================================================
# 10. RBF PREDICTION
# ==========================================================

rbf_predictions = rbf_model.predict(
    R_test
)


# ==========================================================
# 11. PERFORMANCE COMPARISON
# ==========================================================

lwr_mse = mean_squared_error(
    y_test,
    lwr_predictions
)

rbf_mse = mean_squared_error(
    y_test,
    rbf_predictions
)

lwr_rmse = np.sqrt(lwr_mse)
rbf_rmse = np.sqrt(rbf_mse)

lwr_r2 = r2_score(
    y_test,
    lwr_predictions
)

rbf_r2 = r2_score(
    y_test,
    rbf_predictions
)


print("\n================================")
print("MODEL COMPARISON")
print("================================")

print("\nLocally Weighted Regression")
print("RMSE:", lwr_rmse)
print("R2 Score:", lwr_r2)

print("\nRadial Basis Function Network")
print("RMSE:", rbf_rmse)
print("R2 Score:", rbf_r2)


# ==========================================================
# 12. CREATE SMOOTH CURVES FOR VISUALIZATION
# ==========================================================

x_min = X_train_scaled.min()
x_max = X_train_scaled.max()

X_curve = np.linspace(
    x_min,
    x_max,
    300
).reshape(-1, 1)


lwr_curve = locally_weighted_regression(
    X_train_scaled,
    y_train,
    X_curve,
    bandwidth=0.5
)


R_curve = rbf_transform(
    X_curve,
    centers,
    sigma
)

rbf_curve = rbf_model.predict(
    R_curve
)


# Convert X back to original temperature scale

X_curve_original = scaler.inverse_transform(
    X_curve
)


# ==========================================================
# 13. PLOT LWR
# ==========================================================

plt.figure(figsize=(10, 6))

plt.scatter(
    X_train,
    y_train,
    s=10,
    alpha=0.3,
    label="Training Data"
)

plt.plot(
    X_curve_original,
    lwr_curve,
    linewidth=2,
    label="LWR"
)

plt.xlabel("Ambient Temperature (°C)")
plt.ylabel("Electrical Energy Output (MW)")
plt.title("Locally Weighted Regression")
plt.legend()
plt.grid(True)

plt.show()


# ==========================================================
# 14. PLOT RBF
# ==========================================================

plt.figure(figsize=(10, 6))

plt.scatter(
    X_train,
    y_train,
    s=10,
    alpha=0.3,
    label="Training Data"
)

plt.plot(
    X_curve_original,
    rbf_curve,
    linewidth=2,
    label="RBF Network"
)

plt.xlabel("Ambient Temperature (°C)")
plt.ylabel("Electrical Energy Output (MW)")
plt.title("Radial Basis Function Network")
plt.legend()
plt.grid(True)

plt.show()


# ==========================================================
# 15. FINAL COMPARISON GRAPH
# ==========================================================

plt.figure(figsize=(10, 6))

plt.scatter(
    X_train,
    y_train,
    s=8,
    alpha=0.2,
    label="Training Data"
)

plt.plot(
    X_curve_original,
    lwr_curve,
    linewidth=2,
    label="LWR"
)

plt.plot(
    X_curve_original,
    rbf_curve,
    linewidth=2,
    label="RBF Network"
)

plt.xlabel("Ambient Temperature (°C)")
plt.ylabel("Electrical Energy Output (MW)")

plt.title(
    "Comparison of LWR and RBF Function Approximation"
)

plt.legend()
plt.grid(True)

plt.show()
