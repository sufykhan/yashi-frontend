"""
Visualization utilities for Airbnb price analysis
"""
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from io import BytesIO
import base64
import json

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

class AirbnbVisualizer:
    """Generate visualizations for Airbnb data analysis"""

    def __init__(self, df):
        self.df = df

    def plot_price_distribution(self, save_path=None):
        """Plot price distribution histogram"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        # Histogram
        ax1.hist(self.df['price'], bins=50, edgecolor='black', alpha=0.7)
        ax1.set_xlabel('Price ($)')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Distribution of Airbnb Prices')
        ax1.axvline(self.df['price'].mean(), color='red', linestyle='--',
                   label=f'Mean: ${self.df["price"].mean():.2f}')
        ax1.axvline(self.df['price'].median(), color='green', linestyle='--',
                   label=f'Median: ${self.df["price"].median():.2f}')
        ax1.legend()

        # Box plot
        ax2.boxplot(self.df['price'], vert=True)
        ax2.set_ylabel('Price ($)')
        ax2.set_title('Price Box Plot')
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return self._fig_to_base64(fig)

    def plot_price_by_property_type(self, save_path=None):
        """Plot average price by property type"""
        avg_price = self.df.groupby('property_type')['price'].mean().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(10, 6))
        avg_price.plot(kind='bar', ax=ax, color='steelblue', edgecolor='black')
        ax.set_xlabel('Property Type')
        ax.set_ylabel('Average Price ($)')
        ax.set_title('Average Nightly Price by Property Type')
        ax.tick_params(axis='x', rotation=45)

        # Add value labels on bars
        for i, v in enumerate(avg_price):
            ax.text(i, v + 2, f'${v:.2f}', ha='center', va='bottom')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return self._fig_to_base64(fig)

    def plot_price_by_bedrooms(self, save_path=None):
        """Plot price vs bedrooms"""
        fig, ax = plt.subplots(figsize=(10, 6))

        bedroom_stats = self.df.groupby('bedrooms')['price'].agg(['mean', 'std'])

        ax.bar(bedroom_stats.index, bedroom_stats['mean'],
               yerr=bedroom_stats['std'], capsize=5,
               color='coral', edgecolor='black', alpha=0.7)
        ax.set_xlabel('Number of Bedrooms')
        ax.set_ylabel('Average Price ($)')
        ax.set_title('Average Price by Number of Bedrooms')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return self._fig_to_base64(fig)

    def plot_monthly_trends(self, save_path=None):
        """Plot monthly price trends"""
        monthly_avg = self.df.groupby('month')['price'].mean()
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(monthly_avg.index, monthly_avg.values, marker='o',
               linewidth=2, markersize=8, color='darkblue')
        ax.fill_between(monthly_avg.index, monthly_avg.values,
                        alpha=0.3, color='lightblue')
        ax.set_xlabel('Month')
        ax.set_ylabel('Average Price ($)')
        ax.set_title('Seasonal Price Trends')
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(month_names)
        ax.grid(True, alpha=0.3)

        # Highlight peak and low seasons
        max_month = monthly_avg.idxmax()
        min_month = monthly_avg.idxmin()
        ax.scatter([max_month], [monthly_avg[max_month]], color='red',
                  s=200, zorder=5, label=f'Peak: ${monthly_avg[max_month]:.2f}')
        ax.scatter([min_month], [monthly_avg[min_month]], color='green',
                  s=200, zorder=5, label=f'Low: ${monthly_avg[min_month]:.2f}')
        ax.legend()

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return self._fig_to_base64(fig)

    def plot_location_heatmap(self, save_path=None):
        """Plot geographic heatmap of prices"""
        fig, ax = plt.subplots(figsize=(12, 8))

        scatter = ax.scatter(self.df['longitude'], self.df['latitude'],
                           c=self.df['price'], s=50, alpha=0.6,
                           cmap='YlOrRd', edgecolors='black', linewidth=0.5)

        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Price ($)', rotation=270, labelpad=20)

        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_title('Geographic Distribution of Airbnb Prices')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return self._fig_to_base64(fig)

    def plot_correlation_heatmap(self, save_path=None):
        """Plot correlation heatmap of numerical features"""
        numeric_cols = ['price', 'bedrooms', 'bathrooms', 'accommodates',
                       'rating', 'reviews_count', 'occupancy_rate']
        corr_data = self.df[numeric_cols].corr()

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_data, annot=True, fmt='.2f', cmap='coolwarm',
                   center=0, square=True, ax=ax,
                   cbar_kws={'label': 'Correlation Coefficient'})
        ax.set_title('Feature Correlation Heatmap')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return self._fig_to_base64(fig)

    def plot_superhost_comparison(self, save_path=None):
        """Compare superhost vs non-superhost prices"""
        fig, ax = plt.subplots(figsize=(10, 6))

        superhost_data = [
            self.df[self.df['is_superhost'] == 0]['price'],
            self.df[self.df['is_superhost'] == 1]['price']
        ]

        bp = ax.boxplot(superhost_data, labels=['Regular Host', 'Superhost'],
                       patch_artist=True)

        colors = ['lightblue', 'lightcoral']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)

        ax.set_ylabel('Price ($)')
        ax.set_title('Price Comparison: Regular Host vs Superhost')
        ax.grid(True, alpha=0.3)

        # Add mean values
        means = [data.mean() for data in superhost_data]
        for i, mean in enumerate(means):
            ax.text(i+1, mean, f'${mean:.2f}', ha='center',
                   va='bottom', fontweight='bold')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return self._fig_to_base64(fig)

    def create_interactive_scatter(self):
        """Create interactive scatter plot with Plotly"""
        fig = px.scatter(self.df, x='bedrooms', y='price',
                        color='property_type', size='accommodates',
                        hover_data=['rating', 'reviews_count'],
                        title='Price vs Bedrooms by Property Type',
                        labels={'bedrooms': 'Number of Bedrooms',
                               'price': 'Price ($)'},
                        template='plotly_white')

        return fig.to_json()

    def create_revenue_projection_chart(self, monthly_revenues):
        """Create revenue projection chart"""
        df_revenue = pd.DataFrame(monthly_revenues)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df_revenue['month_name'],
            y=df_revenue['revenue'],
            name='Monthly Revenue',
            marker_color='steelblue',
            text=df_revenue['revenue'].apply(lambda x: f'${x:,.0f}'),
            textposition='auto'
        ))

        fig.add_trace(go.Scatter(
            x=df_revenue['month_name'],
            y=df_revenue['occupancy_rate'],
            name='Occupancy Rate (%)',
            yaxis='y2',
            mode='lines+markers',
            marker=dict(size=8, color='red'),
            line=dict(width=2, color='red')
        ))

        fig.update_layout(
            title='Projected Monthly Revenue and Occupancy Rate',
            xaxis=dict(title='Month'),
            yaxis=dict(title='Revenue ($)', side='left'),
            yaxis2=dict(title='Occupancy Rate (%)', side='right',
                       overlaying='y', showgrid=False),
            template='plotly_white',
            hovermode='x unified',
            legend=dict(x=0.01, y=0.99)
        )

        return fig.to_json()

    def create_pricing_strategy_chart(self, monthly_prices):
        """Create pricing strategy chart"""
        df_prices = pd.DataFrame(monthly_prices)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_prices['month_name'],
            y=df_prices['recommended_price'],
            name='Recommended Price',
            mode='lines+markers',
            marker=dict(size=10, color='darkblue'),
            line=dict(width=3, color='darkblue')
        ))

        fig.add_trace(go.Scatter(
            x=df_prices['month_name'],
            y=df_prices['market_average'],
            name='Market Average',
            mode='lines+markers',
            marker=dict(size=8, color='gray'),
            line=dict(width=2, color='gray', dash='dash')
        ))

        fig.update_layout(
            title='Monthly Pricing Strategy vs Market Average',
            xaxis=dict(title='Month'),
            yaxis=dict(title='Nightly Price ($)'),
            template='plotly_white',
            hovermode='x unified',
            legend=dict(x=0.01, y=0.99)
        )

        return fig.to_json()

    def _fig_to_base64(self, fig):
        """Convert matplotlib figure to base64 string"""
        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        return f"data:image/png;base64,{image_base64}"

    def generate_all_visualizations(self, output_dir='./output'):
        """Generate all visualizations and save them"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        visualizations = {}

        print("Generating visualizations...")

        print("  - Price distribution...")
        visualizations['price_distribution'] = self.plot_price_distribution(
            f'{output_dir}/price_distribution.png'
        )

        print("  - Price by property type...")
        visualizations['price_by_property_type'] = self.plot_price_by_property_type(
            f'{output_dir}/price_by_property_type.png'
        )

        print("  - Price by bedrooms...")
        visualizations['price_by_bedrooms'] = self.plot_price_by_bedrooms(
            f'{output_dir}/price_by_bedrooms.png'
        )

        print("  - Monthly trends...")
        visualizations['monthly_trends'] = self.plot_monthly_trends(
            f'{output_dir}/monthly_trends.png'
        )

        print("  - Location heatmap...")
        visualizations['location_heatmap'] = self.plot_location_heatmap(
            f'{output_dir}/location_heatmap.png'
        )

        print("  - Correlation heatmap...")
        visualizations['correlation_heatmap'] = self.plot_correlation_heatmap(
            f'{output_dir}/correlation_heatmap.png'
        )

        print("  - Superhost comparison...")
        visualizations['superhost_comparison'] = self.plot_superhost_comparison(
            f'{output_dir}/superhost_comparison.png'
        )

        print("  - Interactive scatter...")
        visualizations['interactive_scatter'] = self.create_interactive_scatter()

        print(f"\nAll visualizations saved to {output_dir}/")

        return visualizations
