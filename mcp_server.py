#!/usr/bin/env python3
"""
Simple MCP-compatible AI Image Generator Server

This server provides AI image generation capabilities compatible with MCP protocol
without requiring the official MCP package (compatible with Python 3.9+).
"""

import asyncio
import json
import sys
import os
import logging
from typing import Any, Dict, List, Optional

# Add current directory to path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from image_generator import generate_image
from prompt_builder import build_web_prompt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleMCPServer:
    """Simple MCP-compatible server implementation."""
    
    def __init__(self):
        self.tools = self._get_tools()
    
    def _get_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools."""
        return [
            {
                "name": "generate-web-image",
                "description": "根据网页内容和图片类型生成图片",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": [
                                "hero_banner",
                                "product_showcase", 
                                "team_photo",
                                "blog_featured",
                                "service_icon",
                                "background_pattern",
                                "call_to_action",
                                "testimonial_bg"
                            ],
                            "description": "图片类型"
                        },
                        "description": {
                            "type": "string",
                            "description": "图片内容描述（中文或英文）"
                        },
                        "customPrompt": {
                            "type": "string",
                            "description": "自定义英文prompt（可选，会覆盖默认模板）"
                        }
                    },
                    "required": ["type", "description"],
                    "additionalProperties": False
                }
            },
            {
                "name": "generate-image",
                "description": "使用FLUX模型生成自定义尺寸的图片",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "英文图片生成prompt"
                        },
                        "width": {
                            "type": "number",
                            "description": "图片宽度（可选，默认1024）"
                        },
                        "height": {
                            "type": "number", 
                            "description": "图片高度（可选，默认1024）"
                        },
                        "description": {
                            "type": "string",
                            "description": "图片用途描述（可选）"
                        }
                    },
                    "required": ["prompt"],
                    "additionalProperties": False
                }
            },
            {
                "name": "generate-custom-web-image",
                "description": "使用完全自定义的prompt生成网页图片",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "英文图片生成prompt"
                        },
                        "description": {
                            "type": "string",
                            "description": "图片用途描述（可选）"
                        }
                    },
                    "required": ["prompt"],
                    "additionalProperties": False
                }
            },
            {
                "name": "list-image-types",
                "description": "查看所有支持的网页图片类型和说明",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "random_string": {
                            "type": "string",
                            "description": "Dummy parameter for no-parameter tools"
                        }
                    },
                    "required": ["random_string"],
                    "additionalProperties": False
                }
            },
            {
                "name": "edit-image",
                "description": "使用AI对图片进行编辑修改",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "imageInput": {
                            "type": "string",
                            "description": "图片输入：可以是本地文件路径、图片URL或base64编码"
                        },
                        "prompt": {
                            "type": "string",
                            "description": "编辑指令（中文或英文），例如：'把女孩的头发变成蓝色'"
                        },
                        "inputType": {
                            "type": "string",
                            "enum": ["file", "url", "base64"],
                            "description": "输入类型（可选，系统会自动检测）"
                        }
                    },
                    "required": ["imageInput", "prompt"],
                    "additionalProperties": False
                }
            }
        ]
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming JSON-RPC request."""
        try:
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")
            
            if method == "tools/list":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": self.tools
                    }
                }
            
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                # Get API key from environment
                api_key = os.getenv("MODELSCOPE_API_KEY", "e3488d72-53b3-40ac-b78a-4f3264f3c04d")
                
                result = await self._call_tool(tool_name, arguments, api_key)
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": result
                            }
                        ]
                    }
                }
            
            elif method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "ai-image-generator",
                            "version": "1.0.0"
                        }
                    }
                }
            
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
                
        except Exception as e:
            logger.error(f"Error handling request: {str(e)}")
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
    
    async def _call_tool(self, tool_name: str, arguments: Dict[str, Any], api_key: str) -> str:
        """Call a specific tool."""
        try:
            if tool_name == "generate-web-image":
                image_type = arguments["type"]
                description = arguments["description"]
                custom_prompt = arguments.get("customPrompt")
                
                # Generate prompt
                if custom_prompt:
                    prompt = custom_prompt
                else:
                    prompt = build_web_prompt(image_type, description)
                
                # Generate image
                result = await generate_image(
                    prompt=prompt,
                    api_key=api_key,
                    width=1024,
                    height=1024
                )
                
                if result["success"]:
                    return f"成功生成 {image_type} 图片！\n\n使用的提示词: {prompt}\n\n图片URL: {result['image_url']}\n\n你可以在HTML中使用这个URL: <img src=\"{result['image_url']}\" alt=\"{image_type}\" />"
                else:
                    return f"生成图片失败: {result['error']}"

            elif tool_name == "generate-image":
                prompt = arguments["prompt"]
                width = arguments.get("width", 1024)
                height = arguments.get("height", 1024)
                
                result = await generate_image(
                    prompt=prompt,
                    api_key=api_key,
                    width=width,
                    height=height
                )
                
                if result["success"]:
                    return f"成功生成自定义图片！\n\n提示词: {prompt}\n尺寸: {width}x{height}\n\n图片URL: {result['image_url']}"
                else:
                    return f"生成图片失败: {result['error']}"

            elif tool_name == "generate-custom-web-image":
                prompt = arguments["prompt"]
                
                result = await generate_image(
                    prompt=prompt,
                    api_key=api_key,
                    width=1024,
                    height=1024
                )
                
                if result["success"]:
                    return f"成功生成自定义网页图片！\n\n提示词: {prompt}\n\n图片URL: {result['image_url']}"
                else:
                    return f"生成图片失败: {result['error']}"

            elif tool_name == "list-image-types":
                image_types = {
                    "hero_banner": "网站主横幅的大图",
                    "product_showcase": "电商产品展示图片",
                    "team_photo": "专业团队成员照片",
                    "blog_featured": "博客文章特色图片",
                    "service_icon": "服务或功能图标",
                    "background_pattern": "背景图案和纹理",
                    "call_to_action": "行动号召区域图片",
                    "testimonial_bg": "客户评价背景图片"
                }
                
                result_text = "支持的网页图片类型：\n\n"
                for img_type, description in image_types.items():
                    result_text += f"• {img_type}: {description}\n"
                
                return result_text

            elif tool_name == "edit-image":
                return "图片编辑功能尚未在此MCP服务器中实现。这需要额外的AI模型来进行图片到图片的编辑。"

            else:
                return f"未知工具: {tool_name}"

        except Exception as e:
            logger.error(f"Error in tool call {tool_name}: {str(e)}")
            return f"执行工具 {tool_name} 时出错: {str(e)}"

async def main():
    """Main entry point for the MCP server."""
    server = SimpleMCPServer()
    
    # Read from stdin and write to stdout (MCP protocol)
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
                
            request = json.loads(line.strip())
            response = await server.handle_request(request)
            
            print(json.dumps(response))
            sys.stdout.flush()
            
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
            continue
        except Exception as e:
            logger.error(f"Error in main loop: {str(e)}")
            break

if __name__ == "__main__":
    asyncio.run(main()) 