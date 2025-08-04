#!/usr/bin/env python3

import asyncio
import json
import boto3
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # ========================================
    # MCP SERVER AUTO-START CONFIGURATION
    # ========================================
    # The client doesn't connect to an already-running server.
    # Instead, it AUTOMATICALLY STARTS its own server subprocess!
    # 
    # StdioServerParameters tells the client to launch a subprocess with:
    # - Command: "python" 
    # - Args: ["-m", "mcp_server.server"]
    # - This runs: `python -m mcp_server.server` as a subprocess
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "mcp_server.server"],
    )
    
    # ========================================
    # CLIENT-SERVER COMMUNICATION SETUP
    # ========================================
    # stdio_client() creates the server subprocess and sets up communication pipes:
    # - Server's stdout → Client's read pipe
    # - Client's write pipe → Server's stdin
    # - All MCP protocol messages flow through these pipes
    async with stdio_client(server_params) as (read, write):
        # ClientSession manages the MCP protocol over the pipes
        async with ClientSession(read, write) as session:
            # Initialize the MCP protocol handshake
            await session.initialize()
            
            print("Connected to MCP Server")
            
            # ========================================
            # CALLING MCP SERVER TOOLS
            # ========================================
            # Now we can call tools provided by our auto-started server
            
            # Call the 'get_current_datetime' tool from the server
            time_result = await session.call_tool("get_current_datetime", {})
            current_time = time_result.content[0].text
            
            # Call the 'hello' tool from the server with a parameter
            hello_result = await session.call_tool("hello", {"name": "Bedrock Agent"})
            greeting = hello_result.content[0].text
            
            print(f"MCP Time: {current_time}")
            print(f"MCP Greeting: {greeting}")
            
            # ========================================
            # AWS BEDROCK INTEGRATION
            # ========================================
            # Use the results from MCP server tools as input to AWS Bedrock
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
    
    # ========================================
    # AUTOMATIC SERVER CLEANUP
    # ========================================
    # When we exit the 'async with' blocks above:
    # 1. The MCP session is closed
    # 2. The server subprocess is automatically terminated
    # 3. All resources are cleaned up
    # 
    # Flow: Client starts → Launches server subprocess → Communicates via pipes → 
    #       Calls tools → Server responds → Client processes → Server terminates

if __name__ == "__main__":
    asyncio.run(main())
