#!/usr/bin/env python3
"""
TokyoFlow Japanese • Daily Japan & Global Hot Event Scanner
Entrypoint CLI: Scans multi-source Japanese feeds, clusters, scores,
and runs AI curation to generate the Daily Top-2 YouTube Topics (Long-form + Shorts).
"""

import os
import sys
import json
import argparse
from datetime import datetime

# Local imports
from sources import fetch_all_sources
from scorer import rank_and_filter_candidates
from llm_curator import curate_daily_topics

def format_markdown_report(data: dict) -> str:
    date_str = data.get("date", datetime.now().strftime("%Y-%m-%d"))
    summary = data.get("editorial_summary", "")
    diff = data.get("difficulty_tier_for_today", {})
    t1 = data.get("topic_1_long_form", {})
    t2 = data.get("topic_2_shorts", {})
    
    md = []
    md.append(f"# 🌸 TokyoFlow Japanese • 每日日本热点选题雷达 ({date_str})")
    md.append(f"\n> **今日日本热点综述**：{summary}\n")
    md.append(f"> 🎯 **今日受众难度配比 (70% N5-N4 / 20% N3-N2 / 10% N2-N1)**：")
    md.append(f"> - 话题 1 (Long-form 难度)：`{t1.get('target_jlpt_level', diff.get('topic_1_level', 'N3-N2'))}`")
    md.append(f"> - 话题 2 (Shorts 难度)：`{t2.get('target_jlpt_level', diff.get('topic_2_level', 'N5-N4 (初学友好)'))}`\n")
    md.append("---\n")
    
    # Topic 1
    md.append("## 📌 话题 1 (当日前置/榜首主打) — 🎬 娱乐·动漫·影视·流行文化")
    md.append(f"- **归属播放列表**：`{t1.get('matched_playlist', 'Playlist 1: 🎬 动漫·影视·娱乐·流行文化')}`")
    md.append(f"- **事件原标题**：`{t1.get('event_headline')}`")
    md.append(f"- **分类与难度**：`{t1.get('event_category')}` | 🎯 **目标级别**: `{t1.get('target_jlpt_level', 'N5-N4 (初学友好)')}`")
    if t1.get("dramatic_conflict_hook"):
        md.append(f"- **🎭 核心戏剧冲突与悬念**：*{t1.get('dramatic_conflict_hook')}*")
    md.append(f"- **入选理由 & 教学价值**：{t1.get('why_selected')}\n")
    
    pkg1 = t1.get("yt_packaging", {})
    md.append("### 🎬 YouTube 包装与点击率策略")
    md.append(f"- **推荐主标题**：`{pkg1.get('selected_title')}`")
    md.append(f"- **备选标题库**：")
    for opt in pkg1.get("title_options", []):
        md.append(f"  - {opt}")
    md.append(f"- **封面高转化文案 (Thumbnail Hook)**：`{pkg1.get('thumbnail_hook_text')}`")
    md.append(f"- **封面视觉构图**：{pkg1.get('thumbnail_visual_concept')}")
    md.append(f"- **SEO 标签 (Tags)**：`{', '.join(pkg1.get('tags', []))}`\n")
    
    ped1 = t1.get("pedagogical_payload", {})
    md.append("### 📚 核心日语教学资产 (Pedagogical Payload)")
    md.append("#### 1. 核心词汇精讲 (Core Vocabulary)")
    for v in ped1.get("core_vocabulary", []):
        md.append(f"- **{v.get('kanji')}** 【{v.get('furigana')}】 (`{v.get('jlpt_level')}`): {v.get('meaning_cn')} ({v.get('meaning_en')})")
        md.append(f"  - *地法语感*：{v.get('usage_nuance')}")
        md.append(f"  - *热点例句*：{v.get('example_sentence')}")
        md.append(f"  - *例句翻译*：{v.get('sentence_translation')}")
        
    md.append("\n#### 2. 高阶语法与表达 (Grammar & Syntax)")
    for g in ped1.get("grammar_and_syntax", []):
        md.append(f"- **句型**：`{g.get('pattern')}` (`{g.get('jlpt_level')}`)")
        md.append(f"  - *语法说明*：{g.get('explanation')}")
        md.append(f"  - *事件语境应用*：{g.get('news_context_usage')}")

    netizen = ped1.get("netizen_reaction_quote")
    if netizen:
        md.append("\n#### 3. 日本网民神评与网络潜台词 (Netizen Voice & Subtext)")
        md.append(f"- **网民原声**：`{netizen.get('japanese')}`")
        md.append(f"- **假名标注**：{netizen.get('furigana')}")
        md.append(f"- **中文释义**：{netizen.get('translation_cn')}")
        md.append(f"- **吐槽潜台词**：*{netizen.get('slang_or_subtext')}*")
        
    md.append(f"\n#### 4. 日本社会文化潜台词 (Cultural Insight)")
    md.append(f"{ped1.get('cultural_insight')}\n")
    
    md.append("### 🎙️ 视频分镜与音频台词大纲 (Production Script Outline)")
    for sc in t1.get("production_script_outline", []):
        md.append(f"#### Scene {sc.get('scene_number')}: {sc.get('scene_name')}")
        md.append(f"- **日语音频**：`{sc.get('audio_ja')}`")
        md.append(f"- **振假名标注**：{sc.get('furigana')}")
        md.append(f"- **中文对照**：{sc.get('text_cn')}")
        md.append(f"- **画面指示**：*{sc.get('visual_slide_prompt')}*")
        
    md.append("\n---\n")
    
    # Topic 2
    md.append("## ⚡ 话题 2 (辅助/精讲短视频) — 🍱 美食/便利店/交通 或 🗞️ 社会生活热点")
    md.append(f"- **归属播放列表**：`{t2.get('matched_playlist', 'Playlist 2 (Kombini/Foodie) / Playlist 3 (Transit) / Playlist 4 (News)')}`")
    md.append(f"- **事件原标题**：`{t2.get('event_headline')}`")
    md.append(f"- **分类与难度**：`{t2.get('event_category')}` | 🎯 **目标级别**: `{t2.get('target_jlpt_level', 'N5-N4 (初学友好)')}`")
    md.append(f"- **完播与爆款逻辑**：{t2.get('why_selected')}\n")
    
    pkg2 = t2.get("shorts_packaging", {})
    md.append("### 📱 Shorts 包装与吸睛策略")
    md.append(f"- **Shorts 标题**：`{pkg2.get('title')}`")
    md.append(f"- **黄金 3 秒顶部大字 (Hook Overlay)**：`{pkg2.get('hook_overlay_text')}`")
    if pkg2.get("interactive_poll_question"):
        md.append(f"- **🔥 评论区站队/测试互动题**：`{pkg2.get('interactive_poll_question')}`")
    md.append(f"- **置顶互动评论 (Pinned Comment)**：`{pkg2.get('pinned_comment_prompt')}`\n")
    
    ped2 = t2.get("pedagogical_payload", {})
    md.append("### 🎯 爆款词汇与黄金跟读句")
    md.append("#### 1. 核心热词 / 流行语 (Buzzwords)")
    for bw in ped2.get("buzzwords", []):
        md.append(f"- **{bw.get('word')}** 【{bw.get('reading')}】：{bw.get('meaning_cn')} ({bw.get('meaning_en')})")
        md.append(f"  - *流行背景/口语语感*：{bw.get('slang_or_nuance')}")
        
    gs = ped2.get("gold_shadowing_sentence", {})
    md.append(f"\n#### 2. 一秒跟读黄金句 (Gold Shadowing Drill)")
    md.append(f"- **日语原文**：`{gs.get('japanese')}`")
    md.append(f"- **振假名**：{gs.get('furigana')}")
    md.append(f"- **中文释义**：{gs.get('translation_cn')}")
    md.append(f"- **声调与发音要点**：*{gs.get('pitch_accent_note')}*\n")
    
    md.append("### ⏱️ Shorts 45 秒分镜脚本 (Shorts Timeline Script)")
    for st in t2.get("shorts_timeline_script", []):
        md.append(f"- **[{st.get('timeframe')}] {st.get('section')}**")
        md.append(f"  - 日语台词：`{st.get('audio_ja')}`")
        md.append(f"  - 中文对照：{st.get('text_cn')}")
        md.append(f"  - 画面指引：*{st.get('visual_direction')}*")
        
    md.append("\n---\n")
    md.append("💡 *Generated by TokyoFlow Japan Trend Radar System. Directly feeds into `scripts/videogen/pipeline.py` & `build_all_shorts.py`.*")
    return "\n".join(md)

