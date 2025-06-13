# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Model Context Protocol (MCP) server that integrates with the Brewfather API to provide brewing inventory management and recipe analysis capabilities. The server exposes tools for managing fermentables, hops, yeasts, batches, recipes, and miscellaneous brewing supplies.

The API is documented, but not well, at https://docs.brewfather.app/api
In order to make robust code, we need to "test in production" by making calls to tools and debug the results. This is fine to do directly for get and list operations, but not for operations that change data. For that, we _might_ be able to create a test entry (inventory, recipe, batch) first, then test, then clean up by carefully deleting the test item.

## Development Commands

### Package Management
- `uv run pytest` - Run test suite
- `uv run pytest tests/test_file.py::TestClass::test_method` - Run specific test
- `uv run pytest --cov` - Run tests with coverage
- `uv install` - Install dependencies
- `uv sync` - Sync dependencies

### MCP Development

When using claude code, use mcpt commands to test changes to this server. The inbuilt mcp tools don't get reloaded after changes.

- `uv run --with mcp[cli] mcp install` - Install MCP CLI tools
- `uv run --with 'mcp[cli]' mcp run src/main.py` - Run server
- `uv run --with 'mcp[cli]' mcp dev src/main.py` - Run server with inspector
- `mcpt tools uv run --with 'mcp[cli]' mcp run src/main.py` - Use MCP Tools to list tools
- `mcpt call list_batches  uv run --with 'mcp[cli]' mcp run src/main.py` - Call a tool
- `mcpt call get_batch_detail --params '{ "batch_id": "C3hZC7P4zeNH6QJsc7FXizVGN8dkQe" }'  uv run --with 'mcp[cli]' mcp run src/main.py` - Call a tool with params
- `BREWFATHER_MCP_DEBUG=1 mcpt call get_batch_detail --params '{ "batch_id": "C3hZC7P4zeNH6QJsc7FXizVGN8dkQe" }' uv run --with 'mcp[cli]' mcp run src/main.py` - Call tool with debug mode to save API calls to file
- `alias -g BF="uv run --with 'mcp[cli]' mcp run src/main.py"` - Alias to use with mcpt, eg `mcpt tools BF`


## Architecture

### Core Components

**API Client (`src/brewfather_mcp/api.py`)**
- `BrewfatherClient` - Main HTTP client for Brewfather API
- Uses httpx with basic auth (BREWFATHER_API_USER_ID, BREWFATHER_API_KEY)
- Implements CRUD operations for all inventory categories and recipes
- Base URL: `https://api.brewfather.app/v2`

**MCP Server (`src/brewfather_mcp/server.py`)**
- Uses FastMCP framework to expose tools and prompts
- Contains all MCP tool definitions that wrap API client methods
- Includes specialized prompts for beer style suggestions based on inventory
- Logs to `/tmp/application.log`

**Type Definitions (`src/brewfather_mcp/types.py`)**
- Pydantic models for all Brewfather API responses
- Separate models for list views vs detail views
- Handles complex nested structures (recipes, water profiles, fermentation schedules)

**Inventory Utilities (`src/brewfather_mcp/inventory.py`)**
- Helper functions for creating inventory summaries
- Used by the `inventory_summary` MCP tool

### Environment Configuration

Required environment variables:
- `BREWFATHER_API_USER_ID` - Your Brewfather API user ID
- `BREWFATHER_API_KEY` - Your Brewfather API key

For testing, use `.test.env` file (automatically loaded by pytest).
When developing, use `.env` file

### Testing Strategy

- Uses pytest with pytest-vcr for HTTP request recording/replay
- VCR cassettes stored in `tests/cassettes/`
- Test configuration in `tests/conftest.py` includes auth header filtering
- Coverage configuration excludes test files

### Key MCP Tools

The server exposes these main tool categories:
- **Inventory**: List/detail/update for fermentables, hops, yeasts, misc items
- **Recipes**: List and detailed recipe information including ingredients and process
- **Batches**: List, detail, and update brewing batches with measured values
- **Summaries**: Combined inventory overviews and brewing style suggestions

### Code Patterns

- All API methods are async and use httpx
- Pydantic models validate all API responses
- MCP tools provide formatted string outputs for Claude consumption
- Error handling logs exceptions and re-raises them
- Consistent URL building pattern using `_build_url()` method