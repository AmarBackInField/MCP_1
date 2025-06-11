# MCP Server Demo

This project demonstrates a Multi-Component Processing (MCP) server setup with two server instances and a client application.

## Prerequisites

- Python 3.8 or higher
- UV package manager

## Setup Instructions

1. Install UV package manager if you haven't already
2. Set up the environment and install dependencies:

```bash
# Install MCP CLI
uv add "mcp[cli]"

# Create virtual environment
uv venv

# Install requirements
uv add requirements.txt
```

## Running the Servers

### Server 1 (Search Server)
This server handles search functionality and tool input arguments.

```bash
uv run mcp dev server/search.py
```

The MCP inspector will start on a port where you can:
- Test tool input arguments
- Query the server
- Set max results

### Server 2 (Summary Server)
This server handles PDF summary functionality.

```bash
uv run mcp dev server/summary.py
```

The MCP inspector will start on a port where you can:
- Test PDF URL links provided from Server 1
- Process PDF summaries

## Running the Client

To run the client application:

```bash
python client.py
```

The client provides an interactive interface where you can:
- Enter queries
- Receive responses from the servers
- Type 'exit' to quit the application

## Logging

All application logs are stored in the `mcp_log` file, which includes:
- Server operations
- Client queries
- Error messages
- General application events

## Environment Variables

Make sure to set up your environment variables in a `.env` file for:
- API keys
- Server configurations
- Other necessary credentials

## Notes

- Ensure both servers are running before starting the client
- The client will automatically connect to the configured servers
- Check the `mcp_log` file for detailed operation logs and debugging information
