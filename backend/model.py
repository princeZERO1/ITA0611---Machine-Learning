import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, precision_score, recall_score, f1_score, confusion_matrix
import numpy as np

def preprocess_and_train(df, target_col='Suitability_Score'):
    """
    Trains a Random Forest model to predict meal suitability score.
    """
    # Create features by one-hot encoding
    df_features = df.drop(columns=['Meal_ID', 'Meal_Name', 'Base_Rating', target_col])
    
    # Identify categorical columns
    categorical_cols = ['Cuisine', 'Meal_Type']
    df_encoded = pd.get_dummies(df_features, columns=categorical_cols, drop_first=False)
    
    X = df_encoded
    y = df[target_col]
    
    # Train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Model
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    # Evaluate Regression
    y_pred = rf_model.predict(X_test)
    mse = float(mean_squared_error(y_test, y_pred))
    rmse = float(np.sqrt(mse))
    mae = float(mean_absolute_error(y_test, y_pred))
    r2 = float(r2_score(y_test, y_pred))
    
    # Evaluate Classification (Threshold = 75 for 'Recommended')
    threshold = 75
    y_test_class = (y_test >= threshold).astype(int)
    y_pred_class = (y_pred >= threshold).astype(int)
    
    precision = float(precision_score(y_test_class, y_pred_class, zero_division=0))
    recall = float(recall_score(y_test_class, y_pred_class, zero_division=0))
    f1 = float(f1_score(y_test_class, y_pred_class, zero_division=0))
    cm = confusion_matrix(y_test_class, y_pred_class).tolist()
    
    # Feature Importances
    feature_importances = pd.DataFrame({
        'Feature': X.columns,
        'Importance': rf_model.feature_importances_
    }).sort_values(by='Importance', ascending=False)
    
    metrics = {
        'MSE': round(mse, 2),
        'RMSE': round(rmse, 2),
        'MAE': round(mae, 2),
        'R2': round(r2, 4),
        'Train_Samples': len(X_train),
        'Test_Samples': len(X_test),
        'Precision': round(precision, 4),
        'Recall': round(recall, 4),
        'F1_Score': round(f1, 4),
        'Confusion_Matrix': cm
    }
    
    # Format feature importances for JSON
    top_features = feature_importances.head(10).to_dict('records')
    
    # Generate actual vs predicted sample for frontend visualization
    # We sample up to 100 points to keep the graph readable
    sample_size = min(100, len(y_test))
    indices = np.random.choice(len(y_test), sample_size, replace=False)
    actual_vs_predicted = [
        {"Actual": float(y_test.iloc[i]), "Predicted": float(y_pred[i])}
        for i in indices
    ]
    # Sort by actual to make visualization cleaner
    actual_vs_predicted = sorted(actual_vs_predicted, key=lambda x: x["Actual"])
    
    return rf_model, X.columns, top_features, metrics, actual_vs_predicted
