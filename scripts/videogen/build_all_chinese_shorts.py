#!/usr/bin/env python3
"""
TokyoFlow Japanese - Chinese YouTube Shorts Master Factory
============================================================
Produces 9:16 vertical videos (1080x1920) for Chinese Edition (WS.01, WS.02, EP.01 ~ EP.11):
1. Frame 0-5: First-Frame Master Cover Injection (for 100% YouTube Shorts Thumbnail Auto-Capture)
2. Stage 0: Scenario Introduction & Hook (zh-CN-YunxiNeural)
3. Stage 1: STEP 1 Native Tokyo Speed Blind Listening + Millisecond Ruby Karaoke (ja-JP-NanamiNeural)
4. Stage 2: STEP 2 Seamless In-Line Bilingual Breakdown (Yunxi Chinese + Nanami Tokyo Japanese)
5. Stage 3: STEP 3 YOUR TURN Shadow Out Loud (3-2-1 Beep + Nanami Practice Drill Voice + Live Glowing Karaoke)
6. Stage 4: STEP 4 AI Pitch Match Scoring (98.6% MATCH) + Masterclass Funnel CTA / App CTA

Strict Zero Emoji Discipline is enforced across all operations.
"""

import os
import sys
import math
import shutil
import asyncio
import subprocess
import edge_tts
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timing_engine import align_sentence_tokens_with_audio
from seamless_tts_engine import synthesize_seamless_bilingual_audio

FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"

def get_font(size: int):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

