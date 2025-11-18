# Airbnb Location Tracking & Price Prediction System

A comprehensive Python-based machine learning system for analyzing Airbnb markets, predicting prices, and generating actionable insights for property investment decisions.

## Features

- **Multiple Regression Models**: Linear, Ridge, Lasso, Random Forest, Gradient Boosting, XGBoost, and LightGBM
- **Price Prediction**: Monthly price forecasting based on property features and seasonal trends
- **Market Analysis**: Comprehensive market statistics and competitive analysis
- **Revenue Projection**: Annual revenue forecasting with occupancy rate modeling
- **Actionable Insights**: Data-driven recommendations for pricing and property optimization
- **Interactive Visualizations**: Rich visualizations using Matplotlib, Seaborn, and Plotly
- **REST API**: Flask-based API for integration with frontend applications

## System Architecture

```
backend/
├── app.py                      # Flask API server
├── requirements.txt            # Python dependencies
├── airbnb_analysis.ipynb      # Jupyter notebook for analysis
├── models/
│   ├── __init__.py
│   └── price_predictor.py     # Regression model implementations
├── utils/
│   ├── __init__.py
│   ├── data_generator.py      # Sample data generation
│   └── insights_generator.py  # Insights and recommendations
└── visualizations.py          # Visualization utilities
```

## Installation

### 1. Create Virtual Environment (Recommended)

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\\Scripts\\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Quick Start

### Option 1: Use the Jupyter Notebook (Recommended for Analysis)

```bash
jupyter notebook airbnb_analysis.ipynb
```

The notebook provides:
- Interactive data analysis
- Model training and evaluation
- Comprehensive visualizations
- Scenario analysis
- Exportable results

### Option 2: Run the Flask API Server

```bash
python app.py
```

The API server will start on `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /api/health
```

### Generate Sample Data
```
POST /api/generate-sample-data
Body: {
  "latitude": 40.7128,
  "longitude": -74.0060,
  "radius_km": 5,
  "num_properties": 200
}
```

### Train Model
```
POST /api/train-model
Body: {
  "training_data": [...]  // Optional, uses sample data if not provided
}
```

### Predict Price
```
POST /api/predict-price
Body: {
  "property_type": "Entire home/apt",
  "bedrooms": 2,
  "bathrooms": 2,
  "accommodates": 4,
  "latitude": 40.7128,
  "longitude": -74.0060,
  "rating": 4.5,
  "reviews_count": 50,
  "is_superhost": 1,
  "instant_bookable": 1,
  "month": 6
}
```

### Analyze Location
```
POST /api/analyze-location
Body: {
  "latitude": 40.7128,
  "longitude": -74.0060,
  "radius_km": 5,
  "property_type": "Entire home/apt",
  "bedrooms": 2
}
```

### Market Analysis
```
POST /api/market-analysis
Body: {
  "latitude": 40.7128,
  "longitude": -74.0060,
  "radius_km": 5
}
```

### Find Optimal Property
```
POST /api/optimal-property
Body: {
  "latitude": 40.7128,
  "longitude": -74.0060,
  "budget": 500000
}
```

## Regression Models

The system implements and compares 7 different regression algorithms:

1. **Linear Regression**: Baseline model
2. **Ridge Regression**: L2 regularization
3. **Lasso Regression**: L1 regularization
4. **Random Forest**: Ensemble of decision trees
5. **Gradient Boosting**: Sequential ensemble method
6. **XGBoost**: Optimized gradient boosting
7. **LightGBM**: Fast gradient boosting framework

The best-performing model is automatically selected based on R² score.

## Features Used for Prediction

- Property type
- Number of bedrooms
- Number of bathrooms
- Accommodates (guest capacity)
- Geographic coordinates (latitude, longitude)
- Rating
- Number of reviews
- Superhost status
- Instant bookable status
- Month (seasonal effects)
- Derived features (distance from center, price per person, bath/bed ratio)

## Sample Usage (Python)

