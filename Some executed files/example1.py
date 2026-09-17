import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error, r2_score
from scipy.linalg import pinv
 
data = fetch_california_housing(as_frame=True)
X = data.data[['MedInc', 'AveRooms']].values
y = data.target.values
 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
 
def locally_weighted_regression(X_train, y_train, x_query, tau=0.5):
    m = X_train.shape[0]
    X_b = np.c_[np.ones(m), X_train]
    x_q = np.r_[1, x_query]
    weights = np.exp(-np.sum((X_train - x_query) ** 2, axis=1) / (2 * tau ** 2))
    W = np.diag(weights)
    theta = pinv(X_b.T @ W @ X_b) @ X_b.T @ W @ y_train
    return x_q @ theta
 
lwr_preds = np.array([locally_weighted_regression(X_train, y_train, x, tau=0.5) for x in X_test[:50]])
lwr_rmse = mean_squared_error(y_test[:50], lwr_preds, squared=False)
lwr_r2 = r2_score(y_test[:50], lwr_preds)
 
def rbf_network_train(X_train, y_train, n_centers=15, sigma=1.0):
    kmeans = KMeans(n_clusters=n_centers, random_state=42, n_init=10).fit(X_train)
    centers = kmeans.cluster_centers_
    G_train = np.zeros((X_train.shape[0], centers.shape[0]))
    for i, c in enumerate(centers):
        G_train[:, i] = np.exp(-np.sum((X_train - c) ** 2, axis=1) / (2 * sigma ** 2))
    weights = pinv(G_train.T @ G_train) @ G_train.T @ y_train
    return centers, weights, sigma
 
def rbf_network_predict(X, centers, weights, sigma):
    G = np.zeros((X.shape[0], centers.shape[0]))
    for i, c in enumerate(centers):
        G[:, i] = np.exp(-np.sum((X - c) ** 2, axis=1) / (2 * sigma ** 2))
    return G @ weights
 
centers, weights, sigma = rbf_network_train(X_train, y_train, n_centers=15, sigma=1.0)
rbf_preds = rbf_network_predict(X_test, centers, weights, sigma)
rbf_rmse = mean_squared_error(y_test, rbf_preds, squared=False)
rbf_r2 = r2_score(y_test, rbf_preds)
 
print("LWR -> RMSE: {:.3f}, R2: {:.3f}".format(lwr_rmse, lwr_r2))
print("RBF -> RMSE: {:.3f}, R2: {:.3f}".format(rbf_rmse, rbf_r2))
