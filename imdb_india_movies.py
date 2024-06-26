# -*- coding: utf-8 -*-
"""IMDB India Movies

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PQrY90GrlPZCPRf638lVYX_2xzAXGPFm
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Step 1: Data Collection
# Load the dataset
data = pd.read_csv('/content/IMDb Movies India.csv', encoding='latin1')

# Step 2: Data Preprocessing
# Drop rows with missing values
data.dropna(inplace=True)

# Step 3: Feature Engineering
# No additional feature engineering in this example

# Step 4: Model Selection
# Define features and target variable
features = ['Genre', 'Director']
target = 'Rating'

# Step 5: Model Training
# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data[features], data[target], test_size=0.2, random_state=42)

# Preprocessing for categorical features
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Combine preprocessing steps
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', categorical_transformer, features)
    ])

# Define model
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Create pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('model', model)])

# Fit the model
pipeline.fit(X_train, y_train)

# Step 6: Model Evaluation
# Make predictions
y_pred = pipeline.predict(X_test)

# Calculate mean squared error
mse = mean_squared_error(y_test, y_pred)
print('Mean Squared Error:', mse)

# Step 7: Model Interpretation and Analysis
# Feature importance analysis
feature_importances = pipeline.named_steps['model'].feature_importances_
encoded_features = pipeline.named_steps['preprocessor'].transformers_[0][1].named_steps['onehot'].get_feature_names_out(input_features=features)
feature_importance_df = pd.DataFrame({'Feature': encoded_features, 'Importance': feature_importances}).sort_values(by='Importance', ascending=False)
print('Feature Importance:')
print(feature_importance_df)

# Step 8: Fine-tuning and Optimization
# Can perform hyperparameter tuning or try different models here

# Step 9: Deployment
# Once satisfied with the model's performance, save the model for future use

# Step 10: Monitoring and Maintenance
# Periodically retrain the model with updated data