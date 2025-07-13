from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional, Dict
from image_generator import generate_image_url
from prompt_builder import build_prompt
from html_parser import parse_and_fill_images, parse_article_and_insert_images

app = FastAPI(title="AI 图片生成 MCP Server", version="1.0.0")

@app.get("/")
def root():
    return {"message": "AI 图片生成 MCP Server 正在运行", "version": "1.0.0", "endpoints": ["/generate-images", "/generate-article-images"]}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "AI Image Generation MCP Server"}

class GenerateImagesRequest(BaseModel):
    html: str
    api_key: str
    styles: Optional[Dict[str, str]] = None  # e.g. {"banner": "modern", "avatar": "cartoon"}
    sizes: Optional[Dict[str, str]] = None   # e.g. {"banner": "1200x400", "avatar": "256x256"}

class GenerateArticleImagesRequest(BaseModel):
    content: str
    api_key: str
    styles: Optional[Dict[str, str]] = None
    sizes: Optional[Dict[str, str]] = None

@app.post("/generate-images")
def generate_images(req: GenerateImagesRequest):
    # 1. 解析HTML，识别图片区域
    image_areas = parse_and_fill_images(req.html)
    # 2. 针对每个区域生成prompt并生成图片，构造新区域列表
    filled_areas = []
    for area in image_areas:
        if isinstance(area, dict):
            area_type = area.get('type', '')
            desc = area.get('desc', '')
        else:
            area_type = ''
            desc = ''
        style = req.styles.get(area_type, "modern") if req.styles else "modern"
        size = req.sizes.get(area_type, None) if req.sizes else None
        if size is None:
            size = ''
        prompt = build_prompt(area_type, desc, style, size)
        image_url = generate_image_url(prompt, req.api_key)
        filled_areas.append({'type': area_type, 'desc': desc, 'img_url': image_url})
    # 3. 填充图片链接到HTML
    filled_html = parse_and_fill_images(req.html, filled_areas)
    return {"html": filled_html}

@app.post("/generate-article-images")
def generate_article_images(req: GenerateArticleImagesRequest):
    # 1. 解析文章内容，识别需要插图的位置
    article_areas = parse_article_and_insert_images(req.content)
    # 2. 为每个位置生成图片
    filled_areas = []
    for area in article_areas:
        if isinstance(area, dict):
            area_type = area.get('type', 'article')
            desc = area.get('desc', '')
            position = area.get('position', 0)
        else:
            area_type = 'article'
            desc = ''
            position = 0
        style = req.styles.get(area_type, "realistic") if req.styles else "realistic"
        size = req.sizes.get(area_type, "512x512") if req.sizes else "512x512"
        prompt = build_prompt(area_type, desc, style, size)
        image_url = generate_image_url(prompt, req.api_key)
        filled_areas.append({'type': area_type, 'desc': desc, 'img_url': image_url, 'position': position})
    # 3. 插入图片到文章
    filled_content = parse_article_and_insert_images(req.content, filled_areas)
    return {"html": filled_content} 