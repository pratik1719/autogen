"""
Utility functions for AutoGen-EDA
"""
import re
import os
from typing import Any, Dict, List
import pandas as pd
import numpy as np


def detect_missing_value_codes(df: pd.DataFrame) -> Dict[str, List[Any]]:
    """
    Detect common missing value codes in the dataset.
    
    Returns:
        Dictionary mapping column names to detected missing value codes
    """
    common_codes = [
        -999, -99, -1, 999, 9999,
        'NA', 'N/A', 'na', 'n/a',
        'NULL', 'null', 'Null',
        'None', 'none',
        'Unknown', 'unknown', 'UNKNOWN',
        '', ' ', 'NaN', 'nan'
    ]
    
    missing_codes = {}
    
    for col in df.columns:
        detected = []
        for code in common_codes:
            if code in df[col].values:
                detected.append(code)
        
        if detected:
            missing_codes[col] = detected
    
    return missing_codes


def detect_privacy_concerns(df: pd.DataFrame) -> List[str]:
    """
    Detect potential privacy-sensitive columns.
    
    Returns:
        List of column names that might contain sensitive data
    """
    sensitive_patterns = [
        r'ssn|social.security',
        r'email',
        r'phone|tel|mobile',
        r'address|street|zip',
        r'credit|card|account',
        r'password|pwd',
        r'dob|birth.date',
        r'license|passport'
    ]
    
    sensitive_cols = []
    
    for col in df.columns:
        col_lower = col.lower()
        for pattern in sensitive_patterns:
            if re.search(pattern, col_lower):
                sensitive_cols.append(col)
                break
    
    return sensitive_cols


def infer_column_types(df: pd.DataFrame) -> Dict[str, str]:
    """
    Infer semantic types of columns beyond pandas dtypes.
    
    Returns:
        Dictionary mapping column names to inferred types
        (numeric, categorical, datetime, text, id, binary)
    """
    inferred_types = {}
    
    for col in df.columns:
        dtype = df[col].dtype
        n_unique = df[col].nunique()
        n_total = len(df[col])
        
        # Numeric
        if pd.api.types.is_numeric_dtype(dtype):
            if n_unique == 2:
                inferred_types[col] = 'binary'
            elif n_unique == n_total or n_unique > 0.9 * n_total:
                inferred_types[col] = 'id'  # Likely an ID column
            else:
                inferred_types[col] = 'numeric'
        
        # Datetime
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            inferred_types[col] = 'datetime'
        
        # Object/String
        else:
            if n_unique <= 20 or n_unique < 0.05 * n_total:
                inferred_types[col] = 'categorical'
            elif n_unique == n_total:
                inferred_types[col] = 'id'
            else:
                inferred_types[col] = 'text'
    
    return inferred_types


def safe_percentage(value: float, total: float) -> float:
    """Calculate percentage safely, handling division by zero."""
    if total == 0:
        return 0.0
    return (value / total) * 100


def format_number(num: float, decimals: int = 2) -> str:
    """Format number with thousand separators."""
    if pd.isna(num):
        return "N/A"
    if isinstance(num, (int, np.integer)):
        return f"{num:,}"
    return f"{num:,.{decimals}f}"


def create_output_dir(base_dir: str = "output") -> str:
    """Create output directory if it doesn't exist."""
    os.makedirs(base_dir, exist_ok=True)
    return base_dir


def sanitize_filename(filename: str) -> str:
    """Remove invalid characters from filename."""
    return re.sub(r'[^\w\s-]', '', filename).strip().replace(' ', '_')


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."
