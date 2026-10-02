"""
TokyoFlow Japanese • Multi-Source Trend Radar Feeds
Fetches real-time trending news from top Japanese sources:
- Yahoo News Japan (Top, Domestic, World, Business, IT, Entertainment)
- NHK News Web (Top, Society, Science, Culture, World)
- Google News Japan (Top, World, Tech, Entertainment)
- Asahi Shimbun & Mainichi Shimbun Flash
- Hatena Bookmark Hotentries (Viral discussions, Tech, Culture)
"""

import urllib.request
import xml.etree.ElementTree as ET
import re
import html
from typing import List, Dict, Any
from datetime import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

FEED_DEFINITIONS = [
    # Yahoo News Japan
    {"name": "Yahoo! ニュース (主要)", "category": "General", "url": "https://news.yahoo.co.jp/rss/topics/top-picks.xml", "weight": 1.2},
    {"name": "Yahoo! ニュース (国内)", "category": "Domestic", "url": "https://news.yahoo.co.jp/rss/topics/domestic.xml", "weight": 1.1},
    {"name": "Yahoo! ニュース (国際)", "category": "World", "url": "https://news.yahoo.co.jp/rss/topics/world.xml", "weight": 1.1},
    {"name": "Yahoo! ニュース (経済)", "category": "Business", "url": "https://news.yahoo.co.jp/rss/topics/business.xml", "weight": 1.0},
    {"name": "Yahoo! ニュース (IT・科学)", "category": "Tech", "url": "https://news.yahoo.co.jp/rss/topics/it.xml", "weight": 1.0},
    {"name": "Yahoo! ニュース (エンタメ)", "category": "Entertainment", "url": "https://news.yahoo.co.jp/rss/topics/entertainment.xml", "weight": 0.9},

    # NHK News
    {"name": "NHK ニュース (主要)", "category": "General", "url": "https://www.nhk.or.jp/rss/news/cat0.xml", "weight": 1.2},
    {"name": "NHK ニュース (社会)", "category": "Society", "url": "https://www.nhk.or.jp/rss/news/cat1.xml", "weight": 1.0},
    {"name": "NHK ニュース (科学・文化)", "category": "Culture", "url": "https://www.nhk.or.jp/rss/news/cat4.xml", "weight": 1.0},

    # Google News JP
    {"name": "Google News 日本 (Top)", "category": "General", "url": "https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja", "weight": 1.1},
    {"name": "Google News 日本 (World)", "category": "World", "url": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=ja&gl=JP&ceid=JP:ja", "weight": 1.0},
    {"name": "Google News 日本 (Tech)", "category": "Tech", "url": "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=ja&gl=JP&ceid=JP:ja", "weight": 1.0},

    # Asahi / Mainichi
    {"name": "朝日新聞 (速報)", "category": "General", "url": "https://rss.asahi.com/rss/asahi/newsheadlines.rdf", "weight": 1.0},
    {"name": "毎日新聞 (速報)", "category": "General", "url": "https://mainichi.jp/rss/etc/mainichi-flash.rss", "weight": 1.0},

    # Hatena Hotentries (Viral Social & Tech Buzz)
    {"name": "はてなブックマーク (総合人気)", "category": "Viral", "url": "https://b.hatena.ne.jp/hotentry.rss", "weight": 1.1},
    {"name": "はてなブックマーク (テクノロジー)", "category": "Tech", "url": "https://b.hatena.ne.jp/hotentry/it.rss", "weight": 0.9},
    {"name": "はてなブックマーク (暮らし・学び)", "category": "Culture", "url": "https://b.hatena.ne.jp/hotentry/life.rss", "weight": 0.9},
]

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def fetch_feed(feed_def: Dict[str, Any], timeout: int = 8) -> List[Dict[str, Any]]:
    items = []
    try:
        req = urllib.request.Request(feed_def["url"], headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content = resp.read()
            root = ET.fromstring(content)
            
            # Match items regardless of XML namespaces
            xml_items = [elem for elem in root.iter() if elem.tag.endswith('item')]
            
            for item in xml_items:
                title = ""
                link = ""
                desc = ""
                pub_date = ""
                
                for child in item:
                    tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                    if tag == 'title' and child.text:
                        title = clean_text(child.text)
                    elif tag == 'link' and child.text:
                        link = child.text.strip()
                    elif tag in ('description', 'encoded') and child.text and not desc:
                        desc = clean_text(child.text)
                    elif tag in ('pubDate', 'date') and child.text:
                        pub_date = child.text.strip()
                        
                if title:
                    items.append({
                        "source": feed_def["name"],
                        "category": feed_def["category"],
                        "source_weight": feed_def["weight"],
                        "title": title,
                        "link": link,
                        "description": desc,
                        "pub_date": pub_date,
                        "fetched_at": datetime.now().isoformat()
                    })
    except Exception as e:
        # Graceful degradation for single feed failure
        pass
        
    return items

def fetch_all_sources(timeout: int = 8) -> List[Dict[str, Any]]:
    all_items = []
    for feed in FEED_DEFINITIONS:
        items = fetch_feed(feed, timeout=timeout)
        all_items.extend(items)
    return all_items
