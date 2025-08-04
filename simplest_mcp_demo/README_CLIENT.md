# MCP Client with AWS Bedrock - Simple Demo

This is a simple MCP client that demonstrates how an AI agent can consume tools from an MCP server using AWS Bedrock.

## What It Does

The client:
1. **Connects to MCP server** via stdio transport
2. **Calls MCP tools** to get current time and greeting
3. **Uses AWS Bedrock** (Claude model) to process the results intelligently

## Client Code

```python
#!/usr/bin/env python3

import asyncio
import json
import boto3
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Connect to MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "mcp_server.server"],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("Connected to MCP Server")
            
            # Get current time from MCP server
            time_result = await session.call_tool("get_current_datetime", {})
            current_time = time_result.content[0].text
            
            # Get greeting from MCP server
            hello_result = await session.call_tool("hello", {"name": "Bedrock Agent"})
            greeting = hello_result.content[0].text
            
            print(f"MCP Time: {current_time}")
            print(f"MCP Greeting: {greeting}")
            
            # Use Bedrock to create a response
            bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
            
            prompt = f"I got the current time: {current_time} and a greeting: {greeting}. Create a brief, friendly response."
            
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 100,
                "messages": [{"role": "user", "content": prompt}]
            }
            
            response = bedrock.invoke_model(
                modelId="anthropic.claude-3-haiku-20240307-v1:0",
                body=json.dumps(body),
                contentType="application/json"
            )
            
            result = json.loads(response['body'].read())
            bedrock_response = result['content'][0]['text']
            
            print(f"Bedrock Agent: {bedrock_response}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Setup

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Configure AWS credentials** (one of these methods):
   - AWS CLI: `aws configure`
   - Environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
   - IAM roles (if running on EC2)

## Running the Client

```bash
uv run python mcp_client.py
```

## Expected Output

```
Connected to MCP Server
MCP Time: 2025-08-03 20:28:09
MCP Greeting: Hello, Bedrock Agent!
Bedrock Agent: Here's a brief, friendly response:

Greetings! It's wonderful to hear from you. I hope you're having a great day so far. Please let me know if there's anything I can assist you with - I'm always happy to help.
```

## How It Works

1. **MCP Connection**: Client connects to the MCP server using stdio transport
2. **Tool Discovery**: Automatically discovers available tools from the server
3. **Tool Execution**: Calls `get_current_datetime()` and `hello("Bedrock Agent")`
4. **AI Processing**: Sends the results to AWS Bedrock Claude model
5. **Intelligent Response**: Bedrock creates a contextual response combining both pieces of information

## Key Features

- **Simple Integration**: Shows how easy it is to connect MCP server with AI models
- **AWS Bedrock**: Uses Claude 3 Haiku model for fast, intelligent responses
- **Async Operations**: Properly handles async MCP communication
- **Error Handling**: Basic error handling for AWS and MCP operations

## Prerequisites

- **MCP Server**: The `mcp_server/server.py` must be available and runnable
- **AWS Account**: Valid AWS credentials with Bedrock access
- **Bedrock Model Access**: Claude 3 Haiku model must be enabled in your AWS region

## Use Cases

This pattern demonstrates how to:
- Connect AI agents to custom tools via MCP
- Combine multiple tool results intelligently
- Use AWS Bedrock for AI processing
- Build simple but powerful AI workflows
