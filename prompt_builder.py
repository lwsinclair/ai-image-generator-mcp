from typing import Optional

def build_prompt(area_type: str, desc: str, style: str, size: Optional[str] = None) -> str:
    if size is None:
        size = ''
    prompt = f"A {style} {area_type} for a website. "
    if desc:
        prompt += f"Description: {desc}. "
    if size:
        prompt += f"Size: {size}. "
    prompt += "High quality, professional, web design."
    return prompt

def build_web_prompt(image_type: str, description: str) -> str:
    """Build prompt for web images based on type and description."""
    type_styles = {
        "hero_banner": "modern, professional hero banner with clean design",
        "product_showcase": "elegant product showcase with clean background",
        "team_photo": "professional team member portrait with business attire",
        "blog_featured": "engaging featured image for blog article",
        "service_icon": "clean, minimalist service icon with modern design",
        "background_pattern": "subtle background pattern with elegant texture",
        "call_to_action": "compelling call-to-action visual with modern design",
        "testimonial_bg": "warm, trustworthy background for customer testimonials"
    }
    
    style = type_styles.get(image_type, "professional web design element")
    prompt = f"A {style}. {description}. High quality, professional, modern web design, clean composition."
    
    return prompt 