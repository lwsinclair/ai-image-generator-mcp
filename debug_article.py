#!/usr/bin/env python3
from html_parser import parse_article_and_insert_images

def debug_article_parsing():
    """调试文章解析过程"""
    article_content = """
    人工智能技术正在快速发展，深度学习算法在各个领域都取得了突破性进展。从计算机视觉到自然语言处理，AI技术正在改变我们的生活方式。

    在医疗健康领域，AI辅助诊断系统能够帮助医生更准确地识别疾病。通过分析医学影像，AI可以发现人眼难以察觉的细微病变，大大提高了诊断的准确性和效率。

    自动驾驶技术也是AI应用的重要领域。通过深度学习和计算机视觉技术，自动驾驶汽车能够实时感知周围环境，做出智能决策。这项技术有望在未来几年内实现商业化应用。

    在教育领域，个性化学习系统利用AI技术分析学生的学习行为和知识掌握情况，为每个学生提供定制化的学习方案。这种智能化的教育方式能够显著提高学习效果。
    """
    
    print("调试文章解析过程...")
    print("=" * 50)
    
    # 分析段落分割
    paragraphs = article_content.split('\n\n')
    print(f"分割后的段落数: {len(paragraphs)}")
    for i, paragraph in enumerate(paragraphs):
        paragraph = paragraph.strip()
        print(f"段落 {i}: 长度 {len(paragraph)} - '{paragraph[:50]}...'")
        if len(paragraph) > 100:
            print(f"  -> 符合插图条件")
        else:
            print(f"  -> 不符合插图条件 (长度 <= 100)")
    
    # 1. 解析文章，识别图片区域
    areas = parse_article_and_insert_images(article_content)
    print(f"\n识别到 {len(areas)} 个图片区域:")
    for i, area in enumerate(areas):
        print(f"  {i+1}. {area}")

if __name__ == "__main__":
    debug_article_parsing() 