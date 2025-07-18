import sys
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from bs4.element import Tag

def get_meta_content(soup, name: str) -> str | None:
    tag = soup.find("meta", attrs={"name": name})
    return tag["content"].strip() if tag and tag.has_attr("content") else None

# 제길 중복코드 발생..
def get_meta_property_content(soup, name: str) -> str | None:
    tag = soup.find("meta", attrs={"property": name})
    return tag["content"].strip() if tag and tag.has_attr("content") else None

def parse_keywords(soup) -> str:
    tag = soup.find("meta", attrs={"name": "keywords"})
    if not tag or not tag.has_attr("content"):
        return ""

    raw = tag["content"]
    items = [kw.strip() for kw in raw.split(",") if kw.strip()]
    return ", ".join(f'"{kw}"' for kw in items)

def extract_article_body(soup: BeautifulSoup) -> str:
    article_div = soup.find("article", id="article-view-content-div")
    result = []
    image_counter = 1
    seen_texts = set()

    for tag in article_div.descendants:
        if isinstance(tag, Tag):
            if tag.name == "figure":
                caption = tag.find("figcaption")
                caption_text = caption.get_text(strip=True) if caption else ""
                figure_html = f'''<figure>
  <img src="{image_counter}.jpg" alt="no image" />
  <figcaption>{caption_text}</figcaption>
</figure>
'''
                result.append(figure_html)
                image_counter += 1
            elif tag.name in ("p", "div", "strong"):
                text = tag.get_text(strip=True)
                if text and text not in seen_texts:
                    result.append(text)
                    seen_texts.add(text)

    return "\n\n".join(result)

def parse_article(url: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/116.0.0.0 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    article = {
        "url": url,
        "title": get_meta_content(soup, "title") or "제목 없음",
        "description": get_meta_content(soup, "description") or "",
        "keywords": parse_keywords(soup),
        "categories": get_meta_property_content(soup, "article:section") or "미분류",
        "tags": get_meta_property_content(soup, "article:section") or "태그없음",
        "date": get_meta_property_content(soup, "article:published_time") or "날짜 미상",
        "creator": get_meta_content(soup, "author") or "작성자 미상",
        "body": extract_article_body(soup),
    }

    return article

def save_markdown(article: dict, out_path: Path):
    content = f"""+++
title = '{article['title']}'
date = {article['date']}
categories = ["{article['categories']}"]
tags = ["{article['tags']}"]
keywords = [{article['keywords']}]
description = "{article['description']}"
thumbnail = "1.jpg"
creator = "{article['creator']}"
draft = false
+++

{article['body']}

"""
    out_path.write_text(content, encoding="utf-8")

def main():
    if len(sys.argv) < 2:
        print("사용법: python main.py [기사 URL]")
        sys.exit(1)

    url = sys.argv[1]
    article = parse_article(url)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "index.md"
    save_markdown(article, output_file)
    print(f"✅ 저장 완료: {output_file}")

if __name__ == "__main__":
    main()

