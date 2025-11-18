"""
Generate actionable insights from Airbnb data and predictions
"""
import pandas as pd
import numpy as np

def generate_actionable_insights(df, predictor, user_property):
    """
    Generate comprehensive actionable insights for property investment

    Args:
        df: DataFrame with market data
        predictor: Trained price predictor
        user_property: Dictionary with user's property features

    Returns:
        Dictionary with actionable insights
    """
    insights = {
        'pricing_strategy': {},
        'optimal_features': {},
        'market_comparison': {},
        'revenue_projection': {},
        'recommendations': []
    }

    # 1. Pricing Strategy
    insights['pricing_strategy'] = generate_pricing_strategy(df, predictor, user_property)

    # 2. Optimal Features
    insights['optimal_features'] = identify_optimal_features(df, predictor)

    # 3. Market Comparison
    insights['market_comparison'] = compare_to_market(df, user_property)

    # 4. Revenue Projection
    insights['revenue_projection'] = project_revenue(df, predictor, user_property)

    # 5. Actionable Recommendations
    insights['recommendations'] = generate_recommendations(df, user_property, insights)

    return insights

def generate_pricing_strategy(df, predictor, user_property):
    """Generate monthly pricing strategy"""
    monthly_prices = []

    for month in range(1, 13):
        features = user_property.copy()
        features['month'] = month

        # Predict price
        predicted_price = predictor.predict(pd.DataFrame([features]))[0]

        # Get market data for this month
        month_data = df[df['month'] == month]
        market_avg = month_data['price'].mean() if not month_data.empty else predicted_price

        monthly_prices.append({
            'month': month,
            'month_name': pd.Timestamp(2024, month, 1).strftime('%B'),
            'recommended_price': round(float(predicted_price), 2),
            'market_average': round(float(market_avg), 2),
            'competitive_position': 'above' if predicted_price > market_avg else 'below',
            'demand_level': get_demand_level(month)
        })

    # Find best and worst months
    prices = [m['recommended_price'] for m in monthly_prices]
    best_month = monthly_prices[np.argmax(prices)]
    worst_month = monthly_prices[np.argmin(prices)]

    return {
        'monthly_prices': monthly_prices,
        'best_month': best_month,
        'worst_month': worst_month,
        'average_annual_price': round(np.mean(prices), 2),
        'price_volatility': round(np.std(prices), 2)
    }

def identify_optimal_features(df, predictor):
    """Identify which features drive higher prices"""
    feature_analysis = {}

    # Analyze property types
    property_type_avg = df.groupby('property_type')['price'].agg(['mean', 'count']).to_dict()
    feature_analysis['property_types'] = []
    for prop_type in df['property_type'].unique():
        feature_analysis['property_types'].append({
            'type': prop_type,
            'average_price': round(property_type_avg['mean'].get(prop_type, 0), 2),
            'count': int(property_type_avg['count'].get(prop_type, 0))
        })
    feature_analysis['property_types'].sort(key=lambda x: x['average_price'], reverse=True)

    # Analyze bedrooms
    bedroom_analysis = df.groupby('bedrooms')['price'].mean().to_dict()
    feature_analysis['bedrooms'] = [
        {'bedrooms': int(k), 'average_price': round(v, 2)}
        for k, v in sorted(bedroom_analysis.items())
    ]

    # Analyze superhost impact
    if df['is_superhost'].nunique() > 1:
        superhost_premium = (
            df[df['is_superhost'] == 1]['price'].mean() -
            df[df['is_superhost'] == 0]['price'].mean()
        )
        feature_analysis['superhost_premium'] = round(float(superhost_premium), 2)
    else:
        feature_analysis['superhost_premium'] = 0

    # Analyze rating impact
    high_rated = df[df['rating'] >= 4.5]['price'].mean()
    low_rated = df[df['rating'] < 4.5]['price'].mean()
    feature_analysis['rating_premium'] = round(float(high_rated - low_rated), 2)

    return feature_analysis

def compare_to_market(df, user_property):
    """Compare user's property to market"""
    # Filter similar properties
    similar = df[
        (df['property_type'] == user_property.get('property_type', 'Entire home/apt')) &
        (df['bedrooms'] == user_property.get('bedrooms', 2))
    ]

    if similar.empty:
        similar = df

    comparison = {
        'your_property': user_property,
        'similar_properties_count': len(similar),
        'market_stats': {
            'average_price': round(float(similar['price'].mean()), 2),
            'median_price': round(float(similar['price'].median()), 2),
            'min_price': round(float(similar['price'].min()), 2),
            'max_price': round(float(similar['price'].max()), 2),
            'percentile_25': round(float(similar['price'].quantile(0.25)), 2),
            'percentile_75': round(float(similar['price'].quantile(0.75)), 2)
        },
        'average_rating': round(float(similar['rating'].mean()), 2),
        'average_reviews': round(float(similar['reviews_count'].mean()), 2),
        'average_occupancy': round(float(similar['occupancy_rate'].mean() * 100), 2)
    }

    return comparison

