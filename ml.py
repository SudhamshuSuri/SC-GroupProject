import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_squared_error
from joblib import parallel_backend

# Read the CSV file
df = pd.read_csv('averages_weather_data.csv')

# Define the target variable and features
target = 'Rain (mm)'
features = df.columns.difference([target])

# Drop rows with missing values
df = df.dropna(subset=[target])

# Separate features and target
X = df[features]
y = df[target]

# Define categorical and numerical columns
categorical_cols = X.select_dtypes(include=['object']).columns
numerical_cols = X.select_dtypes(include=['number']).columns

# Data preprocessing pipelines
categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

numerical_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

# Combine preprocessing steps
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

# Define the model
model = LGBMRegressor(n_jobs=-1)  # Use all available cores

# Create a pipeline that first transforms the data then fits the model
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', model)
])

# Custom train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Hyperparameter optimization using GridSearchCV
param_grid = {
    'model__num_leaves': [31, 127],
    'model__learning_rate': [0.05, 0.1, 0.2],
    'model__n_estimators': [100, 200]
}

# Use parallel backend for GridSearchCV to speed up the process
with parallel_backend('threading'):
    grid_search = GridSearchCV(pipeline, param_grid, cv=3, n_jobs=-1, verbose=2)
    grid_search.fit(X_train, y_train)

# Evaluate the model
y_pred = grid_search.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Print best parameters
print(f"Best parameters: {grid_search.best_params_}")

# Train final model on the entire dataset with best parameters
pipeline.set_params(**grid_search.best_params_)
pipeline.fit(X, y)

# Save the model for future use (optional)
import joblib
joblib.dump(pipeline, 'rain_prediction_model.pkl')
