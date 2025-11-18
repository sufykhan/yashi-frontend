"""
Airbnb Price Prediction Model using Multiple Regression Algorithms
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import xgboost as xgb
import lightgbm as lgb
import joblib
import os

class AirbnbPricePredictor:
    """
    Comprehensive price prediction model for Airbnb properties
    Uses ensemble of multiple regression algorithms
    """

    def __init__(self):
        self.models = {}
        self.best_model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = None
        self.is_trained = False

    def preprocess_data(self, df, is_training=True):
        """Preprocess the data for model training/prediction"""
        df = df.copy()

        # Categorical columns to encode
        categorical_cols = ['property_type', 'neighbourhood']

        for col in categorical_cols:
            if col in df.columns:
                if is_training:
                    self.label_encoders[col] = LabelEncoder()
                    df[col] = self.label_encoders[col].fit_transform(df[col].astype(str))
                else:
                    if col in self.label_encoders:
                        # Handle unseen labels
                        df[col] = df[col].astype(str)
                        df[col] = df[col].apply(
                            lambda x: x if x in self.label_encoders[col].classes_
                            else self.label_encoders[col].classes_[0]
                        )
                        df[col] = self.label_encoders[col].transform(df[col])

        # Feature engineering
        if 'latitude' in df.columns and 'longitude' in df.columns:
            # Distance from city center (assuming 0,0 as reference)
            df['distance_from_center'] = np.sqrt(
                df['latitude']**2 + df['longitude']**2
            )

        # Price per person
        if 'price' in df.columns and 'accommodates' in df.columns:
            df['price_per_person'] = df['price'] / df['accommodates'].replace(0, 1)

        # Bathroom to bedroom ratio
        if 'bathrooms' in df.columns and 'bedrooms' in df.columns:
            df['bath_bed_ratio'] = df['bathrooms'] / df['bedrooms'].replace(0, 1)

        return df

    def train(self, df):
        """Train multiple regression models and select the best one"""
        print("Preprocessing data...")
        df = self.preprocess_data(df, is_training=True)

        # Define feature columns
        feature_cols = [
            'property_type', 'bedrooms', 'bathrooms', 'accommodates',
            'latitude', 'longitude', 'rating', 'reviews_count',
            'is_superhost', 'instant_bookable', 'month',
            'distance_from_center', 'bath_bed_ratio'
        ]

        # Keep only available columns
        self.feature_columns = [col for col in feature_cols if col in df.columns]

        X = df[self.feature_columns]
        y = df['price']

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Train multiple models
        print("Training models...")

        # 1. Linear Regression
        print("  - Training Linear Regression...")
        self.models['linear'] = LinearRegression()
        self.models['linear'].fit(X_train_scaled, y_train)

        # 2. Ridge Regression
        print("  - Training Ridge Regression...")
        self.models['ridge'] = Ridge(alpha=1.0)
        self.models['ridge'].fit(X_train_scaled, y_train)

        # 3. Lasso Regression
        print("  - Training Lasso Regression...")
        self.models['lasso'] = Lasso(alpha=1.0)
        self.models['lasso'].fit(X_train_scaled, y_train)

        # 4. Random Forest
        print("  - Training Random Forest...")
        self.models['random_forest'] = RandomForestRegressor(
            n_estimators=100, max_depth=15, random_state=42, n_jobs=-1
        )
        self.models['random_forest'].fit(X_train_scaled, y_train)

        # 5. Gradient Boosting
        print("  - Training Gradient Boosting...")
        self.models['gradient_boosting'] = GradientBoostingRegressor(
            n_estimators=100, max_depth=5, random_state=42
        )
        self.models['gradient_boosting'].fit(X_train_scaled, y_train)

        # 6. XGBoost
        print("  - Training XGBoost...")
        self.models['xgboost'] = xgb.XGBRegressor(
            n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42
        )
        self.models['xgboost'].fit(X_train_scaled, y_train)

        # 7. LightGBM
        print("  - Training LightGBM...")
        self.models['lightgbm'] = lgb.LGBMRegressor(
            n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42
        )
        self.models['lightgbm'].fit(X_train_scaled, y_train)

        # Evaluate all models
        print("\nEvaluating models...")
        metrics = {}
        best_r2 = -np.inf

        for name, model in self.models.items():
            y_pred = model.predict(X_test_scaled)

            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            metrics[name] = {
                'mse': float(mse),
                'rmse': float(rmse),
                'mae': float(mae),
                'r2_score': float(r2)
            }

            print(f"  {name}: R² = {r2:.4f}, RMSE = {rmse:.2f}, MAE = {mae:.2f}")

            # Select best model based on R² score
            if r2 > best_r2:
                best_r2 = r2
                self.best_model = name

        print(f"\nBest model: {self.best_model} (R² = {best_r2:.4f})")

        self.is_trained = True

        # Feature importance (for tree-based models)
        if self.best_model in ['random_forest', 'gradient_boosting', 'xgboost', 'lightgbm']:
            feature_importance = self.models[self.best_model].feature_importances_
            importance_df = pd.DataFrame({
                'feature': self.feature_columns,
                'importance': feature_importance
            }).sort_values('importance', ascending=False)
            metrics['feature_importance'] = importance_df.to_dict(orient='records')

        return {
            'best_model': self.best_model,
            'metrics': metrics,
            'train_size': len(X_train),
            'test_size': len(X_test)
        }

    def predict(self, df):
        """Make predictions using the best trained model"""
        if not self.is_trained:
            raise ValueError("Model not trained yet. Call train() first.")

        df = self.preprocess_data(df, is_training=False)

        # Ensure all feature columns are present
        for col in self.feature_columns:
            if col not in df.columns:
                df[col] = 0

        X = df[self.feature_columns]
        X_scaled = self.scaler.transform(X)

        predictions = self.models[self.best_model].predict(X_scaled)
        return predictions

    def save_model(self, filepath='airbnb_price_model.pkl'):
        """Save the trained model"""
        model_data = {
            'models': self.models,
            'best_model': self.best_model,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_columns': self.feature_columns,
            'is_trained': self.is_trained
        }
        joblib.dump(model_data, filepath)
        print(f"Model saved to {filepath}")

    def load_model(self, filepath='airbnb_price_model.pkl'):
        """Load a trained model"""
        if os.path.exists(filepath):
            model_data = joblib.load(filepath)
            self.models = model_data['models']
            self.best_model = model_data['best_model']
            self.scaler = model_data['scaler']
            self.label_encoders = model_data['label_encoders']
            self.feature_columns = model_data['feature_columns']
            self.is_trained = model_data['is_trained']
            print(f"Model loaded from {filepath}")
        else:
            print(f"Model file {filepath} not found")