def main():
    parser = argparse.ArgumentParser(description="TokyoFlow Japan Daily Hot Trend Scanner")
    parser.add_argument("--dry-run", action="store_true", help="Fetch & cluster news without calling LLM")
    parser.add_argument("--date", type=str, default=datetime.now().strftime("%Y-%m-%d"), help="Target date YYYY-MM-DD")
    parser.add_argument("--top", type=int, default=10, help="Number of top candidate clusters to display")
    parser.add_argument("--out-dir", type=str, default="output/trend_reports", help="Output directory for reports")
    args = parser.parse_args()
    
    os.makedirs(args.out_dir, exist_ok=True)
    
    print(f"📡 [1/4] Scanning Japanese news feeds across 15+ channels...")
    items = fetch_all_sources(timeout=8)
    print(f"✓ Fetched {len(items)} raw headlines.")
    
    print(f"🔍 [2/4] Clustering events & scoring pedagogical value...")
    ranked_candidates = rank_and_filter_candidates(items)
    print(f"✓ Formed {len(ranked_candidates)} distinct event clusters.")
    
    print("\n" + "=" * 80)
    print(f"🏆 TOP {min(args.top, len(ranked_candidates))} CANDIDATE CLUSTERS (Date: {args.date})")
    print("=" * 80)
    for idx, c in enumerate(ranked_candidates[:args.top], 1):
        scores = c['scores']
        print(f"#{idx:02d} [{c['category']}] {c['representative_title']}")
        print(f"     📊 Composite Score: {scores['composite_score']} (Virality: {scores['virality']}, Pedagogy: {scores['pedagogical_value']}, Fit: {scores['channel_fit']})")
        print(f"     🗞️ Sources ({len(c['sources'])}): {', '.join(c['sources'][:3])} | Rec Format: {c['format_recommendation']}")
        if c.get("boost_keywords"):
            print(f"     🔑 Key Learning Hooks: {', '.join(c['boost_keywords'][:5])}")
        print("-" * 80)
        
    if args.dry_run:
        print("\n⚡ --dry-run specified. Skipping LLM curation.")
        return
        
    print(f"\n🤖 [3/4] Invoking LLM Editorial Curator for Top-2 Topics & Scripts...")
    editorial_payload = curate_daily_topics(ranked_candidates, args.date)
    print("✓ Successfully curated Top-2 Topics and generated video production scripts.")
    
    print(f"\n💾 [4/4] Writing reports to {args.out_dir}...")
    json_path = os.path.join(args.out_dir, f"{args.date}_japan_trends.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(editorial_payload, f, ensure_ascii=False, indent=2)
    print(f"✓ Saved JSON: {json_path}")
    
    md_content = format_markdown_report(editorial_payload)
    md_path = os.path.join(args.out_dir, f"{args.date}_daily_editorial.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"✓ Saved Markdown Report: {md_path}")
    
    print("\n✨ Daily Trend Scan & Editorial Planning Completed Successfully!")

if __name__ == "__main__":
    main()
