# bedrock-examples-demo

## Prerequsite 
- Python 3.10
- AWS Account
- Bedrock Model Access

## 1. Bedrock AgentCore

### Bedrock AgentCore Memory
To demo each of this feature we will be using Streamlit app. 

#### 1.1 No Memory Agent
To demo the problem of Simple Agent without memory.

##### 📚 [`BedrockAgentCore-Demo/Memory/01-NoMemory`](./BedrockAgentCore-Demo/Memory/01-NoMemory/no-memory-demo.py)
The conversation will be store AS IS in the backend(at Bedrock service side). Returning user/customer will get personalized experience as Agent or LLM models will refer the old converstion. 

#### 1.2 Agent with Short Term Memory

##### 📚 [`BedrockAgentCore-Demo/Memory/02-ShortTerm/`](./BedrockAgentCore-Demo/Memory/02-ShortTerm/short-term-memory_demo.py)
The conversation will be store AS IS in the backend(at Bedrock service side). Returning user/customer will get personalized experience as Agent or LLM models will refer the old converstion. 

#### 1.3 Agent with Long Term Memory

##### 📚 [`BedrockAgentCore-Demo/Memory/03-LongTerm/`](./BedrockAgentCore-Demo/Memory/02-LongTerm/long-term-memory-demo.py)
The conversation will be stored after apply the different stragey like summerization the stored in the backend(at Bedrock service side). Returning user/customer will get personalized experience as Agent or LLM models will refer the user preference or historical information. 

- User-preference (built-in)
- Semantic (built-in)
- Summarization (built-in)
- Or you build your own strategy. 

## 2. MCP (Model Context Protocol) Demos

### 2.1 Simple MCP Server & Client Demo with AWS Bedrock

##### 📚 [`simplest_mcp_demo/`](./simplest_mcp_demo/)

A complete MCP (Model Context Protocol) ecosystem demonstration featuring both server and client implementations using AWS Bedrock. This demo shows how AI agents can access custom functionality through MCP tools.

**What this demo includes:**
- **MCP Server** - Provides tools (`hello` and `get_current_datetime`) for AI agents
- **MCP Client** - Uses AWS Bedrock to consume server tools intelligently  
- **Complete Integration** - Shows how AI agents can access custom functionality

**Key Features:**
- FastMCP framework for modern server implementation
- AWS Bedrock integration with Claude 3 Haiku model
- Interactive testing with MCP Inspector
- Security best practices with `.env` files properly ignored

**Quick Start:**
```bash
cd simplest_mcp_demo
uv sync
mcp-inspector python mcp_server/server.py  # Test server
uv run python mcp_client.py                # Run client with Bedrock
```

For detailed setup instructions and documentation, see the [MCP Demo README](./simplest_mcp_demo/README.md).
