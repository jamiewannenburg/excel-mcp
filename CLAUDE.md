# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Excel MCP (Model Context Protocol) server built with FastMCP. The project provides comprehensive tools for exploring and analyzing Excel datasets through MCP protocol, allowing LLMs to interact with Excel data.

## Architecture

- **main.py**: Primary MCP server entry point using FastMCP framework
- **src/**: Source code modules for Excel operations
  - **src/file_operations.py**: Excel file loading, sheet listing, metadata extraction
- **data/**: Contains Excel files for processing (currently has food_reviews.xlsx)
- **FastMCP Framework**: Uses the fastmcp library for MCP server implementation

## Current Implementation Status

### ✅ Completed: File Operations (Phase 1)
- `load_excel(file_path, sheet_name)`: Load Excel files with caching
- `list_sheets(file_path)`: List all sheets in Excel file
- `get_file_info(file_path)`: File metadata (size, dates, sheet count)
- `clear_cache()`: Memory management for cached data

All file operations are implemented in `src/file_operations.py` with the `ExcelFileManager` class.

### ✅ Completed: Data Discovery & Structure (Phase 2)
- `get_schema(file_path, sheet_name)`: Complete schema analysis with semantic types
- `get_sample_data(file_path, sheet_name, rows, sample_type)`: Head/tail/random samples
- `get_column_info(file_path, column_name, sheet_name)`: Detailed column profiling
- `get_dimensions(file_path, sheet_name)`: Dataset dimensions and memory usage
- `describe_dataset(file_path, sheet_name, include_all)`: Statistical summaries and data quality

All data discovery tools are implemented in `src/data_discovery.py` with the `DataDiscoveryEngine` class.

## Development Setup

### Environment Setup
```bash
# Activate pipx environment for this project
source activate-pipx.sh

# Install dependencies using uv (lockfile present)  
uv sync
```

### Running the MCP Server
```bash
python main.py
```

## Key Implementation Details

### MCP Tools Structure
Tools are defined using the `@mcp.tool` decorator on the FastMCP instance:

**Excel Tools (Active):**

*File Operations:*
- `load_excel(file_path, sheet_name)`: Load Excel file and return dataset info
- `list_sheets(file_path)`: Get all sheet names in Excel file  
- `get_file_info(file_path)`: Get file metadata and statistics
- `clear_cache()`: Clear cached Excel data from memory

*Data Discovery:*
- `get_schema(file_path, sheet_name)`: Schema analysis with semantic types
- `get_sample_data(file_path, sheet_name, rows, sample_type)`: Sample data extraction
- `get_column_info(file_path, column_name, sheet_name)`: Detailed column analysis
- `get_dimensions(file_path, sheet_name)`: Dataset dimensions and memory usage
- `describe_dataset(file_path, sheet_name, include_all)`: Statistical summaries

**Legacy Tools (Kept for compatibility):**
- `roll_non_standard_dice(n_dice: int)`: Returns random numbers 16-64
- `roll_standard_dice(n_dice: int)`: Returns random numbers 1-6

### Data Handling
- The `data/` directory is gitignored except for .gitignore itself
- Excel files should be placed in `data/` for processing
- Current sample file: `food_reviews.xlsx`

## Project Dependencies

- **fastmcp**: >=2.10.6 (MCP server framework)
- **pandas**: >=2.0.0 (Data manipulation and analysis)
- **openpyxl**: >=3.1.0 (Excel file reading/writing)
- **xlrd**: >=2.0.0 (Legacy Excel file support)
- **Python**: >=3.13 required
- **uv**: Used for dependency management (uv.lock present)

## Development Commands

```bash
# Install/update dependencies
uv sync

# Run the MCP server
python main.py

# Run tests (when available)
python -m pytest tests/
```

## Development Environment

The project uses pipx with local configuration:
- `PIPX_HOME`: Set to `$PWD/.pipx_home`  
- `PIPX_BIN_DIR`: Set to `$PWD/.pipx_bin`
- Custom PATH includes local pipx bin directory