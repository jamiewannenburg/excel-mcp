"""File operations module for Excel MCP server."""

import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import pandas as pd
from datetime import datetime


class ExcelFileManager:
    """Manages Excel file operations and metadata."""
    
    def __init__(self):
        self._cached_files: Dict[str, pd.DataFrame] = {}
    
    def load_excel(self, file_path: str, sheet_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Load Excel file and return basic info about the loaded data.
        
        Args:
            file_path: Path to the Excel file
            sheet_name: Optional sheet name to load (default: first sheet)
            
        Returns:
            Dict with file info and loading status
        """
        try:
            # Validate file exists
            if not os.path.exists(file_path):
                return {"error": f"File not found: {file_path}"}
            
            # Validate file extension
            if not file_path.lower().endswith(('.xlsx', '.xls', '.xlsm')):
                return {"error": f"Invalid file type. Expected .xlsx or .xls or .xlsm, got: {Path(file_path).suffix}"}
            
            # Load the Excel file
            if sheet_name:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                loaded_sheet = sheet_name
            else:
                df = pd.read_excel(file_path)
                # Get the first sheet name
                xl_file = pd.ExcelFile(file_path)
                loaded_sheet = xl_file.sheet_names[0]
            
            # Cache the dataframe
            cache_key = f"{file_path}:{loaded_sheet}"
            self._cached_files[cache_key] = df
            
            return {
                "success": True,
                "file_path": file_path,
                "sheet_name": loaded_sheet,
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": list(df.columns),
                "cache_key": cache_key
            }
            
        except Exception as e:
            return {"error": f"Failed to load Excel file: {str(e)}"}
    
    def list_sheets(self, file_path: str) -> Dict[str, Any]:
        """
        List all sheet names in an Excel file.
        
        Args:
            file_path: Path to the Excel file
            
        Returns:
            Dict with sheet names list
        """
        try:
            if not os.path.exists(file_path):
                return {"error": f"File not found: {file_path}"}
            
            if not file_path.lower().endswith(('.xlsx', '.xls', '.xlsm')):
                return {"error": f"Invalid file type. Expected .xlsx or .xls or .xlsm, got: {Path(file_path).suffix}"}
            
            xl_file = pd.ExcelFile(file_path)
            sheets = xl_file.sheet_names
            
            return {
                "success": True,
                "file_path": file_path,
                "sheet_count": len(sheets),
                "sheet_names": sheets
            }
            
        except Exception as e:
            return {"error": f"Failed to read Excel file sheets: {str(e)}"}
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get comprehensive file metadata.
        
        Args:
            file_path: Path to the Excel file
            
        Returns:
            Dict with file metadata
        """
        try:
            if not os.path.exists(file_path):
                return {"error": f"File not found: {file_path}"}
            
            file_path_obj = Path(file_path)
            stat = file_path_obj.stat()
            
            # Get basic file info
            info = {
                "success": True,
                "file_path": file_path,
                "file_name": file_path_obj.name,
                "file_size": stat.st_size,
                "file_size_mb": round(stat.st_size / (1024 * 1024), 2),
                "created_date": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified_date": datetime.fromtimestamp(stat.st_mtime).isoformat()
            }
            
            # If it's an Excel file, get sheet info
            if file_path.lower().endswith(('.xlsx', '.xls', '.xlsm')):
                try:
                    xl_file = pd.ExcelFile(file_path)
                    info.update({
                        "file_type": "Excel",
                        "sheet_count": len(xl_file.sheet_names),
                        "sheet_names": xl_file.sheet_names
                    })
                except:
                    # If we can't read as Excel, still return basic file info
                    info["file_type"] = "Unknown Excel format"
            else:
                info["file_type"] = file_path_obj.suffix
            
            return info
            
        except Exception as e:
            return {"error": f"Failed to get file info: {str(e)}"}
    
    def get_cached_data(self, cache_key: str) -> Optional[pd.DataFrame]:
        """Get cached DataFrame by cache key."""
        return self._cached_files.get(cache_key)
    
    def clear_cache(self) -> Dict[str, Any]:
        """Clear all cached DataFrames."""
        count = len(self._cached_files)
        self._cached_files.clear()
        return {"success": True, "cleared_files": count}


# Global instance for MCP tools
file_manager = ExcelFileManager()
