"""
Flask API for Airbnb Location Tracking and Price Prediction
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from models.price_predictor import AirbnbPricePredictor
from utils.data_generator import generate_sample_data
from utils.insights_generator import generate_actionable_insights
import json

app = Flask(__name__)
CORS(app)

# Initialize the predictor
predictor = AirbnbPricePredictor()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Airbnb Price Prediction API is running'})

@app.route('/api/generate-sample-data', methods=['POST'])
def generate_data():
    """Generate sample Airbnb data for a location"""
    data = request.json
    latitude = data.get('latitude', 40.7128)  # Default NYC
    longitude = data.get('longitude', -74.0060)
    radius_km = data.get('radius_km', 5)
    num_properties = data.get('num_properties', 200)

    df = generate_sample_data(latitude, longitude, radius_km, num_properties)

    return jsonify({
        'success': True,
        'data': df.to_dict(orient='records'),
        'count': len(df)
    })

@app.route('/api/train-model', methods=['POST'])
def train_model():
    """Train the price prediction model"""
    data = request.json
    training_data = pd.DataFrame(data.get('training_data', []))

    if training_data.empty:
        # Generate sample data if none provided
        training_data = generate_sample_data()

    metrics = predictor.train(training_data)

    return jsonify({
        'success': True,
        'metrics': metrics,
        'message': 'Model trained successfully'
    })

@app.route('/api/predict-price', methods=['POST'])
def predict_price():
    """Predict price for a property"""
    data = request.json
    property_features = pd.DataFrame([data])

    prediction = predictor.predict(property_features)

    return jsonify({
        'success': True,
        'predicted_price': float(prediction[0]),
        'currency': 'USD'
    })

@app.route('/api/predict-monthly-prices', methods=['POST'])
def predict_monthly_prices():
    """Predict prices for all 12 months"""
    data = request.json
    base_features = data.copy()

    monthly_predictions = []
    for month in range(1, 13):
        features = base_features.copy()
        features['month'] = month
        prediction = predictor.predict(pd.DataFrame([features]))
        monthly_predictions.append({
            'month': month,
            'predicted_price': float(prediction[0])
        })

    return jsonify({
        'success': True,
        'monthly_predictions': monthly_predictions
    })

@app.route('/api/analyze-location', methods=['POST'])
def analyze_location():
    """Analyze Airbnb properties in a location and generate insights"""
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    radius_km = data.get('radius_km', 5)
    property_type = data.get('property_type', 'Entire home/apt')
    bedrooms = data.get('bedrooms', 2)

    # Generate sample data for the location
    df = generate_sample_data(latitude, longitude, radius_km, 200)

    # Train model if not already trained
    if not predictor.is_trained:
        predictor.train(df)

    # Generate insights
    insights = generate_actionable_insights(df, predictor, {
        'property_type': property_type,
        'bedrooms': bedrooms,
        'latitude': latitude,
        'longitude': longitude
    })

    return jsonify({
        'success': True,
        'insights': insights,
        'properties_analyzed': len(df)
    })

@app.route('/api/market-analysis', methods=['POST'])
def market_analysis():
    """Get comprehensive market analysis for a location"""
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    radius_km = data.get('radius_km', 5)

    # Generate sample data
    df = generate_sample_data(latitude, longitude, radius_km, 300)

    # Calculate market statistics
    analysis = {
        'average_price': float(df['price'].mean()),
        'median_price': float(df['price'].median()),
        'price_range': {
            'min': float(df['price'].min()),
            'max': float(df['price'].max()),
            'percentile_25': float(df['price'].quantile(0.25)),
            'percentile_75': float(df['price'].quantile(0.75))
        },
        'property_types': df['property_type'].value_counts().to_dict(),
        'bedroom_distribution': df['bedrooms'].value_counts().to_dict(),
        'average_occupancy': float(df['occupancy_rate'].mean()),
        'average_rating': float(df['rating'].mean()),
        'total_properties': len(df),
        'monthly_trends': []
    }

    # Calculate monthly price trends
    for month in range(1, 13):
        month_data = df[df['month'] == ((month - 1) % 12 + 1)]
        if not month_data.empty:
            analysis['monthly_trends'].append({
                'month': month,
                'average_price': float(month_data['price'].mean()),
                'property_count': len(month_data)
            })

    return jsonify({
        'success': True,
        'analysis': analysis
    })

@app.route('/api/optimal-property', methods=['POST'])
def find_optimal_property():
    """Find optimal property type and features for investment"""
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    budget = data.get('budget', 500000)

    # Generate sample data
    df = generate_sample_data(latitude, longitude, 5, 300)

    # Train model
    if not predictor.is_trained:
        predictor.train(df)

    # Calculate profitability score for each property type
    recommendations = []

    for prop_type in df['property_type'].unique():
        for beds in range(1, 5):
            features = {
                'property_type': prop_type,
                'bedrooms': beds,
                'bathrooms': beds,
                'accommodates': beds * 2,
                'latitude': latitude,
                'longitude': longitude,
                'rating': 4.5,
                'reviews_count': 50,
                'is_superhost': 1,
                'instant_bookable': 1,
                'month': 6  # Mid-year average
            }

            predicted_price = predictor.predict(pd.DataFrame([features]))[0]

            # Calculate estimated annual revenue (assuming 70% occupancy)
            annual_revenue = predicted_price * 365 * 0.70
            roi = (annual_revenue / budget) * 100 if budget > 0 else 0

            recommendations.append({
                'property_type': prop_type,
                'bedrooms': beds,
                'predicted_nightly_price': float(predicted_price),
                'estimated_annual_revenue': float(annual_revenue),
                'estimated_roi': float(roi),
                'profitability_score': float(annual_revenue)
            })

    # Sort by profitability
    recommendations.sort(key=lambda x: x['profitability_score'], reverse=True)

    return jsonify({
        'success': True,
        'recommendations': recommendations[:10],  # Top 10
        'budget': budget
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
