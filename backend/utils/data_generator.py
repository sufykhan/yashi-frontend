"""
Generate sample Airbnb data for testing and demonstration
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data(latitude=40.7128, longitude=-74.0060, radius_km=5, num_properties=200):
    """
    Generate realistic sample Airbnb data for a given location

    Args:
        latitude: Center latitude
        longitude: Center longitude
        radius_km: Radius in kilometers
        num_properties: Number of properties to generate

    Returns:
        DataFrame with sample Airbnb data
    """
    np.random.seed(42)

    property_types = ['Entire home/apt', 'Private room', 'Shared room', 'Hotel room']
    neighbourhoods = ['Downtown', 'Midtown', 'Uptown', 'Suburbs', 'Waterfront', 'Historic District']

    # Generate coordinates within radius
    angles = np.random.uniform(0, 2 * np.pi, num_properties)
    radii = np.random.uniform(0, radius_km / 111, num_properties)  # 111 km per degree

    lats = latitude + radii * np.cos(angles)
    longs = longitude + radii * np.sin(angles)

    data = {
        'property_id': range(1, num_properties + 1),
        'property_type': np.random.choice(property_types, num_properties,
                                         p=[0.5, 0.3, 0.1, 0.1]),
        'neighbourhood': np.random.choice(neighbourhoods, num_properties),
        'latitude': lats,
        'longitude': longs,
        'bedrooms': np.random.choice([1, 2, 3, 4, 5], num_properties,
                                    p=[0.3, 0.35, 0.2, 0.1, 0.05]),
        'bathrooms': np.random.choice([1, 1.5, 2, 2.5, 3], num_properties,
                                     p=[0.4, 0.25, 0.2, 0.1, 0.05]),
        'accommodates': np.random.randint(1, 11, num_properties),
        'rating': np.random.uniform(3.5, 5.0, num_properties),
        'reviews_count': np.random.randint(0, 500, num_properties),
        'is_superhost': np.random.choice([0, 1], num_properties, p=[0.7, 0.3]),
        'instant_bookable': np.random.choice([0, 1], num_properties, p=[0.4, 0.6]),
        'month': np.random.randint(1, 13, num_properties),
        'occupancy_rate': np.random.uniform(0.5, 0.95, num_properties)
    }

    df = pd.DataFrame(data)

    # Generate price based on features (realistic pricing model)
    base_price = 50

    # Property type multiplier
    property_multiplier = df['property_type'].map({
        'Entire home/apt': 1.5,
        'Private room': 1.0,
        'Shared room': 0.6,
        'Hotel room': 1.3
    })

    # Bedroom multiplier
    bedroom_multiplier = 1 + (df['bedrooms'] - 1) * 0.3

    # Rating multiplier
    rating_multiplier = df['rating'] / 4.0

    # Superhost bonus
    superhost_bonus = 1 + df['is_superhost'] * 0.15

    # Seasonal multiplier (summer months are more expensive)
    seasonal_multiplier = 1 + np.where(
        df['month'].isin([6, 7, 8]), 0.3,
        np.where(df['month'].isin([12, 1]), 0.2, 0)
    )

    # Location premium (closer to center is more expensive)
    distance_from_center = np.sqrt((df['latitude'] - latitude)**2 +
                                   (df['longitude'] - longitude)**2)
    location_multiplier = 1 + (1 - distance_from_center / distance_from_center.max()) * 0.5

    # Calculate final price with some random noise
    df['price'] = (
        base_price *
        property_multiplier *
        bedroom_multiplier *
        rating_multiplier *
        superhost_bonus *
        seasonal_multiplier *
        location_multiplier *
        np.random.uniform(0.8, 1.2, num_properties)
    ).round(2)

    # Ensure minimum prices
    df['price'] = df['price'].clip(lower=30)

    return df

def generate_time_series_data(base_df, start_date='2023-01-01', days=365):
    """
    Generate time series data for a property over a period

    Args:
        base_df: Base DataFrame with property features
        start_date: Start date for time series
        days: Number of days to generate

    Returns:
        DataFrame with daily data
    """
    dates = pd.date_range(start=start_date, periods=days)

    time_series_data = []

    for _, property_row in base_df.iterrows():
        for date in dates:
            row = property_row.copy()
            row['date'] = date
            row['month'] = date.month
            row['day_of_week'] = date.dayofweek
            row['is_weekend'] = 1 if date.dayofweek >= 5 else 0

            # Add seasonal price variation
            seasonal_factor = 1 + 0.2 * np.sin(2 * np.pi * date.dayofyear / 365)
            row['price'] = row['price'] * seasonal_factor

            # Add random booking status
            row['is_booked'] = np.random.choice([0, 1], p=[0.3, 0.7])

            time_series_data.append(row)

    return pd.DataFrame(time_series_data)
