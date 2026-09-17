"""
Program 4: Artificial Neural Network using Backpropagation
----------------------------------------------------------
Builds and trains an Artificial Neural Network (ANN)
using the Backpropagation algorithm on the Iris dataset.
"""

import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay

# -----------------------------
# Load Dataset
# -----------------------------
iris = load_iris()

X = iris.data
y = iris.target

# -----------------------------
# Split Dataset
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.30,
    random_state=42
)

# -----------------------------
# Feature Scaling
# -----------------------------
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# -----------------------------
# Build ANN using Backpropagation
# -----------------------------
ann = MLPClassifier(
    hidden_layer_sizes=(10,),
    activation='logistic',
    solver='sgd',
    learning_rate_init=0.1,
    max_iter=500,
    random_state=42
)

# Train the network
ann.fit(X_train, y_train)

# -----------------------------
# Prediction
# -----------------------------
y_pred = ann.predict(X_test)

# -----------------------------
# Accuracy
# -----------------------------
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy :", accuracy * 100, "%")

# -----------------------------
# Sample Prediction
# -----------------------------
sample = [X_test[0]]

prediction = ann.predict(sample)

print("\nPredicted Class :", iris.target_names[prediction[0]])

print("Actual Class    :", iris.target_names[y_test[0]])

# -----------------------------
# Graph 1 : Loss Curve
# -----------------------------

plt.figure(figsize=(7,5))

plt.plot(ann.loss_curve_, linewidth=2)

plt.title("Training Loss Curve")
plt.xlabel("Iterations")
plt.ylabel("Loss")

plt.grid(True)

plt.show()

# -----------------------------
# Graph 2 : Confusion Matrix
# -----------------------------
cm = confusion_matrix(y_test, y_pred)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=iris.target_names
)

disp.plot()

plt.title("Confusion Matrix")

plt.show()

# -----------------------------
# Graph 3 : Actual vs Predicted
# -----------------------------
plt.figure(figsize=(8,5))

plt.plot(y_test, 'bo-', label="Actual")

plt.plot(y_pred, 'r*-', label="Predicted")

plt.title("Actual vs Predicted")

plt.xlabel("Sample Number")

plt.ylabel("Class")

plt.legend()

plt.grid(True)

plt.show()
