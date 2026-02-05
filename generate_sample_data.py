"""
Generate sample datasets for testing AutoGen-EDA
Run this if you want to test without downloading real datasets
"""
import pandas as pd
import numpy as np
from pathlib import Path


def generate_health_survey_data(n_rows=5000):
    """Generate sample health survey dataset (categorical-heavy)."""
    print("📊 Generating sample health survey dataset...")
    
    np.random.seed(42)
    
    states = ['California', 'Texas', 'Florida', 'New York', 'Pennsylvania', 
              'Illinois', 'Ohio', 'Georgia', 'North Carolina', 'Michigan']
    
    age_groups = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
    
    education = ['Less than HS', 'High School', 'Some College', 
                'College Graduate', 'Graduate Degree']
    
    health_status = ['Excellent', 'Very Good', 'Good', 'Fair', 'Poor']
    
    exercise_levels = ['None', 'Light', 'Moderate', 'Heavy']
    
    data = {
        'state': np.random.choice(states, n_rows),
        'age_group': np.random.choice(age_groups, n_rows),
        'gender': np.random.choice(['Male', 'Female', 'Other'], n_rows, p=[0.48, 0.5, 0.02]),
        'education_level': np.random.choice(education, n_rows, p=[0.1, 0.25, 0.3, 0.25, 0.1]),
        'health_status': np.random.choice(health_status, n_rows, p=[0.15, 0.25, 0.35, 0.15, 0.1]),
        'bmi': np.random.normal(27, 5, n_rows).clip(15, 50),
        'exercise_level': np.random.choice(exercise_levels, n_rows, p=[0.3, 0.3, 0.3, 0.1]),
        'hours_sleep': np.random.normal(7, 1.5, n_rows).clip(3, 12),
        'daily_calories': np.random.normal(2200, 500, n_rows).clip(1000, 4000),
        'has_chronic_disease': np.random.choice([0, 1], n_rows, p=[0.7, 0.3]),
        'smoker': np.random.choice(['Yes', 'No', 'Former'], n_rows, p=[0.15, 0.7, 0.15]),
        'drinks_per_week': np.random.poisson(3, n_rows).clip(0, 20),
        'satisfaction_score': np.random.randint(1, 11, n_rows)
    }
    
    df = pd.DataFrame(data)
    
    # Add some missing values
    for col in ['bmi', 'hours_sleep', 'daily_calories', 'drinks_per_week']:
        mask = np.random.random(n_rows) < 0.05
        df.loc[mask, col] = np.nan
    
    # Round numeric columns
    df['bmi'] = df['bmi'].round(1)
    df['hours_sleep'] = df['hours_sleep'].round(1)
    df['daily_calories'] = df['daily_calories'].round(0)
    
    return df


def generate_sales_data(n_rows=3000):
    """Generate sample sales dataset (numeric-heavy)."""
    print("📊 Generating sample sales dataset...")
    
    np.random.seed(42)
    
    products = ['Product_A', 'Product_B', 'Product_C', 'Product_D', 'Product_E']
    regions = ['North', 'South', 'East', 'West']
    channels = ['Online', 'Retail', 'Wholesale']
    
    # Generate dates
    dates = pd.date_range('2023-01-01', periods=n_rows, freq='h')
    
    data = {
        'date': dates,
        'product': np.random.choice(products, n_rows),
        'region': np.random.choice(regions, n_rows),
        'channel': np.random.choice(channels, n_rows, p=[0.5, 0.3, 0.2]),
        'units_sold': np.random.poisson(15, n_rows).clip(1, 100),
        'unit_price': np.random.normal(50, 15, n_rows).clip(10, 200),
        'discount_percent': np.random.choice([0, 5, 10, 15, 20, 25], n_rows, p=[0.4, 0.2, 0.2, 0.1, 0.05, 0.05]),
        'shipping_cost': np.random.normal(8, 3, n_rows).clip(2, 25),
        'customer_rating': np.random.choice([1, 2, 3, 4, 5], n_rows, p=[0.05, 0.1, 0.15, 0.35, 0.35]),
        'returns': np.random.choice([0, 1], n_rows, p=[0.95, 0.05])
    }
    
    df = pd.DataFrame(data)
    
    # Calculate derived columns
    df['revenue'] = df['units_sold'] * df['unit_price'] * (1 - df['discount_percent']/100)
    df['profit'] = df['revenue'] - (df['units_sold'] * df['unit_price'] * 0.6) - df['shipping_cost']
    
    # Add some missing values
    mask = np.random.random(n_rows) < 0.03
    df.loc[mask, 'customer_rating'] = np.nan
    
    # Round numeric columns
    df['unit_price'] = df['unit_price'].round(2)
    df['shipping_cost'] = df['shipping_cost'].round(2)
    df['revenue'] = df['revenue'].round(2)
    df['profit'] = df['profit'].round(2)
    
    return df


def main():
    """Generate and save sample datasets."""
    print("="*80)
    print("🎲 Sample Dataset Generator for AutoGen-EDA")
    print("="*80 + "\n")
    
    # Create data directory if it doesn't exist
    Path('data').mkdir(exist_ok=True)
    
    # Generate datasets
    health_df = generate_health_survey_data()
    sales_df = generate_sales_data()
    
    # Save to CSV
    health_path = 'data/sample_health_survey.csv'
    sales_path = 'data/sample_sales_data.csv'
    
    health_df.to_csv(health_path, index=False)
    print(f"   ✅ Saved: {health_path}")
    print(f"      Shape: {health_df.shape[0]:,} rows × {health_df.shape[1]} columns")
    
    sales_df.to_csv(sales_path, index=False)
    print(f"   ✅ Saved: {sales_path}")
    print(f"      Shape: {sales_df.shape[0]:,} rows × {sales_df.shape[1]} columns")
    
    print("\n" + "="*80)
    print("✅ Sample datasets generated successfully!")
    print("="*80)
    print("\nYou can now test AutoGen-EDA with:")
    print(f"  python src/main.py {health_path}")
    print(f"  python src/main.py {sales_path}")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
