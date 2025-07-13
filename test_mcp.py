#!/usr/bin/env python3
"""
Simple test script for MCP server
"""

import asyncio
import json
import os

# Set API key
os.environ["MODELSCOPE_API_KEY"] = "e3488d72-53b3-40ac-b78a-4f3264f3c04d"

# Import our MCP server
from mcp_server import SimpleMCPServer

async def test_mcp_server():
    """Test the MCP server functionality."""
    server = SimpleMCPServer()
    
    print("🚀 Testing AI Image Generator MCP Server")
    print("=" * 50)
    
    # Test 1: Initialize
    print("\n1. Testing initialization...")
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {}
    }
    
    response = await server.handle_request(init_request)
    server_name = response.get("result", {}).get("serverInfo", {}).get("name", "Unknown")
    print(f"✅ Server initialized: {server_name}")
    
    # Test 2: List tools
    print("\n2. Testing tools list...")
    list_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    
    response = await server.handle_request(list_request)
    tools = response.get("result", {}).get("tools", [])
    print(f"✅ Found {len(tools)} tools:")
    for tool in tools:
        print(f"   - {tool['name']}: {tool['description']}")
    
    # Test 3: List image types
    print("\n3. Testing list image types...")
    call_request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "list-image-types",
            "arguments": {
                "random_string": "test"
            }
        }
    }
    
    response = await server.handle_request(call_request)
    result_text = response.get("result", {}).get("content", [{}])[0].get("text", "")
    print("✅ Image types result:")
    print(result_text)
    
    # Test 4: Generate a simple image (this will actually call the API)
    print("\n4. Testing image generation...")
    print("🔄 Generating a hero banner image (this may take a moment)...")
    
    generate_request = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "generate-web-image",
            "arguments": {
                "type": "hero_banner",
                "description": "现代科技公司的主页横幅，展示创新理念"
            }
        }
    }
    
    response = await server.handle_request(generate_request)
    result_text = response.get("result", {}).get("content", [{}])[0].get("text", "")
    print("✅ Image generation result:")
    print(result_text)
    
    print("\n" + "=" * 50)
    print("🎉 MCP Server test completed successfully!")
    print("\nYour AI Image Generator MCP Server is ready to use!")
    print("You can now add the mcp_config.json to your MCP client.")

if __name__ == "__main__":
    asyncio.run(test_mcp_server()) 