from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd

# Load Iris dataset
iris = load_iris()

# Display dataset
data = pd.DataFrame(iris.data, columns=iris.feature_names)
data['Target'] = iris.target
pd.set_option('display.max_rows', None)

print("IRIS DATASET:")
print(data)

# Input and output
X = iris.data
y = iris.target

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# Create Logistic Regression model
model = LogisticRegression(
    max_iter=200,
    solver='lbfgs',
    C=1.0
)

# Train model
model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

# Results
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("Actual:", y_test)
print("Predict:", y_pred)
