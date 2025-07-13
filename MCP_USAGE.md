# AI图片生成 MCP 服务器使用说明

## 概述

这是一个基于Model Context Protocol (MCP)的AI图片生成服务器，提供了使用ModelScope FLUX模型生成图片的功能。

## 文件说明

- `simple_mcp_server.py` - 主要的MCP服务器文件（兼容Python 3.9+）
- `mcp_config.json` - MCP客户端配置文件
- `test_mcp.py` - 测试脚本
- `mcp_server.py` - 完整版MCP服务器（需要Python 3.10+和官方MCP包）

## 配置

### 1. 环境变量设置

```bash
export MODELSCOPE_API_KEY="你的API密钥"
```

或者在`mcp_config.json`中设置：

```json
{
  "mcpServers": {
    "ai-image-generator": {
      "command": "python",
      "args": ["simple_mcp_server.py"],
      "cwd": ".",
      "env": {
        "MODELSCOPE_API_KEY": "你的API密钥"
      }
    }
  }
}
```

### 2. 依赖安装

```bash
pip install -r requirements.txt
```

## 可用工具

### 1. generate-web-image
根据网页内容和图片类型生成图片

**参数：**
- `type` (必需): 图片类型，可选值：
  - `hero_banner` - 网站主横幅的大图
  - `product_showcase` - 电商产品展示图片
  - `team_photo` - 专业团队成员照片
  - `blog_featured` - 博客文章特色图片
  - `service_icon` - 服务或功能图标
  - `background_pattern` - 背景图案和纹理
  - `call_to_action` - 行动号召区域图片
  - `testimonial_bg` - 客户评价背景图片
- `description` (必需): 图片内容描述（中文或英文）
- `customPrompt` (可选): 自定义英文prompt

**示例：**
```json
{
  "name": "generate-web-image",
  "arguments": {
    "type": "hero_banner",
    "description": "科技公司的主页横幅，展示创新和未来感"
  }
}
```

### 2. generate-image
使用FLUX模型生成自定义尺寸的图片

**参数：**
- `prompt` (必需): 英文图片生成prompt
- `width` (可选): 图片宽度，默认1024
- `height` (可选): 图片高度，默认1024
- `description` (可选): 图片用途描述

**示例：**
```json
{
  "name": "generate-image",
  "arguments": {
    "prompt": "A futuristic cityscape with flying cars and neon lights",
    "width": 1920,
    "height": 1080
  }
}
```

### 3. generate-custom-web-image
使用完全自定义的prompt生成网页图片

**参数：**
- `prompt` (必需): 英文图片生成prompt
- `description` (可选): 图片用途描述

### 4. list-image-types
查看所有支持的网页图片类型和说明

**参数：**
- `random_string` (必需): 占位参数

### 5. edit-image
使用AI对图片进行编辑修改（功能占位，尚未实现）

## 使用方式

### 方式1：作为MCP服务器运行

1. 将`mcp_config.json`添加到你的MCP客户端配置中
2. 启动支持MCP的客户端（如Claude Desktop等）
3. 客户端会自动发现并连接服务器

### 方式2：直接命令行测试

```bash
python test_mcp.py
```

### 方式3：手动JSON-RPC调用

```bash
python simple_mcp_server.py
```

然后发送JSON-RPC请求：

```json
{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
{"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "generate-web-image", "arguments": {"type": "hero_banner", "description": "科技公司横幅"}}}
```

## 响应格式

成功响应：
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "成功生成图片！\n\n图片URL: https://..."
      }
    ]
  }
}
```

错误响应：
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32603,
    "message": "Internal error: ..."
  }
}
```

## 注意事项

1. 需要有效的ModelScope API密钥
2. 图片生成可能需要几秒钟时间
3. 返回的是图片URL，可直接在HTML中使用
4. 服务器支持中文描述，会自动转换为英文prompt

## 故障排除

1. **API密钥错误**: 确保API密钥正确且已绑定阿里云账号
2. **导入错误**: 确保所有依赖文件都在同一目录下
3. **网络错误**: 检查网络连接和API服务状态

## 扩展

你可以通过修改以下文件来扩展功能：
- `prompt_builder.py` - 自定义prompt生成逻辑
- `image_generator.py` - 修改API调用或添加新的图片生成服务
- `simple_mcp_server.py` - 添加新的工具或修改现有工具行为 