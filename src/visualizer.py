"""
Visualizer Module
Creates visualizations based on EDA plan and analysis results
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, List
import os
from utils import sanitize_filename, infer_column_types


class DataVisualizer:
    """Creates visualizations for EDA"""
    
    def __init__(self, df: pd.DataFrame, output_dir: str = "output"):
        """
        Initialize visualizer.
        
        Args:
            df: DataFrame to visualize
            output_dir: Directory to save plots
        """
        self.df = df
        self.output_dir = output_dir
        self.column_types = infer_column_types(df)
        self.plot_paths = []
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['font.size'] = 10
        
        os.makedirs(output_dir, exist_ok=True)
    
    def create_all_plots(self, plan: Dict[str, Any] = None) -> List[str]:
        """
        Create all visualizations.
        
        Args:
            plan: Optional EDA plan with recommended visualizations
        
        Returns:
            List of paths to saved plots
        """
        print("\n📈 Creating visualizations...")
        
        if plan and 'recommended_visualizations' in plan:
            # Use LLM-recommended visualizations
            for viz in plan['recommended_visualizations']:
                self._create_plot_from_spec(viz)
        else:
            # Fallback: create default plots
            self._create_default_plots()
        
        print(f"   ✅ Created {len(self.plot_paths)} plots")
        return self.plot_paths
    
    def _create_plot_from_spec(self, spec: Dict[str, Any]):
        """Create a plot from LLM specification."""
        try:
            plot_type = spec.get('type', '').lower()
            
            if plot_type == 'histogram':
                self._plot_histogram(spec)
            elif plot_type == 'boxplot':
                self._plot_boxplot(spec)
            elif plot_type == 'bar':
                self._plot_bar(spec)
            elif plot_type == 'scatter':
                self._plot_scatter(spec)
            elif plot_type == 'correlation_heatmap':
                self._plot_correlation_heatmap(spec)
            else:
                print(f"   ⚠️  Unknown plot type: {plot_type}")
        
        except Exception as e:
            print(f"   ⚠️  Error creating {spec.get('type')} plot: {e}")
    
    def _plot_histogram(self, spec: Dict[str, Any]):
        """Create histogram."""
        col = spec.get('column')
        if col not in self.df.columns:
            return
        
        plt.figure(figsize=(10, 6))
        
        data = self.df[col].dropna()
        plt.hist(data, bins=30, edgecolor='black', alpha=0.7, color='skyblue')
        
        plt.title(spec.get('title', f'Distribution of {col}'))
        plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.grid(axis='y', alpha=0.3)
        
        # Add mean and median lines
        mean_val = data.mean()
        median_val = data.median()
        plt.axvline(mean_val, color='red', linestyle='--', label=f'Mean: {mean_val:.2f}')
        plt.axvline(median_val, color='green', linestyle='--', label=f'Median: {median_val:.2f}')
        plt.legend()
        
        filename = f"histogram_{sanitize_filename(col)}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.tight_layout()
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        self.plot_paths.append(filepath)
    
    def _plot_boxplot(self, spec: Dict[str, Any]):
        """Create boxplot."""
        col = spec.get('column')
        if col not in self.df.columns:
            return
        
        plt.figure(figsize=(10, 6))
        
        data = self.df[col].dropna()
        plt.boxplot(data, vert=True, patch_artist=True,
                   boxprops=dict(facecolor='lightblue', alpha=0.7),
                   medianprops=dict(color='red', linewidth=2))
        
        plt.title(spec.get('title', f'Boxplot of {col}'))
        plt.ylabel(col)
        plt.grid(axis='y', alpha=0.3)
        
        filename = f"boxplot_{sanitize_filename(col)}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.tight_layout()
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        self.plot_paths.append(filepath)
    
    def _plot_bar(self, spec: Dict[str, Any]):
        """Create bar chart."""
        col = spec.get('column')
        if col not in self.df.columns:
            return
        
        plt.figure(figsize=(12, 6))
        
        value_counts = self.df[col].value_counts().head(20)
        
        # Use horizontal bar if many categories
        if len(value_counts) > 10:
            value_counts.plot(kind='barh', color='steelblue', alpha=0.8)
            plt.xlabel('Count')
            plt.ylabel(col)
        else:
            value_counts.plot(kind='bar', color='steelblue', alpha=0.8)
            plt.xlabel(col)
            plt.ylabel('Count')
            plt.xticks(rotation=45, ha='right')
        
        plt.title(spec.get('title', f'Frequency of {col}'))
        plt.grid(axis='y' if len(value_counts) <= 10 else 'x', alpha=0.3)
        
        filename = f"bar_{sanitize_filename(col)}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.tight_layout()
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        self.plot_paths.append(filepath)
    
    def _plot_scatter(self, spec: Dict[str, Any]):
        """Create scatter plot."""
        x_col = spec.get('x')
        y_col = spec.get('y')
        
        if x_col not in self.df.columns or y_col not in self.df.columns:
            return
        
        plt.figure(figsize=(10, 6))
        
        # Remove NaN values
        plot_data = self.df[[x_col, y_col]].dropna()
        
        plt.scatter(plot_data[x_col], plot_data[y_col], alpha=0.5, s=30, color='steelblue')
        
        # Add regression line
        if len(plot_data) > 2:
            z = np.polyfit(plot_data[x_col], plot_data[y_col], 1)
            p = np.poly1d(z)
            plt.plot(plot_data[x_col], p(plot_data[x_col]), "r--", alpha=0.8, linewidth=2)
        
        plt.title(spec.get('title', f'{x_col} vs {y_col}'))
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.grid(alpha=0.3)
        
        filename = f"scatter_{sanitize_filename(x_col)}_vs_{sanitize_filename(y_col)}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.tight_layout()
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        self.plot_paths.append(filepath)
    
    def _plot_correlation_heatmap(self, spec: Dict[str, Any]):
        """Create correlation heatmap."""
        columns = spec.get('columns', [])
        
        # If no columns specified, use all numeric columns
        if not columns:
            columns = [col for col, ctype in self.column_types.items() 
                      if ctype == 'numeric']
        
        # Filter to only columns that exist
        columns = [col for col in columns if col in self.df.columns]
        
        if len(columns) < 2:
            return
        
        plt.figure(figsize=(12, 10))
        
        corr_matrix = self.df[columns].corr()
        
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', 
                   cmap='coolwarm', center=0, square=True,
                   linewidths=1, cbar_kws={"shrink": 0.8})
        
        plt.title(spec.get('title', 'Correlation Matrix'))
        
        filename = "correlation_heatmap.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.tight_layout()
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        self.plot_paths.append(filepath)
    
    def _create_default_plots(self):
        """Create default set of plots if no plan provided."""
        numeric_cols = [col for col, ctype in self.column_types.items() 
                       if ctype == 'numeric']
        categorical_cols = [col for col, ctype in self.column_types.items() 
                          if ctype in ['categorical', 'binary']]
        
        # Histograms for numeric columns
        for col in numeric_cols[:3]:
            self._plot_histogram({'column': col, 'title': f'Distribution of {col}'})
        
        # Boxplots for numeric columns
        for col in numeric_cols[:2]:
            self._plot_boxplot({'column': col, 'title': f'Outliers in {col}'})
        
        # Bar charts for categorical columns
        for col in categorical_cols[:2]:
            self._plot_bar({'column': col, 'title': f'Frequency of {col}'})
        
        # Correlation heatmap if we have numeric columns
        if len(numeric_cols) >= 2:
            self._plot_correlation_heatmap({
                'columns': numeric_cols[:10],
                'title': 'Correlation Matrix'
            })


# Test
if __name__ == "__main__":
    # Create sample data
    df = pd.DataFrame({
        'age': np.random.randint(18, 80, 1000),
        'income': np.random.normal(50000, 20000, 1000),
        'category': np.random.choice(['A', 'B', 'C'], 1000),
        'score': np.random.uniform(0, 100, 1000)
    })
    
    viz = DataVisualizer(df)
    plot_paths = viz.create_all_plots()
    
    print(f"\n✅ Created {len(plot_paths)} plots:")
    for path in plot_paths:
        print(f"   - {path}")
