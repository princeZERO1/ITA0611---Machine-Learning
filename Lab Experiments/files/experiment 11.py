# Credit Score Classification using Python

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

# Create sample credit score dataset
data = {
    "Age": [25, 45, 35, 50, 23, 40, 30, 55, 28, 48,
            32, 52, 26, 43, 37],
    "Annual_Income": [25000, 75000, 50000, 90000, 22000,
                      65000, 40000, 100000, 30000, 80000,
                      45000, 95000, 28000, 70000, 55000],
    "Outstanding_Debt": [15000, 5000, 10000, 3000, 18000,
                         6000, 12000, 2000, 14000, 4000,
                         9000, 2500, 16000, 5500, 8500],
    "Credit_Utilization": [80, 20, 45, 15, 90,
                           25, 60, 10, 75, 18,
                           40, 12, 85, 30, 50],
    "Payment_History": [55, 95, 80, 98, 45,
                        90, 65, 99, 50, 92,
                        82, 97, 48, 88, 75],
    "Credit_Score": [
        "Poor", "Good", "Standard", "Good", "Poor",
        "Good", "Standard", "Good", "Poor", "Good",
        "Standard", "Good", "Poor", "Good", "Standard"
    ]
}

# Convert data into DataFrame
df = pd.DataFrame(data)

print("Credit Score Dataset")
print("--------------------")
print(df)

# Separate input and target
X = df.drop("Credit_Score", axis=1)
y = df["Credit_Score"]

# Encode target labels
encoder = LabelEncoder()
y = encoder.fit_transform(y)

# Split dataset into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Create Decision Tree Classifier
model = DecisionTreeClassifier(
    max_depth=4,
    random_state=42
)

# Train the model
model.fit(X_train, y_train)

# Predict test data
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nActual Values    :", y_test)
print("Predicted Values :", y_pred)

print("\nAccuracy:", accuracy)

# Display confusion matrix
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Predict credit score for a new customer
new_customer = pd.DataFrame({
    "Age": [34],
    "Annual_Income": [48000],
    "Outstanding_Debt": [8000],
    "Credit_Utilization": [35],
    "Payment_History": [85]
})

prediction = model.predict(new_customer)

# Convert numerical prediction back to original class
credit_score = encoder.inverse_transform(prediction)

print("\nNew Customer Details:")
print(new_customer)

print("\nPredicted Credit Score:", credit_score[0])
