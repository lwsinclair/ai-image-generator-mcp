#!/bin/bash

echo "🚀 Starting AI Image Generator MCP Server..."
echo "=================================================="

# 检查是否在正确的目录
if [ ! -f "mcp_server.py" ]; then
    echo "❌ Error: mcp_server.py not found in current directory"
    echo "Please run this script from the project root directory"
    exit 1
fi

# 检查虚拟环境
if [ -d ".venv" ]; then
    echo "📦 Activating virtual environment..."
    source .venv/bin/activate
else
    echo "⚠️  Virtual environment not found, using system Python"
fi

# 设置API密钥
export MODELSCOPE_API_KEY="e3488d72-53b3-40ac-b78a-4f3264f3c04d"
export PYTHONPATH="$(pwd)"

echo "🔑 API key configured"
echo "📁 Working directory: $(pwd)"
echo "🐍 Python path: $(which python)"

# 检查依赖
echo "📋 Checking dependencies..."
python -c "import requests, asyncio; print('✅ Dependencies OK')" 2>/dev/null || {
    echo "❌ Missing dependencies. Installing..."
    pip install -r requirements.txt
}

echo "🎯 Starting MCP Server..."
echo "=================================================="
echo "💡 The server will communicate via stdin/stdout (MCP protocol)"
echo "💡 To test the server, run: python test_mcp.py"
echo "💡 To stop the server, press Ctrl+C"
echo "=================================================="

# 启动MCP服务器
python mcp_server.py 