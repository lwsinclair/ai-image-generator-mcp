from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Union
import re

def parse_and_fill_images(html: str, image_areas: Optional[List[Dict]] = None) -> Union[List[Dict], str]:
    soup = BeautifulSoup(html, 'html.parser')
    if image_areas is None:
        # 识别所有 <img> 占位图和常见banner区域
        areas = []
        for img in soup.find_all('img'):
            desc = img.get('alt', '') or 'placeholder image'
            area_type = img.get('data-type', 'image')
            areas.append({'type': area_type, 'desc': desc})
        # 识别 banner/hero section
        for section in soup.find_all(['header', 'section']):
            if 'banner' in section.get('class', []) or 'hero' in section.get('class', []):
                desc = section.get_text(strip=True)[:50]
                areas.append({'type': 'banner', 'desc': desc})
        return areas
    else:
        # 填充图片链接
        for area in image_areas:
            area_type = area['type']
            desc = area['desc']
            img_url = area['img_url']
            # 优先填充 <img> 匹配 alt/desc
            found = False
            for img in soup.find_all('img'):
                if (img.get('alt', '') or 'placeholder image') == desc and img.get('data-type', 'image') == area_type:
                    img['src'] = img_url
                    found = True
                    break
            if not found:
                # 填充 banner/hero section
                for section in soup.find_all(['header', 'section']):
                    if (('banner' in section.get('class', []) or 'hero' in section.get('class', [])) and section.get_text(strip=True)[:50] == desc):
                        new_img = soup.new_tag('img', src=img_url)
                        section.insert(0, new_img)
                        break
        return str(soup)

def parse_article_and_insert_images(content: str, image_areas: Optional[List[Dict]] = None) -> Union[List[Dict], str]:
    if image_areas is None:
        # 分析文章内容，识别需要插图的位置
        areas = []
        paragraphs = content.split('\n\n')
        for i, paragraph in enumerate(paragraphs):
            paragraph = paragraph.strip()
            if len(paragraph) > 50:  # 调整阈值为 50 字符
                # 提取关键词作为图片描述
                desc = paragraph[:80]  # 增加描述长度
                areas.append({'type': 'article', 'desc': desc, 'position': i})
        return areas
    else:
        # 插入图片到文章
        paragraphs = content.split('\n\n')
        result_paragraphs = []
        
        for i, paragraph in enumerate(paragraphs):
            result_paragraphs.append(paragraph)
            # 查找匹配的图片区域
            for area in image_areas:
                if area.get('position') == i:
                    img_html = f'\n\n<img src="{area["img_url"]}" alt="{area["desc"][:50]}" style="max-width: 100%; height: auto; margin: 20px 0; display: block;" />\n'
                    result_paragraphs.append(img_html)
        
        return '\n\n'.join(result_paragraphs) 