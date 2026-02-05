"""
EDA Planner Module
Uses LLM to generate a custom analysis strategy based on dataset characteristics
"""
import json
from typing import Dict, Any, List
from llm_client import LLMClient


class EDAPlanner:
    """Generates custom EDA strategy using LLM"""
    
    def __init__(self, llm_client: LLMClient):
        """
        Initialize EDA Planner.
        
        Args:
            llm_client: Instance of LLMClient
        """
        self.llm = llm_client
    
    def generate_analysis_plan(self, profile: Dict[str, Any], 
                              schema: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate custom EDA plan based on dataset profile.
        
        Args:
            profile: Dataset profile from DataLoader
            schema: Optional schema information
        
        Returns:
            Analysis plan dictionary
        """
        print("\n🧠 Generating EDA strategy with LLM...")
        
        # Build context for LLM
        context = self._build_context(profile, schema)
        
        # Create prompt
        prompt = f"""You are an expert data scientist. Analyze this dataset profile and create a comprehensive EDA plan.

DATASET PROFILE:
{json.dumps(context, indent=2)}

Generate a detailed EDA plan in JSON format with the following structure:

{{
  "dataset_type": "categorical-heavy | numeric-heavy | mixed | time-series",
  "key_columns": {{
    "categorical": ["col1", "col2"],
    "numeric": ["col3", "col4"],
    "datetime": ["col5"],
    "potential_target": "col_name or null"
  }},
  "recommended_analyses": {{
    "categorical": [
      {{"column": "col1", "analysis": "frequency_distribution", "reason": "why"}},
      {{"column": "col2", "analysis": "value_counts", "reason": "why"}}
    ],
    "numeric": [
      {{"column": "col3", "analysis": "distribution_outliers", "reason": "why"}},
      {{"column": "col4", "analysis": "correlation_analysis", "reason": "why"}}
    ],
    "relationships": [
      {{"columns": ["col1", "col3"], "analysis": "group_statistics", "reason": "why"}},
      {{"columns": ["col3", "col4"], "analysis": "correlation", "reason": "why"}}
    ]
  }},
  "recommended_visualizations": [
    {{"type": "histogram", "column": "col3", "title": "Distribution of col3"}},
    {{"type": "boxplot", "column": "col3", "title": "Outliers in col3"}},
    {{"type": "bar", "column": "col1", "title": "Frequency of col1"}},
    {{"type": "correlation_heatmap", "columns": ["col3", "col4"], "title": "Correlation Matrix"}},
    {{"type": "scatter", "x": "col3", "y": "col4", "title": "col3 vs col4"}}
  ],
  "data_quality_checks": [
    "check_duplicates",
    "check_high_missing_columns",
    "check_constant_columns",
    "check_high_cardinality"
  ],
  "expected_insights": [
    "Distribution patterns in key numeric variables",
    "Relationship between categorical and numeric variables",
    "Outliers and anomalies",
    "Missing data patterns"
  ]
}}

Ensure you select AT LEAST 5 visualizations. Focus on the most informative columns.
Respond ONLY with valid JSON."""

        # Get LLM response
        try:
            plan = self.llm.generate_json(prompt, purpose="EDA Strategy Planning")
            
            # Validate plan structure
            plan = self._validate_and_fix_plan(plan, profile)
            
            print("   ✅ EDA plan generated successfully")
            return plan
        
        except Exception as e:
            print(f"   ⚠️  Error generating plan, using fallback: {e}")
            return self._generate_fallback_plan(profile)
    
    def _build_context(self, profile: Dict[str, Any], 
                      schema: Dict[str, Any] = None) -> Dict[str, Any]:
        """Build condensed context for LLM prompt."""
        context = {
            'shape': profile['shape'],
            'missing_percentage': round(profile['missing_summary']['missing_percentage'], 2),
            'columns': {}
        }
        
        # Summarize column info
        for col, info in profile['columns'].items():
            context['columns'][col] = {
                'dtype': info['dtype'],
                'null_pct': round(info['null_percentage'], 2),
                'unique': info['unique_count'],
                'samples': info['sample_values'][:3]
            }
            
            if 'min' in info and 'max' in info:
                context['columns'][col]['range'] = [info['min'], info['max']]
        
        if schema:
            context['schema'] = schema
        
        return context
    
    def _validate_and_fix_plan(self, plan: Dict[str, Any], 
                               profile: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and fix LLM-generated plan."""
        # Ensure required keys exist
        required_keys = ['recommended_visualizations', 'recommended_analyses']
        for key in required_keys:
            if key not in plan:
                plan[key] = []
        
        # Ensure at least 5 visualizations
        if len(plan['recommended_visualizations']) < 5:
            print("   ⚠️  Plan has fewer than 5 visualizations, adding defaults")
            plan = self._generate_fallback_plan(profile)
        
        return plan
    
    def _generate_fallback_plan(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a simple fallback plan if LLM fails."""
        print("   🔄 Generating fallback EDA plan...")
        
        columns = profile['columns']
        
        # Categorize columns
        numeric_cols = [col for col, info in columns.items() 
                       if 'int' in info['dtype'].lower() or 'float' in info['dtype'].lower()]
        categorical_cols = [col for col, info in columns.items() 
                          if col not in numeric_cols and info['unique_count'] < 50]
        
        plan = {
            'dataset_type': 'mixed',
            'key_columns': {
                'categorical': categorical_cols[:5],
                'numeric': numeric_cols[:5]
            },
            'recommended_visualizations': [],
            'recommended_analyses': {
                'categorical': [],
                'numeric': []
            }
        }
        
        # Add visualizations
        for col in numeric_cols[:2]:
            plan['recommended_visualizations'].append({
                'type': 'histogram',
                'column': col,
                'title': f'Distribution of {col}'
            })
            plan['recommended_visualizations'].append({
                'type': 'boxplot',
                'column': col,
                'title': f'Outliers in {col}'
            })
        
        for col in categorical_cols[:2]:
            plan['recommended_visualizations'].append({
                'type': 'bar',
                'column': col,
                'title': f'Frequency of {col}'
            })
        
        if len(numeric_cols) >= 2:
            plan['recommended_visualizations'].append({
                'type': 'correlation_heatmap',
                'columns': numeric_cols[:5],
                'title': 'Correlation Matrix'
            })
        
        # Ensure at least 5 visualizations
        while len(plan['recommended_visualizations']) < 5 and numeric_cols:
            col = numeric_cols[len(plan['recommended_visualizations']) % len(numeric_cols)]
            plan['recommended_visualizations'].append({
                'type': 'histogram',
                'column': col,
                'title': f'Distribution of {col}'
            })
        
        return plan


# Test
if __name__ == "__main__":
    # Mock profile for testing
    mock_profile = {
        'shape': {'rows': 1000, 'columns': 10},
        'columns': {
            'age': {'dtype': 'int64', 'null_percentage': 5.0, 'unique_count': 50},
            'income': {'dtype': 'float64', 'null_percentage': 10.0, 'unique_count': 800},
            'category': {'dtype': 'object', 'null_percentage': 2.0, 'unique_count': 5}
        },
        'missing_summary': {'missing_percentage': 5.5}
    }
    
    try:
        client = LLMClient()
        planner = EDAPlanner(client)
        plan = planner.generate_analysis_plan(mock_profile)
        print(json.dumps(plan, indent=2))
    except Exception as e:
        print(f"Error: {e}")
