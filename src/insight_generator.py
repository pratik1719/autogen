"""
Insight Generator Module
Uses LLM to generate insights based on VERIFIED statistical facts
Prevents hallucination by only allowing LLM to interpret provided data
"""
from typing import Dict, Any, List
from llm_client import LLMClient


class InsightGenerator:
    """Generates human-readable insights from analysis results"""
    
    def __init__(self, llm_client: LLMClient):
        """
        Initialize insight generator.
        
        Args:
            llm_client: Instance of LLMClient
        """
        self.llm = llm_client
    
    def generate_insights(self, facts: str, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate insights from verified facts.
        
        Args:
            facts: Formatted string of verified statistical facts
            analysis_results: Complete analysis results dictionary
        
        Returns:
            Dictionary with insights and limitations
        """
        print("\n💡 Generating insights with LLM...")
        
        prompt = f"""You are a data scientist writing insights from an exploratory data analysis.

VERIFIED STATISTICAL FACTS:
{facts}

Based ONLY on these verified facts above, generate:

1. **Key Insights** (5-10 bullet points):
   - Each insight must reference specific columns and specific numbers from the facts
   - Focus on: distributions, patterns, outliers, correlations, missing data patterns
   - Be specific, not generic (BAD: "there are outliers" GOOD: "Column X has 156 outliers (15.6% of data)")
   - Avoid statements not supported by the facts

2. **Data Quality & Limitations** (3-5 points):
   - Comment on missing data patterns
   - Mention data quality issues found
   - Note any limitations or biases that might exist
   - Suggest what additional data or analysis might be valuable

Return your response in JSON format:
{{
  "key_insights": [
    "Insight 1 with specific numbers and column names",
    "Insight 2 with specific patterns observed",
    ...
  ],
  "data_quality_notes": [
    "Quality note 1",
    "Quality note 2",
    ...
  ],
  "limitations": [
    "Limitation 1",
    "Limitation 2",
    ...
  ],
  "suggested_next_steps": [
    "Suggestion 1",
    "Suggestion 2",
    ...
  ]
}}

CRITICAL: Only reference numbers and facts explicitly provided above. Do not invent statistics."""

        try:
            insights = self.llm.generate_json(prompt, purpose="Insight Generation from Facts")
            
            # Validate insights
            insights = self._validate_insights(insights)
            
            print(f"   ✅ Generated {len(insights.get('key_insights', []))} key insights")
            return insights
        
        except Exception as e:
            print(f"   ⚠️  Error generating insights: {e}")
            return self._generate_fallback_insights(analysis_results)
    
    def _validate_insights(self, insights: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean up LLM-generated insights."""
        # Ensure all required keys exist
        required_keys = ['key_insights', 'data_quality_notes', 'limitations']
        for key in required_keys:
            if key not in insights:
                insights[key] = []
        
        # Ensure insights are lists
        for key in required_keys:
            if not isinstance(insights[key], list):
                insights[key] = []
        
        # Optional: suggested_next_steps
        if 'suggested_next_steps' not in insights:
            insights['suggested_next_steps'] = []
        
        return insights
    
    def _generate_fallback_insights(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate basic insights if LLM fails."""
        insights = {
            'key_insights': [],
            'data_quality_notes': [],
            'limitations': [],
            'suggested_next_steps': []
        }
        
        # Basic insights from overview
        overview = analysis_results.get('overview', {})
        insights['key_insights'].append(
            f"Dataset contains {overview.get('total_rows', 0):,} rows and "
            f"{overview.get('total_columns', 0)} columns"
        )
        
        # Data quality insights
        quality = analysis_results.get('data_quality', {})
        if quality.get('high_missing_columns'):
            insights['data_quality_notes'].append(
                f"Found {len(quality['high_missing_columns'])} columns with >50% missing data"
            )
        
        if quality.get('duplicate_rows', 0) > 0:
            insights['data_quality_notes'].append(
                f"Dataset contains {overview.get('duplicate_rows', 0)} duplicate rows"
            )
        
        # Limitations
        insights['limitations'].append(
            "Analysis is limited to basic descriptive statistics"
        )
        insights['limitations'].append(
            "Missing data patterns may indicate sampling bias"
        )
        
        return insights
    
    def generate_summary(self, dataset_name: str, insights: Dict[str, Any]) -> str:
        """
        Generate a short executive summary.
        
        Args:
            dataset_name: Name of the dataset
            insights: Generated insights dictionary
        
        Returns:
            Executive summary text
        """
        print("\n📝 Generating executive summary...")
        
        key_insights_text = "\n".join(f"- {insight}" for insight in insights.get('key_insights', [])[:3])
        
        prompt = f"""Write a 2-3 sentence executive summary for an exploratory data analysis report.

DATASET: {dataset_name}

TOP INSIGHTS:
{key_insights_text}

Write a concise summary that captures the essence of what we learned about this dataset.
Make it professional and informative. Return ONLY the summary text, no JSON."""

        try:
            summary = self.llm.generate(
                prompt, 
                purpose="Executive Summary Generation",
                temperature=0.7
            )
            
            return summary.strip()
        
        except Exception as e:
            print(f"   ⚠️  Error generating summary: {e}")
            return f"Exploratory analysis of {dataset_name} revealing key patterns in the data."


# Test
if __name__ == "__main__":
    # Mock facts
    mock_facts = """
- Dataset has 1,000 rows and 5 columns
- Column 'age': mean=45.2, median=44.0, std=15.3
- Column 'age' has 23 outliers (2.3% of data)
- Column 'income': mean=52,340, median=50,200, std=18,750
- Strong correlation between 'age' and 'income': r=0.78
- Column 'category' has 3 unique values
- Most frequent value in 'category': 'A' (45.2%)
"""
    
    try:
        client = LLMClient()
        generator = InsightGenerator(client)
        insights = generator.generate_insights(mock_facts, {})
        
        print("\n💡 Generated Insights:")
        import json
        print(json.dumps(insights, indent=2))
    except Exception as e:
        print(f"Error: {e}")
