#!/usr/bin/env python3
import requests
import json
import time

def test_direct_api():
    """直接测试 ModelScope API"""
    url = 'https://api-inference.modelscope.cn/v1/images/generations'
    payload = {
        'model': 'MusePublic/489_ckpt_FLUX_1',
        'prompt': 'A beautiful modern website banner with blue gradient'
    }
    headers = {
        'Authorization': 'Bearer e3488d72-53b3-40ac-b78a-4f3264f3c04d',
        'Content-Type': 'application/json'
    }
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"正在测试 ModelScope API... (尝试 {attempt + 1}/{max_retries})")
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            
            print(f"状态码: {response.status_code}")
            print(f"响应头: {response.headers}")
            print(f"响应内容: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                if 'images' in data:
                    print(f"🎉 图片生成成功: {data['images'][0]['url']}")
                    return True
                else:
                    print("响应中没有图片数据")
            else:
                print(f"API 调用失败: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"⏰ 第 {attempt + 1} 次尝试超时，等待 5 秒后重试...")
            if attempt < max_retries - 1:
                time.sleep(5)
        except Exception as e:
            print(f"错误: {e}")
            break
    
    print("❌ 所有尝试都失败了")
    return False

if __name__ == "__main__":
    test_direct_api() 