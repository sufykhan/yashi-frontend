"""
Quick Demo Script for Airbnb Price Prediction System

This script demonstrates the core functionality without requiring the full API or notebook.
Perfect for quick testing and understanding how the system works.
"""

import pandas as pd
import numpy as np
from models.price_predictor import AirbnbPricePredictor
from utils.data_generator import generate_sample_data
from utils.insights_generator import generate_actionable_insights
from visualizations import AirbnbVisualizer
import warnings
warnings.filterwarnings('ignore')

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def print_section(text):
    """Print formatted section"""
    print("\n" + "-" * 70)
    print(f"  {text}")
    print("-" * 70)

def main():
    """Run the demo"""

    print_header("AIRBNB PRICE PREDICTION SYSTEM - DEMO")

    # Configuration
    print("Configuration:")
    print("  Location: New York City")
    print("  Coordinates: (40.7128, -74.0060)")
    print("  Radius: 5 km")
    print("  Properties to analyze: 300")

    LOCATION = {
        'latitude': 40.7128,
        'longitude': -74.0060,
        'radius_km': 5
    }

    YOUR_PROPERTY = {
        'property_type': 'Entire home/apt',
        'bedrooms': 2,
        'bathrooms': 2,
        'accommodates': 4,
        'latitude': LOCATION['latitude'],
        'longitude': LOCATION['longitude'],
        'rating': 4.5,
        'reviews_count': 50,
        'is_superhost': 1,
        'instant_bookable': 1
    }

    print(f"  Your Property: {YOUR_PROPERTY['bedrooms']} bed, {YOUR_PROPERTY['bathrooms']} bath")
    print(f"  Property Type: {YOUR_PROPERTY['property_type']}")

    # Step 1: Generate Sample Data
    print_section("Step 1: Generating Sample Market Data")

    df = generate_sample_data(
        latitude=LOCATION['latitude'],
        longitude=LOCATION['longitude'],
        radius_km=LOCATION['radius_km'],
        num_properties=300
    )

    print(f"✓ Generated {len(df)} properties")
    print(f"\nMarket Overview:")
    print(f"  Average Price: ${df['price'].mean():.2f}/night")
    print(f"  Price Range: ${df['price'].min():.2f} - ${df['price'].max():.2f}")
    print(f"  Average Rating: {df['rating'].mean():.2f}")
    print(f"  Average Occupancy: {df['occupancy_rate'].mean()*100:.1f}%")

    # Step 2: Train Models
    print_section("Step 2: Training Machine Learning Models")

    predictor = AirbnbPricePredictor()
    print("Training 7 regression models (this may take 30-60 seconds)...")

    metrics = predictor.train(df)

    print(f"\n✓ Training Complete!")
    print(f"\nModel Performance Summary:")
    print(f"  Best Model: {metrics['best_model'].upper()}")
    print(f"  R² Score: {metrics['metrics'][metrics['best_model']]['r2_score']:.4f} (higher is better)")
    print(f"  RMSE: ${metrics['metrics'][metrics['best_model']]['rmse']:.2f} (lower is better)")
    print(f"  MAE: ${metrics['metrics'][metrics['best_model']]['mae']:.2f}")

    print(f"\nAll Models Comparison:")
    for model_name, model_metrics in sorted(
        metrics['metrics'].items(),
        key=lambda x: x[1]['r2_score'],
        reverse=True
    ):
        print(f"  {model_name:20s}: R²={model_metrics['r2_score']:.4f}, RMSE=${model_metrics['rmse']:.2f}")

    # Step 3: Monthly Price Predictions
    print_section("Step 3: Monthly Price Predictions for Your Property")

    month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']

    monthly_predictions = []
    for month in range(1, 13):
        features = YOUR_PROPERTY.copy()
        features['month'] = month

        predicted_price = predictor.predict(pd.DataFrame([features]))[0]
        monthly_predictions.append({
            'month': month,
            'month_name': month_names[month-1],
            'price': predicted_price
        })

    print("\nRecommended Nightly Prices by Month:")
    for pred in monthly_predictions:
        print(f"  {pred['month_name']:12s}: ${pred['price']:6.2f}")

    monthly_df = pd.DataFrame(monthly_predictions)
    avg_price = monthly_df['price'].mean()
    best_month = monthly_df.loc[monthly_df['price'].idxmax()]
    worst_month = monthly_df.loc[monthly_df['price'].idxmin()]

    print(f"\n  Average Annual: ${avg_price:.2f}")
    print(f"  Best Month: {best_month['month_name']} (${best_month['price']:.2f})")
    print(f"  Worst Month: {worst_month['month_name']} (${worst_month['price']:.2f})")
    print(f"  Seasonal Variation: ${best_month['price'] - worst_month['price']:.2f}")

    # Step 4: Revenue Projection
    print_section("Step 4: Annual Revenue Projection")

    insights = generate_actionable_insights(df, predictor, YOUR_PROPERTY)
    revenue = insights['revenue_projection']

    print(f"\nAnnual Revenue Forecast:")
    print(f"  Gross Revenue: ${revenue['annual_gross_revenue']:,.2f}")
    print(f"  Est. Expenses (25%): -${revenue['estimated_expenses']:,.2f}")
    print(f"  Net Revenue: ${revenue['estimated_net_revenue']:,.2f}")
    print(f"  Avg Monthly Revenue: ${revenue['average_monthly_revenue']:,.2f}")

    print(f"\nTop 3 Revenue Months:")
    sorted_months = sorted(
        revenue['monthly_revenues'],
        key=lambda x: x['revenue'],
        reverse=True
    )[:3]
    for i, month in enumerate(sorted_months, 1):
        print(f"  {i}. {month['month_name']:12s}: ${month['revenue']:,.2f} "
              f"({month['occupancy_rate']:.0f}% occupancy)")

    # Step 5: Market Comparison
    print_section("Step 5: Market Comparison")

    market = insights['market_comparison']
    stats = market['market_stats']

    print(f"\nYour Property vs Market:")
    print(f"  Market Average: ${stats['average_price']:.2f}/night")
    print(f"  Your Predicted Avg: ${avg_price:.2f}/night")

    diff_pct = ((avg_price / stats['average_price']) - 1) * 100
    position = "above" if diff_pct > 0 else "below"
    print(f"  Position: {diff_pct:+.1f}% {position} market average")

    print(f"\nMarket Statistics ({market['similar_properties_count']} similar properties):")
    print(f"  25th Percentile: ${stats['percentile_25']:.2f}")
    print(f"  50th Percentile (Median): ${stats['median_price']:.2f}")
    print(f"  75th Percentile: ${stats['percentile_75']:.2f}")
    print(f"  Average Rating: {market['average_rating']:.2f}")
    print(f"  Average Occupancy: {market['average_occupancy']:.1f}%")

    # Step 6: Actionable Recommendations
    print_section("Step 6: Actionable Recommendations")

    print(f"\nTop {min(5, len(insights['recommendations']))} Recommendations:\n")

    for i, rec in enumerate(insights['recommendations'][:5], 1):
        priority_symbol = "🔴" if rec['priority'] == 'High' else "🟡"
        print(f"{priority_symbol} [{i}] {rec['title']} ({rec['priority']} Priority)")
        print(f"     Category: {rec['category']}")
        print(f"     {rec['description']}")
        print(f"     → Action: {rec['action']}\n")

    # Step 7: What-If Scenarios
    print_section("Step 7: What-If Scenario Analysis")

    scenarios = [
        {
            'name': 'Current Setup (2 bed, Superhost)',
            'bedrooms': 2,
            'is_superhost': 1,
            'rating': 4.5
        },
        {
            'name': 'Upgrade to 3 Bedrooms',
            'bedrooms': 3,
            'is_superhost': 1,
            'rating': 4.5
        },
        {
            'name': 'Without Superhost Status',
            'bedrooms': 2,
            'is_superhost': 0,
            'rating': 4.5
        },
        {
            'name': 'Premium (3 bed + Perfect Rating)',
            'bedrooms': 3,
            'is_superhost': 1,
            'rating': 5.0
        }
    ]

    print("\nComparing Different Property Configurations:\n")

    scenario_results = []
    for scenario in scenarios:
        features = YOUR_PROPERTY.copy()
        features.update(scenario)
        features['month'] = 6  # June average

        price = predictor.predict(pd.DataFrame([features]))[0]
        annual_revenue = price * 365 * 0.70  # 70% occupancy

        scenario_results.append({
            'name': scenario['name'],
            'price': price,
            'revenue': annual_revenue
        })

        print(f"  {scenario['name']}")
        print(f"    Nightly Rate: ${price:.2f}")
        print(f"    Est. Annual Revenue: ${annual_revenue:,.2f}")
        print()

    # Find best scenario
    best_scenario = max(scenario_results, key=lambda x: x['revenue'])
    current_scenario = scenario_results[0]

    if best_scenario != current_scenario:
        improvement = best_scenario['revenue'] - current_scenario['revenue']
        print(f"💡 Insight: Switching to '{best_scenario['name']}' could increase")
        print(f"   annual revenue by ${improvement:,.2f} ({(improvement/current_scenario['revenue']*100):.1f}%)")

    # Summary
    print_header("EXECUTIVE SUMMARY")

    print("Key Findings:\n")
    print(f"✓ Best ML Model: {metrics['best_model']} (R²={metrics['metrics'][metrics['best_model']]['r2_score']:.3f})")
    print(f"✓ Predicted Annual Revenue: ${revenue['estimated_net_revenue']:,.2f} (net)")
    print(f"✓ Average Nightly Rate: ${avg_price:.2f}")
    print(f"✓ Market Position: {diff_pct:+.1f}% vs average")
    print(f"✓ Best Performing Month: {best_month['month_name']} (${best_month['price']:.2f})")
    print(f"✓ Recommendations Generated: {len(insights['recommendations'])}")

    print("\nNext Steps:")
    print("  1. Review monthly pricing strategy")
    print("  2. Implement high-priority recommendations")
    print("  3. Monitor market trends regularly")
    print("  4. Adjust prices based on booking pace")
    print("  5. Consider scenario upgrades for higher revenue")

    print("\n" + "=" * 70)
    print("  Demo Complete! Check backend/README.md for more details.")
    print("=" * 70 + "\n")

    # Optional: Save model
    save_model = input("Save trained model? (y/n): ").strip().lower()
    if save_model == 'y':
        predictor.save_model('airbnb_price_model.pkl')
        print("✓ Model saved to airbnb_price_model.pkl")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\nError occurred: {str(e)}")
        import traceback
        traceback.print_exc()
