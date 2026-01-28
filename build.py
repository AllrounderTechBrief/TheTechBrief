import os, json, re, time
import feedparser
from bs4 import BeautifulSoup
from slugify import slugify
from jinja2 import Template
from summarize import summarize_text

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA = os.path.join(ROOT, 'data', 'feeds.json')
META = os.path.join(ROOT, 'data', 'meta.json')
SITE = os.path.join(ROOT, 'site')

# Load templates
with open(os.path.join(SITE, 'template_category.html'), 'r', encoding='utf-8') as f:
    CATEGORY_TPL = Template(f.read())
with open(os.path.join(SITE, 'template_home.html'), 'r', encoding='utf-8') as f:
    HOME_TPL = Template(f.read())
with open(DATA, 'r', encoding='utf-8') as f:
    FEEDS = json.load(f)
with open(META, 'r', encoding='utf-8') as f:
    META_MAP = json.load(f)


def clean_text(html):
    txt = BeautifulSoup(html or '', 'html.parser').get_text(' ')
    return re.sub(r"\s+", " ", txt).strip()


def first_image(entry):
    media = entry.get('media_content') or entry.get('media_thumbnail')
    if media and isinstance(media, list):
        url = media[0].get('url')
        if url: return url
    enc = entry.get('enclosures')
    if enc and isinstance(enc, list):
        for e in enc:
            if 'image' in e.get('type',''):
                if e.get('href'): return e.get('href')
    desc = entry.get('summary') or entry.get('description') or ''
    soup = BeautifulSoup(desc, 'html.parser')
    img = soup.find('img')
    return img['src'] if img and img.has_attr('src') else None


def parse_time(entry):
    t = entry.get('published_parsed') or entry.get('updated_parsed')
    if t:
        return time.mktime(t)
    return 0


def build_category(category, urls):
    items = []
    for url in urls:
        feed = feedparser.parse(url)
        for e in feed.entries[:10]:
            title = e.get('title', 'Untitled')
            link = e.get('link')
            source = feed.feed.get('title', 'Unknown')
            text = clean_text(e.get('summary') or e.get('description') or '')
            summary = summarize_text(text, sentences=2)
            img = first_image(e)
            items.append({
                'title': title,
                'link': link,
                'source': source,
                'summary': summary,
                'image': img,
                'ts': parse_time(e),
                'category': category
            })
    items.sort(key=lambda x: x['ts'], reverse=True)
    meta = META_MAP.get(category, {'title': category, 'description': category, 'h1': category, 'h2': ''})
    html = CATEGORY_TPL.render(meta=meta, cards=items)
    out = os.path.join(SITE, f"{slugify(category)}.html")
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    return items[:24]


def build_home(all_items):
    meta = META_MAP['Home']
    html = HOME_TPL.render(meta=meta, cards=all_items[:24])
    with open(os.path.join(SITE, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    all_items = []
    for cat, urls in FEEDS.items():
        top_items = build_category(cat, urls)
        all_items.extend(top_items)
    all_items.sort(key=lambda x: x['ts'], reverse=True)
    build_home(all_items)

if __name__ == '__main__':
    main()
