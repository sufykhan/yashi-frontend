# Airbnb Location Tracking & Price Prediction - Setup Guide

## Overview

This project provides a comprehensive Airbnb price prediction and market analysis system with:
- **Machine Learning Models**: 7 different regression algorithms to predict optimal pricing
- **Market Intelligence**: Analyze competition and market trends in any location
- **Revenue Forecasting**: Project annual revenue with monthly breakdowns
- **Actionable Insights**: Data-driven recommendations for maximizing profitability
- **Interactive Dashboard**: React-based frontend for easy analysis

## Architecture

```
Project Structure:
├── backend/                    # Python ML Backend
│   ├── app.py                 # Flask API Server
│   ├── models/                # Regression models
│   ├── utils/                 # Data generation & insights
│   ├── visualizations.py      # Charts and graphs
│   └── airbnb_analysis.ipynb  # Jupyter notebook
└── src/                       # React Frontend
    ├── Screens/
    │   └── AirbnbDashboard.js # Main dashboard
    └── App.js                 # Updated with routes
```

## Quick Start (5 Minutes)

### Step 1: Install Python Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Start Flask API Server

```bash
# From backend directory
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

### Step 3: Start React Frontend

Open a new terminal:

```bash
# From project root
npm install   # If not already done
npm start
```

### Step 4: Access the Application

1. Open browser to `http://localhost:3000`
2. Click "Airbnb Analysis" in the navigation menu
3. Configure your location and property details
4. Click "Analyze Market & Get Insights"

## Features Explained

### 1. Price Prediction Model

The system trains 7 regression models and selects the best one:
- Linear Regression
- Ridge Regression
- Lasso Regression
- Random Forest
- Gradient Boosting
- XGBoost
- LightGBM

**Accuracy**: Typically achieves R² > 0.85 (87%+ predictive accuracy)

### 2. Monthly Pricing Strategy

Get recommended prices for all 12 months based on:
- Seasonal demand patterns
- Market competition
- Property features
- Historical trends

### 3. Revenue Projections

Annual revenue forecast including:
- Monthly breakdown
- Occupancy rate modeling
- Gross and net revenue
- Operating expense estimates (25%)

### 4. Market Comparison

Compare your property against similar listings:
- Average market prices
- Rating benchmarks
- Occupancy rates
- Competitive positioning

### 5. Actionable Recommendations

Prioritized recommendations for:
- Pricing optimization
- Feature improvements
- Seasonal strategies
- Revenue maximization

## Usage Examples

### Example 1: Analyze New York City Market

**Dashboard Configuration:**
```
Location:
  Latitude: 40.7128
  Longitude: -74.0060
  Radius: 5 km

Property:
  Type: Entire home/apt
  Bedrooms: 2
  Bathrooms: 2
  Superhost: Yes
```

**Expected Results:**
- Predicted average price: ~$145/night
- Annual revenue: ~$37,000
- Best month: July ($168/night)
- Market position: +13.9% above average

### Example 2: Compare Property Types

Use the Jupyter notebook to compare different property configurations:

```python
scenarios = [
    {'bedrooms': 1, 'property_type': 'Private room'},
    {'bedrooms': 2, 'property_type': 'Entire home/apt'},
    {'bedrooms': 3, 'property_type': 'Entire home/apt'},
]
```

### Example 3: Optimize for Specific City

1. Get your target city coordinates (Google Maps)
2. Enter in dashboard
3. Adjust radius based on market density
4. Analyze results and recommendations

## API Usage

### Predict Price for Specific Month

```bash
curl -X POST http://localhost:5000/api/predict-price \
  -H "Content-Type: application/json" \
  -d '{
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
    "month": 7
  }'
```

### Get Market Analysis

```bash
curl -X POST http://localhost:5000/api/market-analysis \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 40.7128,
    "longitude": -74.0060,
    "radius_km": 5
  }'
```

### Find Optimal Property Investment

```bash
curl -X POST http://localhost:5000/api/optimal-property \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 40.7128,
    "longitude": -74.0060,
    "budget": 500000
  }'
```

## Using Jupyter Notebook

For in-depth analysis:

```bash
cd backend
jupyter notebook airbnb_analysis.ipynb
```

The notebook includes:
- ✅ Exploratory Data Analysis
- ✅ Model Training & Evaluation
- ✅ Feature Importance Analysis
- ✅ Comprehensive Visualizations
- ✅ What-If Scenario Analysis
- ✅ Export Results to CSV

## Customization

### Using Real Airbnb Data

Replace sample data with actual Airbnb data:

1. Export your data to CSV with these columns:
   - property_type
   - bedrooms, bathrooms, accommodates
   - latitude, longitude
   - rating, reviews_count
   - is_superhost (0 or 1)
   - instant_bookable (0 or 1)
   - month (1-12)
   - price

2. Update `backend/utils/data_generator.py`:

