```
 FastMCP 2.0 ────────────────────────────────────────────────────────────────────

    ███████╗██╗  ██╗ ██████╗███████╗██╗         ███╗   ███╗ ██████╗██████╗ 
    ██╔════╝╚██╗██╔╝██╔════╝██╔════╝██║         ████╗ ████║██╔════╝██╔══██╗
    █████╗   ╚███╔╝ ██║     █████╗  ██║         ██╔████╔██║██║     ██████╔╝
    ██╔══╝   ██╔██╗ ██║     ██╔══╝  ██║         ██║╚██╔╝██║██║     ██╔═══╝ 
    ███████╗██╔╝ ██╗╚██████╗███████╗███████╗    ██║ ╚═╝ ██║╚██████╗██║     
    ╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚══════╝    ╚═╝     ╚═╝ ╚═════╝╚═╝     
                                                                            
 📊 Server name:     Excel Explorer
 📦 Transport:       Streamable-HTTP / Direct
 🔗 Server URL:      http://127.0.0.1:8000/mcp
 
 📚 Docs:            https://gofastmcp.com
 🚀 Deploy:          https://fastmcp.cloud
 
 ⚡ FastMCP version: 2.10.6
 🔧 MCP version:     1.12.3

────────────────────────────────────────────────────────────────────────────────
```

# 📊 Excel MCP Server

## What is this project?

**Excel MCP Server** is a Model Context Protocol (MCP) server that allows Large Language Models (like Claude) to read, explore, and analyze Excel files. It provides tools for:

- **📂 File Operations**: Load Excel files, list sheets, get metadata
- **🔍 Data Discovery**: Analyze schemas, sample data, get column statistics
- **📊 Analysis**: Comprehensive dataset summaries and data quality reports

Built with FastMCP and pandas, it transforms your Excel files into interactive datasets that AI can understand and query.

## Install Dependencies

```bash
# Set up environment (optional)
source activate-pipx.sh

# Install dependencies
uv sync
```

**Requirements:**
- Python >=3.13
- fastmcp >=2.10.6
- pandas >=2.3.1
- openpyxl >=3.1.5
- xlrd >=2.0.2
- pytest >=8.4.1

## Start the MCP Server

```bash
python main.py
```
or
```bash
fastmcp run main.py:mcp --transport http --host 127.0.0.1 --port 8000 --path /mcp
```

The server will start and listen for MCP connections. You'll see output confirming the server is running.

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test files
python -m pytest tests/test_file_operations.py -v
python -m pytest tests/test_data_discovery.py -v

# With coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## Integrate with Claude

### 1. Claude Desktop Integration

Add to your Claude Desktop config file (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "excel-explorer": {
      "command": "python",
      "args": ["/path/to/excel-mcp/main.py"],
      "env": {}
    }
  }
}
```

or

```json
{

    "excelExplorer": {
        "command": "npx",
        "args": [
            "-y",
            "mcp-remote",
            "http://127.0.0.1:8000/mcp"
        ],
        "env": {
            "MCP_TRANSPORT_STRATEGY": "http-only"
        }
    }
}
```

### 2. Available Tools

Once connected, Claude can use these tools:

**File Operations:**
- `load_excel(file_path, sheet_name)` - Load Excel file
- `list_sheets(file_path)` - List all sheets
- `get_file_info(file_path)` - File metadata
- `clear_cache()` - Clear memory

**Data Discovery:**
- `get_schema(file_path, sheet_name)` - Column types and stats
- `get_sample_data(file_path, rows=5, sample_type="head")` - Sample data
- `get_column_info(file_path, column_name)` - Column analysis
- `get_dimensions(file_path)` - Dataset size and memory
- `describe_dataset(file_path, include_all=False)` - Statistical summary

### 3. Example Usage with Claude

```
You: "Load the file data/dataset.xlsx and tell me about its structure"

Claude will use:
1. load_excel("data/dataset.xlsx")
2. get_schema("data/dataset.xlsx")
3. get_dimensions("data/dataset.xlsx")
4. describe_dataset("data/dataset.xlsx")

Then provide insights about your data!
```

---

**Ready to explore your Excel data with AI!** 🚀📊