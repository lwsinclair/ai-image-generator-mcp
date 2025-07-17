[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/alexandrali0506-ai-image-generator-mcp-badge.png)](https://mseep.ai/app/alexandrali0506-ai-image-generator-mcp)

# AI图片生成 MCP 服务器

一个基于Model Context Protocol (MCP)的AI图片生成服务器，使用ModelScope FLUX模型自动生成高质量的网页图片。

## ✨ 功能特点

- 🎨 **智能图片生成** - 支持8种网页图片类型（横幅、产品展示、团队照片等）
- 🌐 **MCP协议兼容** - 完全符合MCP标准，可集成到支持MCP的客户端
- 🔧 **灵活配置** - 支持自定义尺寸、提示词和图片类型
- 🚀 **即开即用** - 简单配置即可在Cursor等编辑器中使用
- 🎯 **高质量输出** - 基于FLUX模型生成专业级图片

## 🛠️ 支持的图片类型

| 类型 | 描述 | 用途 |
|------|------|------|
| `hero_banner` | 网站主横幅的大图 | 首页横幅、着陆页 |
| `product_showcase` | 电商产品展示图片 | 产品页面、商品展示 |
| `team_photo` | 专业团队成员照片 | 关于我们、团队介绍 |
| `blog_featured` | 博客文章特色图片 | 文章封面、内容配图 |
| `service_icon` | 服务或功能图标 | 服务介绍、功能展示 |
| `background_pattern` | 背景图案和纹理 | 页面背景、装饰元素 |
| `call_to_action` | 行动号召区域图片 | CTA按钮、引导区域 |
| `testimonial_bg` | 客户评价背景图片 | 客户证言、评价展示 |

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/你的用户名/ai-image-generator-mcp.git
cd ai-image-generator-mcp
```

### 2. 安装依赖

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. 配置API密钥

获取ModelScope API密钥并设置环境变量：

```bash
export MODELSCOPE_API_KEY="你的API密钥"
```

### 4. 测试服务器

```bash
python test_mcp.py
```

### 5. 配置MCP客户端

将以下配置添加到你的MCP客户端配置文件中：

#### Cursor配置 (`~/.cursor/mcp_servers.json`)

```json
{
  "mcpServers": {
    "ai-image-generator": {
      "command": "python",
      "args": ["/path/to/your/project/mcp_server.py"],
      "cwd": "/path/to/your/project",
      "env": {
        "MODELSCOPE_API_KEY": "你的API密钥"
      }
    }
  }
}
```

#### Claude Desktop配置

在Claude Desktop的设置中添加相同的配置。

## 🔧 MCP工具说明

### 1. generate-web-image
根据网页内容和图片类型生成图片

```json
{
  "name": "generate-web-image",
  "arguments": {
    "type": "hero_banner",
    "description": "现代科技公司的主页横幅，展示创新理念",
    "customPrompt": "可选的自定义英文提示词"
  }
}
```

### 2. generate-image
生成自定义尺寸的图片

```json
{
  "name": "generate-image",
  "arguments": {
    "prompt": "A futuristic cityscape with flying cars",
    "width": 1920,
    "height": 1080
  }
}
```

### 3. generate-custom-web-image
使用完全自定义的提示词生成网页图片

```json
{
  "name": "generate-custom-web-image",
  "arguments": {
    "prompt": "Professional business team in modern office"
  }
}
```

### 4. list-image-types
查看所有支持的图片类型

```json
{
  "name": "list-image-types",
  "arguments": {
    "random_string": "test"
  }
}
```

## 📁 项目结构

```
ai-image-generator-mcp/
├── mcp_server.py           # 主MCP服务器文件
├── mcp_config.json         # MCP客户端配置示例
├── image_generator.py      # 图片生成核心逻辑
├── prompt_builder.py       # 提示词构建工具
├── test_mcp.py            # 测试脚本
├── requirements.txt        # Python依赖
├── README.md              # 项目说明
└── MCP_USAGE.md          # 详细使用指南
```

## 🔑 API密钥获取

1. 访问 [ModelScope](https://modelscope.cn/)
2. 注册并登录账号
3. 绑定阿里云账号
4. 在API管理页面获取密钥

## 🛠️ 开发和扩展

### 添加新的图片类型

在 `prompt_builder.py` 中的 `build_web_prompt` 函数中添加新的类型映射：

```python
type_styles = {
    "your_new_type": "description of the new image type style",
    # ... existing types
}
```

### 自定义提示词模板

修改 `prompt_builder.py` 中的提示词生成逻辑来适应你的需求。

### 添加新的AI模型

在 `image_generator.py` 中修改API调用逻辑来支持其他图片生成模型。

## 🐛 故障排除

### 常见问题

1. **API密钥错误**
   - 确保API密钥正确
   - 确认已绑定阿里云账号

2. **导入错误**
   - 确保在正确的虚拟环境中
   - 检查所有依赖是否已安装

3. **网络错误**
   - 检查网络连接
   - 确认ModelScope服务状态

### 调试模式

设置环境变量启用详细日志：

```bash
export PYTHONPATH=.
export LOG_LEVEL=DEBUG
python test_mcp.py
```

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 支持

如有问题，请在GitHub Issues中提出。

---

⭐ 如果这个项目对你有帮助，请给个Star！ 