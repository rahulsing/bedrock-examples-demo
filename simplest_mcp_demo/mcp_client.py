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
