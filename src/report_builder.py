"""
Report Builder Module
Assembles all components into beautiful HTML and Markdown reports
"""
import os
import json
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path
import base64


class ReportBuilder:
    """Builds final EDA reports in multiple formats"""
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize report builder.
        
        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def build_reports(self, dataset_name: str, profile: Dict[str, Any],
                     analysis_results: Dict[str, Any], insights: Dict[str, Any],
                     plot_paths: List[str], summary: str = None) -> Dict[str, str]:
        """
        Build both HTML and Markdown reports.
        
        Args:
            dataset_name: Name of the dataset
            profile: Dataset profile
            analysis_results: Statistical analysis results
            insights: LLM-generated insights
            plot_paths: List of paths to plot images
            summary: Executive summary
        
        Returns:
            Dictionary with paths to generated reports
        """
        print("\n📄 Building reports...")
        
        # Generate both formats
        html_path = self._build_html_report(
            dataset_name, profile, analysis_results, insights, plot_paths, summary
        )
        
        md_path = self._build_markdown_report(
            dataset_name, profile, analysis_results, insights, plot_paths, summary
        )
        
        print(f"   ✅ HTML report: {html_path}")
        print(f"   ✅ Markdown report: {md_path}")
        
        return {
            'html': html_path,
            'markdown': md_path
        }
    
    def _build_html_report(self, dataset_name: str, profile: Dict[str, Any],
                          analysis_results: Dict[str, Any], insights: Dict[str, Any],
                          plot_paths: List[str], summary: str = None) -> str:
        """Build HTML report."""
        
        # Read plots as base64 for embedding
        embedded_plots = []
        for plot_path in plot_paths:
            try:
                with open(plot_path, 'rb') as f:
                    img_data = base64.b64encode(f.read()).decode()
                    embedded_plots.append({
                        'name': Path(plot_path).stem.replace('_', ' ').title(),
                        'data': img_data
                    })
            except Exception as e:
                print(f"   ⚠️  Error embedding plot {plot_path}: {e}")
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EDA Report - {dataset_name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0 0 10px 0;
            font-size: 2.5em;
        }}
        .header p {{
            margin: 0;
            opacity: 0.9;
            font-size: 1.1em;
        }}
        .section {{
            background: white;
            padding: 30px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h2 {{
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        h3 {{
            color: #764ba2;
            margin-top: 25px;
        }}
        .metric {{
            display: inline-block;
            background: #f8f9fa;
            padding: 15px 25px;
            margin: 10px 10px 10px 0;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }}
        .metric-label {{
            font-size: 0.9em;
            color: #666;
            display: block;
        }}
        .metric-value {{
            font-size: 1.8em;
            font-weight: bold;
            color: #333;
        }}
        ul {{
            line-height: 1.8;
        }}
        li {{
            margin-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #667eea;
            color: white;
            font-weight: 600;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .plot {{
            margin: 30px 0;
            text-align: center;
        }}
        .plot img {{
            max-width: 100%;
            height: auto;
            border-radius: 5px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .plot-title {{
            font-size: 1.1em;
            color: #666;
            margin-bottom: 10px;
            font-weight: 500;
        }}
        .insight {{
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
        }}
        .warning {{
            background: #fff3e0;
            border-left: 4px solid #ff9800;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
        }}
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Exploratory Data Analysis Report</h1>
        <p><strong>Dataset:</strong> {dataset_name}</p>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
"""
        
        # Executive Summary
        if summary:
            html_content += f"""
    <div class="section">
        <h2>Executive Summary</h2>
        <p style="font-size: 1.1em; line-height: 1.8;">{summary}</p>
    </div>
"""
        
        # Dataset Overview
        overview = analysis_results.get('overview', {})
        html_content += f"""
    <div class="section">
        <h2>📋 Dataset Overview</h2>
        <div class="metric">
            <span class="metric-label">Total Rows</span>
            <span class="metric-value">{overview.get('total_rows', 0):,}</span>
        </div>
        <div class="metric">
            <span class="metric-label">Total Columns</span>
            <span class="metric-value">{overview.get('total_columns', 0)}</span>
        </div>
        <div class="metric">
            <span class="metric-label">Memory Usage</span>
            <span class="metric-value">{overview.get('memory_usage_mb', 0):.2f} MB</span>
        </div>
        <div class="metric">
            <span class="metric-label">Duplicate Rows</span>
            <span class="metric-value">{overview.get('duplicate_rows', 0):,}</span>
        </div>
    </div>
"""
        
        # Key Insights
        html_content += f"""
    <div class="section">
        <h2>💡 Key Insights</h2>
"""
        for insight in insights.get('key_insights', []):
            html_content += f'        <div class="insight">{insight}</div>\n'
        
        html_content += "    </div>\n"
        
        # Data Quality
        quality = analysis_results.get('data_quality', {})
        html_content += """
    <div class="section">
        <h2>🔍 Data Quality Assessment</h2>
"""
        
        if quality.get('high_missing_columns'):
            html_content += "        <h3>⚠️ High Missing Data Columns</h3>\n"
            html_content += "        <table>\n"
            html_content += "            <tr><th>Column</th><th>Missing %</th></tr>\n"
            for item in quality['high_missing_columns']:
                html_content += f"            <tr><td>{item['column']}</td><td>{item['missing_pct']:.2f}%</td></tr>\n"
            html_content += "        </table>\n"
        
        if quality.get('constant_columns'):
            html_content += f"        <div class='warning'><strong>Constant Columns:</strong> {', '.join(quality['constant_columns'])}</div>\n"
        
        html_content += "    </div>\n"
        
        # Statistical Analysis
        categorical = analysis_results.get('categorical_analysis', {})
        numeric = analysis_results.get('numeric_analysis', {})
        
        if categorical:
            html_content += """
    <div class="section">
        <h2>📊 Categorical Analysis</h2>
"""
            for col, info in list(categorical.items())[:5]:
                html_content += f"        <h3>{col}</h3>\n"
                html_content += f"        <p><strong>Unique Values:</strong> {info['unique_values']}</p>\n"
                html_content += "        <table>\n"
                html_content += "            <tr><th>Value</th><th>Count</th><th>Percentage</th></tr>\n"
                for item in info['value_distribution'][:10]:
                    html_content += f"            <tr><td>{item['value']}</td><td>{item['count']:,}</td><td>{item['percentage']:.2f}%</td></tr>\n"
                html_content += "        </table>\n"
            
            html_content += "    </div>\n"
        
        if numeric:
            html_content += """
    <div class="section">
        <h2>📈 Numeric Analysis</h2>
"""
            for col, info in list(numeric.items())[:5]:
                html_content += f"        <h3>{col}</h3>\n"
                html_content += "        <table>\n"
                html_content += "            <tr><th>Statistic</th><th>Value</th></tr>\n"
                html_content += f"            <tr><td>Count</td><td>{info['count']:,}</td></tr>\n"
                html_content += f"            <tr><td>Mean</td><td>{info['mean']:.2f}</td></tr>\n"
                html_content += f"            <tr><td>Median</td><td>{info['median']:.2f}</td></tr>\n"
                html_content += f"            <tr><td>Std Dev</td><td>{info['std']:.2f}</td></tr>\n"
                html_content += f"            <tr><td>Min</td><td>{info['min']:.2f}</td></tr>\n"
                html_content += f"            <tr><td>Max</td><td>{info['max']:.2f}</td></tr>\n"
                html_content += f"            <tr><td>Outliers</td><td>{info['outliers']['count']:,} ({info['outliers']['percentage']:.2f}%)</td></tr>\n"
                html_content += "        </table>\n"
            
            html_content += "    </div>\n"
        
        # Visualizations
        if embedded_plots:
            html_content += """
    <div class="section">
        <h2>📊 Visualizations</h2>
"""
            for plot in embedded_plots:
                html_content += f"""
        <div class="plot">
            <div class="plot-title">{plot['name']}</div>
            <img src="data:image/png;base64,{plot['data']}" alt="{plot['name']}">
        </div>
"""
            html_content += "    </div>\n"
        
        # Limitations
        html_content += """
    <div class="section">
        <h2>⚠️ Limitations & Considerations</h2>
        <ul>
"""
        for limitation in insights.get('limitations', []):
            html_content += f"            <li>{limitation}</li>\n"
        
        for note in insights.get('data_quality_notes', []):
            html_content += f"            <li>{note}</li>\n"
        
        html_content += "        </ul>\n    </div>\n"
        
        # Footer
        html_content += """
    <div class="footer">
        <p>Generated by AutoGen-EDA | LLM-Assisted Exploratory Data Analysis</p>
    </div>
</body>
</html>
"""
        
        # Save HTML
        html_path = os.path.join(self.output_dir, f"eda_report_{dataset_name}.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_path
    
    def _build_markdown_report(self, dataset_name: str, profile: Dict[str, Any],
                              analysis_results: Dict[str, Any], insights: Dict[str, Any],
                              plot_paths: List[str], summary: str = None) -> str:
        """Build Markdown report."""
        
        md_content = f"""# 📊 Exploratory Data Analysis Report

**Dataset:** {dataset_name}  
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

"""
        
        # Executive Summary
        if summary:
            md_content += f"""## Executive Summary

{summary}

---

"""
        
        # Dataset Overview
        overview = analysis_results.get('overview', {})
        md_content += f"""## 📋 Dataset Overview

- **Total Rows:** {overview.get('total_rows', 0):,}
- **Total Columns:** {overview.get('total_columns', 0)}
- **Memory Usage:** {overview.get('memory_usage_mb', 0):.2f} MB
- **Duplicate Rows:** {overview.get('duplicate_rows', 0):,}

---

"""
        
        # Key Insights
        md_content += """## 💡 Key Insights

"""
        for insight in insights.get('key_insights', []):
            md_content += f"- {insight}\n"
        
        md_content += "\n---\n\n"
        
        # Data Quality
        quality = analysis_results.get('data_quality', {})
        md_content += """## 🔍 Data Quality Assessment

"""
        
        if quality.get('high_missing_columns'):
            md_content += """### ⚠️ High Missing Data Columns

| Column | Missing % |
|--------|-----------|
"""
            for item in quality['high_missing_columns']:
                md_content += f"| {item['column']} | {item['missing_pct']:.2f}% |\n"
            md_content += "\n"
        
        if quality.get('constant_columns'):
            md_content += f"**Constant Columns:** {', '.join(quality['constant_columns'])}\n\n"
        
        md_content += "---\n\n"
        
        # Statistical Analysis
        categorical = analysis_results.get('categorical_analysis', {})
        if categorical:
            md_content += """## 📊 Categorical Analysis

"""
            for col, info in list(categorical.items())[:5]:
                md_content += f"""### {col}

**Unique Values:** {info['unique_values']}

| Value | Count | Percentage |
|-------|-------|------------|
"""
                for item in info['value_distribution'][:10]:
                    md_content += f"| {item['value']} | {item['count']:,} | {item['percentage']:.2f}% |\n"
                md_content += "\n"
        
        numeric = analysis_results.get('numeric_analysis', {})
        if numeric:
            md_content += """## 📈 Numeric Analysis

"""
            for col, info in list(numeric.items())[:5]:
                md_content += f"""### {col}

| Statistic | Value |
|-----------|-------|
| Count | {info['count']:,} |
| Mean | {info['mean']:.2f} |
| Median | {info['median']:.2f} |
| Std Dev | {info['std']:.2f} |
| Min | {info['min']:.2f} |
| Max | {info['max']:.2f} |
| Outliers | {info['outliers']['count']:,} ({info['outliers']['percentage']:.2f}%) |

"""
        
        # Visualizations
        if plot_paths:
            md_content += """## 📊 Visualizations

"""
            for plot_path in plot_paths:
                plot_name = Path(plot_path).stem.replace('_', ' ').title()
                rel_path = Path(plot_path).name
                md_content += f"### {plot_name}\n\n![{plot_name}]({rel_path})\n\n"
        
        # Limitations
        md_content += """## ⚠️ Limitations & Considerations

"""
        for limitation in insights.get('limitations', []):
            md_content += f"- {limitation}\n"
        
        for note in insights.get('data_quality_notes', []):
            md_content += f"- {note}\n"
        
        md_content += "\n---\n\n"
        md_content += "*Generated by AutoGen-EDA | LLM-Assisted Exploratory Data Analysis*\n"
        
        # Save Markdown
        md_path = os.path.join(self.output_dir, f"eda_report_{dataset_name}.md")
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        return md_path
