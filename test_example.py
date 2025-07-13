#!/usr/bin/env python3
"""
AI 图片生成 MCP Server 测试示例
"""
import requests
import json

# 服务地址
BASE_URL = "http://localhost:8000"

def test_generate_images():
    """测试网页图片生成"""
    html_content = """
    <header class="hero banner">
        <h1>Welcome to Our Amazing Product</h1>
        <p>Discover the future of technology</p>
    </header>
    <section>
        <img alt="featured product showcase" data-type="product" />
        <img alt="user profile avatar" data-type="avatar" />
        <img alt="company team photo" data-type="image" />
    </section>
    """
    
    payload = {
        "html": html_content,
        "api_key": "e3488d72-53b3-40ac-b78a-4f3264f3c04d",
        "styles": {
            "banner": "modern",
            "product": "realistic",
            "avatar": "cartoon",
            "image": "professional"
        },
        "sizes": {
            "banner": "1200x400",
            "product": "512x512",
            "avatar": "256x256",
            "image": "800x600"
        }
    }
    
    response = requests.post(f"{BASE_URL}/generate-images", json=payload)
    print("网页图片生成结果:")
    print(f"状态码: {response.status_code}")
    print(f"响应头: {response.headers}")
    print(f"响应内容: {response.text}")
    
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError as e:
            print(f"JSON 解析错误: {e}")
            return None
    else:
        print(f"请求失败，状态码: {response.status_code}")
        return None

def test_generate_article_images():
    """测试文章图片生成"""
    article_content = """
    人工智能技术正在快速发展，深度学习算法在各个领域都取得了突破性进展。从计算机视觉到自然语言处理，AI技术正在改变我们的生活方式。

    在医疗健康领域，AI辅助诊断系统能够帮助医生更准确地识别疾病。通过分析医学影像，AI可以发现人眼难以察觉的细微病变，大大提高了诊断的准确性和效率。

    自动驾驶技术也是AI应用的重要领域。通过深度学习和计算机视觉技术，自动驾驶汽车能够实时感知周围环境，做出智能决策。这项技术有望在未来几年内实现商业化应用。

    在教育领域，个性化学习系统利用AI技术分析学生的学习行为和知识掌握情况，为每个学生提供定制化的学习方案。这种智能化的教育方式能够显著提高学习效果。
    """
    
    payload = {
        "content": article_content,
        "api_key": "e3488d72-53b3-40ac-b78a-4f3264f3c04d",
        "styles": {
            "article": "realistic"
        },
        "sizes": {
            "article": "512x512"
        }
    }
    
    response = requests.post(f"{BASE_URL}/generate-article-images", json=payload)
    print("\n文章图片生成结果:")
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError as e:
            print(f"JSON 解析错误: {e}")
            return None
    else:
        print(f"请求失败，状态码: {response.status_code}")
        return None

if __name__ == "__main__":
    print("开始测试 AI 图片生成 MCP Server...")
    print("=" * 50)
    
    try:
        # 测试网页图片生成
        test_generate_images()
        
        # 测试文章图片生成
        test_generate_article_images()
        
        print("\n测试完成！")
        
    except requests.exceptions.ConnectionError:
        print("错误：无法连接到服务器，请确保服务已启动：uvicorn app:app --reload")
    except Exception as e:
        print(f"测试过程中出现错误：{e}") 