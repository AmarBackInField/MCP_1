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

In .env file mention the 
```bash
    LLM_PROVIDER="openai"
    OPENAI_API_KEY=sk-********************Vhka
```

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

## Results
# MCP Server 1 :-
![Screenshot 2025-06-11 151450](https://github.com/user-attachments/assets/937a4137-728c-4a7e-9135-8a267c285eeb)
![Screenshot 2025-06-11 151458](https://github.com/user-attachments/assets/b5ec062d-8698-49f9-b263-1ddeb7973833)

# MCP Server 2:-
![Screenshot 2025-06-11 151517](https://github.com/user-attachments/assets/f79500ca-a7c0-46b2-a374-cf03315fe10e)
![Screenshot 2025-06-11 151529](https://github.com/user-attachments/assets/d8895352-b899-461b-8f7a-450bde2c3f30)

# MCP Client
![Screenshot 2025-06-11 151550](https://github.com/user-attachments/assets/c27d8fc1-32e1-4812-b760-16923c9959a2)
![Screenshot 2025-06-11 151608](https://github.com/user-attachments/assets/2103c36e-786f-454a-b7b7-bc86f4f36577)

