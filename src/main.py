"""
Main Entry Point for AutoGen-EDA
Orchestrates the entire EDA pipeline
"""
import sys
import argparse
from pathlib import Path
import json

from data_loader import DataLoader
from llm_client import LLMClient
from eda_planner import EDAPlanner
from analyzer import DataAnalyzer
from visualizer import DataVisualizer
from insight_generator import InsightGenerator
from report_builder import ReportBuilder
from utils import sanitize_filename, create_output_dir


class AutoGenEDA:
    """Main EDA Pipeline Orchestrator"""
    
    def __init__(self, csv_path: str, schema_path: str = None, output_dir: str = "output"):
        """
        Initialize AutoGen-EDA.
        
        Args:
            csv_path: Path to CSV file
            schema_path: Optional path to schema file
            output_dir: Directory for outputs
        """
        self.csv_path = csv_path
        self.schema_path = schema_path
        self.output_dir = output_dir
        
        # Initialize components
        print("\n" + "="*80)
        print("🚀 AutoGen-EDA: LLM-Assisted Dataset Analysis")
        print("="*80)
        
        create_output_dir(output_dir)
    
    def run(self) -> dict:
        """
        Run complete EDA pipeline.
        
        Returns:
            Dictionary with paths to generated outputs
        """
        try:
            # Step 1: Load Data
            print("\n" + "─"*80)
            print("STEP 1: DATA LOADING")
            print("─"*80)
            
            loader = DataLoader(self.csv_path, self.schema_path)
            df, schema, profile = loader.load_all()
            
            dataset_name = sanitize_filename(Path(self.csv_path).stem)
            
            # Step 2: Initialize LLM
            print("\n" + "─"*80)
            print("STEP 2: LLM INITIALIZATION")
            print("─"*80)
            
            llm_client = LLMClient()
            
            # Step 3: Generate EDA Plan
            print("\n" + "─"*80)
            print("STEP 3: STRATEGY PLANNING")
            print("─"*80)
            
            planner = EDAPlanner(llm_client)
            eda_plan = planner.generate_analysis_plan(profile, schema)
            
            # Save plan for reference
            plan_path = Path(self.output_dir) / f"eda_plan_{dataset_name}.json"
            with open(plan_path, 'w') as f:
                json.dump(eda_plan, f, indent=2)
            print(f"   💾 Saved EDA plan to: {plan_path}")
            
            # Step 4: Statistical Analysis
            print("\n" + "─"*80)
            print("STEP 4: STATISTICAL ANALYSIS")
            print("─"*80)
            
            analyzer = DataAnalyzer(df)
            analysis_results = analyzer.analyze_all(eda_plan)
            
            # Save raw results
            results_path = Path(self.output_dir) / f"analysis_results_{dataset_name}.json"
            with open(results_path, 'w') as f:
                json.dump(analysis_results, f, indent=2, default=str)
            print(f"   💾 Saved analysis results to: {results_path}")
            
            # Step 5: Create Visualizations
            print("\n" + "─"*80)
            print("STEP 5: VISUALIZATION")
            print("─"*80)
            
            visualizer = DataVisualizer(df, self.output_dir)
            plot_paths = visualizer.create_all_plots(eda_plan)
            
            # Step 6: Generate Insights
            print("\n" + "─"*80)
            print("STEP 6: INSIGHT GENERATION")
            print("─"*80)
            
            insight_gen = InsightGenerator(llm_client)
            facts = analyzer.get_facts_for_llm()
            insights = insight_gen.generate_insights(facts, analysis_results)
            
            # Generate summary
            summary = insight_gen.generate_summary(dataset_name, insights)
            
            # Step 7: Build Reports
            print("\n" + "─"*80)
            print("STEP 7: REPORT GENERATION")
            print("─"*80)
            
            report_builder = ReportBuilder(self.output_dir)
            report_paths = report_builder.build_reports(
                dataset_name, profile, analysis_results, insights, plot_paths, summary
            )
            
            # Final Summary
            print("\n" + "="*80)
            print("✅ ANALYSIS COMPLETE!")
            print("="*80)
            print(f"\n📊 Dataset: {dataset_name}")
            print(f"   Rows: {profile['shape']['rows']:,}")
            print(f"   Columns: {profile['shape']['columns']}")
            print(f"\n📈 Generated {len(plot_paths)} visualizations")
            print(f"💡 Generated {len(insights.get('key_insights', []))} key insights")
            print(f"\n📄 Reports:")
            print(f"   HTML: {report_paths['html']}")
            print(f"   Markdown: {report_paths['markdown']}")
            print(f"\n📝 GenAI Log: logs/genai_log.md")
            print("\n" + "="*80 + "\n")
            
            return {
                'dataset_name': dataset_name,
                'reports': report_paths,
                'plots': plot_paths,
                'plan': str(plan_path),
                'results': str(results_path)
            }
        
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description='AutoGen-EDA: LLM-Assisted Automated Dataset Analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/main.py data/my_dataset.csv
  python src/main.py data/my_dataset.csv --schema data/schema.json
  python src/main.py data/my_dataset.csv --output custom_output/
        """
    )
    
    parser.add_argument(
        'csv_file',
        help='Path to CSV file to analyze'
    )
    
    parser.add_argument(
        '--schema', '-s',
        help='Optional path to schema/data dictionary file',
        default=None
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output directory for reports and plots (default: output/)',
        default='output'
    )
    
    args = parser.parse_args()
    
    # Validate CSV file exists
    if not Path(args.csv_file).exists():
        print(f"❌ Error: CSV file not found: {args.csv_file}")
        sys.exit(1)
    
    # Validate schema file if provided
    if args.schema and not Path(args.schema).exists():
        print(f"❌ Error: Schema file not found: {args.schema}")
        sys.exit(1)
    
    # Run EDA
    eda = AutoGenEDA(args.csv_file, args.schema, args.output)
    eda.run()


if __name__ == "__main__":
    main()
