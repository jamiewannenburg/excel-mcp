# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Excel MCP (Model Context Protocol) server built with FastMCP. The project provides tools for working with Excel files through MCP protocol, with dice rolling functionality as an example implementation.

## Architecture

- **main.py**: Primary MCP server entry point using FastMCP framework
- **data/**: Contains Excel files for processing (currently has food_reviews.xlsx)
- **FastMCP Framework**: Uses the fastmcp library (>=2.10.6) for MCP server implementation

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
- `roll_non_standard_dice(n_dice: int)`: Returns random numbers 16-64
- `roll_standard_dice(n_dice: int)`: Returns random numbers 1-6

### Data Handling
- The `data/` directory is gitignored except for .gitignore itself
- Excel files should be placed in `data/` for processing
- Current sample file: `food_reviews.xlsx`

## Project Dependencies

- **fastmcp**: >=2.10.6 (MCP server framework)
- **Python**: >=3.13 required
- **uv**: Used for dependency management (uv.lock present)

## Development Environment

The project uses pipx with local configuration:
- `PIPX_HOME`: Set to `$PWD/.pipx_home`  
- `PIPX_BIN_DIR`: Set to `$PWD/.pipx_bin`
- Custom PATH includes local pipx bin directory