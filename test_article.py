#!/usr/bin/env python3
import requests
import json

def test_article_images():
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
        "styles": {"article": "realistic"},
        "sizes": {"article": "512x512"}
    }
    
    print("测试文章图片生成...")
    print("=" * 50)
    
    response = requests.post("http://localhost:8000/generate-article-images", json=payload)
    
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        html_result = result.get('html', '')
        print("\n生成的文章内容:")
        print(html_result)
        
        # 检查是否包含真实图片链接
        image_count = html_result.count('modelscope-studios.oss-cn-zhangjiakou.aliyuncs.com')
        if image_count > 0:
            print(f"\n✅ 成功生成了 {image_count} 张真实 AI 图片！")
        else:
            print("\n⚠️ 没有生成图片")
    else:
        print(f"请求失败: {response.status_code}")
        print(f"错误信息: {response.text}")

if __name__ == "__main__":
    test_article_images() 