def project_revenue(df, predictor, user_property):
    """Project annual revenue for the property"""
    monthly_revenues = []
    total_revenue = 0

    for month in range(1, 13):
        features = user_property.copy()
        features['month'] = month

        predicted_price = predictor.predict(pd.DataFrame([features]))[0]

        # Assume varying occupancy by season
        occupancy = get_occupancy_rate(month)
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1]

        monthly_revenue = predicted_price * days_in_month * occupancy
        total_revenue += monthly_revenue

        monthly_revenues.append({
            'month': month,
            'month_name': pd.Timestamp(2024, month, 1).strftime('%B'),
            'nightly_rate': round(float(predicted_price), 2),
            'occupancy_rate': round(occupancy * 100, 2),
            'days_booked': round(days_in_month * occupancy, 0),
            'revenue': round(float(monthly_revenue), 2)
        })

    # Calculate expenses (rough estimate: 25% of revenue)
    operating_expenses = total_revenue * 0.25
    net_revenue = total_revenue - operating_expenses

    return {
        'monthly_revenues': monthly_revenues,
        'annual_gross_revenue': round(float(total_revenue), 2),
        'estimated_expenses': round(float(operating_expenses), 2),
        'estimated_net_revenue': round(float(net_revenue), 2),
        'average_monthly_revenue': round(float(total_revenue / 12), 2)
    }

def generate_recommendations(df, user_property, insights):
    """Generate actionable recommendations"""
    recommendations = []

    # Pricing recommendations
    avg_price = insights['pricing_strategy']['average_annual_price']
    market_avg = insights['market_comparison']['market_stats']['average_price']

    if avg_price > market_avg * 1.1:
        recommendations.append({
            'category': 'Pricing',
            'priority': 'High',
            'title': 'Premium Pricing Opportunity',
            'description': f'Your property can command ${avg_price:.2f}/night, which is {((avg_price/market_avg - 1) * 100):.1f}% above market average.',
            'action': 'Position as a premium listing with high-quality photos and amenities.'
        })
    elif avg_price < market_avg * 0.9:
        recommendations.append({
            'category': 'Pricing',
            'priority': 'Medium',
            'title': 'Competitive Pricing Strategy',
            'description': f'Market average is ${market_avg:.2f}/night. Consider adding features to justify higher rates.',
            'action': 'Enhance property features or adjust pricing to match market standards.'
        })

    # Seasonal recommendations
    best_month = insights['pricing_strategy']['best_month']
    worst_month = insights['pricing_strategy']['worst_month']

    recommendations.append({
        'category': 'Seasonal Strategy',
        'priority': 'High',
        'title': 'Maximize Peak Season Revenue',
        'description': f'{best_month["month_name"]} is your best month (${best_month["recommended_price"]:.2f}/night).',
        'action': f'Block calendar for {best_month["month_name"]} early and require minimum stay requirements.'
    })

    recommendations.append({
        'category': 'Seasonal Strategy',
        'priority': 'Medium',
        'title': 'Off-Season Strategy',
        'description': f'{worst_month["month_name"]} has lower rates (${worst_month["recommended_price"]:.2f}/night).',
        'action': 'Offer weekly/monthly discounts to maintain occupancy during slower months.'
    })

    # Feature recommendations
    optimal_features = insights['optimal_features']

    if optimal_features.get('superhost_premium', 0) > 10:
        recommendations.append({
            'category': 'Features',
            'priority': 'High',
            'title': 'Achieve Superhost Status',
            'description': f'Superhosts earn ${optimal_features["superhost_premium"]:.2f} more per night.',
            'action': 'Focus on 5-star reviews, fast response times, and low cancellation rates.'
        })

    if optimal_features.get('rating_premium', 0) > 10:
        recommendations.append({
            'category': 'Quality',
            'priority': 'High',
            'title': 'Improve Guest Ratings',
            'description': f'High-rated properties earn ${optimal_features["rating_premium"]:.2f} more per night.',
            'action': 'Provide exceptional cleanliness, amenities, and guest communication.'
        })

    # Revenue optimization
    annual_revenue = insights['revenue_projection']['annual_gross_revenue']

    recommendations.append({
        'category': 'Revenue',
        'priority': 'High',
        'title': 'Annual Revenue Projection',
        'description': f'Estimated annual gross revenue: ${annual_revenue:,.2f}',
        'action': 'Monitor performance monthly and adjust pricing based on booking pace.'
    })

    # Market positioning
    similar_count = insights['market_comparison']['similar_properties_count']

    recommendations.append({
        'category': 'Competition',
        'priority': 'Medium',
        'title': 'Competitive Landscape',
        'description': f'There are {similar_count} similar properties in your area.',
        'action': 'Differentiate with unique amenities, professional photos, and exceptional service.'
    })

    return recommendations

def get_demand_level(month):
    """Get demand level for a month"""
    high_demand_months = [6, 7, 8, 12]  # Summer and December
    medium_demand_months = [3, 4, 5, 9, 10, 11]  # Spring and Fall

    if month in high_demand_months:
        return 'High'
    elif month in medium_demand_months:
        return 'Medium'
    else:
        return 'Low'

def get_occupancy_rate(month):
    """Get estimated occupancy rate for a month"""
    # Seasonal occupancy rates
    occupancy_map = {
        1: 0.60, 2: 0.62, 3: 0.68, 4: 0.72,
        5: 0.75, 6: 0.85, 7: 0.90, 8: 0.88,
        9: 0.75, 10: 0.70, 11: 0.68, 12: 0.80
    }
    return occupancy_map.get(month, 0.70)