def get_audio_duration(audio_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        return float(res.stdout.strip())
    except Exception:
        return 5.0

async def synth_audio(text: str, voice: str, out_path: str, rate: str = "+0%", pitch: str = "+0Hz"):
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(out_path)

def generate_beep(freq: int, duration: float, out_path: str):
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", f"sine=frequency={freq}:duration={duration}",
        "-c:a", "libmp3lame", out_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

CHINESE_SHORTS_CONFIGS = [
    # -------------------------------------------------------------------------
    # WS.01: 《最后的里程》电影高光台词 (JLPT N3) - WL.01 Funnel
    # -------------------------------------------------------------------------
    {
        "ep_num": 101,
        "shorts_code": "WS.01",
        "folder": "WL01-last-mile-masterclass-v1.0-zh",
        "jlpt_level": "JLPT N3",
        "district": "关东物流中心 • 满岛光 2024 大片",
        "category": "影视沉浸 • 悬疑剧情",
        "hook_title": "2.7米/秒 绝不停运？\n《最后的里程》高光台词",
        "hook_audio_zh": "在2024日本现象级悬疑大片《最后的里程》中，这句话决定了整座物流中心的生死！",
        "jp_sentence": "ベルトコンベアを止めるわけにはいきません。",
        "kana_sentence": "べるとこんべあをとめるわけにはいきません",
        "romaji_sentence": "Beruto konbea o tomeru wake ni wa ikimasen.",
        "zh_translation": "「我们绝不能停下传送带。」",
        "tokens": [
            {"orig": "ベルトコンベアを", "kana": "べるとこんべあを", "romaji": "beruto konbea o", "meaning": "传送带"},
            {"orig": "止める", "kana": "とめる", "romaji": "tomeru", "meaning": "停下"},
            {"orig": "わけには", "kana": "わけには", "romaji": "wake ni wa", "meaning": "由于责任约束"},
            {"orig": "いきません", "kana": "いきません", "romaji": "ikimasen", "meaning": "绝不能"}
        ],
        "pro_tip_title": "影视名师语法 Pro-Tip",
        "pro_tip_body": "注意「~わけにはいかない」！表示在道德责任或社会契约约束下“绝不能做某事”，是 JLPT N3 职场必考高频句型。",
        "speech_chunks_tip": [
            {"lang": "zh", "text": "注意核心语法"},
            {"lang": "ja", "text": "わけにはいかない"},
            {"lang": "zh", "text": "！表示在道德责任或社会契约约束下的绝不能，是 JLPT N3 职场必考高频句型。"}
        ],
        "yt_short_title": "【JLPT N3】电影《最后的里程》高光台词跟读！2.7m/s绝不停运？（WS.01） #Shorts",
        "slug": "last_mile_climax_zh",
        "is_funnel": True,
        "funnel_target": "WL.01《最后的里程》25分钟影视沉浸大课"
    },
    # -------------------------------------------------------------------------
    # WS.02: 山手线电车站台广播 (JLPT N4) - WL.02 Funnel
    # -------------------------------------------------------------------------
    {
        "ep_num": 102,
        "shorts_code": "WS.02",
        "folder": "WM01-weekday_survival_mega_compilation-v1.0-zh",
        "jlpt_level": "JLPT N4",
        "district": "新宿站 • JR山手线站台",
        "category": "东京日常 • 站台广播",
        "hook_title": "听懂东京电车站\n广播高频神句！",
        "hook_audio_zh": "在东京电车和地铁站，每天必听的这一句高频神句，你听懂了吗？",
        "jp_sentence": "黄色い点字ブロックの内側までお下がりください。",
        "kana_sentence": "きいろいてんじぶろっくのうちがわまでおさがりください",
        "romaji_sentence": "Kiiroi tenji burokku no uchigawa made osagari kudasai.",
        "zh_translation": "「请退到黄色盲道安全线以内。」",
        "tokens": [
            {"orig": "黄色い", "kana": "きいろい", "romaji": "kiiroi", "meaning": "黄色的"},
            {"orig": "点字ブロックの", "kana": "てんじぶろっくの", "romaji": "tenji burokku no", "meaning": "盲道提示砖"},
            {"orig": "内側まで", "kana": "うちがわまで", "romaji": "uchigawa made", "meaning": "内侧位置"},
            {"orig": "お下がり", "kana": "おさがり", "romaji": "osagari", "meaning": "退后/等候"},
            {"orig": "ください", "kana": "ください", "romaji": "kudasai", "meaning": "请……"}
        ],
        "pro_tip_title": "JR 东京电车名师 Pro-Tip",
        "pro_tip_body": "注意「お下がりください」！「お + 动词连用形 + ください」是全日本公共交通最标准的礼貌敬语祈使句式。",
        "speech_chunks_tip": [
            {"lang": "zh", "text": "注意核心敬语"},
            {"lang": "ja", "text": "お下がりください"},
            {"lang": "zh", "text": "。お加动词连用形加ください，是全日本公共交通最标准的礼貌祈使句式。"}
        ],
        "yt_short_title": "【JLPT N4】听懂东京山手线报站！1分钟实景原声跟读挑战（WS.02） #Shorts",
        "slug": "yamanote_transit_mega_zh",
        "is_funnel": True,
        "funnel_target": "WL.02 周一到周五东京生活全景大合集（28分钟）"
    },
    # -------------------------------------------------------------------------
    # EP.01: 山手线报站 (JLPT N4)
    # -------------------------------------------------------------------------
    {
        "ep_num": 1,
        "folder": "E01-Yamanote_Transit-v1.0-zh",
        "jlpt_level": "JLPT N4",
        "district": "新宿站 • JR山手线",
        "category": "东京出行 • 站台广播",
        "hook_title": "听懂东京电车站\n广播高频神句！",
        "hook_audio_zh": "在东京电车和地铁站，每天必听的这一句，你听懂了吗？",
        "jp_sentence": "黄色い点字ブロックの内側までお下がりください。",
        "kana_sentence": "きいろいてんじぶろっくのうちがわまでおさがりください",
        "romaji_sentence": "Kiiroi tenji burokku no uchigawa made osagari kudasai.",
        "zh_translation": "「请退到黄色盲道安全线以内。」",
        "tokens": [
            {"orig": "黄色い", "kana": "きいろい", "romaji": "kiiroi", "meaning": "黄色的"},
            {"orig": "点字ブロックの", "kana": "てんじぶろっくの", "romaji": "tenji burokku no", "meaning": "盲道提示砖"},
            {"orig": "内側まで", "kana": "うちがわまで", "romaji": "uchigawa made", "meaning": "内侧位置"},
            {"orig": "お下がり", "kana": "おさがり", "romaji": "osagari", "meaning": "退后/等候"},
            {"orig": "ください", "kana": "ください", "romaji": "kudasai", "meaning": "请……"}
        ],
        "pro_tip_title": "JR 东京电车名师 Pro-Tip",
        "pro_tip_body": "注意「お下がりください」！「お + 动词连用形 + ください」是日本公共交通最标准的礼貌敬语祈使句式。",
        "speech_chunks_tip": [
            {"lang": "zh", "text": "注意核心敬语"},
            {"lang": "ja", "text": "お下がりください"},
            {"lang": "zh", "text": "。お加动词连用形加ください，是全日本公共交通最标准的礼貌祈使句式。"}
        ],
        "yt_short_title": "【JLPT N4】听懂东京山手线报站！1分钟实景原声跟读挑战（EP.01） #Shorts",
        "slug": "yamanote_transit_zh"
    },
    # -------------------------------------------------------------------------
    # EP.02: 7-Eleven 便利店结账 (JLPT N5)
    # -------------------------------------------------------------------------
    {
        "ep_num": 2,
        "folder": "E02-Kombini_Checkout-v1.0-zh",
        "jlpt_level": "JLPT N5",
        "district": "涩谷 • 7-Eleven 收银台",
        "category": "便利店日常 • 结账指南",
        "hook_title": "东京便利店结账\n两秒听懂店员神句！",
        "hook_audio_zh": "去日本7-Eleven买便当，店员收银时一定会问你这一句！",
        "jp_sentence": "お弁当温めますか？袋は大丈夫です。",
        "kana_sentence": "おべんとうあたためますか？ふくろはだいじょうぶです",
        "romaji_sentence": "Obentou atatamemasu ka? Fukuro wa daijoubu desu.",
        "zh_translation": "「便当需要加热吗？不用塑料袋了，谢谢。」",
        "tokens": [
            {"orig": "お弁当", "kana": "おべんとう", "romaji": "obentou", "meaning": "便当盒饭"},
            {"orig": "温めますか", "kana": "あたためますか", "romaji": "atatamemasu ka", "meaning": "需要加热吗"},
            {"orig": "袋は", "kana": "ふくろは", "romaji": "fukuro wa", "meaning": "塑料袋"},
            {"orig": "大丈夫", "kana": "だいじょうぶ", "romaji": "daijoubu", "meaning": "不用/没关系"},
            {"orig": "です", "kana": "です", "romaji": "desu", "meaning": "礼貌断定"}
        ],
        "pro_tip_title": "便利店秒回礼貌秘籍",
        "pro_tip_body": "「袋は大丈夫です」是日本最温和礼貌的拒绝方式！想加热回答「お願いします」，不加热回答「大丈夫です」。",
        "speech_chunks_tip": [
            {"lang": "ja", "text": "袋は大丈夫です"},
            {"lang": "zh", "text": "是极具礼貌的拒绝表达。想加热回答"},
            {"lang": "ja", "text": "お願いします"},
            {"lang": "zh", "text": "，不加热回答"},
            {"lang": "ja", "text": "大丈夫です"},
            {"lang": "zh", "text": "即可。"}
        ],
        "yt_short_title": "【JLPT N5】去日本便利店买便当必听！收银台原声跟读挑战（EP.02） #Shorts",
        "slug": "kombini_checkout_zh"
    },
    # -------------------------------------------------------------------------
    # EP.03: 居酒屋生啤开场 (JLPT N5)
    # -------------------------------------------------------------------------
    {
        "ep_num": 3,
        "folder": "E03-Izakaya_Night-v1.0-zh",
        "jlpt_level": "JLPT N5",
        "district": "新桥 • 居酒屋街",
        "category": "居酒屋美食 • 点单秘籍",
        "hook_title": "像东京老饕一样点单！\n居酒屋黄金开场句",
        "hook_audio_zh": "在日本居酒屋落座两秒内喊出这一句，店员立刻对你刮目相看！",
        "jp_sentence": "とりあえず生で、ビールを二つお願いします！",
        "kana_sentence": "とりあえずなまで、びーるをふたつおねがいします",
        "romaji_sentence": "Toriaezu nama de, biiru o futatsu onegaishimasu!",
        "zh_translation": "「先来生啤，麻烦上两杯啤酒！」",
        "tokens": [
            {"orig": "とりあえず", "kana": "とりあえず", "romaji": "toriaezu", "meaning": "首先/先来"},
            {"orig": "生で", "kana": "な制作で", "romaji": "nama de", "meaning": "生啤酒"},
            {"orig": "ビールを", "kana": "びーるを", "romaji": "biiru o", "meaning": "啤酒"},
            {"orig": "二つ", "kana": "ふたつ", "romaji": "futatsu", "meaning": "两杯"},
            {"orig": "お願いします", "kana": "おねがいします", "romaji": "onegaishimasu", "meaning": "拜托了"}
        ],
        "pro_tip_title": "居酒屋黄金文化 Pro-Tip",
        "pro_tip_body": "「とりあえず生で」是全日本通用的开场暗号！数量词点单公式：物品 + を + 数量（ひとつ/ふたつ）+ お願いします。",
        "speech_chunks_tip": [
            {"lang": "ja", "text": "とりあえず生で"},
            {"lang": "zh", "text": "是居酒屋通用的开场暗号。先点生啤干杯，是日本职场最经典的聚会礼仪。"}
        ],
        "yt_short_title": "【JLPT N5】像本地人一样进居酒屋！先来生啤原声跟读挑战（EP.03） #Shorts",
        "slug": "izakaya_night_zh"
    },
    # -------------------------------------------------------------------------
    # EP.04: 秋叶原手办免税 (JLPT N5)
    # -------------------------------------------------------------------------
    {
        "ep_num": 4,
        "folder": "E04-Akiba_Pilgrimage-v1.0-zh",
        "jlpt_level": "JLPT N5",
        "district": "秋叶原 • 二次元手办专门店",
        "category": "秋叶原购物 • 手办免税",
        "hook_title": "秋叶原淘手办立省10%！\n免税结账必说神句",
        "hook_audio_zh": "在秋叶原动漫店结账时，出示护照说出这一句，直接享受10%免税！",
        "jp_sentence": "免税手続きは、ここでできますか？",
        "kana_sentence": "めんぜいてつづきは、ここでできますか",
        "romaji_sentence": "Menzei tetsuzuki wa, koko de dekimasu ka?",
        "zh_translation": "「请问可以在这里办理免税退税吗？」",
        "tokens": [
            {"orig": "免税", "kana": "めんぜい", "romaji": "menzei", "meaning": "免税"},
            {"orig": "手続きは", "kana": "てつづきは", "romaji": "tetsuzuki wa", "meaning": "手续/办理"},
            {"orig": "ここで", "kana": "ここで", "romaji": "koko de", "meaning": "在这里"},
            {"orig": "できますか", "kana": "できますか", "romaji": "dekimasu ka", "meaning": "可以做……吗"}
        ],
        "pro_tip_title": "日本购物免税规则",
        "pro_tip_body": "单店消费满 5000 日元即可办理免税！「~できますか」是初学者最高频实用的能力与许可疑问句。",
        "speech_chunks_tip": [
            {"lang": "zh", "text": "单店消费满5000日元即可出示护照退税。"},
            {"lang": "ja", "text": "できますか"},
            {"lang": "zh", "text": "是询问是否支持该项服务的最常用句型。"}
        ],
        "yt_short_title": "【JLPT N5】秋叶原淘手办必学！免税退税1分钟原声跟读（EP.04） #Shorts",
        "slug": "akiba_pilgrimage_zh"
    },
    # -------------------------------------------------------------------------
    # EP.05: 东京地铁换乘与精算机 (JLPT N4)
    # -------------------------------------------------------------------------
    {
        "ep_num": 5,
        "folder": "E05-Tokyo_Subway_Rush-v1.0-zh",
        "jlpt_level": "JLPT N4",
        "district": "赤坂见附 • 地铁闸机口",
        "category": "东京交通 • 地铁补票",
        "hook_title": "东京地铁刷卡不过？\n精算机补票求助神句！",
        "hook_audio_zh": "在东京坐地铁出站时西瓜卡余额不足亮红灯？找站务员说这句立刻解决！",
        "jp_sentence": "すみません、乗り越し精算機はどこにありますか？",
        "kana_sentence": "すみません、のりこしせいさんきはどこにありますか",
        "romaji_sentence": "Sumimasen, norikoshi seisanki wa doko ni arimasu ka?",
        "zh_translation": "「不好意思，请问坐过站的补票机在哪里？」",
        "tokens": [
            {"orig": "すみません", "kana": "すみません", "romaji": "sumimasen", "meaning": "不好意思"},
            {"orig": "乗り越し", "kana": "のりこし", "romaji": "norikoshi", "meaning": "坐过站"},
            {"orig": "精算機は", "kana": "せいさんきは", "romaji": "seisanki wa", "meaning": "补票机"},
            {"orig": "どこに", "kana": "どこに", "romaji": "doko ni", "meaning": "在哪里"},
            {"orig": "ありますか", "kana": "ありますか", "romaji": "arimasu ka", "meaning": "有/在吗"}
        ],
        "pro_tip_title": "地铁出行精算机 Pro-Tip",
        "pro_tip_body": "「精算機（せいさんき）」是日本闸机旁的黄色补票机，放入西瓜卡补齐差价后即可顺畅出闸。",
        "speech_chunks_tip": [
            {"lang": "ja", "text": "精算機"},
            {"lang": "zh", "text": "是日本地铁闸机旁的补票机。插入西瓜卡补齐差额后，就可以顺利刷卡出闸了。"}
        ],
        "yt_short_title": "【JLPT N4】东京地铁坐过站/余额不足？精算机补票跟读精讲（EP.05） #Shorts",
        "slug": "tokyo_subway_rush_zh"
    },
    # -------------------------------------------------------------------------
    # EP.06: 便利店现磨冰咖啡 (JLPT N5)
    # -------------------------------------------------------------------------
    {
        "ep_num": 6,
        "folder": "E06-Kombini_Coffee_ATM-v1.0-zh",
        "jlpt_level": "JLPT N5",
        "district": "新宿 • 便利店咖啡机",
        "category": "便利店日常 • 咖啡点单",
        "hook_title": "日本便利店买冰咖啡\n动线与点单秘籍！",
        "hook_audio_zh": "日本便利店冰咖啡不能直接点！必须先去冷柜拿冰杯，结账时说这一句！",
        "jp_sentence": "アイスコーヒーのRを、ひとつください！",
        "kana_sentence": "あいすこーひーのあーるを、ひとつください",
        "romaji_sentence": "Aisu koohii no aaru o, hitotsu kudasai!",
        "zh_translation": "「请给我一杯常规中杯冰咖啡！」",
        "tokens": [
            {"orig": "アイスコーヒーの", "kana": "あいすこーひーの", "romaji": "aisu koohii no", "meaning": "冰咖啡的"},
            {"orig": "Rを", "kana": "あーるを", "romaji": "aaru o", "meaning": "Regular中杯"},
            {"orig": "ひとつ", "kana": "ひとつ", "romaji": "hitotsu", "meaning": "一个/一杯"},
            {"orig": "ください", "kana": "ください", "romaji": "kudasai", "meaning": "请给我"}
        ],
        "pro_tip_title": "便利店冷热咖啡差异",
        "pro_tip_body": "点单公式：物品 + の + 尺寸（R / L）+ を + 数量 + ください。热咖啡在收银台拿纸杯，冰咖啡必须先在冷冻柜自取冰杯！",
        "speech_chunks_tip": [
            {"lang": "zh", "text": "记住公式：物品加の加尺寸加を加数量加"},
            {"lang": "ja", "text": "ください"},
            {"lang": "zh", "text": "。热咖啡在柜台拿杯，冰咖啡先在冷柜拿冰杯。"}
        ],
        "yt_short_title": "【JLPT N5】日本便利店冰咖啡怎么买？冷柜取杯与点单跟读（EP.06） #Shorts",
        "slug": "kombini_coffee_atm_zh"
    },
    # -------------------------------------------------------------------------
    # EP.07: 一兰拉面食券机与定制 (JLPT N5)
    # -------------------------------------------------------------------------
    {
        "ep_num": 7,
        "folder": "E07-Ramen_Ticket_Vending-v1.0-zh",
        "jlpt_level": "JLPT N5",
        "district": "池袋 • 拉面激战区",
        "category": "拉面美食 • 食券与定制",
        "hook_title": "像拉面老饕一样点餐！\n面硬汤浓定制黑话",
        "hook_audio_zh": "在日本吃拉面，交食券时向主厨喊出这串定制口诀，面硬汤浓超地道！",
        "jp_sentence": "麺硬め、味濃いめ、替玉をお願いします！",
        "kana_sentence": "めんかため、あじこいめ、かえだまをおねがいします",
        "romaji_sentence": "Men katame, aji koime, kaedama o onegaishimasu!",
        "zh_translation": "「面条要偏硬、汤头要浓郁，麻烦再加一份面！」",
        "tokens": [
            {"orig": "麺硬め", "kana": "めんかため", "romaji": "men katame", "meaning": "面偏硬"},
            {"orig": "味濃いめ", "kana": "あじこいめ", "romaji": "aji koime", "meaning": "汤偏浓"},
            {"orig": "替玉を", "kana": "かえだまを", "romaji": "kaedama o", "meaning": "加面"},
            {"orig": "お願いします", "kana": "おねがいします", "romaji": "onegaishimasu", "meaning": "麻烦了"}
        ],
        "pro_tip_title": "东京拉面定制三剑客",
        "pro_tip_body": "面条口感：硬め（katame）/ 普通（futsuu）；汤头浓度：濃いめ（koime）/ 薄め（usume）；追加面条：替玉（kaedama）！",
        "speech_chunks_tip": [
            {"lang": "zh", "text": "拉面老饕三剑客："},
            {"lang": "ja", "text": "硬め"},
            {"lang": "zh", "text": "面偏硬，"},
            {"lang": "ja", "text": "濃いめ"},
            {"lang": "zh", "text": "汤偏浓，"},
            {"lang": "ja", "text": "替玉"},
            {"lang": "zh", "text": "是吃完后续加一份面。"}
        ],
        "yt_short_title": "【JLPT N5】像老饕一样吃拉面！面硬汤浓加面口诀原声跟读（EP.07） #Shorts",
        "slug": "ramen_ticket_vending_zh"
    },
    # -------------------------------------------------------------------------
    # EP.08: 银座精品店试穿 (JLPT N5)
    # -------------------------------------------------------------------------
    {
        "ep_num": 8,
        "folder": "E08-Ginza_TaxFree_Shopping-v1.0-zh",
        "jlpt_level": "JLPT N5",
        "district": "银座 • 优衣库旗舰店",
        "category": "银座购物 • 试穿礼仪",
        "hook_title": "在东京买衣服试穿！\n精品店优雅礼貌神句",
        "hook_audio_zh": "在银座或表参道买衣服，进试衣间前一定要礼貌询问店员这一句！",
        "jp_sentence": "これのMサイズを、試着してもいいですか？",
        "kana_sentence": "これのえむさいずを、しちゃくしてもいいですか",
        "romaji_sentence": "Kore no emu saizu o, shichaku shite mo ii desu ka?",
        "zh_translation": "「请问这件有M号可以试穿一下吗？」",
        "tokens": [
            {"orig": "これの", "kana": "これの", "romaji": "kore no", "meaning": "这件的"},
            {"orig": "Mサイズを", "kana": "えむさいずを", "romaji": "emu saizu o", "meaning": "M号"},
            {"orig": "試着して", "kana": "しちゃくして", "romaji": "shichaku shite", "meaning": "试穿"},
            {"orig": "もいいですか", "kana": "もいいですか", "romaji": "mo ii desu ka", "meaning": "可以……吗"}
        ],
        "pro_tip_title": "试衣间礼仪与请求句式",
        "pro_tip_body": "「~てもいいですか」是初级日语最核心的许可请求句式！在日本试衣前务必脱鞋踩在地毯上。",
        "speech_chunks_tip": [
            {"lang": "ja", "text": "てもいいですか"},
            {"lang": "zh", "text": "表示可以做某事吗。在日本进试衣间前一定要脱鞋踩在地毯上保持干净。"}
        ],
        "yt_short_title": "【JLPT N5】银座买衣服优雅试穿！试衣间许可请求跟读（EP.08） #Shorts",
        "slug": "ginza_taxfree_shopping_zh"
    },
    # -------------------------------------------------------------------------
    # EP.09: 动漫跨界桑拿 (JLPT N5)
    # -------------------------------------------------------------------------
    {
        "ep_num": 9,
        "folder": "E09-anime_sauna_trend-v1.0-zh",
        "jlpt_level": "JLPT N5",
        "district": "赤坂 • 动漫女性桑拿",
        "category": "东京热点 • 桑拿流行语",
        "hook_title": "日本年轻人超火的\n桑拿身心放松流行语！",
        "hook_audio_zh": "日本年轻人最近都在说的桑拿流行语整う，代表身心彻底治愈放松！",
        "jp_sentence": "サウナに入って、身も心もととのいました！",
        "kana_sentence": "さうなにはいって、みもこころもととのいました",
        "romaji_sentence": "Sauna ni haitte, mi mo kokoro mo totonoimashita!",
        "zh_translation": "「蒸完桑拿，身心都彻底放松治愈了！」",
        "tokens": [
            {"orig": "サウナに", "kana": "さうなに", "romaji": "sauna ni", "meaning": "桑拿房"},
            {"orig": "入って", "kana": "はいって", "romaji": "haitte", "meaning": "进入后"},
            {"orig": "身も心も", "kana": "みもこころも", "romaji": "mi mo kokoro mo", "meaning": "身与心都"},
            {"orig": "ととのいました", "kana": "ととのいました", "romaji": "totonoimashita", "meaning": "调节放松"}
        ],
        "pro_tip_title": "流行语「整う」深度解析",
        "pro_tip_body": "「ととのう」在桑拿文化中特指桑拿与冷水浴交替后，脑内分泌多巴胺带来的极度舒适感与治愈状态。",
        "speech_chunks_tip": [
            {"lang": "ja", "text": "ととのう"},
            {"lang": "zh", "text": "在桑拿文化中特指桑拿与冷水浴交替后，身心进入极度放松与治愈的神奇状态。"}
        ],
        "yt_short_title": "【JLPT N5】动漫公司开桑拿？身心放松「整う」流行语跟读（EP.09） #Shorts",
        "slug": "anime_sauna_trend_zh"
    },
    # -------------------------------------------------------------------------
    # EP.10: 绫濑遥天然呆日综 (JLPT N5)
    # -------------------------------------------------------------------------
    {
        "ep_num": 10,
        "folder": "E10-ayase_haruka_tennen-v1.0-zh",
        "jlpt_level": "JLPT N5",
        "district": "六本木 • 电影发布会现场",
        "category": "日综娱乐 • 艺人性格萌点",
        "hook_title": "日综爆笑反差萌！\n天然呆性格地道表达",
        "hook_audio_zh": "日本综艺里高频出现的天然呆，用日语怎么地道表达其性格魅力？",
        "jp_sentence": "天然な発言で、会場を笑わせました！",
        "kana_sentence": "てんねんなはつげんで、かいじょうをわらわせました",
        "romaji_sentence": "Tennen na hatsugen de, kaijou o warawasemashita!",
        "zh_translation": "「天然呆的一句话，把全场都逗笑了！」",
        "tokens": [
            {"orig": "天然な", "kana": "てんねんな", "romaji": "tennen na", "meaning": "天然呆的"},
            {"orig": "発言で", "kana": "はつげんで", "romaji": "hatsugen de", "meaning": "发言让"},
            {"orig": "会場を", "kana": "かいじょうを", "romaji": "kaijou o", "meaning": "全场"},
            {"orig": "笑わせました", "kana": "わらわせました", "romaji": "warawasemashita", "meaning": "逗笑了"}
        ],
        "pro_tip_title": "语法精讲：使役态表达",
        "pro_tip_body": "「笑わせる」是动词「笑う」的使役态，意为“让……笑、逗笑某人”。「天然（てんねん）」常用来夸赞可爱不做作的性格。",
        "speech_chunks_tip": [
            {"lang": "ja", "text": "笑わせる"},
            {"lang": "zh", "text": "是"},
            {"lang": "ja", "text": "笑う"},
            {"lang": "zh", "text": "的使役态，意思是逗笑全场。"},
            {"lang": "ja", "text": "天然"},
            {"lang": "zh", "text": "常用来形容纯真可爱、不做作的性格魅力。"}
        ],
        "yt_short_title": "【JLPT N5】绫濑遥天然呆引爆笑！日综反差萌流行语跟读（EP.10） #Shorts",
        "slug": "ayase_haruka_tennen_zh"
    },
    # -------------------------------------------------------------------------
    # EP.11: 涩谷科幻微剧 (JLPT N4)
    # -------------------------------------------------------------------------
    {
        "ep_num": 11,
        "folder": "E11-shabuya-robot-drama-v1.0-zh",
        "jlpt_level": "JLPT N4",
        "district": "涩谷 • 未来科技街区",
        "category": "科技科幻 • 社交网络热点",
        "hook_title": "涩谷AI微剧全网爆火！\n科技热点探讨必备句",
        "hook_audio_zh": "近未来科技与AI机器人在东京引发全网热议，看日剧时必学的讨论句！",
        "jp_sentence": "近未来の渋谷を、一度訪れてみたいです！",
        "kana_sentence": "きんみらいのしぶやを、いちどおとずれてみたいです",
        "romaji_sentence": "Kin-mirai no Shibuya o, ichido otozurete mitai desu!",
        "zh_translation": "「真想去探访一次近未来风貌的涩谷！」",
        "tokens": [
            {"orig": "近未来の", "kana": "きんみらいの", "romaji": "kin-mirai no", "meaning": "近未来的"},
            {"orig": "渋谷を", "kana": "しぶやを", "romaji": "shibuya o", "meaning": "涩谷街区"},
            {"orig": "一度", "kana": "いちど", "romaji": "ichido", "meaning": "一次"},
            {"orig": "訪れてみたい", "kana": "おとずれてみたい", "romaji": "otozurete mitai", "meaning": "想探访看看"},
            {"orig": "です", "kana": "です", "romaji": "desu", "meaning": "礼貌断定"}
        ],
        "pro_tip_title": "愿望句型：~てみたいです",
        "pro_tip_body": "「动词て形 + みたいです」表示“想尝试做某事看看”，是表达旅行心愿与体验愿望的最地道句型。",
        "speech_chunks_tip": [
            {"lang": "zh", "text": "动词て形加"},
            {"lang": "ja", "text": "みたいです"},
            {"lang": "zh", "text": "表示想尝试做某事看看，表达旅游向往与愿望时非常地道。"}
        ],
        "yt_short_title": "【JLPT N4】涩谷AI机器人微剧爆火！近未来科技热点跟读（EP.11） #Shorts",
        "slug": "shabuya_robot_drama_zh"
    }
]

def prepare_shorts_background(bg_path: str, width: int = 1080, height: int = 1920) -> Image.Image:
    """Prepares an authentic scene photograph base canvas for 9:16 vertical shorts."""
    if bg_path and os.path.exists(bg_path):
        try:
            raw_img = Image.open(bg_path).convert("RGB")
            src_w, src_h = raw_img.size
            target_ratio = width / height
            src_ratio = src_w / src_h

            if src_ratio > target_ratio:
                new_w = int(src_h * target_ratio)
                center_x = int(src_w * 0.50)
                left = max(0, min(src_w - new_w, center_x - new_w // 2))
                raw_img = raw_img.crop((left, 0, left + new_w, src_h))
            else:
                new_h = int(src_w / target_ratio)
                top = max(0, (src_h - new_h) // 2)
                raw_img = raw_img.crop((0, top, src_w, top + new_h))

            base_img = raw_img.resize((width, height), Image.Resampling.LANCZOS)
            from PIL import ImageEnhance
            base_img = ImageEnhance.Contrast(base_img).enhance(1.15)
            base_img = ImageEnhance.Color(base_img).enhance(1.15)
        except Exception:
            base_img = Image.new("RGB", (width, height), (12, 17, 29))
    else:
        base_img = Image.new("RGB", (width, height), (12, 17, 29))

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    # 1. Dark atmospheric overlay across whole screen
    draw_ov.rectangle([(0, 0), (width, height)], fill=(10, 14, 23, 140))

    # 2. Top header gradient (y=0..320)
    for y in range(320):
        rel = (320 - y) / 320.0
        alpha = int(180 * (rel ** 1.2))
        draw_ov.line([(0, y), (width, y)], fill=(8, 12, 22, alpha))

    # 3. Bottom footer gradient (y=1450..1920)
    for y in range(1450, height):
        rel = (y - 1450) / 470.0
        alpha = int(220 * (rel ** 1.1))
        draw_ov.line([(0, y), (width, y)], fill=(6, 10, 18, alpha))

    return Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB")

def render_chinese_interactive_frame(
    width: int,
    height: int,
    conf: dict,
    active_token_idx: int,
    stage_num: int,
    stage_title: str,
    stage_subtext: str,
    speaking_prog: float,
    total_progress: float,
    frame_idx: int,
    base_canvas: Image.Image = None
) -> Image.Image:
    img = base_canvas.copy() if base_canvas is not None else Image.new("RGB", (width, height), color=(12, 17, 29))
    draw = ImageDraw.Draw(img)

    # 1. Top Header Brand Capsule (Top JLPT Badge)
    code_str = conf.get("shorts_code", f"SH.{conf['ep_num']:02d}")
    header_str = f"TokyoFlow  •  [{conf.get('jlpt_level', 'JLPT N5')}] {code_str}"
    font_brand = get_font(24)
    bbox_hdr = draw.textbbox((0, 0), header_str, font=font_brand)
    hdr_w = bbox_hdr[2] - bbox_hdr[0]
    brand_w = hdr_w + 64
    bx = (width - brand_w) // 2
    draw.rounded_rectangle([(bx, 65), (bx + brand_w, 115)], radius=24, fill=(24, 32, 47, 240), outline=(225, 29, 72), width=2)
    draw.text((bx + 32, 77), header_str, fill=(255, 255, 255), font=font_brand)

    # 3. Hook Title (Chinese Bold Catchphrase)
    font_hook = get_font(44)
    hook_lines = conf["hook_title"].split("\n")
    cur_hy = 135
    for hline in hook_lines:
        bbox = draw.textbbox((0, 0), hline, font=font_hook)
        hw = bbox[2] - bbox[0]
        hx = (width - hw) // 2
        draw.text((hx + 3, cur_hy + 3), hline, fill=(0, 0, 0), font=font_hook)
        draw.text((hx, cur_hy), hline, fill=(250, 204, 21), font=font_hook)
        cur_hy += 50

    # 4. District / Scenario Pill
    font_dist = get_font(21)
    dist_text = f"场景：{conf['district']}"
    bbox_d = draw.textbbox((0, 0), dist_text, font=font_dist)
    dw = bbox_d[2] - bbox_d[0] + 40
    dx = (width - dw) // 2
    draw.rounded_rectangle([(dx, 255), (dx + dw, 298)], radius=12, fill=(224, 231, 255), outline=(165, 180, 252), width=1)
    draw.text((dx + 20, 264), dist_text, fill=(49, 46, 129), font=font_dist)

    # 5. Central 3-Tier Dialogue Card (y=320..940, height=620)
    card_x, card_y, card_w, card_h = 50, 320, width - 100, 620
    is_shadow_stage = (stage_num == 3)
    card_border = (239, 68, 68) if is_shadow_stage else (71, 85, 105)
    card_bg = (24, 24, 37) if is_shadow_stage else (30, 41, 59)
    draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=28, fill=card_bg, outline=card_border, width=4 if is_shadow_stage else 2)

    # Card Top Header
    font_card_head = get_font(22)
    card_header_title = "[跟读训练] 实时开口复述句子" if is_shadow_stage else "[东京原声] 东京实景高频原声"
    draw.text((card_x + 36, card_y + 24), card_header_title, fill=(239, 68, 68) if is_shadow_stage else (148, 163, 184), font=font_card_head)
    
    # Tag
    level_tag = "跟读训练" if is_shadow_stage else "东京原声"
    tag_bg = (239, 68, 68) if is_shadow_stage else (225, 29, 72)
    draw.rounded_rectangle([(card_x + card_w - 160, card_y + 18), (card_x + card_w - 30, card_y + 52)], radius=10, fill=tag_bg)
    draw.text((card_x + card_w - 146, card_y + 24), level_tag, fill=(255, 255, 255), font=get_font(18))

    draw.line([(card_x + 30, card_y + 64), (card_x + card_w - 30, card_y + 64)], fill=(51, 65, 85), width=2)

    # 3-Tier Ruby Tokens
    font_jp = get_font(44)
    font_kana = get_font(21)
    font_meaning = get_font(20)

    tokens = conf["tokens"]
    lines = []
    current_line = []
    current_w = 0
    max_line_w = card_w - 60

    for idx, tok in enumerate(tokens):
        bbox_j = draw.textbbox((0, 0), tok["orig"], font=font_jp)
        w_j = bbox_j[2] - bbox_j[0]
        tok_w = max(w_j + 16, 75)
        if current_w + tok_w > max_line_w and len(current_line) > 0:
            lines.append(current_line)
            current_line = [(idx, tok, tok_w)]
            current_w = tok_w
        else:
            current_line.append((idx, tok, tok_w))
            current_w += tok_w + 12
    if current_line:
        lines.append(current_line)

    start_y = card_y + 84
    for line in lines:
        line_total_w = sum(item[2] for item in line) + (len(line) - 1) * 12
        start_x = card_x + (card_w - line_total_w) // 2

        for idx, tok, tok_w in line:
            is_active = (idx == active_token_idx)
            
            if is_active:
                pill_bg = (251, 191, 36) if not is_shadow_stage else (239, 68, 68)
                pill_outline = (245, 158, 11) if not is_shadow_stage else (255, 255, 255)
                draw.rounded_rectangle([(start_x - 6, start_y - 6), (start_x + tok_w + 6, start_y + 140)], radius=14, fill=pill_bg, outline=pill_outline, width=3)
                
                # Bouncing mora dot
                dot_cx = start_x + tok_w // 2
                draw.ellipse([(dot_cx - 6, start_y - 18), (dot_cx + 6, start_y - 6)], fill=(225, 29, 72) if not is_shadow_stage else (254, 240, 138))

                c_k = (146, 64, 14) if not is_shadow_stage else (255, 255, 255)
                c_j = (15, 23, 42) if not is_shadow_stage else (255, 255, 255)
                c_m = (146, 64, 14) if not is_shadow_stage else (254, 240, 138)
            else:
                c_k = (148, 163, 184)
                c_j = (255, 255, 255)
                c_m = (148, 163, 184)

            # Kana
            bbox_k = draw.textbbox((0, 0), tok.get("kana", ""), font=font_kana)
            kw = bbox_k[2] - bbox_k[0]
            draw.text((start_x + (tok_w - kw) // 2, start_y), tok.get("kana", ""), fill=c_k, font=font_kana)

            # Kanji
            bbox_j = draw.textbbox((0, 0), tok["orig"], font=font_jp)
            jw = bbox_j[2] - bbox_j[0]
            draw.text((start_x + (tok_w - jw) // 2, start_y + 32), tok["orig"], fill=c_j, font=font_jp)

            # Meaning
            if tok.get("meaning"):
                bbox_m = draw.textbbox((0, 0), tok["meaning"], font=font_meaning)
                mw = bbox_m[2] - bbox_m[0]
                draw.text((start_x + (tok_w - mw) // 2, start_y + 92), tok["meaning"], fill=c_m, font=font_meaning)

            start_x += tok_w + 12
        start_y += 155

    # Target Full Romaji & Translation Sub-block inside Central Card
    draw.line([(card_x + 30, card_y + 440), (card_x + card_w - 30, card_y + 440)], fill=(51, 65, 85), width=2)
    font_sub_ro = get_font(23)
    draw.text((card_x + 40, card_y + 460), f"罗马音：{conf['romaji_sentence']}", fill=(244, 114, 182), font=font_sub_ro)
    
    font_sub_zh = get_font(26)
    draw.text((card_x + 40, card_y + 510), f"中文释义：{conf['zh_translation']}", fill=(254, 240, 138), font=font_sub_zh)

    # Studio micro-ribbon inside card
    draw.rounded_rectangle([(card_x + 30, card_y + 565), (card_x + card_w - 30, card_y + 605)], radius=8, fill=(15, 23, 42))
    draw.text((card_x + 45, card_y + 574), "[ TOKYOFLOW 官方口语金句 ] 100% 东京原声 • 毫秒级音拍卡拉OK对齐", fill=(56, 189, 248), font=get_font(18))

    # 6. LOWER INTERACTIVE PANEL (y=960..1520, height=560)
    mid_x, mid_y, mid_w, mid_h = 50, 960, width - 100, 560

    if stage_num == 3: # STAGE 3: SHADOWING PRACTICE
        draw.rounded_rectangle([(mid_x, mid_y), (mid_x + mid_w, mid_y + mid_h)], radius=24, fill=(45, 15, 25), outline=(239, 68, 68), width=4)
        
        # Header
        draw.text((mid_x + 30, mid_y + 24), "【STEP 3】跟着原声大声开口跟读！", fill=(239, 68, 68), font=get_font(28))
        draw.line([(mid_x + 24, mid_y + 64), (mid_x + mid_w - 24, mid_y + 64)], fill=(127, 29, 29), width=2)

        # Big pulsing indicator
        mic_cx = mid_x + mid_w // 2
        mic_cy = mid_y + 140
        pulse_r1 = int(45 + math.sin(frame_idx * 0.3) * 6)
        pulse_r2 = int(58 + math.cos(frame_idx * 0.3) * 8)
        draw.ellipse([(mic_cx - pulse_r2, mic_cy - pulse_r2), (mic_cx + pulse_r2, mic_cy + pulse_r2)], outline=(239, 68, 68, 100), width=2)
        draw.ellipse([(mic_cx - pulse_r1, mic_cy - pulse_r1), (mic_cx + pulse_r1, mic_cy + pulse_r1)], fill=(225, 29, 72), outline=(255, 255, 255), width=2)
        
        draw.text((mic_cx - 24, mic_cy - 18), "LIVE", fill=(255, 255, 255), font=get_font(22))

        # Prompt text
        font_mic_prompt = get_font(30)
        prompt_txt = "大声朗读！跟随纯正东京原声同步开口"
        bbox_p = draw.textbbox((0, 0), prompt_txt, font=font_mic_prompt)
        pw = bbox_p[2] - bbox_p[0]
        draw.text((mid_x + (mid_w - pw) // 2, mid_y + 215), prompt_txt, fill=(255, 255, 255), font=font_mic_prompt)

        # Animated Audio Waveform Bars
        num_bars = 22
        wave_start_x = mid_x + 40
        bar_w = (mid_w - 80) // num_bars - 6
        wave_base_y = mid_y + 310
        for b_i in range(num_bars):
            amp = math.sin((frame_idx * 0.3) + (b_i * 0.5)) * 0.5 + 0.5
            bar_h = int(24 + amp * 70)
            bx_bar = wave_start_x + b_i * (bar_w + 6)
            draw.rounded_rectangle(
                [(bx_bar, wave_base_y - bar_h // 2), (bx_bar + bar_w, wave_base_y + bar_h // 2)],
                radius=6,
                fill=(239, 68, 68) if b_i % 2 == 0 else (244, 114, 182)
            )

        # Speaking Progress Bar inside Shadow Card
        prog_bar_y = mid_y + 380
        draw.text((mid_x + 30, prog_bar_y), "跟读进度倒计时：", fill=(203, 213, 225), font=get_font(22))
        draw.rounded_rectangle([(mid_x + 30, prog_bar_y + 34), (mid_x + mid_w - 30, prog_bar_y + 64)], radius=12, fill=(15, 23, 42), outline=(71, 85, 105), width=2)
        sp_fill_w = int((mid_w - 60) * max(0.0, min(1.0, speaking_prog)))
        if sp_fill_w > 0:
            draw.rounded_rectangle([(mid_x + 30, prog_bar_y + 34), (mid_x + 30 + sp_fill_w, prog_bar_y + 64)], radius=12, fill=(239, 68, 68))
        
        # Helper coaching text
        draw.text((mid_x + 40, mid_y + 465), "技巧：跟随上方红色发光卡拉OK胶囊开口跟读", fill=(254, 240, 138), font=get_font(22))
        draw.text((mid_x + 40, mid_y + 500), "保持声调起伏平稳，音拍节奏与东京原声保持一致。", fill=(203, 213, 225), font=get_font(20))

    elif stage_num == 4: # AI SCORING & TOKYOFLOW APP / MASTERCLASS RESULT
        draw.rounded_rectangle([(mid_x, mid_y), (mid_x + mid_w, mid_y + mid_h)], radius=24, fill=(16, 44, 87), outline=(56, 189, 248), width=3)
        draw.text((mid_x + 30, mid_y + 24), "AI 声调发音智能评估报告", fill=(56, 189, 248), font=get_font(28))
        draw.line([(mid_x + 24, mid_y + 64), (mid_x + mid_w - 24, mid_y + 64)], fill=(30, 58, 138), width=2)

        # Huge 98.6% Score Pill
        draw.rounded_rectangle([(mid_x + 40, mid_y + 90), (mid_x + mid_w - 40, mid_y + 230)], radius=20, fill=(30, 58, 138), outline=(96, 165, 250), width=2)
        font_score = get_font(52)
        score_str = "98.6% 匹配度 [优秀]"
        bbox_sc = draw.textbbox((0, 0), score_str, font=font_score)
        scw = bbox_sc[2] - bbox_sc[0]
        draw.text((mid_x + (mid_w - scw) // 2, mid_y + 110), score_str, fill=(250, 204, 21), font=font_score)
        
        font_subscore = get_font(24)
        sub_str = "东京标准音调（首都圏アクセント）已认证"
        bbox_sub = draw.textbbox((0, 0), sub_str, font=font_subscore)
        subw = bbox_sub[2] - bbox_sub[0]
        draw.text((mid_x + (mid_w - subw) // 2, mid_y + 180), sub_str, fill=(255, 255, 255), font=font_subscore)

        # Breakdown stats
        draw.text((mid_x + 40, mid_y + 265), "- 节奏与语调（Rhythm & Pitch）：极佳 (100%)", fill=(241, 245, 249), font=get_font(23))
        draw.text((mid_x + 40, mid_y + 305), "- 高低音调起伏（High-Low Pattern）：接近母语者", fill=(241, 245, 249), font=get_font(23))
        draw.text((mid_x + 40, mid_y + 345), "- 音拍连贯性（Mora Cadence）：0.12s 标准音程", fill=(241, 245, 249), font=get_font(23))

        # App / Masterclass Recommendation Pill
        if conf.get("is_funnel"):
            draw.rounded_rectangle([(mid_x + 40, mid_y + 400), (mid_x + mid_w - 40, mid_y + 510)], radius=18, fill=(225, 29, 72), outline=(254, 240, 138), width=2)
            draw.text((mid_x + 60, mid_y + 420), f"完整长视频大课已上线！点击下方链接", fill=(255, 255, 255), font=get_font(25))
            draw.text((mid_x + 60, mid_y + 460), f"掌握全场景 80+ 真实口语句型与深度文化潜台词", fill=(254, 240, 138), font=get_font(20))
        else:
            draw.rounded_rectangle([(mid_x + 40, mid_y + 400), (mid_x + mid_w - 40, mid_y + 510)], radius=18, fill=(15, 23, 42), outline=(52, 211, 153), width=2)
            draw.text((mid_x + 60, mid_y + 420), "欢迎在 TokyoFlow App 中进行录音跟读", fill=(52, 211, 153), font=get_font(25))
            draw.text((mid_x + 60, mid_y + 460), "10,000+ JLPT 核心高频词与东京全实景会话练习", fill=(203, 213, 225), font=get_font(20))

    else: # PRO-TIP & VALUE MODE (stage 1 & 2)
        draw.rounded_rectangle([(mid_x, mid_y), (mid_x + mid_w, mid_y + mid_h)], radius=24, fill=(30, 41, 59), outline=(52, 211, 153) if stage_num==2 else (51, 65, 85), width=3 if stage_num==2 else 2)
        
        draw.text((mid_x + 30, mid_y + 24), conf["pro_tip_title"], fill=(52, 211, 153), font=get_font(28))
        draw.line([(mid_x + 24, mid_y + 64), (mid_x + mid_w - 24, mid_y + 64)], fill=(51, 65, 85), width=2)

        font_tip_body = get_font(25)
        tip_text = conf["pro_tip_body"]
        
        max_tip_w = mid_w - 60
        tip_lines = []
        cur_line = ""
        for ch in tip_text:
            if ch == "\n":
                tip_lines.append(cur_line)
                cur_line = ""
                continue
            test_line = cur_line + ch
            if draw.textbbox((0, 0), test_line, font=font_tip_body)[2] > max_tip_w:
                tip_lines.append(cur_line)
                cur_line = ch
            else:
                cur_line = test_line
        if cur_line:
            tip_lines.append(cur_line)

        cur_ty = mid_y + 84
        for sline in tip_lines:
            draw.text((mid_x + 30, cur_ty), sline, fill=(241, 245, 249), font=font_tip_body)
            cur_ty += 38

        # Step indicator guide inside pro tip card
        draw.rounded_rectangle([(mid_x + 30, mid_y + 360), (mid_x + mid_w - 30, mid_y + 510)], radius=16, fill=(15, 23, 42))
        draw.text((mid_x + 50, mid_y + 380), "3步影子跟读法高效练习：", fill=(250, 204, 21), font=get_font(22))
        draw.text((mid_x + 50, mid_y + 420), "1. 盲听原声  2. 名师拆解  3. 开口跟读", fill=(203, 213, 225), font=get_font(21))
        draw.text((mid_x + 50, mid_y + 458), "听到「3-2-1」提示音后，跟随原声大声复述！", fill=(244, 114, 182), font=get_font(21))

    # 7. Dynamic 4-Step Floating Progress Status Badge (y=1545..1625)
    status_x, status_y, status_w, status_h = 50, 1545, width - 100, 75
    if stage_num == 3:
        s_bg = (225, 29, 72)
        s_text_color = (255, 255, 255)
    elif stage_num == 4:
        s_bg = (16, 185, 129)
        s_text_color = (255, 255, 255)
    elif stage_num == 2:
        s_bg = (245, 158, 11)
        s_text_color = (15, 23, 42)
    elif stage_num == 1:
        s_bg = (79, 70, 229)
        s_text_color = (255, 255, 255)
    else:
        s_bg = (51, 65, 85)
        s_text_color = (255, 255, 255)

    draw.rounded_rectangle([(status_x, status_y), (status_x + status_w, status_y + status_h)], radius=18, fill=s_bg)
    font_status = get_font(28)
    full_status_str = stage_title
    bbox_st = draw.textbbox((0, 0), full_status_str, font=font_status)
    stw = bbox_st[2] - bbox_st[0]
    stx = status_x + (status_w - stw) // 2
    draw.text((stx, status_y + 20), full_status_str, fill=s_text_color, font=font_status)

    # 8. Bottom CTA Conversion Block (y=1640..1870, height=230)
    cta_x, cta_y, cta_w, cta_h = 50, 1640, width - 100, 230
    draw.rounded_rectangle([(cta_x, cta_y), (cta_x + cta_w, cta_y + cta_h)], radius=22, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    font_cta_app = get_font(24)
    if conf.get("is_funnel"):
        draw.text((cta_x + 30, cta_y + 20), "TokyoFlow 日语大师课 • 完整精讲已上线", fill=(56, 189, 248), font=font_cta_app)
        font_cta_sub = get_font(20)
        draw.text((cta_x + 30, cta_y + 56), conf.get("funnel_target", "点击下方关联视频观看完整25分钟大课"), fill=(203, 213, 225), font=font_cta_sub)
        # Action Subscribe Pill
        draw.rounded_rectangle([(cta_x + 24, cta_y + 105), (cta_x + cta_w - 24, cta_y + 195)], radius=16, fill=(225, 29, 72))
        font_sub_btn = get_font(28)
        btn_text = "点击下方关联视频 • 观看完整大课"
    else:
        draw.text((cta_x + 30, cta_y + 20), "TokyoFlow 日语口语伴侣 (iOS App)", fill=(56, 189, 248), font=font_cta_app)
        font_cta_sub = get_font(20)
        draw.text((cta_x + 30, cta_y + 56), "AI声调精准打分 • 10,000+ JLPT 高频词实景原声跟读", fill=(203, 213, 225), font=font_cta_sub)
        # Action Subscribe Pill
        draw.rounded_rectangle([(cta_x + 24, cta_y + 105), (cta_x + cta_w - 24, cta_y + 195)], radius=16, fill=(225, 29, 72))
        font_sub_btn = get_font(28)
        btn_text = "订阅频道 • 每日 60 秒东京原声跟读"

    bbox_btn = draw.textbbox((0, 0), btn_text, font=font_sub_btn)
    btn_w = bbox_btn[2] - bbox_btn[0]
    draw.text((cta_x + (cta_w - btn_w) // 2, cta_y + 130), btn_text, fill=(255, 255, 255), font=font_sub_btn)

    # 9. Bottom Progress Line (y=1900..1910)
    draw.rectangle([(0, 1900), (width, 1910)], fill=(30, 41, 59))
    prog_w = int(width * max(0.0, min(1.0, total_progress)))
    draw.rectangle([(0, 1900), (prog_w, 1910)], fill=(250, 204, 21))

    return img

async def generate_single_chinese_short(conf: dict):
    ep_num = conf["ep_num"]
    folder_name = conf["folder"]
    release_dir = os.path.join("docs", "youtube_releases", folder_name)
    os.makedirs(release_dir, exist_ok=True)

    tmp_dir = os.path.join("tmp", f"tokyoflow_zh_short_ep{ep_num:02d}")
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir, exist_ok=True)

    code_lbl = conf.get("shorts_code", f"EP.{ep_num:02d}")
    print(f"\n==========================================")
    print(f"Building Chinese Interactive Short [{code_lbl}]: {conf['yt_short_title']}")
    print(f"==========================================")

    # 1. Synthesize Audio Tracks
    # 1.1 Yunxi Hook (zh-CN-YunxiNeural)
    hook_audio = os.path.join(tmp_dir, "01_hook.mp3")
    await synth_audio(conf["hook_audio_zh"], "zh-CN-YunxiNeural", hook_audio, rate="+4%")

    # 1.2 Nanami Native Normal Speed (Listen Phase)
    jp_audio_norm = os.path.join(tmp_dir, "02_jp_norm.mp3")
    await synth_audio(conf["jp_sentence"], "ja-JP-NanamiNeural", jp_audio_norm, rate="-4%", pitch="+2Hz")

    # 1.3 Seamless Bilingual In-Line Speech for Pro-Tip (Yunxi + Nanami)
    tip_audio = os.path.join(tmp_dir, "03_tip.mp3")
    speech_chunks_tip = conf.get("speech_chunks_tip")
    if speech_chunks_tip:
        await synthesize_seamless_bilingual_audio(speech_chunks_tip, tip_audio, temp_dir=os.path.join(tmp_dir, "chunks"))
    else:
        tip_text = conf.get("pro_tip_audio_zh", conf["pro_tip_body"])
        await synth_audio(tip_text, "zh-CN-YunxiNeural", tip_audio, rate="+4%")

    # 1.4 Yunxi Countdown Prompt
    shadow_cue_audio = os.path.join(tmp_dir, "04_shadow_cue.mp3")
    await synth_audio("轮到你跟读啦！准备倒计时，3、2、1，开口大声读！", "zh-CN-YunxiNeural", shadow_cue_audio, rate="+6%")

    # 1.5 Beeps (3-2-1 countdown)
    beep_low = os.path.join(tmp_dir, "beep_low.mp3")
    generate_beep(800, 0.12, beep_low)
    beep_high = os.path.join(tmp_dir, "beep_high.mp3")
    generate_beep(1600, 0.25, beep_high)

    # 1.6 Nanami Native Practice Drill Voice for Shadowing (Stage 3)
    jp_audio_drill = os.path.join(tmp_dir, "05_jp_drill.mp3")
    await synth_audio(conf["jp_sentence"], "ja-JP-NanamiNeural", jp_audio_drill, rate="-10%", pitch="+2Hz")

    # 1.7 Chime Success + Outro Feedback & CTA
    chime_audio = os.path.join(tmp_dir, "chime.mp3")
    generate_beep(1200, 0.25, chime_audio)
    outro_audio = os.path.join(tmp_dir, "06_outro.mp3")
    if conf.get("is_funnel"):
        await synth_audio("太棒了！下方已关联完整长视频大课，快点击观看吧！", "zh-CN-YunxiNeural", outro_audio, rate="+4%")
    else:
        await synth_audio("太棒了！快下载 TokyoFlow App 体验实时声调发音打分吧！", "zh-CN-YunxiNeural", outro_audio, rate="+4%")

    # 2. Extract Token Timings with Whisper
    print("Aligning tokens with Whisper for precise karaoke glow (Normal & Practice Drill)...")
    token_objs = conf["tokens"]
    aligned_tokens_norm = align_sentence_tokens_with_audio(jp_audio_norm, token_objs)
    aligned_tokens_drill = align_sentence_tokens_with_audio(jp_audio_drill, token_objs)

    dur_hook = get_audio_duration(hook_audio)
    dur_jp_norm = get_audio_duration(jp_audio_norm)
    dur_tip = get_audio_duration(tip_audio)
    dur_cue = get_audio_duration(shadow_cue_audio)
    dur_drill = get_audio_duration(jp_audio_drill)
    dur_out = get_audio_duration(outro_audio)

    audio_segments = [
        {"file": hook_audio, "dur": dur_hook, "pause": 0.25},
        {"file": jp_audio_norm, "dur": dur_jp_norm, "pause": 0.35},
        {"file": tip_audio, "dur": dur_tip, "pause": 0.35},
        {"file": shadow_cue_audio, "dur": dur_cue, "pause": 0.15},
        {"file": beep_low, "dur": 0.12, "pause": 0.25},
        {"file": beep_low, "dur": 0.12, "pause": 0.25},
        {"file": beep_high, "dur": 0.25, "pause": 0.2},
        {"file": jp_audio_drill, "dur": dur_drill, "pause": 0.3},
        {"file": chime_audio, "dur": 0.25, "pause": 0.2},
        {"file": outro_audio, "dur": dur_out, "pause": 0.4}
    ]

    full_audio_path = os.path.join(tmp_dir, "full_shadow_audio.mp3")
    concat_filter = "".join([f"[{i}:a]" for i in range(len(audio_segments))]) + f"concat=n={len(audio_segments)}:v=0:a=1[outa]"
    cmd_audio = ["ffmpeg", "-y"]
    for seg in audio_segments:
        cmd_audio.extend(["-i", seg["file"]])
    cmd_audio.extend(["-filter_complex", concat_filter, "-map", "[outa]", "-c:a", "libmp3lame", full_audio_path])
    subprocess.run(cmd_audio, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    total_duration = get_audio_duration(full_audio_path)
    print(f"Total Chinese Short Duration: {total_duration:.2f}s")

    # Time boundaries calculation
    t_hook = dur_hook + 0.25
    t_listen = t_hook + dur_jp_norm + 0.35
    t_tip = t_listen + dur_tip + 0.35
    t_countdown = t_tip + dur_cue + 0.15 + (0.12+0.25)*2 + 0.25 + 0.2
    t_shadow_start = t_countdown
    t_shadow_end = t_shadow_start + dur_drill + 0.3
    t_score_end = total_duration

    # 3. Load or Generate Short Cover Thumbnail for First-Frame Injection
    short_thumb_path = os.path.join(release_dir, "short_thumbnail.jpg")
    cover_frame_img = None
    if not os.path.exists(short_thumb_path):
        try:
            from generate_shorts_thumbnails import create_shorts_cover
            hook_title_parts = conf.get("hook_title", "JAPAN TREND\nPOP CULTURE").split("\n")
            cover_item = {
                "bg_image_path": conf.get("bg_image", ""),
                "jlpt_level": conf.get("jlpt_level", "JLPT N5"),
                "sh_code": conf.get("shorts_code", f"SH.{ep_num:02d}"),
                "ep_num": ep_num,
                "hook_main": hook_title_parts[0],
                "hook_sub": hook_title_parts[1] if len(hook_title_parts) > 1 else "POP CULTURE",
                "jp_phrase": conf.get("jp_sentence", ""),
                "romaji": conf.get("romaji_sentence", ""),
                "en_meaning": conf.get("zh_translation", ""),
                "grammar_tag": conf.get("pro_tip_title", "JLPT 核心要点")
            }
            c_img = create_shorts_cover(cover_item)
            c_img.save(short_thumb_path, "JPEG", quality=95)
        except Exception as e:
            print(f"Warning generating cover on the fly: {e}")

    if os.path.exists(short_thumb_path):
        try:
            cover_frame_img = Image.open(short_thumb_path).convert("RGB").resize((1080, 1920), Image.Resampling.LANCZOS)
        except Exception:
            cover_frame_img = None

    # Discover authentic base scene image for background canvas
    bg_cand = os.path.join(release_dir, "news_bg.jpg")
    if not os.path.exists(bg_cand):
        bg_cand = os.path.join(release_dir, "thumbnail.jpg")
    if not os.path.exists(bg_cand):
        scene_dir = "docs/youtube_assets/scene_backgrounds"
        if os.path.exists(scene_dir):
            for f in os.listdir(scene_dir):
                if f.startswith(f"E{conf['ep_num']:02d}") or f.startswith(f"E{conf['ep_num']}"):
                    bg_cand = os.path.join(scene_dir, f)
                    break
    base_canvas_9_16 = prepare_shorts_background(bg_cand)

    # 4. Render Video Frames
    frames_dir = os.path.join(tmp_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)
    fps = 30
    total_frames = int(total_duration * fps)
    print(f"Rendering {total_frames} interactive shadowing frames with first-frame cover injection...")

    for frame_idx in range(total_frames):
        cur_t = frame_idx / fps
        prog = cur_t / total_duration

        # First-Frame Injection: Frames 0..7 (first ~0.26s) use the exact 9:16 master cover
        if frame_idx < 8 and cover_frame_img is not None:
            frame_img = cover_frame_img
        elif cur_t < t_hook:
            stg = 0
            active_tok = -1
            stg_title = "[场景引入] 真实东京日常口语"
            stg_sub = "场景预习"
            spk_prog = 0.0
            frame_img = render_chinese_interactive_frame(
                1080, 1920, conf,
                active_token_idx=active_tok,
                stage_num=stg,
                stage_title=stg_title,
                stage_subtext=stg_sub,
                speaking_prog=spk_prog,
                total_progress=prog,
                frame_idx=frame_idx,
                base_canvas=base_canvas_9_16
            )
        elif cur_t < t_listen:
            stg = 1
            rel_t = cur_t - t_hook
            active_tok = -1
            for tok_i, tok in enumerate(aligned_tokens_norm):
                st = tok.get("start", 0.0) - 0.08
                et = tok.get("end", 0.0)
                if st <= rel_t <= et:
                    active_tok = tok_i
                    break
            stg_title = "[STEP 1] 东京原声原速盲听"
            stg_sub = "仔细聆听"
            spk_prog = 0.0
            frame_img = render_chinese_interactive_frame(
                1080, 1920, conf,
                active_token_idx=active_tok,
                stage_num=stg,
                stage_title=stg_title,
                stage_subtext=stg_sub,
                speaking_prog=spk_prog,
                total_progress=prog,
                frame_idx=frame_idx,
                base_canvas=base_canvas_9_16
            )
        elif cur_t < t_countdown:
            stg = 2
            active_tok = -1
            stg_title = "[STEP 2] 名师语法与文化拆解"
            stg_sub = "核心句型"
            spk_prog = 0.0
            frame_img = render_chinese_interactive_frame(
                1080, 1920, conf,
                active_token_idx=active_tok,
                stage_num=stg,
                stage_title=stg_title,
                stage_subtext=stg_sub,
                speaking_prog=spk_prog,
                total_progress=prog,
                frame_idx=frame_idx,
                base_canvas=base_canvas_9_16
            )
        elif cur_t < t_shadow_end:
            stg = 3
            rel_spk_t = cur_t - t_shadow_start
            spk_prog = rel_spk_t / max(0.1, dur_drill)
            active_tok = -1
            for tok_i, tok in enumerate(aligned_tokens_drill):
                st = tok.get("start", 0.0) - 0.05
                et = tok.get("end", 0.0)
                if st <= rel_spk_t <= et:
                    active_tok = tok_i
                    break
            stg_title = "[STEP 3] 跟着原声开口大声跟读！"
            stg_sub = "大声开口"
            frame_img = render_chinese_interactive_frame(
                1080, 1920, conf,
                active_token_idx=active_tok,
                stage_num=stg,
                stage_title=stg_title,
                stage_subtext=stg_sub,
                speaking_prog=spk_prog,
                total_progress=prog,
                frame_idx=frame_idx,
                base_canvas=base_canvas_9_16
            )
        else:
            stg = 4
            active_tok = -1
            stg_title = "[STEP 4] AI 声调发音打分"
            stg_sub = "TokyoFlow App"
            spk_prog = 1.0
            frame_img = render_chinese_interactive_frame(
                1080, 1920, conf,
                active_token_idx=active_tok,
                stage_num=stg,
                stage_title=stg_title,
                stage_subtext=stg_sub,
                speaking_prog=spk_prog,
                total_progress=prog,
                frame_idx=frame_idx,
                base_canvas=base_canvas_9_16
            )

        frame_file = os.path.join(frames_dir, f"frame_{frame_idx:05d}.jpg")
        frame_img.save(frame_file, "JPEG", quality=90)

    # 5. Assemble Video with ffmpeg
    out_video_path = os.path.join(release_dir, "short.mp4")
    print(f"Encoding Chinese Interactive Short to {out_video_path}...")
    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-r", str(fps),
        "-i", os.path.join(frames_dir, "frame_%05d.jpg"),
        "-i", full_audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "medium",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        out_video_path
    ]
    subprocess.run(cmd_ffmpeg, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # 6. Output short_metadata.md (Strict Zero Emoji Discipline)
    meta_path = os.path.join(release_dir, "short_metadata.md")
    tokens_txt = "\n".join([f"- {t['orig']} ({t['kana']}) : {t.get('meaning', '')}" for t in conf["tokens"]])
    
    meta_content = f"""# YouTube Short 发布包：{conf['folder']}
# {conf['yt_short_title']}

## 发布基本信息
- 剧集：{code_lbl} ({conf['folder']})
- 格式：9:16 竖屏短视频 (1080x1920, 30 fps)
- 跟读引擎：4阶段沉浸式跟读训练（盲听 -> 名师拆解 -> 3-2-1 原声领读录音 -> AI声调打分）
- 视频文件：short.mp4
- 竖屏封面：short_thumbnail.jpg
- 视频时长：{total_duration:.1f}秒

---

## YouTube Shorts 标题 (Title)

```
{conf['yt_short_title']}
```

---

## YouTube Shorts 简介栏 (Description)

```markdown
{conf['yt_short_title']}

东京真实生活场景沉浸式短视频跟读精讲，30秒掌握日本高频地道实用口语。

【日语句子】
{conf['jp_sentence']}
{conf['romaji_sentence']}

【中文翻译】
{conf['zh_translation']}

【词汇拆解】
{tokens_txt}

【名师语法精讲与避坑指南】
{conf['pro_tip_body']}

【3步跟读法】
1. 盲听原声：感受母语者自然发音与节奏。
2. 语法拆解：掌握句型公式与场景文化。
3. 开口复述：在 3-2-1 倒计时后跟随原声大声跟读，校准声调。

【练习推荐】
欢迎在 App Store 下载 TokyoFlow - 日语口语伴侣 App，体验精准 AI 声调打分与 10,000+ 实景原声练习！

订阅 TokyoFlow 日语频道，每天 1 分钟轻松提升日语听力与口语。

#Shorts #学日语 #日语口语 #东京日语 #JLPT #{conf.get('jlpt_level', 'JLPT N5').replace(' ', '')} #日语跟读 #TokyoFlow #{conf['slug']}
```

---

## YouTube 标签 (Tags)

```
shorts, 学日语, 日语口语, 东京日语, jlpt, {conf.get('jlpt_level', 'JLPT N5').lower().replace(' ', '')}, 日语跟读, tokyoflow, {conf['slug']}
```
"""
    with open(meta_path, "w", encoding="utf-8") as fp:
        fp.write(meta_content)

    # Clean tmp dir
    shutil.rmtree(tmp_dir, ignore_errors=True)
    print(f"Completed Chinese Interactive Short for [{code_lbl}] -> {release_dir}/short.mp4")

async def main():
    import argparse
    parser = argparse.ArgumentParser(description="TokyoFlow Chinese YouTube Shorts Master Factory")
    parser.add_argument("--ep", "--episode", type=int, help="Target episode number to generate (e.g. 1)")
    parser.add_argument("--code", type=str, help="Target shorts code (e.g. WS.01, WS.02, EP.01)")
    parser.add_argument("--all", action="store_true", help="Explicitly regenerate all configured Chinese shorts")
    args = parser.parse_args()

    if args.ep:
        targets = [c for c in CHINESE_SHORTS_CONFIGS if c["ep_num"] == args.ep]
        if not targets:
            print(f"[ERROR] No Chinese short configuration found for EP.{args.ep:02d}")
            return
        for conf in targets:
            await generate_single_chinese_short(conf)
    elif args.code:
        code_upper = args.code.upper().strip()
        targets = [c for c in CHINESE_SHORTS_CONFIGS if c.get("shorts_code", "").upper() == code_upper or f"EP.{c['ep_num']:02d}" == code_upper]
        if not targets:
            print(f"[ERROR] No Chinese short configuration found for code: {args.code}")
            return
        for conf in targets:
            await generate_single_chinese_short(conf)
    elif args.all:
        print("==================================================")
        print("Starting Batch Chinese YouTube Shorts Producer (First-Frame Cover Injected)")
        print(f"Target Queue: {len(CHINESE_SHORTS_CONFIGS)} Shorts (WS.01, WS.02, EP.01 ~ EP.11)")
        print("==================================================")
        for conf in CHINESE_SHORTS_CONFIGS:
            await generate_single_chinese_short(conf)
        print("\nAll Chinese interactive shorts successfully generated.")
    else:
        print("[INFO] No target specified. Use --ep <NUM>, --code <CODE>, or --all to process shorts.")
        codes = [c.get("shorts_code", f"EP.{c['ep_num']:02d}") for c in CHINESE_SHORTS_CONFIGS]
        print(f"Available codes: {codes}")

if __name__ == "__main__":
    asyncio.run(main())


