"""
TokyoFlow Japanese • Event Clustering & Pedagogical Scorer
Deduplicates news across multiple Japanese sources, clusters related events,
and evaluates candidates for virality, Japanese language learning value, and TokyoFlow channel fit.
"""

import re
from typing import List, Dict, Any

# Keywords that boost pedagogical and cultural value for Japanese learners
PEDAGOGICAL_BOOST_KEYWORDS = [
    # Top Priority: Entertainment, Anime, Manga, Film, TV & Pop Culture
    "アニメ", "マンガ", "声優", "映画", "ドラマ", "大ヒット", "記録", "新作", "特報",
    "主題歌", "聖地巡礼", "推し活", "オタク", "トレンド", "SNS", "バズ", "炎上",
    "流行", "話題", "新語", "注目", "人気", "若者", "イベント", "コラボ",
    # Foodie, Kombini & Street Life
    "コンビニ", "グルメ", "スイーツ", "限定", "新発売", "居酒屋", "ラーメン", "カフェ",
    # Transit & City Living
    "鉄道", "駅", "ダイヤ改正", "山手線", "地下鉄", "マナー", "ルール",
    # Society, Tech & General News (Auxiliary)
    "法案", "減税", "方針", "発表", "統合", "改革", "義務化", "導入", "議論",
    "値上げ", "円安", "物価", "訪日", "観光", "免税", "インバウンド",
    "AI", "技術", "開発", "サービス", "新型", "対策", "トラブル", "実態"
]

# Penalty keywords for topics with poor learning/creative video fit
NOISE_PENALTY_KEYWORDS = [
    "震度1", "震度2", "津波の心配なし", "小雨", "波浪注意报",
    "高校野球結果", "Jリーグ結果", "競馬", "競艇", "パチンコ",
    "容疑で逮捕", "ひき逃げ", "物置小屋全焼"  # Routine petty crime or minor local blots
]

def extract_keywords(title: str) -> set:
    """Extracts significant Japanese words/tokens from title for clustering."""
    clean = re.sub(r'【[^】]*】|\[[^\]]*\]|（[^）]*）|\([^\)]*\)| - .*$', '', title)
    tokens = re.findall(r'[\u4e00-\u9faf]{2,}|[ァ-ヶー]{2,}|[a-zA-Z0-9]{2,}', clean)
    return set(tokens)

def compute_similarity(tokens1: set, tokens2: set) -> float:
    if not tokens1 or not tokens2:
        return 0.0
    intersection = len(tokens1 & tokens2)
    union = len(tokens1 | tokens2)
    return intersection / union if union > 0 else 0.0

def cluster_events(items: List[Dict[str, Any]], similarity_threshold: float = 0.28) -> List[Dict[str, Any]]:
    """Groups related news items into clusters based on shared keywords."""
    clusters = []
    
    for item in items:
        item_tokens = extract_keywords(item["title"])
        if not item_tokens:
            continue
            
        matched_cluster = None
        best_sim = 0.0
        
        for cluster in clusters:
            sim = compute_similarity(item_tokens, cluster["all_tokens"])
            if sim > best_sim and sim >= similarity_threshold:
                best_sim = sim
                matched_cluster = cluster
                
        if matched_cluster:
            matched_cluster["items"].append(item)
            matched_cluster["all_tokens"].update(item_tokens)
            matched_cluster["sources"].add(item["source"])
            matched_cluster["total_weight"] += item["source_weight"]
        else:
            clusters.append({
                "representative_title": item["title"],
                "items": [item],
                "all_tokens": set(item_tokens),
                "sources": {item["source"]},
                "category": item["category"],
                "total_weight": item["source_weight"]
            })
            
    # Sort items within each cluster by source weight
    for cluster in clusters:
        cluster["items"].sort(key=lambda x: x["source_weight"], reverse=True)
        cluster["representative_title"] = cluster["items"][0]["title"]
        cluster["sources"] = list(cluster["sources"])
        del cluster["all_tokens"]
        
    return clusters

def score_cluster(cluster: Dict[str, Any]) -> Dict[str, Any]:
    """Calculates Virality, Pedagogical Value, and Channel Fit scores."""
    rep_title = cluster["representative_title"]
    all_titles_text = " ".join([it["title"] + " " + it.get("description", "") for it in cluster["items"]])
    
    # 1. Virality & Multi-source resonance (0-10)
    source_count = len(cluster["sources"])
    virality_score = min(10.0, 3.0 + (source_count * 1.5) + (cluster["total_weight"] * 1.0))
    if any(kw in all_titles_text for kw in ["話題", "注目", "急増", "人気", "異例", "初", "新語"]):
        virality_score = min(10.0, virality_score + 1.5)
        
    # 2. Pedagogical Value (0-10)
    pedagogy_score = 5.0
    boost_matches = [kw for kw in PEDAGOGICAL_BOOST_KEYWORDS if kw in all_titles_text]
    pedagogy_score += min(4.0, len(boost_matches) * 0.8)
    
    # Check for kanji compounds count (rich vocabulary)
    kanji_compounds = len(re.findall(r'[\u4e00-\u9faf]{2,}', rep_title))
    if kanji_compounds >= 3:
        pedagogy_score = min(10.0, pedagogy_score + 1.0)
        
    # 3. Penalties for noise / routine local incidents
    for penalty_kw in NOISE_PENALTY_KEYWORDS:
        if penalty_kw in rep_title:
            pedagogy_score -= 3.5
            virality_score -= 2.0
            
    # 4. TokyoFlow Channel Fit (0-10)
    # TokyoFlow Playlists Priority:
    # Top 1: Anime, Manga, Film, TV, Pop Culture & Entertainment (当日前置/榜首)
    # Top 2: Kombini, Street Foodie & Izakaya
    # Top 3: Transit & City Navigation
    # Top 4: Society, Tech & Real News (辅助/次选)
    category = cluster.get("category", "General")
    cat_bonus = {
        "Entertainment": 2.5,
        "Culture": 2.3,
        "Viral": 2.2,
        "Tech": 1.4,
        "Domestic": 1.2,
        "Society": 1.1,
        "Business": 1.0,
        "World": 0.9,
        "General": 1.0
    }.get(category, 1.0)
    
    fit_score = min(10.0, (pedagogy_score * 0.5 + virality_score * 0.5) * (cat_bonus / 1.5))
    
    # Total Composite Score
    total_score = round(virality_score * 0.35 + pedagogy_score * 0.40 + fit_score * 0.25, 2)
    
    # Format Recommendation
    is_long_form_suited = (category in ["Entertainment", "Culture", "Tech", "Society", "Domestic"]) and len(cluster["items"]) >= 2
    format_recommendation = "Long-Form Deep Dive" if is_long_form_suited else "Shorts Viral Immersion"
    
    cluster["scores"] = {
        "virality": round(virality_score, 1),
        "pedagogical_value": round(pedagogy_score, 1),
        "channel_fit": round(fit_score, 1),
        "composite_score": total_score
    }
    cluster["format_recommendation"] = format_recommendation
    cluster["boost_keywords"] = boost_matches
    
    return cluster

def rank_and_filter_candidates(items: List[Dict[str, Any]], min_score: float = 4.5) -> List[Dict[str, Any]]:
    """Runs clustering and scoring, returns ranked candidate topics."""
    clusters = cluster_events(items)
    scored = [score_cluster(c) for c in clusters]
    filtered = [c for c in scored if c["scores"]["composite_score"] >= min_score]
    filtered.sort(key=lambda x: x["scores"]["composite_score"], reverse=True)
    return filtered
