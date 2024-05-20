import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import joblib
from sklearn.metrics import *


df = pd.read_csv('averages_weather_data.csv')
df.dropna()

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


# Load the trained model
pipeline = joblib.load('rain_prediction_model.pkl')

# Make predictions on new data
predictions = pipeline.predict(df)

print(mean_squared_error(y, predictions))
print(r2_score(y, predictions))