import sys
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urlparse, parse_qs

def parse_article(url: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/116.0.0.0 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    header = soup.find("header", class_="article-view-header")
    if not header:
        raise Exception("기사 헤더를 찾을 수 없습니다")

    title_tag = header.find("h1", class_="heading")
    reporter_tag = header.find("li", class_="name")
    date_tag = header.find_all("li")[-1]

    title = title_tag.get_text(strip=True) if title_tag else "제목 없음"
    reporter = reporter_tag.get_text(strip=True) if reporter_tag else "기자명 없음"
    date = date_tag.get_text(strip=True) if date_tag else "날짜 없음"

    article_body = soup.find("div", class_="article-body")
    if article_body:
        paragraphs = article_body.find_all(["p", "div"])
        body = "\n\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
    else:
        body = "(본문을 찾을 수 없습니다)"

    return {
        "title": title,
        "reporter": reporter,
        "date": date,
        "url": url,
        "body": body,
    }

def save_markdown(article: dict, out_path: Path):
    content = f"""# {article['title']}

- 기자: {article['reporter']}
- 날짜: {article['date']}
- 원문 링크: {article['url']}

---

{article['body']}
"""
    out_path.write_text(content, encoding="utf-8")

def main():
    if len(sys.argv) < 2:
        print("사용법: python main.py [기사 URL]")
        sys.exit(1)

    url = sys.argv[1]
    article = parse_article(url)

    # URL에서 idxno 추출 (예: idxno=202)
    parsed_url = urlparse(url)
    qs = parse_qs(parsed_url.query)
    idxno = qs.get("idxno", ["unknown"])[0]

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / f"{idxno}.md"
    save_markdown(article, output_file)
    print(f"✅ 저장 완료: {output_file}")

if __name__ == "__main__":
    main()

