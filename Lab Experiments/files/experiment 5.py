# Implementation of K-Nearest Neighbours (K-NN) in Python

import numpy as np
from collections import Counter

# Training data
X_train = np.array([
    [1, 2],
    [2, 3],
    [3, 3],
    [6, 7],
    [7, 8],
    [8, 7]
])

# Class labels
y_train = np.array([
    'A',
    'A',
    'A',
    'B',
    'B',
    'B'
])

# Test data
X_test = np.array([
    [4, 4],
    [7, 7]
])

# Value of K
k = 3


# Function to calculate Euclidean distance
def euclidean_distance(x1, x2):
    return np.sqrt(np.sum((x1 - x2) ** 2))


# K-NN prediction function
def knn_predict(X_train, y_train, x_test, k):

    distances = []

    # Calculate distance from test point
    # to every training point
    for i in range(len(X_train)):
        distance = euclidean_distance(X_train[i], x_test)
        distances.append((distance, y_train[i]))

    # Sort according to distance
    distances.sort(key=lambda x: x[0])

    # Select K nearest neighbours
    nearest_neighbours = distances[:k]

    # Get the class labels
    labels = [label for distance, label in nearest_neighbours]

    # Majority voting
    prediction = Counter(labels).most_common(1)[0][0]

    return prediction


# Predict the class for each test point
print("K-Nearest Neighbours Classification")
print("-----------------------------------")

for test_point in X_test:

    prediction = knn_predict(
        X_train,
        y_train,
        test_point,
        k
    )

    print("Test Point:", test_point)
    print("Predicted Class:", prediction)
    print()
