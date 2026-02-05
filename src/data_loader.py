"""
Data Loader Module
Handles loading CSV files and optional schema/data dictionary files
"""
import pandas as pd
import json
from typing import Optional, Dict, Any, Tuple
import chardet
from pathlib import Path


class DataLoader:
    """Handles loading and initial processing of datasets"""
    
    def __init__(self, csv_path: str, schema_path: Optional[str] = None):
        """
        Initialize DataLoader.
        
        Args:
            csv_path: Path to CSV file
            schema_path: Optional path to schema/data dictionary file
        """
        self.csv_path = csv_path
        self.schema_path = schema_path
        self.df: Optional[pd.DataFrame] = None
        self.schema: Optional[Dict[str, Any]] = None
        self.encoding: str = 'utf-8'
    
    def _detect_encoding(self) -> str:
        """Detect file encoding."""
        with open(self.csv_path, 'rb') as f:
            raw_data = f.read(100000)  # Read first 100KB
            result = chardet.detect(raw_data)
            return result['encoding'] or 'utf-8'
    
    def load_csv(self) -> pd.DataFrame:
        """
        Load CSV file with robust error handling.
        
        Returns:
            Loaded DataFrame
        """
        print(f"📂 Loading CSV: {self.csv_path}")
        
        # Try to detect encoding
        try:
            self.encoding = self._detect_encoding()
            print(f"   Detected encoding: {self.encoding}")
        except Exception as e:
            print(f"   ⚠️  Encoding detection failed, using UTF-8: {e}")
            self.encoding = 'utf-8'
        
        # Try loading with different strategies
        strategies = [
            {'encoding': self.encoding},
            {'encoding': 'utf-8'},
            {'encoding': 'latin-1'},
            {'encoding': 'iso-8859-1'},
        ]
        
        for i, kwargs in enumerate(strategies):
            try:
                self.df = pd.read_csv(self.csv_path, **kwargs, low_memory=False)
                print(f"   ✅ Loaded successfully with {kwargs['encoding']}")
                print(f"   Shape: {self.df.shape[0]:,} rows × {self.df.shape[1]} columns")
                return self.df
            except Exception as e:
                if i == len(strategies) - 1:
                    raise Exception(f"Failed to load CSV with all encoding strategies: {e}")
                continue
    
    def load_schema(self) -> Optional[Dict[str, Any]]:
        """
        Load optional schema/data dictionary file.
        Supports JSON, CSV, or TXT formats.
        
        Returns:
            Schema dictionary or None if not provided
        """
        if not self.schema_path:
            print("   ℹ️  No schema file provided")
            return None
        
        print(f"📋 Loading schema: {self.schema_path}")
        
        suffix = Path(self.schema_path).suffix.lower()
        
        try:
            if suffix == '.json':
                with open(self.schema_path, 'r') as f:
                    self.schema = json.load(f)
            
            elif suffix == '.csv':
                # Assume schema CSV has columns like: column_name, type, description, etc.
                schema_df = pd.read_csv(self.schema_path)
                self.schema = schema_df.to_dict('records')
            
            elif suffix in ['.txt', '.md']:
                # Simple text format
                with open(self.schema_path, 'r') as f:
                    self.schema = {'raw_text': f.read()}
            
            else:
                print(f"   ⚠️  Unsupported schema format: {suffix}")
                return None
            
            print(f"   ✅ Schema loaded successfully")
            return self.schema
        
        except Exception as e:
            print(f"   ⚠️  Failed to load schema: {e}")
            return None
    
    def get_initial_profile(self) -> Dict[str, Any]:
        """
        Generate initial data profile for LLM analysis.
        
        Returns:
            Dictionary with dataset overview
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_csv() first.")
        
        profile = {
            'filename': Path(self.csv_path).name,
            'shape': {
                'rows': int(self.df.shape[0]),
                'columns': int(self.df.shape[1])
            },
            'columns': {},
            'missing_summary': {},
            'memory_usage_mb': float(self.df.memory_usage(deep=True).sum() / 1024**2)
        }
        
        # Column-level information
        for col in self.df.columns:
            col_data = self.df[col]
            
            profile['columns'][col] = {
                'dtype': str(col_data.dtype),
                'non_null_count': int(col_data.count()),
                'null_count': int(col_data.isna().sum()),
                'null_percentage': float(col_data.isna().sum() / len(col_data) * 100),
                'unique_count': int(col_data.nunique()),
                'sample_values': [str(v) for v in col_data.dropna().head(5).tolist()]
            }
            
            # Add min/max for numeric columns
            if pd.api.types.is_numeric_dtype(col_data):
                profile['columns'][col]['min'] = float(col_data.min()) if not col_data.isna().all() else None
                profile['columns'][col]['max'] = float(col_data.max()) if not col_data.isna().all() else None
        
        # Overall missing data summary
        total_cells = self.df.shape[0] * self.df.shape[1]
        missing_cells = self.df.isna().sum().sum()
        profile['missing_summary'] = {
            'total_missing_cells': int(missing_cells),
            'total_cells': int(total_cells),
            'missing_percentage': float(missing_cells / total_cells * 100)
        }
        
        return profile
    
    def load_all(self) -> Tuple[pd.DataFrame, Optional[Dict[str, Any]], Dict[str, Any]]:
        """
        Load CSV, schema (if provided), and generate initial profile.
        
        Returns:
            Tuple of (dataframe, schema, profile)
        """
        df = self.load_csv()
        schema = self.load_schema()
        profile = self.get_initial_profile()
        
        return df, schema, profile


# Test function
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python data_loader.py <csv_file> [schema_file]")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    schema_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    loader = DataLoader(csv_path, schema_path)
    df, schema, profile = loader.load_all()
    
    print("\n📊 Data Profile:")
    print(json.dumps(profile, indent=2, default=str))
