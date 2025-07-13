#!/usr/bin/env python3
"""
验证MCP服务器设置的脚本
"""

import json
import os
import sys
from pathlib import Path

def verify_setup():
    """验证MCP服务器设置"""
    
    print("🔍 验证AI图片生成MCP服务器设置...")
    print("="*50)
    
    # 检查当前目录
    current_dir = Path.cwd()
    print(f"📁 当前目录: {current_dir}")
    
    # 检查必要文件
    required_files = [
        "mcp_server.py",
        "image_generator.py", 
        "prompt_builder.py",
        "requirements.txt",
        "mcp_config.json"
    ]
    
    print("\n📋 检查必要文件:")
    all_files_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (缺失)")
            all_files_exist = False
    
    # 检查虚拟环境
    print("\n🐍 检查Python环境:")
    venv_path = current_dir / ".venv"
    if venv_path.exists():
        python_path = venv_path / "bin" / "python"
        if python_path.exists():
            print(f"  ✅ 虚拟环境: {venv_path}")
            print(f"  ✅ Python路径: {python_path}")
        else:
            print(f"  ⚠️  虚拟环境存在但Python可执行文件未找到")
    else:
        print(f"  ⚠️  虚拟环境未找到: {venv_path}")
    
    # 检查依赖
    print("\n📦 检查Python依赖:")
    try:
        import requests
        print("  ✅ requests")
    except ImportError:
        print("  ❌ requests (未安装)")
        all_files_exist = False
    
    try:
        import asyncio
        print("  ✅ asyncio")
    except ImportError:
        print("  ❌ asyncio (未安装)")
        all_files_exist = False
    
    # 检查API密钥
    print("\n🔑 检查API配置:")
    api_key = os.getenv("MODELSCOPE_API_KEY")
    if api_key:
        print(f"  ✅ 环境变量API密钥: {api_key[:10]}...")
    else:
        print("  ⚠️  环境变量API密钥未设置")
    
    # 检查Cursor配置
    print("\n🖥️  检查Cursor配置:")
    cursor_config_path = Path.home() / ".cursor" / "mcp_servers.json"
    if cursor_config_path.exists():
        try:
            with open(cursor_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            if "mcpServers" in config and "ai-image-generator" in config["mcpServers"]:
                ai_config = config["mcpServers"]["ai-image-generator"]
                print(f"  ✅ Cursor MCP配置文件: {cursor_config_path}")
                print(f"  ✅ 工作目录: {ai_config.get('cwd', '未设置')}")
                print(f"  ✅ Python命令: {ai_config.get('command', '未设置')}")
                
                if "env" in ai_config and "MODELSCOPE_API_KEY" in ai_config["env"]:
                    key = ai_config["env"]["MODELSCOPE_API_KEY"]
                    print(f"  ✅ 配置文件API密钥: {key[:10]}...")
                else:
                    print("  ⚠️  配置文件中API密钥未设置")
            else:
                print("  ❌ ai-image-generator配置未找到")
                all_files_exist = False
        except json.JSONDecodeError:
            print("  ❌ Cursor配置文件格式错误")
            all_files_exist = False
    else:
        print(f"  ❌ Cursor配置文件未找到: {cursor_config_path}")
        all_files_exist = False
    
    # 测试模块导入
    print("\n🧪 测试模块导入:")
    try:
        sys.path.append(str(current_dir))
        from mcp_server import SimpleMCPServer
        print("  ✅ mcp_server.SimpleMCPServer")
    except ImportError as e:
        print(f"  ❌ mcp_server导入失败: {e}")
        all_files_exist = False
    
    try:
        from image_generator import generate_image
        print("  ✅ image_generator.generate_image")
    except ImportError as e:
        print(f"  ❌ image_generator导入失败: {e}")
        all_files_exist = False
    
    try:
        from prompt_builder import build_web_prompt
        print("  ✅ prompt_builder.build_web_prompt")
    except ImportError as e:
        print(f"  ❌ prompt_builder导入失败: {e}")
        all_files_exist = False
    
    print("\n" + "="*50)
    
    if all_files_exist:
        print("🎉 验证完成！所有配置正确！")
        print("\n📋 现在你可以:")
        print("1. 重启Cursor编辑器")
        print("2. 在Cursor中使用AI图片生成功能")
        print("3. 运行 'python test_mcp.py' 进行完整测试")
        print("\n💡 在Cursor中试试输入:")
        print("   '帮我生成一个科技公司的横幅图片'")
        print("   MCP服务器会自动调用AI生成图片！")
    else:
        print("❌ 验证失败！请检查上述错误项目")
        print("\n🔧 建议操作:")
        print("1. 确保在正确的项目目录中")
        print("2. 激活虚拟环境: source .venv/bin/activate")
        print("3. 安装依赖: pip install -r requirements.txt") 
        print("4. 重新运行配置: python setup_cursor.py")
    
    print("="*50)

if __name__ == "__main__":
    verify_setup() 