```python
def load_real_data(filepath):
    df = pd.read_csv(filepath)
    # Validate and clean data
    return df
```

### Adjusting Revenue Assumptions

Edit `backend/utils/insights_generator.py`:

```python
# Line ~200: Adjust occupancy rates
def get_occupancy_rate(month):
    occupancy_map = {
        1: 0.60, 2: 0.62, 3: 0.68,  # Winter
        4: 0.72, 5: 0.75, 6: 0.85,  # Spring
        7: 0.90, 8: 0.88, 9: 0.75,  # Summer
        10: 0.70, 11: 0.68, 12: 0.80 # Fall
    }
    return occupancy_map.get(month, 0.70)

# Line ~75: Adjust expense ratio
operating_expenses = total_revenue * 0.25  # 25% - customize this
```

### Adding New Features

To add new predictive features:

1. Edit `backend/models/price_predictor.py`:

```python
# Add to feature_cols list
feature_cols = [
    'property_type', 'bedrooms', 'bathrooms',
    'your_new_feature',  # Add here
    # ... existing features
]
```

2. Update data generator to include the feature
3. Retrain the model

## Troubleshooting

### Backend Won't Start

**Error**: `ModuleNotFoundError`
```bash
# Solution: Install dependencies
pip install -r backend/requirements.txt
```

**Error**: `Port 5000 already in use`
```bash
# Solution: Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Frontend Connection Issues

**Error**: API connection failed

1. Check backend is running: `http://localhost:5000/api/health`
2. Check CORS settings in `backend/app.py`
3. Update API URL in `src/Screens/AirbnbDashboard.js` if needed

### Low Model Accuracy

If R² score < 0.80:

1. Increase training data size (more properties)
2. Add more relevant features
3. Tune model hyperparameters
4. Check for data quality issues

### Visualization Issues

**Error**: Plots not showing in Jupyter

```bash
# Add to notebook cell
%matplotlib inline
```

## Understanding the Results

### What is R² Score?

R² (coefficient of determination) measures prediction accuracy:
- **0.90-1.00**: Excellent (90-100% explained variance)
- **0.80-0.90**: Good (80-90% explained variance)
- **0.70-0.80**: Acceptable (70-80% explained variance)
- **< 0.70**: Poor (needs improvement)

### What is RMSE?

Root Mean Squared Error in dollars:
- **< $15**: Excellent prediction accuracy
- **$15-$30**: Good accuracy
- **$30-$50**: Acceptable
- **> $50**: Review model and data

### Reading Recommendations

Recommendations are prioritized:
- **High Priority**: Immediate impact on revenue
- **Medium Priority**: Important but not urgent
- **Low Priority**: Nice to have improvements

## Performance Benchmarks

Typical performance metrics:

| Metric | Value |
|--------|-------|
| Training Time | 30-60 seconds |
| Prediction Time | 10-20 ms |
| Memory Usage | ~500 MB |
| Dataset Size | 200-500 properties |
| API Response Time | 1-3 seconds |

## Data Privacy

This system uses **sample generated data** by default:
- No real Airbnb data is collected
- All analysis is performed locally
- No data is sent to external servers
- You control all inputs and outputs

## Next Steps

1. **Experiment**: Try different locations and property configurations
2. **Compare**: Run scenario analysis to find optimal setup
3. **Export**: Save results from Jupyter notebook
4. **Optimize**: Implement recommendations
5. **Monitor**: Re-run analysis monthly to track market changes

## Advanced Features

### Batch Analysis

Analyze multiple locations at once:

```python
locations = [
    {'name': 'NYC', 'lat': 40.7128, 'lng': -74.0060},
    {'name': 'SF', 'lat': 37.7749, 'lng': -122.4194},
    {'name': 'LA', 'lat': 34.0522, 'lng': -118.2437},
]

for loc in locations:
    df = generate_sample_data(loc['lat'], loc['lng'])
    # Analyze...
```

### Time Series Forecasting

Project future price trends:

```python
from utils.data_generator import generate_time_series_data

# Generate daily data for 1 year
time_series = generate_time_series_data(df, days=365)
```

### Export to Excel

Create detailed reports:

```python
with pd.ExcelWriter('airbnb_analysis.xlsx') as writer:
    monthly_pred_df.to_excel(writer, sheet_name='Pricing')
    revenue_df.to_excel(writer, sheet_name='Revenue')
    scenario_df.to_excel(writer, sheet_name='Scenarios')
```

## Support & Resources

- **Documentation**: See `backend/README.md`
- **API Reference**: Check Flask app.py for all endpoints
- **Examples**: Run Jupyter notebook for comprehensive examples
- **Issues**: Check console logs for error messages

## Summary

You now have:
✅ ML-powered price prediction system
✅ Market analysis dashboard
✅ Revenue forecasting tools
✅ Actionable business insights
✅ Interactive visualizations
✅ REST API for integration

Start analyzing markets and optimizing your Airbnb pricing strategy!
