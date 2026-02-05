"""
Analyzer Module
Performs statistical analysis on the dataset
NO LLM - only verified computations
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple
from scipy import stats
from utils import safe_percentage, format_number, infer_column_types


class DataAnalyzer:
    """Performs statistical analysis on datasets"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize analyzer.
        
        Args:
            df: DataFrame to analyze
        """
        self.df = df
        self.column_types = infer_column_types(df)
        self.results = {}
    
    def analyze_all(self, plan: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Run complete analysis.
        
        Args:
            plan: Optional EDA plan from LLM
        
        Returns:
            Dictionary of all analysis results
        """
        print("\n📊 Running statistical analysis...")
        
        self.results = {
            'overview': self._get_overview(),
            'data_quality': self._check_data_quality(),
            'categorical_analysis': self._analyze_categorical(),
            'numeric_analysis': self._analyze_numeric(),
            'relationships': self._analyze_relationships()
        }
        
        print("   ✅ Analysis complete")
        return self.results
    
    def _get_overview(self) -> Dict[str, Any]:
        """Get dataset overview."""
        return {
            'total_rows': int(self.df.shape[0]),
            'total_columns': int(self.df.shape[1]),
            'total_cells': int(self.df.shape[0] * self.df.shape[1]),
            'memory_usage_mb': float(self.df.memory_usage(deep=True).sum() / 1024**2),
            'duplicate_rows': int(self.df.duplicated().sum()),
            'column_types': self.column_types
        }
    
    def _check_data_quality(self) -> Dict[str, Any]:
        """Check data quality issues."""
        quality = {
            'missing_by_column': {},
            'high_missing_columns': [],
            'constant_columns': [],
            'high_cardinality_columns': []
        }
        
        for col in self.df.columns:
            missing_count = int(self.df[col].isna().sum())
            missing_pct = safe_percentage(missing_count, len(self.df))
            
            quality['missing_by_column'][col] = {
                'count': missing_count,
                'percentage': round(missing_pct, 2)
            }
            
            # Flag high missing (>50%)
            if missing_pct > 50:
                quality['high_missing_columns'].append({
                    'column': col,
                    'missing_pct': round(missing_pct, 2)
                })
            
            # Check for constant columns
            if self.df[col].nunique() == 1:
                quality['constant_columns'].append(col)
            
            # Check for high cardinality
            if self.column_types[col] in ['categorical', 'text']:
                unique_ratio = self.df[col].nunique() / len(self.df)
                if unique_ratio > 0.9:
                    quality['high_cardinality_columns'].append({
                        'column': col,
                        'unique_count': int(self.df[col].nunique()),
                        'unique_ratio': round(unique_ratio, 3)
                    })
        
        return quality
    
    def _analyze_categorical(self) -> Dict[str, Any]:
        """Analyze categorical columns."""
        categorical_cols = [col for col, ctype in self.column_types.items() 
                           if ctype in ['categorical', 'binary']]
        
        results = {}
        
        for col in categorical_cols[:5]:  # Limit to top 5
            value_counts = self.df[col].value_counts()
            total = len(self.df[col].dropna())
            
            results[col] = {
                'unique_values': int(self.df[col].nunique()),
                'most_frequent': {
                    'value': str(value_counts.index[0]) if len(value_counts) > 0 else None,
                    'count': int(value_counts.iloc[0]) if len(value_counts) > 0 else 0,
                    'percentage': round(safe_percentage(value_counts.iloc[0], total), 2) if len(value_counts) > 0 else 0
                },
                'value_distribution': [
                    {
                        'value': str(val),
                        'count': int(count),
                        'percentage': round(safe_percentage(count, total), 2)
                    }
                    for val, count in value_counts.head(10).items()
                ]
            }
        
        return results
    
    def _analyze_numeric(self) -> Dict[str, Any]:
        """Analyze numeric columns."""
        numeric_cols = [col for col, ctype in self.column_types.items() 
                       if ctype == 'numeric']
        
        results = {}
        
        for col in numeric_cols[:10]:  # Analyze up to 10 numeric columns
            col_data = self.df[col].dropna()
            
            if len(col_data) == 0:
                continue
            
            # Basic statistics
            results[col] = {
                'count': int(len(col_data)),
                'mean': float(col_data.mean()),
                'median': float(col_data.median()),
                'std': float(col_data.std()),
                'min': float(col_data.min()),
                'max': float(col_data.max()),
                'q25': float(col_data.quantile(0.25)),
                'q75': float(col_data.quantile(0.75))
            }
            
            # IQR and outliers
            q1 = results[col]['q25']
            q3 = results[col]['q75']
            iqr = q3 - q1
            
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
            
            results[col]['outliers'] = {
                'count': int(len(outliers)),
                'percentage': round(safe_percentage(len(outliers), len(col_data)), 2),
                'lower_bound': float(lower_bound),
                'upper_bound': float(upper_bound)
            }
            
            # Skewness and kurtosis
            results[col]['skewness'] = float(stats.skew(col_data))
            results[col]['kurtosis'] = float(stats.kurtosis(col_data))
        
        return results
    
    def _analyze_relationships(self) -> Dict[str, Any]:
        """Analyze relationships between columns."""
        numeric_cols = [col for col, ctype in self.column_types.items() 
                       if ctype == 'numeric']
        
        results = {}
        
        # Correlation matrix for numeric columns
        if len(numeric_cols) >= 2:
            corr_matrix = self.df[numeric_cols].corr()
            
            # Find strong correlations (|r| > 0.5)
            strong_correlations = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_val = corr_matrix.iloc[i, j]
                    if abs(corr_val) > 0.5 and not np.isnan(corr_val):
                        strong_correlations.append({
                            'column1': corr_matrix.columns[i],
                            'column2': corr_matrix.columns[j],
                            'correlation': round(float(corr_val), 3)
                        })
            
            results['correlations'] = {
                'matrix': corr_matrix.round(3).to_dict(),
                'strong_correlations': sorted(
                    strong_correlations,
                    key=lambda x: abs(x['correlation']),
                    reverse=True
                )[:10]  # Top 10
            }
        
        return results
    
    def get_facts_for_llm(self) -> str:
        """
        Format analysis results as facts for LLM insight generation.
        This ensures LLM doesn't hallucinate numbers.
        
        Returns:
            Formatted string of verified facts
        """
        facts = []
        
        # Overview facts
        facts.append(f"Dataset has {format_number(self.results['overview']['total_rows'])} rows and {self.results['overview']['total_columns']} columns")
        facts.append(f"Total of {format_number(self.results['overview']['total_cells'])} cells")
        
        if self.results['overview']['duplicate_rows'] > 0:
            facts.append(f"Found {format_number(self.results['overview']['duplicate_rows'])} duplicate rows")
        
        # Data quality facts
        quality = self.results['data_quality']
        
        if quality['high_missing_columns']:
            for item in quality['high_missing_columns'][:3]:
                facts.append(f"Column '{item['column']}' has {item['missing_pct']}% missing values")
        
        if quality['constant_columns']:
            facts.append(f"Constant columns (single value): {', '.join(quality['constant_columns'][:5])}")
        
        # Categorical facts
        for col, info in list(self.results['categorical_analysis'].items())[:3]:
            facts.append(f"Column '{col}' has {format_number(info['unique_values'])} unique values")
            if info['most_frequent']['value']:
                facts.append(
                    f"Most frequent value in '{col}': '{info['most_frequent']['value']}' "
                    f"({info['most_frequent']['percentage']}%)"
                )
        
        # Numeric facts
        for col, info in list(self.results['numeric_analysis'].items())[:5]:
            facts.append(
                f"Column '{col}': mean={format_number(info['mean'])}, "
                f"median={format_number(info['median'])}, "
                f"std={format_number(info['std'])}"
            )
            
            if info['outliers']['count'] > 0:
                facts.append(
                    f"Column '{col}' has {format_number(info['outliers']['count'])} outliers "
                    f"({info['outliers']['percentage']}% of data)"
                )
        
        # Correlation facts
        if 'correlations' in self.results['relationships']:
            for corr in self.results['relationships']['correlations']['strong_correlations'][:5]:
                facts.append(
                    f"Strong correlation between '{corr['column1']}' and '{corr['column2']}': "
                    f"r={corr['correlation']}"
                )
        
        return "\n".join(f"- {fact}" for fact in facts)


# Test
if __name__ == "__main__":
    # Create sample data
    df = pd.DataFrame({
        'age': np.random.randint(18, 80, 1000),
        'income': np.random.normal(50000, 20000, 1000),
        'category': np.random.choice(['A', 'B', 'C'], 1000),
        'score': np.random.uniform(0, 100, 1000)
    })
    
    analyzer = DataAnalyzer(df)
    results = analyzer.analyze_all()
    
    print("\n📊 Analysis Results:")
    print(json.dumps(results, indent=2, default=str))
