"""
Naive Bayes Classification for Bank Loan Prediction
"""

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import classification_report

# ----------------------------
# Load Dataset
# ----------------------------

data = pd.read_csv("loan.csv")

print(data)

# ----------------------------
# Features and Target
# ----------------------------

X = data.iloc[:, :-1]

y = data.iloc[:, -1]

# ----------------------------
# Train Test Split
# ----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42
)

# ----------------------------
# Model
# ----------------------------

model = GaussianNB()

model.fit(X_train, y_train)

# ----------------------------
# Prediction
# ----------------------------

y_pred = model.predict(X_test)

# ----------------------------
# Accuracy
# ----------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy = {:.2f}%".format(accuracy*100))

# ----------------------------
# Classification Report
# ----------------------------

print(classification_report(y_test,y_pred))

# ----------------------------
# New Prediction
# ----------------------------

sample = [[32,55000,710,175000]]

prediction = model.predict(sample)

print("\nCustomer Details")

print(sample)

print("\nLoan Status =", prediction[0])

# ----------------------------
# Confusion Matrix
# ----------------------------

cm = confusion_matrix(y_test,y_pred)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=model.classes_
)

disp.plot()

plt.title("Confusion Matrix")

plt.show()

# ----------------------------
# Graph 1
# Actual vs Predicted
# ----------------------------

plt.figure(figsize=(8,5))

plt.plot(range(len(y_test)), y_test.map({"Rejected":0,"Approved":1}),
         'bo-', label="Actual")

plt.plot(range(len(y_pred)),
         [0 if x=="Rejected" else 1 for x in y_pred],
         'r*-', label="Predicted")

plt.title("Actual vs Predicted")

plt.xlabel("Test Samples")

plt.ylabel("Loan Status")

plt.yticks([0,1],["Rejected","Approved"])

plt.legend()

plt.grid(True)

plt.show()

# ----------------------------
# Graph 2
# Loan Status Count
# ----------------------------

data["LoanStatus"].value_counts().plot(
    kind="bar"
)

plt.title("Loan Approval Distribution")

plt.xlabel("Loan Status")

plt.ylabel("Count")

plt.show()
