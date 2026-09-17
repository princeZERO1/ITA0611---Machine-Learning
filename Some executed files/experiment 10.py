# Implementation of Expectation-Maximization (EM) Algorithm

import numpy as np

# Dataset
X = np.array([1, 2, 3, 8, 9, 10], dtype=float)

# Number of clusters
k = 2

# Initial parameters
means = np.array([2.0, 9.0])
variances = np.array([1.0, 1.0])
weights = np.array([0.5, 0.5])

# Number of iterations
iterations = 10


# Gaussian Probability Density Function
def gaussian_probability(x, mean, variance):
    return (
        1 / np.sqrt(2 * np.pi * variance)
        * np.exp(-((x - mean) ** 2) / (2 * variance))
    )


# EM Algorithm
for iteration in range(iterations):

    # -----------------------------------------
    # E-STEP: Calculate responsibilities
    # -----------------------------------------

    responsibilities = np.zeros((len(X), k))

    for i in range(len(X)):
        for j in range(k):

            responsibilities[i][j] = (
                weights[j]
                * gaussian_probability(
                    X[i],
                    means[j],
                    variances[j]
                )
            )

        # Normalize probabilities
        responsibilities[i] /= np.sum(responsibilities[i])


    # -----------------------------------------
    # M-STEP: Update parameters
    # -----------------------------------------

    N = np.sum(responsibilities, axis=0)

    # Update means
    for j in range(k):
        means[j] = np.sum(
            responsibilities[:, j] * X
        ) / N[j]

    # Update variances
    for j in range(k):
        variances[j] = np.sum(
            responsibilities[:, j]
            * (X - means[j]) ** 2
        ) / N[j]

    # Update mixture weights
    weights = N / len(X)


    # -----------------------------------------
    # Display iteration results
    # -----------------------------------------

    print("\nIteration:", iteration + 1)

    print("Means      :", means)
    print("Variances  :", variances)
    print("Weights    :", weights)


# -----------------------------------------
# Final Cluster Assignment
# -----------------------------------------

cluster_assignment = np.argmax(
    responsibilities,
    axis=1
)

print("\nFinal Cluster Assignment")
print("------------------------")

for i in range(len(X)):
    print(
        "Data:",
        X[i],
        "-> Cluster:",
        cluster_assignment[i] + 1
    )
