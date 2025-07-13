# Cursor AI图片生成MCP服务器设置指南

## 🎉 恭喜！你的AI图片生成MCP服务器已经配置完成！

本指南将帮你在Cursor中使用这个强大的AI图片生成功能。

## ✅ 当前状态

根据验证结果，你的设置已经完成：

- ✅ **MCP服务器文件** - 所有必要文件已就位
- ✅ **Python环境** - 虚拟环境和依赖已配置
- ✅ **Cursor配置** - MCP服务器已添加到Cursor配置
- ✅ **API密钥** - ModelScope API密钥已配置
- ✅ **模块导入** - 所有Python模块可正常导入

## 🚀 如何在Cursor中使用

### 第1步：重启Cursor
1. 完全关闭Cursor编辑器
2. 重新打开Cursor
3. Cursor会自动加载MCP服务器配置

### 第2步：验证MCP服务器状态
在Cursor中，你应该能看到MCP服务器已连接的指示。

### 第3步：开始使用AI图片生成

你可以通过以下方式使用AI图片生成功能：

#### 🎨 方式1：自然语言请求
直接在Cursor中输入自然语言请求，例如：

```
帮我生成一个科技公司的横幅图片
```

```
我需要一个产品展示图片，展示现代智能手机
```

```
生成一个团队照片，展示专业的商务团队
```

#### 🛠️ 方式2：使用具体的MCP工具

你也可以直接调用MCP工具：

**生成网页图片：**
```
使用generate-web-image工具，类型是hero_banner，描述是"现代科技公司主页横幅"
```

**生成自定义尺寸图片：**
```
使用generate-image工具，提示词是"A futuristic cityscape"，尺寸1920x1080
```

**查看支持的图片类型：**
```
使用list-image-types工具查看所有支持的图片类型
```

## 🎯 支持的图片类型

| 类型 | 描述 | 适用场景 |
|------|------|----------|
| `hero_banner` | 网站主横幅 | 首页、着陆页 |
| `product_showcase` | 产品展示图 | 产品页面 |
| `team_photo` | 团队照片 | 关于我们页面 |
| `blog_featured` | 博客特色图 | 文章封面 |
| `service_icon` | 服务图标 | 功能介绍 |
| `background_pattern` | 背景图案 | 页面装饰 |
| `call_to_action` | 行动号召图 | CTA区域 |
| `testimonial_bg` | 评价背景图 | 客户证言 |

## 💡 使用技巧

### 1. 描述要具体
```
❌ 不好：生成一个图片
✅ 好：生成一个现代科技公司的主页横幅，展示创新和未来感
```

### 2. 指定图片类型
```
✅ 好：生成一个hero_banner类型的图片，用于科技公司主页
```

### 3. 自定义提示词
```
✅ 好：使用自定义提示词"A minimalist tech company logo with blue gradient"生成图片
```

## 🔧 故障排除

### 问题1：MCP服务器未连接
**解决方案：**
1. 检查Cursor是否已重启
2. 运行 `python verify_setup.py` 检查配置
3. 查看Cursor的MCP服务器状态

### 问题2：图片生成失败
**解决方案：**
1. 检查网络连接
2. 确认API密钥有效
3. 运行 `python test_mcp.py` 测试服务器

### 问题3：导入错误
**解决方案：**
1. 确保在项目目录中
2. 激活虚拟环境：`source .venv/bin/activate`
3. 重新安装依赖：`pip install -r requirements.txt`

## 📋 完整测试

运行以下命令进行完整测试：

```bash
# 验证配置
python verify_setup.py

# 测试MCP服务器
python test_mcp.py

# 如果需要重新配置
python setup_cursor.py
```

## 🎊 开始使用！

现在你可以：

1. **重启Cursor编辑器**
2. **在Cursor中输入**：`帮我生成一个科技公司的横幅图片`
3. **等待AI生成图片**
4. **享受自动化的图片生成体验！**

## 📞 需要帮助？

如果遇到问题：
1. 查看项目的 `README.md` 文件
2. 运行 `python verify_setup.py` 检查配置
3. 查看 `MCP_USAGE.md` 了解详细用法

---

🎉 **恭喜！你现在拥有了一个强大的AI图片生成助手，可以在Cursor中随时使用！** 