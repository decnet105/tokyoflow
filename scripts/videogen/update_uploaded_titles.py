#!/usr/bin/env python3
import os
import sys
import json
from pathlib import Path
from googleapiclient.discovery import build

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(Path(__file__).resolve().parent))
from youtube_auth import get_authenticated_service

creds = get_authenticated_service()
youtube = build('youtube', 'v3', credentials=creds)

wl_meta = (PROJECT_ROOT / 'docs/youtube_releases/WL01-last-mile-masterclass-v1.0-zh/metadata.md').read_text(encoding='utf-8')
wl_short_meta = (PROJECT_ROOT / 'docs/youtube_releases/WL01-last-mile-masterclass-v1.0-zh/short_metadata.md').read_text(encoding='utf-8')
wm_meta = (PROJECT_ROOT / 'docs/youtube_releases/WM01-weekday_survival_mega_compilation-v1.0-zh/metadata.md').read_text(encoding='utf-8')
wm_short_meta = (PROJECT_ROOT / 'docs/youtube_releases/WM01-weekday_survival_mega_compilation-v1.0-zh/short_metadata.md').read_text(encoding='utf-8')

updates = [
    {
        'id': 'AaWSZ4J2fSI',
        'title': '【JLPT N5-N2】电影《最后的里程》影视沉浸精讲（WL.01）| 满岛光×冈田将生 2024票房冠军超长深度解析',
        'desc': wl_meta.split('```')[3].strip(),
        'tags': ['日语学习', '最后的里程', '满岛光', '冈田将生', '看电影学日语', 'JLPT N5', 'JLPT N4', 'JLPT N3', 'JLPT N2', 'TokyoFlow']
    },
    {
        'id': 'vMM1KrOG4j4',
        'title': '【JLPT N3】电影《最后的里程》高光台词跟读！2.7m/s绝不停运？（WS.01） #Shorts',
        'desc': wl_short_meta.split('```')[3].strip(),
        'tags': ['Shorts', '日语学习', '最后的里程', '满岛光', 'JLPTN3', 'TokyoFlow']
    },
    {
        'id': 'jFEtdDNpvlg',
        'title': '【JLPT N5-N3】周一到周五东京生活全景大合集（WM.01）| 电车·便利店·居酒屋·秋叶原·拉面·温泉全场景28分钟精讲',
        'desc': wm_meta.split('```')[3].strip(),
        'tags': ['日语学习', '东京生活', '日本旅游日语', 'JLPT N5', 'JLPT N4', 'JLPT N3', '山手线', '便利店日语', 'TokyoFlow']
    },
    {
        'id': '4_95LXM4uj0',
        'title': '【JLPT N4】听懂山手线站台广播！黄色盲道退后提示与自谦语精讲（WS.01） #Shorts',
        'desc': wm_short_meta.split('```')[3].strip(),
        'tags': ['Shorts', '日语学习', '山手线', '东京生活', 'JLPTN4', 'TokyoFlow']
    }
]

for item in updates:
    try:
        req = youtube.videos().update(
            part='snippet',
            body={
                'id': item['id'],
                'snippet': {
                    'title': item['title'],
                    'description': item['desc'],
                    'tags': item['tags'],
                    'categoryId': '27',
                    'defaultLanguage': 'zh',
                    'defaultAudioLanguage': 'ja'
                }
            }
        )
        res = req.execute()
        print(f"Updated metadata for {item['id']}: {res['snippet']['title']}")
    except Exception as e:
        print(f"Error updating {item['id']}: {e}")
