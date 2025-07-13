#!/usr/bin/env python3
"""
自动设置Cursor MCP配置的脚本
"""

import json
import os
import shutil
from pathlib import Path

def setup_cursor_mcp():
    """设置Cursor MCP配置"""
    
    # 获取当前项目路径
    current_dir = os.path.abspath(os.path.dirname(__file__))
    
    # Cursor配置目录路径
    cursor_config_dir = Path.home() / ".cursor"
    
    # 创建配置目录（如果不存在）
    cursor_config_dir.mkdir(exist_ok=True)
    
    # MCP服务器配置文件路径
    mcp_config_path = cursor_config_dir / "mcp_servers.json"
    
    # 新的MCP配置
    new_config = {
        "mcpServers": {
            "ai-image-generator": {
                "command": "python",
                "args": ["mcp_server.py"],
                "cwd": current_dir,
                "env": {
                    "MODELSCOPE_API_KEY": "e3488d72-53b3-40ac-b78a-4f3264f3c04d",
                    "PYTHONPATH": current_dir
                }
            }
        }
    }
    
    # 如果配置文件已存在，合并配置
    if mcp_config_path.exists():
        try:
            with open(mcp_config_path, 'r', encoding='utf-8') as f:
                existing_config = json.load(f)
            
            # 合并配置
            if "mcpServers" not in existing_config:
                existing_config["mcpServers"] = {}
            
            existing_config["mcpServers"]["ai-image-generator"] = new_config["mcpServers"]["ai-image-generator"]
            config_to_write = existing_config
            
            print("✅ 已合并到现有的Cursor MCP配置")
            
        except json.JSONDecodeError:
            print("⚠️  现有配置文件格式错误，将创建新配置")
            config_to_write = new_config
    else:
        config_to_write = new_config
        print("✅ 创建新的Cursor MCP配置")
    
    # 写入配置文件
    with open(mcp_config_path, 'w', encoding='utf-8') as f:
        json.dump(config_to_write, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Cursor MCP配置已保存到: {mcp_config_path}")
    print(f"✅ 项目路径: {current_dir}")
    print(f"✅ API密钥已配置")
    
    # 检查虚拟环境
    venv_path = Path(current_dir) / ".venv"
    if venv_path.exists():
        print(f"✅ 虚拟环境已找到: {venv_path}")
        
        # 更新配置以使用虚拟环境中的Python
        python_path = venv_path / "bin" / "python"
        if python_path.exists():
            config_to_write["mcpServers"]["ai-image-generator"]["command"] = str(python_path)
            
            # 重新写入配置
            with open(mcp_config_path, 'w', encoding='utf-8') as f:
                json.dump(config_to_write, f, indent=2, ensure_ascii=False)
            
            print(f"✅ 已配置使用虚拟环境Python: {python_path}")
    
    print("\n" + "="*50)
    print("🎉 Cursor MCP配置完成！")
    print("\n📋 下一步操作：")
    print("1. 重启Cursor编辑器")
    print("2. 在Cursor中，MCP服务器会自动启动")
    print("3. 你可以使用以下工具生成AI图片：")
    print("   - generate-web-image: 生成网页图片")
    print("   - generate-image: 生成自定义图片")
    print("   - list-image-types: 查看支持的图片类型")
    print("\n💡 使用示例：")
    print("   在Cursor中输入：生成一个科技公司的横幅图片")
    print("   MCP服务器会自动调用AI生成合适的图片！")
    print("="*50)

if __name__ == "__main__":
    setup_cursor_mcp() 