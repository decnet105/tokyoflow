"""
TokyoFlow Japanese • LLM Editorial Curator & Script Architect
Leverages OpenAI (GPT-4o / GPT-5.5) to select the daily Top-2 topics and compile
complete pedagogical breakdowns, bilingual YouTube packaging, and video production scripts.
"""

import os
import json
import urllib.request
from typing import List, Dict, Any

def get_openai_api_key() -> str:
    # 1. Check environment variable
    if os.environ.get("OPENAI_API_KEY"):
        return os.environ.get("OPENAI_API_KEY")
        
    # 2. Check shide-story-radar .env
    radar_env = "/Users/kilvonwu/Documents/shide-story-radar/.env"
    if os.path.exists(radar_env):
        try:
            with open(radar_env, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("OPENAI_API_KEY="):
                        return line.strip().split("=", 1)[1]
        except Exception:
            pass
            
    # 3. Check Mystory .env
    mystory_env = "/Users/kilvonwu/Documents/Mystory/.env"
    if os.path.exists(mystory_env):
        try:
            with open(mystory_env, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("OPENAI_API_KEY="):
                        return line.strip().split("=", 1)[1]
        except Exception:
            pass
            
    return ""

def call_openai_chat(messages: List[Dict[str, str]], model: str = "gpt-4o", json_mode: bool = True) -> Dict[str, Any]:
    api_key = get_openai_api_key()
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment or known config paths.")
        
    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.3
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
        
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        data=json.dumps(payload).encode("utf-8")
    )
    
    with urllib.request.urlopen(req, timeout=45) as resp:
        res_data = json.loads(resp.read().decode("utf-8"))
        raw_content = res_data["choices"][0]["message"]["content"]
        if json_mode:
            return json.loads(raw_content)
        return {"content": raw_content}

def curate_daily_topics(top_candidates: List[Dict[str, Any]], date_str: str) -> Dict[str, Any]:
    """
    Sends the top ranked candidates to the LLM to pick exactly 2 topics:
    Topic 1: Long-Form Deep Dive (Social / Policy / Tech / Macro-Culture)
    Topic 2: Shorts Viral Immersion (Life / Buzz / Entertainment / Trendy Slang)
    """
    candidates_summary = []
    for idx, c in enumerate(top_candidates[:12]):
        candidates_summary.append({
            "candidate_id": idx + 1,
            "title": c["representative_title"],
            "category": c["category"],
            "sources": c["sources"],
            "scores": c["scores"],
            "related_articles": [it["title"] for it in c["items"][:3]],
            "descriptions": [it.get("description", "") for it in c["items"] if it.get("description")]
        })
        
    system_prompt = """You are the Senior Executive Producer & Pedagogical Director of 'TokyoFlow Japanese' (a premier YouTube channel teaching real-life, high-engagement Japanese through authentic scenarios, news, and cultural trends).

### 🏆 频道 4 大核心竞争力 (Production Bible & Director Contract / 制作圣经与导演合同):
1. ⚡ **热点反应速度快 + 本地GEO精确定位**：同一天捕捉日本当下最热的流行、动漫、演艺与社会事件，锁定东京具体街区（涩谷、新宿、秋叶原、银座、六本木等）和高热度搜索实体，精准吃透 SEO & GEO 流量。
2. 🎭 **话题和视频好玩 + 真实新闻镜头与原声速报**：拒绝枯燥说教，以强戏剧冲突、反差萌（如天然呆）、文化趣味为核心切口，前置真实电视台新闻 HUD 与原声速报。
3. 🎯 **能学到对应级别 JLPT 内容**：严格坚守 70% JLPT N5（零基础小白友好）+ 20% N4-N3 配比，将复杂的行业新闻降维转化为极度地道的简单主谓宾（SOV）日常句式。
4. 🧠 **容易学 + 慢速发音 + 30fps逐词发光卡拉OK**：放慢语速（-10% ~ -12%），辅以毫秒级卡拉OK发光字幕和纯英语法文化拆解，实现极致无痛跟读。

### 🎬 频道 4 大核心播放列表 (Playlists) 与选品优先级：
1. **Playlist 1: 🎬 动漫·影视·娱乐·流行文化 (Anime, Manga, Film, TV & Pop Culture)** ➔ **【每日榜首/绝对核心主打】**
   - 包含：当季新番/漫画热点、热门电影/电视剧、声优/偶像轶事、日本网络流行梗、SNS 爆火现象、推特大热词。
2. **Playlist 2: 🍱 便利店与街头美食 (Kombini, Street Food & Izakaya)**
   - 包含：便利店新品热抢、网红餐厅、居酒屋点菜潜规则、日本饮食用语。
3. **Playlist 3: 🚃 东京交通与车站出行 (Transit & Station Navigation)**
   - 包含：电车站台广播、新线路/车票规则、交通出行实战口语。
4. **Playlist 4: 🗞️ 真实社会与突发新闻 (Real-Life News & Social Events)** ➔ **【辅助与次选】**
   - 包含：法律/生活新规、物价/消费税动态、社会突发热点、科技突破。

### 📊 选品与难易度配比铁律：
- **今日榜首 (Topic 1)**：**必须优先选择「娱乐·动漫·电影·电视·网络流行文化」**！以最大的趣味性、戏剧冲突和网民讨论度引爆播放。
- **辅助精讲 (Topic 2)**：可选择「便利店/美食/交通」或「社会突发新闻/新法新规」作为辅助，必须适配初学者 (N5-N4)。
- **难易度配比**：整体语料库严格遵守 70% N5-N4 (初学友好)、20% N3-N2 (中级实战)、10% N2-N1 (高级精深)。

### 🎯 降维教学与爆款法则：
1. **降维讲解（小白友好）**：即便热点是宏观大事件，也必须“大事件小切口”，用 N5-N4 的日常词汇和简单句做核心承载。
2. **拒绝开门见山教课**：严禁以“今天我们来学5个单词”开头！前 3-5 秒必须抛出强冲突、反差悬念 Hook。
3. **抓取日本 X/雅虎网民神评（ヤフコメ）**：揭秘真实语境下的吐槽与社会潜规则。
4. **Shorts 锁定 35-45 秒**：0-5s 悬念 Hook ➔ 5-25s 暗语拆解 ➔ 25-35s 黄金跟读 ➔ 35-45s 站队互动题（选A扣1选B扣2）。

Return strict, valid JSON with this exact schema:
{
  "date": "YYYY-MM-DD",
  "editorial_summary": "Rich overview in Chinese and English",
  "topic_1_long_form": {
    "candidate_id": 1,
    "event_headline": "Japanese original headline",
    "matched_playlist": "Playlist 1: 🎬 动漫·影视·娱乐·流行文化",
    "event_category": "Entertainment / Anime / Film / TV / Pop Culture",
    "target_jlpt_level": "N5-N4 (Beginner) / N3-N2 (Intermediate) / N2-N1 (Advanced)",
    "dramatic_conflict_hook": "事件的核心戏剧冲突与文化反差（为什么让人停下来看）",
    "why_selected": "Why this is high-value for Japanese learners & YouTube CTR",
    "yt_packaging": {
      "title_options": [
        "Title Option 1 (高点击悬念型)",
        "Title Option 2 (权威深度型)",
        "Title Option 3 (反常识认知冲突型)"
      ],
      "selected_title": "Primary Title",
      "thumbnail_hook_text": "3-5 word high-impact Japanese text on thumbnail",
      "thumbnail_visual_concept": "Visual description of thumbnail elements",
      "tags": ["Tag1", "Tag2", "Tag3", "Tag4", "Tag5"]
    },
    "pedagogical_payload": {
      "core_vocabulary": [
        {
          "kanji": "単語1",
          "furigana": "たんご1",
          "romaji": "tango1",
          "jlpt_level": "N5/N4/N3/N2/N1",
          "meaning_cn": "中文释义",
          "meaning_en": "English meaning",
          "usage_nuance": "How native Japanese actually use this term in media/life (文化语感与小白避坑提示)",
          "example_sentence": "例文（振り仮名付き）",
          "sentence_translation": "例句中文翻译"
        }
      ],
      "grammar_and_syntax": [
        {
          "pattern": "句型名称",
          "jlpt_level": "N5/N4/N3/N2/N1",
          "explanation": "文法讲解与初学者通俗语感解析",
          "news_context_usage": "在本次热点事件中的典型用法"
        }
      ],
      "netizen_reaction_quote": {
        "japanese": "日本网民高赞评论原句",
        "furigana": "ふりがな",
        "translation_cn": "中文翻译",
        "slang_or_subtext": "网民吐槽背后的潜台词与社会心态"
      },
      "cultural_insight": "Deep cultural context: Japanese societal perspective, unwritten rules, or historical context"
    },
    "production_script_outline": [
      {
        "scene_number": 1,
        "scene_name": "Suspense Hook & Background Drama",
        "audio_ja": "Japanese spoken line",
        "furigana": "Furigana string",
        "text_en": "English translation",
        "text_cn": "中文翻译",
        "visual_slide_prompt": "Slide layout description"
      },
      {
        "scene_number": 2,
        "scene_name": "Official Statement vs. True Nuance",
        "audio_ja": "Japanese spoken line",
        "furigana": "Furigana string",
        "text_en": "English translation",
        "text_cn": "中文翻译",
        "visual_slide_prompt": "Slide layout description"
      },
      {
        "scene_number": 3,
        "scene_name": "Netizen Buzzwords & Real Reaction",
        "audio_ja": "Japanese spoken line",
        "furigana": "Furigana string",
        "text_en": "English translation",
        "text_cn": "中文翻译",
        "visual_slide_prompt": "Slide layout description"
      },
      {
        "scene_number": 4,
        "scene_name": "Practical takeaway & Interactive Shadowing Outro",
        "audio_ja": "Japanese spoken line",
        "furigana": "Furigana string",
        "text_en": "English translation",
        "text_cn": "中文翻译",
        "visual_slide_prompt": "Outro slide with TokyoFlow App CTA"
      }
    ]
  },
  "topic_2_shorts": {
    "candidate_id": 2,
    "event_headline": "Japanese original headline",
    "matched_playlist": "Playlist 2 (Kombini/Foodie) OR Playlist 3 (Transit) OR Playlist 4 (Social News)",
    "event_category": "Viral / Kombini / Food / Transit / Society",
    "target_jlpt_level": "N5-N4 (Must prioritize beginner-friendly N5-N4 for Shorts)",
    "why_selected": "Why this will go viral on Shorts/TikTok",
    "shorts_packaging": {
      "title": "Shorts Title with Hashtags (30-45s optimized)",
      "hook_overlay_text": "Top text badge on vertical video (0-3s 反差大字)",
      "interactive_poll_question": "互动站队/测试题 (如: 遇到这种情况日本人会选A还是B？选A扣1，选B扣2)",
      "pinned_comment_prompt": "置顶评论互动文案"
    },
    "pedagogical_payload": {
      "buzzwords": [
        {
          "word": "流行語・キーワード1",
          "reading": "読み方1",
          "jlpt_level": "N5/N4/N3",
          "meaning_cn": "中文释义",
          "meaning_en": "English meaning",
          "slang_or_nuance": "流行背景与口语语感 (通俗直白)"
        }
      ],
      "gold_shadowing_sentence": {
        "japanese": "一秒抓耳的地道日语句子 (小白也能跟读)",
        "furigana": "ふりがな",
        "translation_cn": "中文翻译",
        "translation_en": "English translation",
        "pitch_accent_note": "音调/语调提示 (如: 頭高型、平板型、起伏标注)"
      }
    },
    "shorts_timeline_script": [
      {
        "timeframe": "0:00 - 0:05",
        "section": "Viral Suspense Hook (反差/冲突)",
        "audio_ja": "台词",
        "text_cn": "中文",
        "visual_direction": "画面视觉描述"
      },
      {
        "timeframe": "0:05 - 0:25",
        "section": "Core Buzzwords & Netizen Subtext (真实暗语/神评拆解)",
        "audio_ja": "台词",
        "text_cn": "中文",
        "visual_direction": "画面视觉描述"
      },
      {
        "timeframe": "0:25 - 0:35",
        "section": "Speed Shadowing Repeat Drill (黄金跟读)",
        "audio_ja": "台词",
        "text_cn": "中文",
        "visual_direction": "画面视觉描述"
      },
      {
        "timeframe": "0:35 - 0:45",
        "section": "Interactive Poll & CTA (站队扣1/2 + TokyoFlow App)",
        "audio_ja": "台词",
        "text_cn": "中文",
        "visual_direction": "画面视觉描述"
      }
    ]
  }
}
"""

    user_prompt = f"""Date: {date_str}

Here are today's top scored candidate events clustered from Yahoo News Japan, NHK, Google News JP, and Hatena:
{json.dumps(candidates_summary, ensure_ascii=False, indent=2)}

Please select Topic 1 (Long-Form Deep Dive) and Topic 2 (Shorts Viral Immersion), and produce the complete JSON production payload according to the system prompt."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    return call_openai_chat(messages, model="gpt-4o", json_mode=True)
