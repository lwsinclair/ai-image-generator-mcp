import requests
import json
import time
import asyncio
from typing import Dict, Any

def generate_image_url(prompt: str, api_key: str) -> str:
    """
    生成图片 URL，如果 API 调用失败则返回占位图片
    """
    max_retries = 2
    for attempt in range(max_retries):
        try:
            url = 'https://api-inference.modelscope.cn/v1/images/generations'
            payload = {
                'model': 'MusePublic/489_ckpt_FLUX_1',
                'prompt': prompt
            }
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            print(f"正在生成图片 (尝试 {attempt + 1}/{max_retries})，prompt: {prompt}")
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            
            print(f"API 响应状态: {response.status_code}")
            
            if response.status_code == 200:
                response_data = response.json()
                if 'images' in response_data and len(response_data['images']) > 0:
                    image_url = response_data['images'][0]['url']
                    print(f"🎉 图片生成成功: {image_url}")
                    return image_url
                else:
                    print(f"响应中没有图片数据: {response_data}")
                    return generate_placeholder_image(prompt, "No Image Data")
            
            elif response.status_code == 401:
                error_data = response.json()
                error_msg = error_data.get('errors', {}).get('message', 'Unauthorized')
                print(f"API 授权失败: {error_msg}")
                if "bind your Alibaba Cloud account" in error_msg:
                    print("提示：请先在 ModelScope 平台绑定阿里云账户")
                return generate_placeholder_image(prompt, "API Auth Failed")
            
            else:
                print(f"API 调用失败: {response.status_code}, {response.text}")
                if attempt < max_retries - 1:
                    print(f"等待 3 秒后重试...")
                    time.sleep(3)
                    continue
                return generate_placeholder_image(prompt, f"API Error {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"⏰ 第 {attempt + 1} 次尝试超时")
            if attempt < max_retries - 1:
                print("等待 3 秒后重试...")
                time.sleep(3)
                continue
            return generate_placeholder_image(prompt, "Timeout")
        except requests.exceptions.RequestException as e:
            print(f"API 调用异常: {e}")
            return generate_placeholder_image(prompt, "Request Error")
        except json.JSONDecodeError as e:
            print(f"JSON 解析错误: {e}")
            return generate_placeholder_image(prompt, "JSON Error")
        except Exception as e:
            print(f"未知错误: {e}")
            return generate_placeholder_image(prompt, "Unknown Error")
    
    return generate_placeholder_image(prompt, "All Retries Failed")

def generate_placeholder_image(prompt: str, error_type: str) -> str:
    """
    生成占位图片 URL，包含提示信息
    """
    # 提取 prompt 中的关键词作为占位图片文本
    keywords = prompt.split()[:3]  # 取前3个词
    text = "+".join(keywords) if keywords else "Image"
    
    # 根据错误类型选择不同的占位图片
    if "Auth" in error_type:
        return f"https://via.placeholder.com/512x512/ffcccc/cc0000?text={text}+Auth+Required"
    elif "Timeout" in error_type:
        return f"https://via.placeholder.com/512x512/ffffcc/cc9900?text={text}+Loading..."
    else:
        return f"https://via.placeholder.com/512x512/cccccc/666666?text={text}+Placeholder"

async def generate_image(prompt: str, api_key: str, width: int = 1024, height: int = 1024) -> Dict[str, Any]:
    """
    异步生成图片，返回结果字典
    """
    try:
        # 在异步环境中调用同步的图片生成函数
        loop = asyncio.get_event_loop()
        image_url = await loop.run_in_executor(None, generate_image_url, prompt, api_key)
        
        return {
            "success": True,
            "image_url": image_url,
            "prompt": prompt,
            "width": width,
            "height": height
        }
    except Exception as e:
        error_msg = str(e)
        placeholder_url = generate_placeholder_image(prompt, error_msg)
        
        return {
            "success": False,
            "error": error_msg,
            "image_url": placeholder_url,
            "prompt": prompt,
            "width": width,
            "height": height
        } 