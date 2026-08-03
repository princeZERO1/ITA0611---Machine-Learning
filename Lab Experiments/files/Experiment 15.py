"""
Experiment 5
Naive Bayes Classifier on Iris Dataset
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import classification_report

# -------------------------------
# Load Iris Dataset
# -------------------------------

iris = load_iris()

X = iris.data
y = iris.target

# Convert to DataFrame (optional)

df = pd.DataFrame(X, columns=iris.feature_names)

df["Species"] = y

print(df.head())

# -------------------------------
# Split Dataset
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

# Train

model.fit(X_train, y_train)

# Predict

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

print(classification_report(
    y_test,
    y_pred,
    target_names=iris.target_names
))

# -------------------------------
# Predict New Sample
# -------------------------------

sample = [[5.1,3.5,1.4,0.2]]

prediction = model.predict(sample)

print("\nPrediction for", sample)

print("Flower =", iris.target_names[prediction[0]])

# -------------------------------
# Graph 1
# Confusion Matrix
# -------------------------------

cm = confusion_matrix(y_test, y_pred)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=iris.target_names
)

disp.plot()

plt.title("Confusion Matrix")

plt.show()

# -------------------------------
# Graph 2
# Scatter Plot
# -------------------------------

plt.figure(figsize=(8,6))

sns.scatterplot(
    x=df.iloc[:,0],
    y=df.iloc[:,2],
    hue=iris.target_names[df["Species"]],
    palette="Set1"
)

plt.title("Iris Flower Classification")

plt.xlabel("Sepal Length")

plt.ylabel("Petal Length")

plt.show()

# -------------------------------
# Graph 3
# Actual vs Predicted
# -------------------------------

plt.figure(figsize=(8,5))

plt.plot(y_test,'bo-',label="Actual")

plt.plot(y_pred,'r*-',label="Predicted")

plt.xlabel("Sample Number")

plt.ylabel("Flower Class")

plt.title("Actual vs Predicted")

plt.legend()

plt.grid(True)

plt.show()
