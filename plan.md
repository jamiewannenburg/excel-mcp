# Excel MCP Server - Dataset Exploration Plan

## Project Goal
Create an MCP server that allows LLMs to read, explore, and ask questions about Excel datasets. The server should provide comprehensive data analysis capabilities for interactive dataset exploration.

## Core Features Required

### 1. File Operations ✅ COMPLETED
- **load_excel**: Load Excel file from path, specify sheet name/index ✅
- **list_sheets**: Get all sheet names in an Excel file ✅
- **get_file_info**: Basic file metadata (size, sheets count, creation date) ✅
- **clear_cache**: Clear cached Excel data to free memory ✅

**Implementation Status**: 
- Created `src/file_operations.py` with `ExcelFileManager` class
- Integrated MCP tools in `main.py` 
- Added required dependencies to `pyproject.toml`
- All basic file operations are functional and tested

### 2. Data Discovery & Structure ✅ COMPLETED
- **get_schema**: Column names, data types, nullable status ✅
- **get_sample_data**: First/last N rows, random sample ✅
- **get_column_info**: Detailed info per column (unique values, null count, data type) ✅
- **get_dimensions**: Row count, column count ✅
- **describe_dataset**: Statistical summary (mean, median, std, min, max for numeric columns) ✅

**Implementation Status**:
- Created `src/data_discovery.py` with `DataDiscoveryEngine` class
- Integrated 5 new MCP tools in `main.py`
- Comprehensive schema analysis with semantic type detection
- Sample data extraction (head/tail/random)
- Detailed column profiling with statistics and value analysis
- Dataset dimensions and memory usage tracking
- Statistical summaries for numeric and categorical data
- Data quality metrics (missing values, duplicates, completeness)

### 3. Data Querying & Filtering
- **query_data**: SQL-like queries or pandas query syntax
- **filter_rows**: Filter by column conditions (equals, contains, greater than, etc.)
- **get_unique_values**: Unique values in specified columns
- **search_text**: Search for text patterns across all columns
- **get_rows_by_index**: Get specific rows by index/range

### 4. Data Analysis
- **get_statistics**: Advanced statistics for numeric columns
- **correlation_matrix**: Correlation between numeric columns
- **value_counts**: Count occurrences of values in categorical columns
- **group_by_analysis**: Group data and perform aggregations
- **find_duplicates**: Identify duplicate rows
- **find_missing_data**: Identify missing/null values patterns

### 5. Data Visualization Support
- **get_chart_data**: Prepare data for specific chart types
- **get_distribution_data**: Data for histograms/distributions
- **get_time_series_data**: Extract time-based data for trends
- **get_category_breakdown**: Data for pie charts/bar charts

### 6. Advanced Analytics
- **detect_patterns**: Identify patterns in data (trends, seasonality)
- **outlier_detection**: Find statistical outliers
- **data_quality_report**: Comprehensive data quality assessment
- **column_profiling**: Detailed profiling of individual columns

## Required Dependencies
```python
dependencies = [
    "fastmcp>=2.10.6",
    "pandas>=2.0.0",
    "openpyxl>=3.1.0",     # Excel reading/writing
    "xlrd>=2.0.0",         # Legacy Excel support
    "numpy>=1.24.0",       # Numerical operations
    "scipy>=1.10.0",       # Statistical functions
]
```

## Implementation Architecture

### Core Classes
```python
class ExcelDataManager:
    """Manages loaded Excel data and caching"""
    
class QueryEngine:
    """Handles data queries and filtering"""
    
class AnalyticsEngine:
    """Provides statistical analysis capabilities"""
    
class DataProfiler:
    """Profiles data quality and structure"""
```

### MCP Tools Structure
- Each feature becomes an `@mcp.tool` decorated function
- Tools accept file_path and sheet_name parameters
- Results returned as structured data (dicts/lists)
- Error handling for file access and data processing

## Usage Examples

### Basic Exploration
```python
# Load and explore structure
load_excel("data/sales.xlsx", "Sheet1")
get_schema("data/sales.xlsx")
get_sample_data("data/sales.xlsx", rows=10)

# Quick analysis
describe_dataset("data/sales.xlsx")
get_column_info("data/sales.xlsx", "revenue")
```

### Advanced Querying
```python
# Filter and search
filter_rows("data/sales.xlsx", {"region": "North", "revenue": ">1000"})
query_data("data/sales.xlsx", "SELECT * FROM data WHERE revenue > 1000")
get_unique_values("data/sales.xlsx", ["region", "product"])
```

### Analytics
```python
# Statistical analysis
correlation_matrix("data/sales.xlsx", ["revenue", "units_sold", "discount"])
group_by_analysis("data/sales.xlsx", group_by="region", agg={"revenue": "sum"})
outlier_detection("data/sales.xlsx", "revenue")
```

## Error Handling Strategy
- File not found errors
- Sheet name validation
- Data type conversion errors
- Memory management for large files
- Invalid query syntax handling

## Performance Considerations
- Lazy loading of data
- Caching frequently accessed datasets
- Chunked processing for large files
- Memory-efficient operations using pandas
- Option to limit result sizes

## Security Considerations
- File path validation (prevent directory traversal)
- File size limits
- Memory usage limits
- Read-only operations (no data modification)

## Future Enhancements
- Support for CSV, JSON, and other formats
- Data export capabilities
- Real-time data streaming
- Machine learning integration
- Custom formula evaluation
- Multi-file dataset joining

## Testing Strategy
- Unit tests for each MCP tool
- Integration tests with sample Excel files
- Performance tests with large datasets
- Error condition testing
- Memory usage testing

## Documentation Requirements
- Tool descriptions for MCP protocol
- Parameter documentation
- Return value specifications
- Usage examples for each tool
- Error code documentation