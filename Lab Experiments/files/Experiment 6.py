"""
Naive Bayes Classification
Student Performance Prediction (Pass/Fail)
"""

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import classification_report

# -------------------------------
# Load Dataset
# -------------------------------

data = pd.read_csv("student.csv")

print("Student Dataset\n")
print(data)

# -------------------------------
# Features and Target
# -------------------------------

X = data[["StudyHours",
          "Attendance",
          "Assignments",
          "InternalMarks"]]

y = data["Result"]

# -------------------------------
# Train-Test Split
# -------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42
)

# -------------------------------
# Create Naive Bayes Model
# -------------------------------

model = GaussianNB()

model.fit(X_train, y_train)

# -------------------------------
# Prediction
# -------------------------------

y_pred = model.predict(X_test)

# -------------------------------
# Accuracy
# -------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy = {:.2f}%".format(accuracy * 100))

# -------------------------------
# Classification Report
# -------------------------------

print("\nClassification Report\n")

print(classification_report(y_test, y_pred))

# -------------------------------
# Predict New Student
# -------------------------------

sample = [[5,80,75,60]]

prediction = model.predict(sample)

print("\nNew Student Details")

print("Study Hours   :", sample[0][0])
print("Attendance    :", sample[0][1])
print("Assignments   :", sample[0][2])
print("Internal Marks:", sample[0][3])

print("\nPrediction =", prediction[0])

# -------------------------------
# Confusion Matrix
# -------------------------------

cm = confusion_matrix(y_test, y_pred)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=model.classes_
)

disp.plot(cmap="Blues")

plt.title("Confusion Matrix")

plt.show()

# -------------------------------
# Graph 2
# Actual vs Predicted
# -------------------------------

actual = [0 if x == "Fail" else 1 for x in y_test]
predicted = [0 if x == "Fail" else 1 for x in y_pred]

plt.figure(figsize=(8,5))

plt.plot(actual, 'bo-', label="Actual")
plt.plot(predicted, 'r*-', label="Predicted")

plt.yticks([0,1],["Fail","Pass"])

plt.title("Actual vs Predicted")

plt.xlabel("Test Samples")

plt.ylabel("Result")

plt.grid(True)

plt.legend()

plt.show()

# -------------------------------
# Graph 3
# Pass / Fail Distribution
# -------------------------------

data["Result"].value_counts().plot(
    kind="bar",
    color=["red","green"]
)

plt.title("Student Result Distribution")

plt.xlabel("Result")

plt.ylabel("Number of Students")

plt.show()
