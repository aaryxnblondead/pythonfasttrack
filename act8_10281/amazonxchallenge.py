
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load datasets
events_df = pd.read_csv('amazon_events_data.csv')
users_df = pd.read_csv('amazon_users_data.csv')
products_df = pd.read_csv('amazon_products_data.csv')

# Data preprocessing
events_df['timestamp'] = pd.to_datetime(events_df['timestamp'])
events_df['month'] = events_df['timestamp'].dt.month
events_df['season'] = pd.cut(events_df['timestamp'].dt.month, 
                            bins=[0,3,6,9,12], 
                            labels=['Winter', 'Spring', 'Summer', 'Fall'])

# 1. Popular Category Analysis
def analyze_popular_categories():
    category_counts = pd.merge(events_df, products_df, on='product_id')['category'].value_counts()
    
    plt.figure(figsize=(12,6))
    category_counts.plot(kind='bar')
    plt.title('Most Popular Product Categories')
    plt.xlabel('Category')
    plt.ylabel('Number of Interactions')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('category_popularity.png')

# 2. Cart Abandonment Analysis
def analyze_cart_abandonment():
    cart_events = events_df[events_df['event_type'].isin(['add_to_cart', 'purchase'])]
    cart_analysis = cart_events.groupby(['product_id', 'event_type']).size().unstack()
    cart_analysis['abandonment_rate'] = 1 - (cart_analysis['purchase'] / cart_analysis['add_to_cart'])
    
    return cart_analysis.sort_values('abandonment_rate', ascending=False)

# 3. Seasonal Trends
def analyze_seasonal_trends():
    seasonal_purchases = events_df[events_df['event_type'] == 'purchase'].groupby('season', observed=True).size()
    
    plt.figure(figsize=(10,6))
    seasonal_purchases.plot(kind='bar')
    plt.title('Purchase Trends by Season')
    plt.xlabel('Season')
    plt.ylabel('Number of Purchases')
    plt.tight_layout()
    plt.savefig('seasonal_trends.png')

# Recommendation System
class AmazonRecommender:
    def __init__(self, events_df, products_df):
        self.events_df = events_df
        self.products_df = products_df
        
    def get_user_preferences(self, user_id):
        user_events = self.events_df[self.events_df['user_id'] == user_id]
        user_products = pd.merge(user_events, self.products_df, on='product_id')
        return user_products['category'].value_counts()
    
    def recommend_products(self, user_id, n_recommendations=5):
        # Get user's preferred categories
        preferred_categories = self.get_user_preferences(user_id)
        
        # Filter products from preferred categories
        recommendations = self.products_df[
            (self.products_df['category'].isin(preferred_categories.index)) &
            (self.products_df['rating'] >= 4.0) &
            (self.products_df['prime_eligible'] == True)
        ]
        
        # Sort by rating and review count
        recommendations['score'] = recommendations['rating'] * np.log1p(recommendations['review_count'])
        return recommendations.nlargest(n_recommendations, 'score')

def main():
    # Run analyses
    analyze_popular_categories()
    cart_abandonment = analyze_cart_abandonment()
    analyze_seasonal_trends()
    
    # Initialize recommender
    recommender = AmazonRecommender(events_df, products_df)
    
    # Example recommendation for a user
    sample_user_id = events_df['user_id'].iloc[0]
    recommendations = recommender.recommend_products(sample_user_id)
    
    # Print insights
    print("\nTop Product Recommendations for User:", sample_user_id)
    print(recommendations[['product_name', 'category', 'rating', 'prime_price']].to_string())
    
    print("\nCart Abandonment Insights:")
    print(cart_abandonment.head().to_string())

if __name__ == "__main__":
    main()
