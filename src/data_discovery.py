"""Data discovery module for Excel MCP server."""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Union
from src.file_operations import file_manager


class DataDiscoveryEngine:
    """Handles data structure discovery and schema analysis."""
    
    def __init__(self):
        self.file_manager = file_manager
    
    def _get_dataframe(self, file_path: str, sheet_name: Optional[str] = None) -> tuple[pd.DataFrame, str]:
        """
        Get DataFrame from cache or load it.
        
        Returns:
            Tuple of (DataFrame, error_message). If successful, error_message is None.
        """
        try:
            # Try to get from cache first
            if sheet_name:
                cache_key = f"{file_path}:{sheet_name}"
            else:
                # Load the file to get the default sheet
                load_result = self.file_manager.load_excel(file_path, sheet_name)
                if 'error' in load_result:
                    return None, load_result['error']
                cache_key = load_result['cache_key']
            
            df = self.file_manager.get_cached_data(cache_key)
            if df is not None:
                return df, None
            
            # If not in cache, load it
            load_result = self.file_manager.load_excel(file_path, sheet_name)
            if 'error' in load_result:
                return None, load_result['error']
            
            df = self.file_manager.get_cached_data(load_result['cache_key'])
            return df, None
            
        except Exception as e:
            return None, f"Failed to get DataFrame: {str(e)}"
    
    def get_schema(self, file_path: str, sheet_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get schema information for the dataset.
        
        Args:
            file_path: Path to the Excel file
            sheet_name: Optional sheet name
            
        Returns:
            Dict with column names, data types, nullable status
        """
        df, error = self._get_dataframe(file_path, sheet_name)
        if error:
            return {"error": error}
        
        try:
            schema_info = []
            
            for col in df.columns:
                col_info = {
                    "column_name": str(col),
                    "data_type": str(df[col].dtype),
                    "pandas_dtype": str(df[col].dtype),
                    "null_count": int(df[col].isnull().sum()),
                    "non_null_count": int(df[col].notna().sum()),
                    "nullable": bool(df[col].isnull().any()),
                    "unique_count": int(df[col].nunique()),
                    "memory_usage": int(df[col].memory_usage(deep=True))
                }
                
                # Infer semantic data type (check boolean first as it can be treated as numeric)
                if pd.api.types.is_bool_dtype(df[col]):
                    col_info["semantic_type"] = "boolean"
                elif pd.api.types.is_datetime64_any_dtype(df[col]):
                    col_info["semantic_type"] = "datetime"
                elif pd.api.types.is_numeric_dtype(df[col]):
                    if pd.api.types.is_integer_dtype(df[col]):
                        col_info["semantic_type"] = "integer"
                    else:
                        col_info["semantic_type"] = "float"
                else:
                    col_info["semantic_type"] = "text"
                
                schema_info.append(col_info)
            
            return {
                "success": True,
                "file_path": file_path,
                "sheet_name": sheet_name,
                "total_columns": len(df.columns),
                "total_rows": len(df),
                "schema": schema_info
            }
            
        except Exception as e:
            return {"error": f"Failed to get schema: {str(e)}"}
    
    def get_sample_data(self, file_path: str, sheet_name: Optional[str] = None, 
                       rows: int = 5, sample_type: str = "head") -> Dict[str, Any]:
        """
        Get sample data from the dataset.
        
        Args:
            file_path: Path to the Excel file
            sheet_name: Optional sheet name
            rows: Number of rows to return
            sample_type: Type of sample - "head", "tail", "random"
            
        Returns:
            Dict with sample data
        """
        df, error = self._get_dataframe(file_path, sheet_name)
        if error:
            return {"error": error}
        
        try:
            if rows <= 0:
                return {"error": "Number of rows must be positive"}
            
            if sample_type == "head":
                sample_df = df.head(rows)
            elif sample_type == "tail":
                sample_df = df.tail(rows)
            elif sample_type == "random":
                sample_size = min(rows, len(df))
                sample_df = df.sample(n=sample_size, random_state=42)
            else:
                return {"error": f"Invalid sample_type: {sample_type}. Use 'head', 'tail', or 'random'"}
            
            # Convert to records format for JSON serialization
            records = sample_df.to_dict('records')
            
            # Handle NaN values
            for record in records:
                for key, value in record.items():
                    if pd.isna(value):
                        record[key] = None
            
            return {
                "success": True,
                "file_path": file_path,
                "sheet_name": sheet_name,
                "sample_type": sample_type,
                "requested_rows": rows,
                "returned_rows": len(records),
                "columns": list(df.columns),
                "data": records
            }
            
        except Exception as e:
            return {"error": f"Failed to get sample data: {str(e)}"}
    
    def get_column_info(self, file_path: str, column_name: str, 
                       sheet_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get detailed information about a specific column.
        
        Args:
            file_path: Path to the Excel file
            column_name: Name of the column to analyze
            sheet_name: Optional sheet name
            
        Returns:
            Dict with detailed column information
        """
        df, error = self._get_dataframe(file_path, sheet_name)
        if error:
            return {"error": error}
        
        try:
            if column_name not in df.columns:
                return {"error": f"Column '{column_name}' not found in dataset"}
            
            col = df[column_name]
            col_info = {
                "success": True,
                "file_path": file_path,
                "sheet_name": sheet_name,
                "column_name": column_name,
                "data_type": str(col.dtype),
                "total_count": len(col),
                "null_count": int(col.isnull().sum()),
                "non_null_count": int(col.notna().sum()),
                "unique_count": int(col.nunique()),
                "memory_usage": int(col.memory_usage(deep=True))
            }
            
            # Add statistics for numeric columns
            if pd.api.types.is_numeric_dtype(col):
                col_info.update({
                    "min": float(col.min()) if not pd.isna(col.min()) else None,
                    "max": float(col.max()) if not pd.isna(col.max()) else None,
                    "mean": float(col.mean()) if not pd.isna(col.mean()) else None,
                    "median": float(col.median()) if not pd.isna(col.median()) else None,
                    "std": float(col.std()) if not pd.isna(col.std()) else None,
                    "q25": float(col.quantile(0.25)) if not pd.isna(col.quantile(0.25)) else None,
                    "q75": float(col.quantile(0.75)) if not pd.isna(col.quantile(0.75)) else None
                })
            
            # Add value counts for categorical data (limit to top 20)
            if col.nunique() <= 50:  # Only for columns with reasonable number of unique values
                value_counts = col.value_counts().head(20)
                col_info["top_values"] = {
                    str(k): int(v) for k, v in value_counts.items()
                }
            
            # Add sample values
            non_null_values = col.dropna()
            if len(non_null_values) > 0:
                sample_size = min(10, len(non_null_values))
                sample_values = non_null_values.sample(n=sample_size, random_state=42).tolist()
                col_info["sample_values"] = [str(v) for v in sample_values]
            
            return col_info
            
        except Exception as e:
            return {"error": f"Failed to get column info: {str(e)}"}
    
    def get_dimensions(self, file_path: str, sheet_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get dataset dimensions and basic info.
        
        Args:
            file_path: Path to the Excel file
            sheet_name: Optional sheet name
            
        Returns:
            Dict with dimensions and basic dataset info
        """
        df, error = self._get_dataframe(file_path, sheet_name)
        if error:
            return {"error": error}
        
        try:
            return {
                "success": True,
                "file_path": file_path,
                "sheet_name": sheet_name,
                "rows": len(df),
                "columns": len(df.columns),
                "total_cells": len(df) * len(df.columns),
                "memory_usage_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 4),
                "column_names": list(df.columns),
                "dtypes": {str(col): str(dtype) for col, dtype in df.dtypes.items()},
                "empty_rows": int((df.isnull().all(axis=1)).sum()),
                "empty_columns": int((df.isnull().all(axis=0)).sum())
            }
            
        except Exception as e:
            return {"error": f"Failed to get dimensions: {str(e)}"}
    
    def describe_dataset(self, file_path: str, sheet_name: Optional[str] = None, 
                        include_all: bool = False) -> Dict[str, Any]:
        """
        Get statistical summary of the dataset.
        
        Args:
            file_path: Path to the Excel file
            sheet_name: Optional sheet name
            include_all: Include statistics for non-numeric columns
            
        Returns:
            Dict with statistical summary
        """
        df, error = self._get_dataframe(file_path, sheet_name)
        if error:
            return {"error": error}
        
        try:
            result = {
                "success": True,
                "file_path": file_path,
                "sheet_name": sheet_name,
                "total_rows": len(df),
                "total_columns": len(df.columns)
            }
            
            # Get numeric statistics
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                numeric_desc = df[numeric_cols].describe()
                result["numeric_summary"] = {}
                
                for col in numeric_cols:
                    result["numeric_summary"][col] = {
                        "count": int(numeric_desc.loc['count', col]),
                        "mean": float(numeric_desc.loc['mean', col]),
                        "std": float(numeric_desc.loc['std', col]),
                        "min": float(numeric_desc.loc['min', col]),
                        "q25": float(numeric_desc.loc['25%', col]),
                        "q50": float(numeric_desc.loc['50%', col]),
                        "q75": float(numeric_desc.loc['75%', col]),
                        "max": float(numeric_desc.loc['max', col])
                    }
            
            # Get categorical statistics
            if include_all:
                categorical_cols = df.select_dtypes(include=['object', 'category']).columns
                if len(categorical_cols) > 0:
                    result["categorical_summary"] = {}
                    
                    for col in categorical_cols:
                        col_data = df[col]
                        result["categorical_summary"][col] = {
                            "count": int(col_data.notna().sum()),
                            "unique": int(col_data.nunique()),
                            "top_value": str(col_data.mode().iloc[0]) if len(col_data.mode()) > 0 else None,
                            "top_freq": int(col_data.value_counts().iloc[0]) if len(col_data.value_counts()) > 0 else 0
                        }
            
            # Overall data quality metrics
            result["data_quality"] = {
                "total_missing_values": int(df.isnull().sum().sum()),
                "missing_percentage": round(df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100, 2),
                "duplicate_rows": int(df.duplicated().sum()),
                "complete_rows": int(df.dropna().shape[0]),
                "completeness_percentage": round(df.dropna().shape[0] / len(df) * 100, 2)
            }
            
            return result
            
        except Exception as e:
            return {"error": f"Failed to describe dataset: {str(e)}"}


# Global instance for MCP tools
data_discovery = DataDiscoveryEngine()