```python
from models.price_predictor import AirbnbPricePredictor
from utils.data_generator import generate_sample_data
import pandas as pd

# Generate sample data
df = generate_sample_data(latitude=40.7128, longitude=-74.0060, radius_km=5, num_properties=300)

# Train model
predictor = AirbnbPricePredictor()
metrics = predictor.train(df)

print(f"Best model: {metrics['best_model']}")
print(f"R² Score: {metrics['metrics'][metrics['best_model']]['r2_score']:.4f}")

# Predict price
property_features = {
    'property_type': 'Entire home/apt',
    'bedrooms': 2,
    'bathrooms': 2,
    'accommodates': 4,
    'latitude': 40.7128,
    'longitude': -74.0060,
    'rating': 4.5,
    'reviews_count': 50,
    'is_superhost': 1,
    'instant_bookable': 1,
    'month': 6
}

predicted_price = predictor.predict(pd.DataFrame([property_features]))[0]
print(f"Predicted price: ${predicted_price:.2f}/night")
```

## Visualizations

The system generates comprehensive visualizations:

- **Price Distribution**: Histogram and box plots
- **Property Type Analysis**: Average prices by property type
- **Seasonal Trends**: Monthly price trends
- **Geographic Heatmap**: Price distribution by location
- **Correlation Matrix**: Feature correlation heatmap
- **Revenue Projections**: Monthly revenue and occupancy charts
- **Model Performance**: Comparison of all regression models
- **Feature Importance**: Top predictive features

## Insights Generated

The system provides actionable insights including:

1. **Pricing Strategy**: Optimal monthly pricing recommendations
2. **Market Comparison**: Position relative to competitors
3. **Revenue Projection**: Annual revenue forecasting
4. **Optimal Features**: Which features drive higher prices
5. **Recommendations**: Prioritized action items for maximizing revenue

## Example Output

```
EXECUTIVE SUMMARY
============================================================

Location: (40.7128, -74.0060)
Analysis Radius: 5 km
Properties Analyzed: 300

Your Property Configuration:
  Type: Entire home/apt
  Bedrooms: 2
  Bathrooms: 2
  Rating: 4.5

Market Statistics:
  Market Average Price: $127.50/night
  Your Predicted Average: $145.20/night
  Position: +13.9% vs market

Revenue Projection:
  Annual Gross Revenue: $37,128
  Net Revenue (after 25% expenses): $27,846
  Monthly Average: $3,094

Best Performing Month: July ($168.50)
Slowest Month: February ($125.30)

Model Performance:
  Best Model: xgboost
  R² Score: 0.8734
  RMSE: $12.45
```

## Customization

### Adding Real Airbnb Data

Replace the sample data generator with real Airbnb data:

```python
# Instead of:
df = generate_sample_data(...)

# Use:
df = pd.read_csv('your_airbnb_data.csv')
```

Ensure your data has the required columns:
- property_type, bedrooms, bathrooms, accommodates
- latitude, longitude
- rating, reviews_count
- is_superhost (0 or 1), instant_bookable (0 or 1)
- month (1-12)
- price (target variable)

### Adjusting Model Parameters

Edit `models/price_predictor.py` to modify:
- Model hyperparameters
- Feature engineering
- Train/test split ratio
- Cross-validation settings

### Customizing Insights

Edit `utils/insights_generator.py` to:
- Adjust occupancy rate assumptions
- Modify expense ratios
- Customize recommendation logic
- Add new insight categories

## Performance Considerations

- **Training Time**: Initial model training takes 30-60 seconds for 300 properties
- **Prediction Time**: ~10ms per prediction after training
- **Memory Usage**: ~500MB for typical dataset (300-500 properties)
- **Scalability**: Can handle 10,000+ properties with longer training time

## Troubleshooting

### Import Errors
```bash
# Make sure you're in the backend directory
cd backend
python app.py
```

### Model Performance Issues
- Increase training data size
- Adjust model hyperparameters
- Add more relevant features
- Check data quality

### API Connection Issues
- Ensure Flask server is running on port 5000
- Check firewall settings
- Verify CORS settings in app.py

## Future Enhancements

- [ ] Integration with real Airbnb API
- [ ] Deep learning models (Neural Networks)
- [ ] Time series forecasting for future demand
- [ ] Competitor analysis dashboard
- [ ] Automated pricing optimization
- [ ] Multi-city comparison
- [ ] Investment ROI calculator
- [ ] Property recommendation engine

## Technologies Used

- **Python 3.8+**
- **Machine Learning**: scikit-learn, XGBoost, LightGBM
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, seaborn, plotly
- **API**: Flask, Flask-CORS
- **Geographic**: geopy
- **Model Persistence**: joblib

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.

## Author

Built with Python, Flask, and Machine Learning for smart Airbnb investment decisions.
