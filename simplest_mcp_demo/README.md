# MCP Server & Client Demo with AWS Bedrock

This project demonstrates a complete MCP (Model Context Protocol) ecosystem with both server and client implementations using AWS Bedrock.

## 🎯 What This Demo Shows

1. **MCP Server** - Provides tools (`hello` and `get_current_datetime`) for AI agents
2. **MCP Client** - Uses AWS Bedrock to consume server tools intelligently
3. **Complete Integration** - Shows how AI agents can access custom functionality

## 📁 Project Structure

```
demo_mcp_server/
├── mcp_server/
│   └── server.py          # MCP server with 2 tools
├── mcp_client.py          # Bedrock client that consumes MCP server
├── README_SERVER.md       # Detailed server documentation
├── README_CLIENT.md       # Detailed client documentation
├── pyproject.toml         # Project dependencies
└── README.md             # This file
```

## 🚀 Quick Start Guide

### Step 1: Install Dependencies

```bash
# Install Python dependencies
uv sync

# Install MCP Inspector (for testing server)
npm install -g @modelcontextprotocol/inspector
```

### Step 2: Test the MCP Server

#### Option A: Using MCP Inspector (Recommended)
```bash
# Run server with web interface
mcp-inspector python mcp_server/server.py
```
- Browser opens at http://localhost:6274
- Test both tools interactively
- See real-time MCP protocol messages

#### Option B: Direct Server Run
```bash
# Run server directly (for debugging)
python mcp_server/server.py
```

### Step 3: Run the MCP Client with Bedrock

#### Configure AWS Credentials (Choose one method):

**Method 1: AWS CLI**
```bash
aws configure
```

**Method 2: Environment Variables**
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=us-east-1
```

**Method 3: IAM Roles** (if running on EC2)
- No additional configuration needed

#### Run the Client:
```bash
uv run python mcp_client.py
```

## 📋 Expected Output

### MCP Inspector (Server Testing)
When you run the inspector, you'll see:
- **Server Status**: "Connected" with server name "simple-server"
- **Available Tools**: `hello` and `get_current_datetime`
- **Interactive Testing**: Click tools to test with different parameters

### MCP Client with Bedrock
```
Connected to MCP Server
MCP Time: 2025-08-03 20:30:30
MCP Greeting: Hello, Bedrock Agent!
Bedrock Agent: Good evening! Thank you for the greeting. I hope you're having a wonderful day. Please let me know if there is anything I can assist you with.
```

## 🔧 Available MCP Tools

### `hello(name: str = "World") -> str`
- **Purpose**: Returns a personalized greeting
- **Parameters**: `name` (optional, default: "World")
- **Examples**:
  - `hello()` → `"Hello, World!"`
  - `hello("Alice")` → `"Hello, Alice!"`

### `get_current_datetime(format: str = "%Y-%m-%d %H:%M:%S") -> str`
- **Purpose**: Returns current date/time in specified format
- **Parameters**: `format` (optional, default: "%Y-%m-%d %H:%M:%S")
- **Examples**:
  - `get_current_datetime()` → `"2025-01-03 20:30:30"`
  - `get_current_datetime("%Y-%m-%d")` → `"2025-01-03"`
  - `get_current_datetime("%H:%M:%S")` → `"20:30:30"`

## 🔄 Demo Workflow

```
1. MCP Server (server.py)
   ├─ Provides hello() tool
   └─ Provides get_current_datetime() tool
   
2. MCP Client (mcp_client.py)
   ├─ Connects to server via stdio
   ├─ Calls hello("Bedrock Agent")
   ├─ Calls get_current_datetime()
   └─ Sends results to AWS Bedrock
   
3. AWS Bedrock (Claude 3 Haiku)
   ├─ Receives: time + greeting
   └─ Returns: intelligent combined response
```

## 🧪 Testing Steps

### Test 1: MCP Server with Inspector
1. Run: `mcp-inspector python mcp_server/server.py`
2. Browser opens automatically
3. Verify "Connected" status
4. Test `hello` tool with different names
5. Test `get_current_datetime` with different formats
6. Check protocol messages tab

### Test 2: MCP Client with Bedrock
1. Configure AWS credentials
2. Run: `uv run python mcp_client.py`
3. Verify server connection
4. Check tool results are displayed
5. Confirm Bedrock generates intelligent response

## 🛠️ Troubleshooting

### Server Issues
- **"Module not found"**: Run `uv sync` to install dependencies
- **"Server not starting"**: Check Python path and permissions
- **"Inspector not opening"**: Verify npm installation and port 6274 availability

### Client Issues
- **"AWS credentials not found"**: Configure AWS credentials (see Step 3)
- **"Bedrock access denied"**: Enable Claude 3 Haiku in AWS Bedrock console
- **"MCP server connection failed"**: Ensure server code is available at `mcp_server/server.py`

### Common Solutions
```bash
# Reinstall dependencies
uv sync

# Check AWS credentials
aws sts get-caller-identity

# Test server directly
python mcp_server/server.py

# Run with verbose output
uv run python -v mcp_client.py
```

## 📚 Prerequisites

- **Python 3.10+**
- **UV package manager** (`pip install uv`)
- **Node.js** (for MCP Inspector)
- **AWS Account** with Bedrock access
- **Claude 3 Haiku model** enabled in AWS region

## 🎓 Learning Outcomes

After running this demo, you'll understand:
- How to create MCP servers with custom tools
- How to connect AI agents to MCP servers
- How AWS Bedrock integrates with MCP
- The complete MCP protocol workflow
- Best practices for MCP development

## 🔗 Additional Resources

- **[Server Documentation](README_SERVER.md)** - Detailed server implementation guide
- **[Client Documentation](README_CLIENT.md)** - Detailed client implementation guide
- **[MCP Protocol Docs](https://modelcontextprotocol.io/)** - Official MCP documentation
- **[AWS Bedrock Docs](https://docs.aws.amazon.com/bedrock/)** - AWS Bedrock documentation

## 🚀 Next Steps

1. **Add More Tools**: Extend the server with database, API, or file system tools
2. **Multiple Clients**: Create different types of clients (web, CLI, etc.)
3. **Authentication**: Add security and authentication layers
4. **Production**: Scale for production use with proper error handling
5. **Advanced Features**: Implement resources, prompts, and complex workflows

---

**Ready to start?** Run `uv sync` and then `mcp-inspector python mcp_server/server.py` to begin! 🎉
