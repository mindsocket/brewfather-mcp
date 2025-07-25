# Brewfather MCP Server

A Model Context Protocol (MCP) server that integrates with the Brewfather API to provide brewing inventory management and recipe analysis capabilities. This server allows MCP clients like Claude to interact with your Brewfather brewing data.

## Features

- **Inventory Management**: List and manage fermentables, hops, yeasts, and miscellaneous brewing supplies
- **Recipe Analysis**: Access detailed recipe information including ingredients and process details
- **Batch Tracking**: Monitor brewing batches, update measurements, and track progress
- **Brewing Insights**: Get brewing process guidance and sensor readings

## Prerequisites

- Python 3.13 or later
- Brewfather account with API access
- Brewfather API credentials (User ID and API Key)

## Getting Your Brewfather API Credentials

1. Log in to your Brewfather account
2. Navigate to Settings → API
3. Generate or copy your API User ID and API Key
4. Keep these credentials secure - you'll need them for configuration

## Installation

1. Clone this repository:
```bash
git clone https://github.com/your-username/brewfather-mcp.git
cd brewfather-mcp
```

2. Install dependencies:
```bash
uv sync
```

## Configuration

#### Claude Desktop Configuration

To use this server with Claude Desktop, add the following to your Claude Desktop configuration file:

**Location of config file:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\\Claude\\claude_desktop_config.json`

**Configuration:**
```json
{
  "mcpServers": {
    "brewfather": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "/absolute/path/to/brewfather-mcp/src/main.py"
      ],
      "cwd": "/absolute/path/to/brewfather-mcp",
      "env": {
        "BREWFATHER_API_USER_ID": "your-api-user-id",
        "BREWFATHER_API_KEY": "your-api-key"
      }
    }
  }
}
```

Replace:
- `/absolute/path/to/brewfather-mcp` with the full path to your cloned repository
- `your-api-user-id` with your Brewfather API User ID
- `your-api-key` with your Brewfather API Key

You may also need to provide the full path to the uv command.

#### Other MCP Clients

For other MCP clients that support stdio transport, use:
- **Command**: `uv run --with mcp[cli] mcp run src/main.py`
- **Working Directory**: Path to this repository
- **Environment Variables**: `BREWFATHER_API_USER_ID` and `BREWFATHER_API_KEY`

### For Local Development & Testing

When developing or testing the server locally, there is the option of providing credentials via a `.env` file instead:
```bash
cp .env.example .env
# Edit .env with your Brewfather API credentials
```

## Available Tools

The server provides the following MCP tools:

### Inventory Management
- `list_fermentables` - List all fermentables (malts, adjuncts, grains)
- `get_fermentable_detail(identifier)` - Get detailed fermentable information
- `list_hops` - List all hops with properties like alpha acids
- `get_hop_detail(identifier)` - Get detailed hop information
- `list_yeasts` - List all yeasts with attenuation and type
- `get_yeast_detail(identifier)` - Get detailed yeast information
- `list_misc_items` - List miscellaneous brewing supplies
- `get_misc_detail(item_id)` - Get detailed misc item information
- `inventory_summary` - Get comprehensive inventory overview

### Recipe Management
- `list_recipes` - List all recipes
- `get_recipe_detail(recipe_id)` - Get detailed recipe information

### Batch Management
- `list_batches` - List all brewing batches
- `get_batch_detail(batch_id)` - Get detailed batch information
- `update_batch(batch_id, ...)` - Update batch measurements and status
- `get_batch_brewtracker(batch_id)` - Get brewing process guidance
- `get_batch_last_reading(batch_id)` - Get latest sensor readings
- `get_batch_readings_summary(batch_id)` - Get sensor readings summary

### Inventory Updates
- `update_fermentable_inventory(item_id, amount)` - Update fermentable stock
- `update_hop_inventory(item_id, amount)` - Update hop stock  
- `update_yeast_inventory(item_id, amount)` - Update yeast stock
- `update_misc_inventory(item_id, amount)` - Update misc item stock

## Development

### Running Tests
```bash
uv run pytest
```

### Testing the Server Locally

[mcptools](https://github.com/f/mcptools) can be handy for local testing:

```bash
# List available tools
mcpt tools uv run --with 'mcp[cli]' mcp run src/main.py

# Call a specific tool
mcpt call list_inventory_categories uv run --with 'mcp[cli]' mcp run src/main.py
```

### HTTP/SSE Server (for cloud deployment)
```bash
PYTHONPATH=src uv run python src/http_runner.py --port 8000
```

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure you've run `uv sync` to install all dependencies

2. **API authentication errors**: 
   - For MCP clients: Check that credentials are correctly set in your client configuration 
   - For local development: Ensure your `.env` file exists with valid credentials
   - Verify your Brewfather API credentials are correct and have the necessary permissions

3. **Connection timeouts**: Check your internet connection and Brewfather API status

4. **Path issues in Claude Desktop**: Ensure you're using absolute paths in the configuration file

### Debug Mode

Enable debug mode to save API responses into a debug folder for troubleshooting:
```bash
BREWFATHER_MCP_DEBUG=1 mcpt call get_batch_detail --params '{"batch_id": "your-batch-id"}' uv run --with 'mcp[cli]' mcp run src/main.py
```
