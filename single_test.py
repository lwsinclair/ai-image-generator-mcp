#!/usr/bin/env python3
import requests
import json

def test_single_image():
    """测试单个图片生成"""
    payload = {
        "html": '<img alt="beautiful sunset landscape" data-type="image" />',
        "api_key": "e3488d72-53b3-40ac-b78a-4f3264f3c04d",
        "styles": {"image": "realistic"},
        "sizes": {"image": "512x512"}
    }
    
    print("测试单个图片生成...")
    print("=" * 50)
    
    response = requests.post("http://localhost:8000/generate-images", json=payload)
    
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        html_result = result.get('html', '')
        print("\n生成的 HTML:")
        print(html_result)
        
        # 检查是否包含真实图片链接
        if 'modelscope-studios.oss-cn-zhangjiakou.aliyuncs.com' in html_result:
            print("\n✅ 成功生成真实 AI 图片！")
        elif 'placeholder' in html_result.lower():
            print("\n⚠️ 返回了占位图片")
        else:
            print("\n❓ 未知结果")
    else:
        print(f"请求失败: {response.status_code}")

if __name__ == "__main__":
    test_single_image() 