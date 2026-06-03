import random
from typing import Dict, Any, Optional
from fastmcp import FastMCP
from src.file_operations import file_manager
from src.data_discovery import data_discovery

mcp = FastMCP(name="Excel Explorer")

# File Operations Tools
@mcp.tool
def load_excel(file_path: str, sheet_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Load an Excel file and return basic information about the dataset.
    
    Args:
        file_path: Path to the Excel file (.xlsx or .xls or .xlsm)
        sheet_name: Optional specific sheet name to load (default: first sheet)
    
    Returns:
        Dictionary containing file info, dimensions, and column names
    """
    return file_manager.load_excel(file_path, sheet_name)

@mcp.tool
def list_sheets(file_path: str) -> Dict[str, Any]:
    """
    List all sheet names in an Excel file.
    
    Args:
        file_path: Path to the Excel file
    
    Returns:
        Dictionary containing list of sheet names and count
    """
    return file_manager.list_sheets(file_path)

@mcp.tool
def get_file_info(file_path: str) -> Dict[str, Any]:
    """
    Get comprehensive metadata about an Excel file.
    
    Args:
        file_path: Path to the Excel file
    
    Returns:
        Dictionary containing file size, creation date, sheets info, etc.
    """
    return file_manager.get_file_info(file_path)

@mcp.tool
def clear_cache() -> Dict[str, Any]:
    """
    Clear all cached Excel data to free memory.
    
    Returns:
        Dictionary with number of files cleared from cache
    """
    return file_manager.clear_cache()

# Data Discovery & Structure Tools
@mcp.tool
def get_schema(file_path: str, sheet_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Get schema information for the dataset including column names, data types, and statistics.
    
    Args:
        file_path: Path to the Excel file
        sheet_name: Optional sheet name (default: first sheet)
    
    Returns:
        Dictionary containing schema with data types, null counts, and semantic types
    """
    return data_discovery.get_schema(file_path, sheet_name)

@mcp.tool
def get_sample_data(file_path: str, sheet_name: Optional[str] = None, 
                   rows: int = 5, sample_type: str = "head") -> Dict[str, Any]:
    """
    Get sample data from the dataset.
    
    Args:
        file_path: Path to the Excel file
        sheet_name: Optional sheet name (default: first sheet)
        rows: Number of rows to return (default: 5)
        sample_type: Type of sample - "head", "tail", or "random" (default: "head")
    
    Returns:
        Dictionary containing sample data records
    """
    return data_discovery.get_sample_data(file_path, sheet_name, rows, sample_type)

@mcp.tool
def get_column_info(file_path: str, column_name: str, 
                   sheet_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Get detailed information about a specific column.
    
    Args:
        file_path: Path to the Excel file
        column_name: Name of the column to analyze
        sheet_name: Optional sheet name (default: first sheet)
    
    Returns:
        Dictionary with detailed column statistics and sample values
    """
    return data_discovery.get_column_info(file_path, column_name, sheet_name)

@mcp.tool
def get_dimensions(file_path: str, sheet_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Get dataset dimensions and basic information.
    
    Args:
        file_path: Path to the Excel file
        sheet_name: Optional sheet name (default: first sheet)
    
    Returns:
        Dictionary with rows, columns, memory usage, and basic stats
    """
    return data_discovery.get_dimensions(file_path, sheet_name)

@mcp.tool
def describe_dataset(file_path: str, sheet_name: Optional[str] = None, 
                    include_all: bool = False) -> Dict[str, Any]:
    """
    Get statistical summary of the dataset.
    
    Args:
        file_path: Path to the Excel file
        sheet_name: Optional sheet name (default: first sheet)
        include_all: Include statistics for non-numeric columns (default: False)
    
    Returns:
        Dictionary with comprehensive statistical summary and data quality metrics
    """
    return data_discovery.describe_dataset(file_path, sheet_name, include_all)


# Keep existing dice tools for compatibility
@mcp.tool
def roll_non_standard_dice(n_dice: int) -> list[int]:
    """Roll `n_dice` a many-sided dice and return the results."""
    return [random.randint(16, 64) for _ in range(n_dice)]

@mcp.tool
def roll_standard_dice(n_dice: int) -> list[int]:
    """Roll `n_dice` 6-sided dice and return the results."""
    return [random.randint(1, 6) for _ in range(n_dice)]

if __name__ == "__main__":
    mcp.run()

