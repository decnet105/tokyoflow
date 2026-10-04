#!/usr/bin/env python3
"""
TokyoFlow Japanese • Batch Multilingual Producer (EP.02 ~ EP.11 Chinese Editions)
=================================================================================
Automates full generation of Chinese localized packages for EP.02 to EP.11:
1. Generates Chinese localized scripts (`script.json`) with precise JLPT badges & cultural insights.
2. Synthesizes Yunxi (zh-CN-YunxiNeural) explainer audio + Nanami (ja-JP-NanamiNeural) Tokyo Japanese.
3. Renders 1080p full HD master video (`video.mp4`) with millisecond karaoke and dynamic HUD cards.
4. Generates 16:9 Chinese Master Thumbnail (`thumbnail.jpg`) and 9:16 Shorts Cover (`short_thumbnail.jpg`).
5. Generates localized metadata (`metadata.md`).
"""

import os
import sys
import json
import asyncio
from pathlib import Path

# Add videogen dir to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from multilingual_video_producer import produce_multilingual_episode

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RELEASES_DIR = PROJECT_ROOT / "docs" / "youtube_releases"

EPISODES_CHINESE_DATA = [
    # -------------------------------------------------------------------------
    # EP.02: 7-Eleven 便利店结账
    # -------------------------------------------------------------------------
    {
        "episode_number": 2,
        "folder_name": "E02-Kombini_Checkout-v1.0-zh",
        "slug": "kombini_checkout_zh",
        "locale": "zh",
        "title": "7-Eleven 与全家便利店结账全流程",
        "yt_title": "【JLPT N5】听懂东京7-Eleven结账！便利店实用口语实景精讲（EP.02）",
        "category": "便利店日常 • 结账指南",
        "level": "JLPT N5",
        "district": "涩谷 (Shibuya)",
        "bg_image": "/Users/kilvonwu/.gemini/antigravity/brain/b34d491c-7bb1-4e81-ab7c-51e66a95dc10/ep02_kombini_16_9_1791043178178.jpg",
        "cover": {
            "hook": "便利店结账秘籍",
            "sub_hook": "两秒听懂收银对话",
            "jp_line1": "レジ袋は結構です、",
            "jp_line2": "袋は大丈夫です！",
            "grammar_tag": "JLPT N5 语法：~は大丈夫です（委婉礼貌拒绝）",
            "translation": "「不用塑料袋了，谢谢。」",
            "context_note": "东京便利店收银台最高频的秒回实用口语",
            "location_tag": "场景：涩谷 7-Eleven 收银台",
            "tag": "🇯🇵 便利店实用原声 • 影子跟读"
        },
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. 便当加热与稍等提示",
                "spoken_text": "お弁当温めますか？少々お待ちください。",
                "meaning": "便当需要加热吗？请稍等片刻。",
                "tip": "回答加热说「温めてください」，不需要说「大丈夫です」。",
                "tokens": [
                    {"orig": "お弁当", "kana": "おべんとう", "romaji": "obentou", "pos": "名词", "meaning": "便当"},
                    {"orig": "温めますか？", "kana": "あたためますか", "romaji": "atatamemasu ka?", "pos": "动词疑问", "meaning": "加热吗？"},
                    {"orig": "少々", "kana": "しょうしょう", "romaji": "shoushou", "pos": "副词", "meaning": "稍微/片刻"},
                    {"orig": "お待ちください。", "kana": "おまちください", "romaji": "omachi kudasai.", "pos": "礼貌请求", "meaning": "请等待"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. 收银台高频词汇与语法拆解",
                "sentence_ja": "お弁当温めますか？少々お待ちください。",
                "vocab": [
                    {"orig": "お弁当", "kana": "おべんとう", "romaji": "obentou", "pos": "名词", "meaning": "便当盒饭"},
                    {"orig": "温めますか", "kana": "あたためますか", "romaji": "atatamemasu ka", "pos": "动词连用", "meaning": "加热吗"},
                    {"orig": "少々", "kana": "しょうしょう", "romaji": "shoushou", "pos": "副词", "meaning": "稍微/稍候"},
                    {"orig": "お待ち", "kana": "おまち", "romaji": "omachi", "pos": "敬语词干", "meaning": "等候"},
                    {"orig": "ください", "kana": "ください", "romaji": "kudasai", "pos": "礼貌祈使", "meaning": "请……"}
                ],
                "grammar_title": "敬语表达：お + 动词ます形词干 + ください",
                "grammar_bullets": [
                    ["1. 敬语祈使句式：", "服务行业向顾客发出礼貌引导的最标准句型。"],
                    ["2. 加热应答技巧：", "想加热直接回答「お願いします（麻烦了）」，不加热回答「大丈夫です（不用了）」。"],
                    ["3. 东京便利店文化：", "日本便利店便当通常在收银台内部由店员统一微波加热。"],
                    ["4. 避坑提示：", "不要使用命令形「待って」，对长辈或服务人员应保持礼貌。"]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "我们来拆解这句便利店收银台每天必听的经典对话。"},
                    {"speaker": "ja", "text": "お弁当", "card_idx": 0},
                    {"speaker": "explainer", "text": "名词：便当、盒饭。", "card_idx": 0},
                    {"speaker": "ja", "text": "温めますか", "card_idx": 1},
                    {"speaker": "explainer", "text": "动词连用形加疑问词：需要帮您加热吗？", "card_idx": 1},
                    {"speaker": "ja", "text": "少々", "card_idx": 2},
                    {"speaker": "explainer", "text": "副词：稍等、片刻。", "card_idx": 2},
                    {"speaker": "ja", "text": "お待ち", "card_idx": 3},
                    {"speaker": "explainer", "text": "动词待つ的敬语连用形，等候。", "card_idx": 3},
                    {"speaker": "ja", "text": "ください", "card_idx": 4},
                    {"speaker": "explainer", "text": "请……礼貌祈使表达。", "card_idx": 4},
                    {"speaker": "explainer", "text": "语法精讲：敬语祈使句式「お加动词词干加ください」。", "is_spotlight": True},
                    {"speaker": "ja", "text": "少々お待ちください。", "is_spotlight": True},
                    {"speaker": "explainer", "text": "意思是请稍等片刻，店员在加热便当或找零时必说。", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "03. 塑料袋礼貌拒绝表达",
                "spoken_text": "レジ袋は結構です、袋は大丈夫です。",
                "meaning": "不需要塑料袋，袋子不用了谢谢。",
                "tip": "「大丈夫です」语气温和，是日本年轻人最常用的委婉礼貌拒绝方式。",
                "tokens": [
                    {"orig": "レジ袋は", "kana": "れじぶくろは", "romaji": "reji-bukuro wa", "pos": "名词+提示", "meaning": "塑料购物袋"},
                    {"orig": "結構です、", "kana": "けっこうです", "romaji": "kekkou desu,", "pos": "形容动词", "meaning": "不用了/足够了"},
                    {"orig": "袋は", "kana": "ふくろは", "romaji": "fukuro wa", "pos": "名词+提示", "meaning": "袋子"},
                    {"orig": "大丈夫です。", "kana": "だいじょうぶです", "romaji": "daijoubu desu.", "pos": "常用表达", "meaning": "不用了/没关系"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "04. 委婉拒绝与袋子表达拆解",
                "sentence_ja": "レジ袋は結構です、袋は大丈夫です。",
                "vocab": [
                    {"orig": "レジ袋", "kana": "れじぶくろ", "romaji": "reji bukuro", "pos": "名词", "meaning": "收银塑料袋"},
                    {"orig": "結構です", "kana": "けっこうです", "romaji": "kekkou desu", "pos": "形容动词", "meaning": "足够了/不用"},
                    {"orig": "袋", "kana": "ふくろ", "romaji": "fukuro", "pos": "名词", "meaning": "袋子"},
                    {"orig": "大丈夫", "kana": "だいじょうぶ", "romaji": "daijoubu", "pos": "形容动词", "meaning": "没关系/不用"},
                    {"orig": "です", "kana": "です", "romaji": "desu", "pos": "助动词", "meaning": "判断助动词"}
                ],
                "grammar_title": "万能口语：〜は大丈夫です（委婉拒绝）",
                "grammar_bullets": [
                    ["1. 委婉拒绝功能：", "在便利店、餐厅等服务场景，表示「不需要、不用麻烦了」。"],
                    ["2. 与結構です对照：", "「結構です」偏向正式，「大丈夫です」在口语中更为自然柔和。"],
                    ["3. 日本环保减塑背景：", "日本便利店塑料袋收费，通常为3至5日元，自带环保袋时常说此句。"],
                    ["4. 肢体配合：", "说话时轻轻摆手，即可瞬间传递地道东京本地人沟通习惯。"]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "接下来拆解两秒委婉拒绝塑料袋的地道口语。"},
                    {"speaker": "ja", "text": "レジ袋", "card_idx": 0},
                    {"speaker": "explainer", "text": "名词：收银台塑料袋。", "card_idx": 0},
                    {"speaker": "ja", "text": "結構です", "card_idx": 1},
                    {"speaker": "explainer", "text": "礼貌拒绝：不用了、足够了。", "card_idx": 1},
                    {"speaker": "ja", "text": "袋", "card_idx": 2},
                    {"speaker": "explainer", "text": "名词：袋子。", "card_idx": 2},
                    {"speaker": "ja", "text": "大丈夫", "card_idx": 3},
                    {"speaker": "explainer", "text": "万能词：不用了、没问题。", "card_idx": 3},
                    {"speaker": "ja", "text": "です", "card_idx": 4},
                    {"speaker": "explainer", "text": "礼貌断定助动词。", "card_idx": 4},
                    {"speaker": "explainer", "text": "语法精讲：大丈夫加断定助动词的委婉拒绝用法。", "is_spotlight": True},
                    {"speaker": "ja", "text": "袋は大丈夫です。", "is_spotlight": True},
                    {"speaker": "explainer", "text": "意思是袋子不用了谢谢，语气温和地道。", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "05. 餐具确认实战问询",
                "spoken_text": "お箸は一膳でよろしいですか？スプーンもお願いします。",
                "meaning": "筷子一双够了吗？请再给我一个勺子。",
                "tip": "「一膳（いちぜん）」是筷子的量词，勺子量词用「本（ほん）」。",
                "tokens": [
                    {"orig": "お箸は", "kana": "おはしは", "romaji": "ohashi wa", "pos": "名词+提示", "meaning": "筷子"},
                    {"orig": "一膳で", "kana": "いちぜんで", "romaji": "ichizen de", "pos": "量词+助词", "meaning": "一双"},
                    {"orig": "よろしいですか？", "kana": "よろしいですか", "romaji": "yoroshii desu ka?", "pos": "敬语疑问", "meaning": "可以吗？"},
                    {"orig": "スプーンも", "kana": "すぷーんも", "romaji": "supuun mo", "pos": "名词+提示", "meaning": "勺子也"},
                    {"orig": "お願いします。", "kana": "おねがいします", "romaji": "onegaishimasu.", "pos": "礼貌短语", "meaning": "拜托了"}
                ]
            },
            {
                "type": "outro",
                "chapter": "06. 关注与练习",
                "spoken_text": "关注 TokyoFlow 日语，欢迎下载 App 一起跟读练习！"
            }
        ]
    },

    # -------------------------------------------------------------------------
    # EP.03: 居酒屋点单
    # -------------------------------------------------------------------------
    {
        "episode_number": 3,
        "folder_name": "E03-Izakaya_Night-v1.0-zh",
        "slug": "izakaya_night_zh",
        "locale": "zh",
        "title": "东京新桥居酒屋点单与经典开场句式",
        "yt_title": "【JLPT N5】像东京本地人一样点单！居酒屋生啤开场实景精讲（EP.03）",
        "category": "居酒屋美食 • 点单秘籍",
        "level": "JLPT N5",
        "district": "新桥 (Shinbashi)",
        "bg_image": "/Users/kilvonwu/.gemini/antigravity/brain/b34d491c-7bb1-4e81-ab7c-51e66a95dc10/ep03_izakaya_16_9_1791043208822.jpg",
        "cover": {
            "hook": "居酒屋点单秘籍",
            "sub_hook": "先来生啤经典神句",
            "jp_line1": "とりあえず生で、",
            "jp_line2": "ビールをお願いします！",
            "grammar_tag": "JLPT N5 语法：とりあえず~で（先来……）",
            "translation": "「先来生啤，麻烦上两杯啤酒！」",
            "context_note": "全日本所有居酒屋通用的黄金开场点单第一句",
            "location_tag": "场景：新桥居酒屋街 • 东京夜生活",
            "tag": "🇯🇵 居酒屋地道点单 • 影子跟读"
        },
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. 居酒屋黄金开场点单",
                "spoken_text": "とりあえず生で、ビールを二つお願いします！",
                "meaning": "先来生啤，请上两杯啤酒！",
                "tip": "在居酒屋落座后店员会先问饮料，用「とりあえず生で」点生啤最地道。",
                "tokens": [
                    {"orig": "とりあえず", "kana": "とりあえず", "romaji": "toriaezu", "pos": "副词", "meaning": "首先/先来"},
                    {"orig": "生で、", "kana": "なまで", "romaji": "nama de,", "pos": "名词+助词", "meaning": "生啤"},
                    {"orig": "ビールを", "kana": "びーるを", "romaji": "biiru o", "pos": "名词+宾格", "meaning": "啤酒"},
                    {"orig": "二つ", "kana": "ふたつ", "romaji": "futatsu", "pos": "量词", "meaning": "两个/两杯"},
                    {"orig": "お願いします！", "kana": "おねがいします", "romaji": "onegaishimasu!", "pos": "礼貌短语", "meaning": "拜托了"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. 点单词汇与酒文化剖析",
                "sentence_ja": "とりあえず生で、ビールを二つお願いします！",
                "vocab": [
                    {"orig": "とりあえず", "kana": "とりあえず", "romaji": "toriaezu", "pos": "副词", "meaning": "首先/暂且"},
                    {"orig": "生", "kana": "なま", "romaji": "nama", "pos": "名词", "meaning": "生啤酒"},
                    {"orig": "ビール", "kana": "びーる", "romaji": "biiru", "pos": "外来语", "meaning": "啤酒"},
                    {"orig": "二つ", "kana": "ふたつ", "romaji": "futatsu", "pos": "量词", "meaning": "两个"},
                    {"orig": "お願いします", "kana": "おねがいします", "romaji": "onegaishimasu", "pos": "礼貌短语", "meaning": "请/拜托"}
                ],
                "grammar_title": "经典句型：とりあえず〜で（先来……）",
                "grammar_bullets": [
                    ["1. 句式用法：", "「とりあえず + 名词 + で」表示在做决定前，先快速点上某样东西。"],
                    ["2. 生（なま）的含义：", "指「生ビール（鲜扎生啤）」，不需要说全称，直接说「生（なま）」即可。"],
                    ["3. 居酒屋开场礼仪：", "日本职场聚会落座后，通常全员先点生啤共同干杯（乾杯，かんぱい）。"],
                    ["4. 数量词点单公式：", "物品 + を + 数量（ひとつ / ふたつ / みっつ）+ お願いします。"]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "我们来拆解日本居酒屋最著名、最高频的开场点单神句。"},
                    {"speaker": "ja", "text": "とりあえず", "card_idx": 0},
                    {"speaker": "explainer", "text": "副词：首先、先来。", "card_idx": 0},
                    {"speaker": "ja", "text": "生", "card_idx": 1},
                    {"speaker": "explainer", "text": "名词：生啤酒、扎啤。", "card_idx": 1},
                    {"speaker": "ja", "text": "ビール", "card_idx": 2},
                    {"speaker": "explainer", "text": "外来语：啤酒。", "card_idx": 2},
                    {"speaker": "ja", "text": "二つ", "card_idx": 3},
                    {"speaker": "explainer", "text": "数量词：两个、两杯。", "card_idx": 3},
                    {"speaker": "ja", "text": "お願いします", "card_idx": 4},
                    {"speaker": "explainer", "text": "万能礼貌句：麻烦了、请给我。", "card_idx": 4},
                    {"speaker": "explainer", "text": "语法精讲：居酒屋点单公式，先来某样东西。", "is_spotlight": True},
                    {"speaker": "ja", "text": "とりあえず生で！", "is_spotlight": True},
                    {"speaker": "explainer", "text": "意思是先来生啤，落座两秒内喊出这句话，店员立即心领神会。", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "03. 冰水与买单常用表达",
                "spoken_text": "すみません、お冷とお会計をお願いします。",
                "meaning": "不好意思，请上一杯冰水，顺便买单结账。",
                "tip": "日本餐厅冰水免费，专有名词称为「お冷（おひや）」。",
                "tokens": [
                    {"orig": "すみません、", "kana": "すみません", "romaji": "sumimasen,", "pos": "短语", "meaning": "不好意思"},
                    {"orig": "お冷と", "kana": "おひやと", "romaji": "ohiya to", "pos": "名词+连词", "meaning": "冰水和"},
                    {"orig": "お会計を", "kana": "おかいけいを", "romaji": "okaikei o", "pos": "名词+宾格", "meaning": "结账/买单"},
                    {"orig": "お願いします。", "kana": "おねがいします", "romaji": "onegaishimasu.", "pos": "礼貌短语", "meaning": "拜托了"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "04. 买单与服务词汇深度剖析",
                "sentence_ja": "すみません、お冷とお会計をお願いします。",
                "vocab": [
                    {"orig": "すみません", "kana": "すみません", "romaji": "sumimasen", "pos": "短语", "meaning": "劳驾/不好意思"},
                    {"orig": "お冷", "kana": "おひや", "romaji": "ohiya", "pos": "名词", "meaning": "免费冰水"},
                    {"orig": "と", "kana": "と", "romaji": "to", "pos": "助词", "meaning": "和/跟"},
                    {"orig": "お会計", "kana": "おかいけい", "romaji": "okaikei", "pos": "名词", "meaning": "结账买单"},
                    {"orig": "お願いします", "kana": "おねがいします", "romaji": "onegaishimasu", "pos": "短语", "meaning": "请/拜托"}
                ],
                "grammar_title": "居酒屋结账文化：お会計 / お勘定",
                "grammar_bullets": [
                    ["1. 结账词汇选择：", "「お会計（おかいけい）」最为普遍优雅；「お勘定（おかんじょう）」略带传统老店气息。"],
                    ["2. お冷（おひや）特指：", "餐厅免费提供的冰水。温水称为「白湯（さゆ）」，热茶称为「あがり/お茶」。"],
                    ["3. 经典肢体语言：", "在嘈杂居酒屋，向店员双手食指交叉比作「X」形，代表请求结账。"],
                    ["4. 找零礼仪：", "结账通常在门口收银台进行，店员会将找零与小票用双手端托盘递上。"]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "接下来拆解居酒屋要冰水与买单的黄金组合句。"},
                    {"speaker": "ja", "text": "すみません", "card_idx": 0},
                    {"speaker": "explainer", "text": "呼叫服务员必备短语：劳驾、不好意思。", "card_idx": 0},
                    {"speaker": "ja", "text": "お冷", "card_idx": 1},
                    {"speaker": "explainer", "text": "名词：餐厅免费提供的冰水。", "card_idx": 1},
                    {"speaker": "ja", "text": "と", "card_idx": 2},
                    {"speaker": "explainer", "text": "并列助词：和、跟。", "card_idx": 2},
                    {"speaker": "ja", "text": "お会計", "card_idx": 3},
                    {"speaker": "explainer", "text": "名词：结账、买单。", "card_idx": 3},
                    {"speaker": "ja", "text": "お願いします", "card_idx": 4},
                    {"speaker": "explainer", "text": "拜托了、麻烦您。", "card_idx": 4},
                    {"speaker": "explainer", "text": "语法精讲：结账与呼叫服务员的地道表达。", "is_spotlight": True},
                    {"speaker": "ja", "text": "お会計をお願いします。", "is_spotlight": True},
                    {"speaker": "explainer", "text": "意思是麻烦结账，也可以配合食指交叉比X手势。", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "05. 招牌推荐实战问询",
                "spoken_text": "おすすめの焼き鳥は何ですか？盛り合わせをください。",
                "meaning": "请问推荐的烤鸡肉串是什么？请给我来一份拼盘。",
                "tip": "不知道点什么时，说「盛り合わせ（拼盘）」可以品尝到主厨招牌组合。",
                "tokens": [
                    {"orig": "おすすめの", "kana": "おすすめの", "romaji": "osusume no", "pos": "名词+助词", "meaning": "推荐的"},
                    {"orig": "焼き鳥は", "kana": "やきとりは", "romaji": "yakitori wa", "pos": "名词+提示", "meaning": "烤鸡肉串"},
                    {"orig": "何ですか？", "kana": "なんですか", "romaji": "nan desu ka?", "pos": "疑问句", "meaning": "是什么？"},
                    {"orig": "盛り合わせを", "kana": "もりあわせを", "romaji": "moriawase o", "pos": "名词+宾格", "meaning": "拼盘组合"},
                    {"orig": "ください。", "kana": "ください", "romaji": "kudasai.", "pos": "短语", "meaning": "请给我"}
                ]
            },
            {
                "type": "outro",
                "chapter": "06. 关注与练习",
                "spoken_text": "关注 TokyoFlow 日语，欢迎下载 App 一起跟读练习！"
            }
        ]
    },

    # -------------------------------------------------------------------------
    # EP.04: 秋叶原手办与免税
    # -------------------------------------------------------------------------
    {
        "episode_number": 4,
        "folder_name": "E04-Akiba_Pilgrimage-v1.0-zh",
        "slug": "akiba_pilgrimage_zh",
        "locale": "zh",
        "title": "秋叶原二次元手办专门店免税购物指南",
        "yt_title": "【JLPT N5】秋叶原淘手办必学！免税退税与查库存实用口语（EP.04）",
        "category": "秋叶原购物 • 手办免税",
        "level": "JLPT N5",
        "district": "秋叶原 (Akihabara)",
        "bg_image": "tmp/videogen/real_photos/ep04_akiba_2.jpg",
        "cover": {
            "hook": "秋叶原购物秘籍",
            "sub_hook": "手办免税立省10%",
            "jp_line1": "免税手続きは、",
            "jp_line2": "ここでできますか？",
            "grammar_tag": "JLPT N5 语法：~できますか（能够……/可以做……吗）",
            "translation": "「请问可以在这里办理免税吗？」",
            "context_note": "秋叶原动漫手办周边店直接享受10%退税省钱神句",
            "location_tag": "场景：秋叶原电器街 • 手办专门店",
            "tag": "🇯🇵 二次元圣地实景 • 影子跟读"
        },
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. 免税退税实战问询",
                "spoken_text": "すみません、免税手続きはここでできますか？",
                "meaning": "不好意思，请问这里可以办理免税吗？",
                "tip": "购物满5000日元出示护照即可办理免税，直接免除10%消费税。",
                "tokens": [
                    {"orig": "すみません、", "kana": "すみません", "romaji": "sumimasen,", "pos": "短语", "meaning": "不好意思"},
                    {"orig": "免税手続きは", "kana": "めんぜいてつづきは", "romaji": "menzei tetsuzuki wa", "pos": "名词+提示", "meaning": "免税手续"},
                    {"orig": "ここで", "kana": "ここで", "romaji": "koko de", "pos": "代词+场所", "meaning": "在这里"},
                    {"orig": "できますか？", "kana": "できますか", "romaji": "dekimasu ka?", "pos": "可能动词", "meaning": "可以做吗？"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. 免税问询核心词汇拆解",
                "sentence_ja": "すみません、免税手続きはここでできますか？",
                "vocab": [
                    {"orig": "すみません", "kana": "すみません", "romaji": "sumimasen", "pos": "短语", "meaning": "打扰一下"},
                    {"orig": "免税", "kana": "めんぜい", "romaji": "menzei", "pos": "名词", "meaning": "免税 Tax-Free"},
                    {"orig": "手続き", "kana": "てつづき", "romaji": "tetsuzuki", "pos": "名词", "meaning": "手续/办理"},
                    {"orig": "ここで", "kana": "ここで", "romaji": "koko de", "pos": "代词", "meaning": "在这里"},
                    {"orig": "できますか", "kana": "できますか", "romaji": "dekimasu ka", "pos": "可能态", "meaning": "可以办理吗"}
                ],
                "grammar_title": "可能表达：〜できますか（能做……吗？）",
                "grammar_bullets": [
                    ["1. 语法功能：", "名词 + が / は + できますか，询问是否具备某种功能或服务。"],
                    ["2. 免税退税门槛：", "同一店铺当天消费满5000日元（不含税）即可办理。"],
                    ["3. 护照携带要求：", "必须出示入境盖有上陆许可章的实体护照原件。"],
                    ["4. 肯定回答对照：", "店员通常回答「はい、レジで承ります（是的，在收银台即可办理）」。"]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "我们来拆解秋叶原购物立省百分之十税费的核心句式。"},
                    {"speaker": "ja", "text": "すみません", "card_idx": 0},
                    {"speaker": "explainer", "text": "常用寒暄：劳驾、不好意思。", "card_idx": 0},
                    {"speaker": "ja", "text": "免税", "card_idx": 1},
                    {"speaker": "explainer", "text": "名词：免税、Tax-Free。", "card_idx": 1},
                    {"speaker": "ja", "text": "手続き", "card_idx": 2},
                    {"speaker": "explainer", "text": "名词：办理、流程手续。", "card_idx": 2},
                    {"speaker": "ja", "text": "ここで", "card_idx": 3},
                    {"speaker": "explainer", "text": "场所代词加助词：在这里。", "card_idx": 3},
                    {"speaker": "ja", "text": "できますか", "card_idx": 4},
                    {"speaker": "explainer", "text": "可能态疑问：可以办理吗？", "card_idx": 4},
                    {"speaker": "explainer", "text": "语法精讲：询问是否可以办理某项手续的经典句型。", "is_spotlight": True},
                    {"speaker": "ja", "text": "免税手続きはここでできますか？", "is_spotlight": True},
                    {"speaker": "explainer", "text": "意思是请问这里能免税吗，结账前必问。", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "03. 手办未拆封库存问询",
                "spoken_text": "このフィギュアの未開封品は在庫がありますか？",
                "meaning": "请问这个手办有未拆封的新品库存吗？",
                "tip": "秋叶原许多展示品已拆封，想要全新盒装请认准「未開封品（みかいふうひん）」。",
                "tokens": [
                    {"orig": "この", "kana": "この", "romaji": "kono", "pos": "连体词", "meaning": "这个"},
                    {"orig": "フィギュアの", "kana": "ふぃぎゅあの", "romaji": "figyua no", "pos": "名词+助词", "meaning": "手办的"},
                    {"orig": "未開封品は", "kana": "みかいふうひんは", "romaji": "mikaifuuhin wa", "pos": "名词+提示", "meaning": "未拆封新品"},
                    {"orig": "在庫が", "kana": "ざいこが", "romaji": "zaiko ga", "pos": "名词+主格", "meaning": "库存"},
                    {"orig": "ありますか？", "kana": "ありますか", "romaji": "arimasu ka?", "pos": "存在动词", "meaning": "有吗？"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "04. 手办收藏与库存词汇拆解",
                "sentence_ja": "このフィギュアの未開封品は在庫がありますか？",
                "vocab": [
                    {"orig": "この", "kana": "この", "romaji": "kono", "pos": "代词", "meaning": "这个"},
                    {"orig": "フィギュア", "kana": "ふぃぎゅあ", "romaji": "figyua", "pos": "外来语", "meaning": "手办模型"},
                    {"orig": "未開封品", "kana": "みかいふうひん", "romaji": "mikaifuuhin", "pos": "名词", "meaning": "未开封盒装"},
                    {"orig": "在庫", "kana": "ざいこ", "romaji": "zaiko", "pos": "名词", "meaning": "库存/存货"},
                    {"orig": "ありますか", "kana": "ありますか", "romaji": "arimasu ka", "pos": "存在动词", "meaning": "有存货吗"}
                ],
                "grammar_title": "存在句型：〜は在庫がありますか（有库存吗？）",
                "grammar_bullets": [
                    ["1. 购物查库存公式：", "商品名 + の + 在庫はありますか，各类专门店通用。"],
                    ["2. 中古与新品区分：", "「未開封品（全新未拆封）」、「開封済み（已拆封）」、「ジャンク品（瑕疵品）」。"],
                    ["3. 店员查找库存回答：", "「バックヤードを確認してまいります（我帮您去后库确认一下）」。"],
                    ["4. 无库存回答对照：", "「申し訳ありません、現品限りとなります（抱歉，只剩柜台展示的现货了）」。"]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "接下来拆解在秋叶原淘全新手办的必备查库存表达。"},
                    {"speaker": "ja", "text": "この", "card_idx": 0},
                    {"speaker": "explainer", "text": "指示连体词：这个。", "card_idx": 0},
                    {"speaker": "ja", "text": "フィギュア", "card_idx": 1},
                    {"speaker": "explainer", "text": "外来语：手办模型、Figure。", "card_idx": 1},
                    {"speaker": "ja", "text": "未開封品", "card_idx": 2},
                    {"speaker": "explainer", "text": "专有名词：全新未拆封商品。", "card_idx": 2},
                    {"speaker": "ja", "text": "在庫", "card_idx": 3},
                    {"speaker": "explainer", "text": "名词：库存、存货。", "card_idx": 3},
                    {"speaker": "ja", "text": "ありますか", "card_idx": 4},
                    {"speaker": "explainer", "text": "存在动词疑问：有吗？", "card_idx": 4},
                    {"speaker": "explainer", "text": "语法精讲：询问是否有未开封新品库存的黄金句型。", "is_spotlight": True},
                    {"speaker": "ja", "text": "未開封品の在庫はありますか？", "is_spotlight": True},
                    {"speaker": "explainer", "text": "意思是请问有未拆封的库存吗，手办玩家必备口语。", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "05. 护照出示实战问询",
                "spoken_text": "パスポートを見せていただけますか？こちらでサインをお願いします。",
                "meaning": "可以出示一下您的护照吗？请在这里签字确认。",
                "tip": "免税办理最后一步，店员会扫描护照并请您在电子屏上签名。",
                "tokens": [
                    {"orig": "パスポートを", "kana": "ぱすぽーとを", "romaji": "pasupooto o", "pos": "名词+宾格", "meaning": "护照"},
                    {"orig": "見せて", "kana": "みせて", "romaji": "misete", "pos": "动词て形", "meaning": "出示"},
                    {"orig": "いただけますか？", "kana": "いただけますか", "romaji": "itadakemasu ka?", "pos": "敬语请求", "meaning": "能给我……吗？"},
                    {"orig": "こちらで", "kana": "こちらで", "romaji": "kochira de", "pos": "代词+场所", "meaning": "在这里"},
                    {"orig": "サインをお願いします。", "kana": "さいんをおねがいします", "romaji": "sain o onegaishimasu.", "pos": "短语", "meaning": "请签字"}
                ]
            },
            {
                "type": "outro",
                "chapter": "06. 关注与练习",
                "spoken_text": "关注 TokyoFlow 日语，欢迎下载 App 一起跟读练习！"
            }
        ]
    },
    # -------------------------------------------------------------------------
    # EP.05: 东京地铁换乘与精算机
    # -------------------------------------------------------------------------
    {
        "episode_number": 5,
        "folder_name": "E05-Tokyo_Subway_Rush-v1.0-zh",
        "slug": "tokyo_subway_rush_zh",
        "locale": "zh",
        "title": "东京地铁出站补票与精算机使用指南",
        "yt_title": "【JLPT N4】东京地铁坐过站/余额不足？精算机补票实景精讲（EP.05）",
        "category": "东京交通 • 地铁补票",
        "level": "JLPT N4",
        "district": "赤坂见附 (Akasaka)",
        "bg_image": "tmp/videogen/real_photos/ep05_metro_gates.jpg",
        "cover": {
            "hook": "地铁补票避坑",
            "sub_hook": "出站余额不足秒解决",
            "jp_line1": "乗り越し精算機は、",
            "jp_line2": "どこにありますか？",
            "grammar_tag": "JLPT N4 语法：~はどこにありますか（询问场所方位）",
            "translation": "「请问补票机在哪里？」",
            "context_note": "东京地铁刷卡不过闸机时最实用的求助句式",
            "location_tag": "场景：东京地铁闸机口 • 精算机前",
            "tag": "🇯🇵 地铁出行必备 • 影子跟读"
        },
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. 站台精算机位置问询",
                "spoken_text": "すみません、乗り越し精算機はどこにありますか？",
                "meaning": "不好意思，请问坐过站的补票机在哪里？",
                "tip": "出站时西瓜卡余额不足导致红灯报警，找「精算機（せいさんき）」补差价即可。",
                "tokens": [
                    {"orig": "すみません、", "kana": "すみません", "romaji": "sumimasen,", "pos": "短语", "meaning": "不好意思"},
                    {"orig": "乗り越し", "kana": "のりこし", "romaji": "norikoshi", "pos": "名词", "meaning": "乘车越站"},
                    {"orig": "精算機は", "kana": "せいさんきは", "romaji": "seisanki wa", "pos": "名词+提示", "meaning": "补票结算机"},
                    {"orig": "どこに", "kana": "どこに", "romaji": "doko ni", "pos": "疑问代词", "meaning": "在哪里"},
                    {"orig": "ありますか？", "kana": "ありますか", "romaji": "arimasu ka?", "pos": "存在动词", "meaning": "有/在吗？"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. 补票词汇与交通文化拆解",
                "sentence_ja": "すみません、乗り越し精算機はどこにありますか？",
                "vocab": [
                    {"orig": "すみません", "kana": "すみません", "romaji": "sumimasen", "pos": "短语", "meaning": "劳驾/抱歉"},
                    {"orig": "乗り越し", "kana": "のりこし", "romaji": "norikoshi", "pos": "名词", "meaning": "乘车越站/坐过站"},
                    {"orig": "精算機", "kana": "せいさんき", "romaji": "seisanki", "pos": "名词", "meaning": "补票机/精算机"},
                    {"orig": "どこ", "kana": "どこ", "romaji": "doko", "pos": "疑问词", "meaning": "哪里"},
                    {"orig": "ありますか", "kana": "ありますか", "romaji": "arimasu ka", "pos": "存在动词", "meaning": "有/在吗"}
                ],
                "grammar_title": "问路句型：名词 + はどこにありますか",
                "grammar_bullets": [
                    ["1. 句式用法：", "用于询问建筑物、设施或物品的具体位置（事物用あります，人物动物用います）。"],
                    ["2. 精算机功能：", "日本所有车站闸机旁均设有黄色「精算機」，放入车票或IC卡投入差价即可通关。"],
                    ["3. 坐过站的表达：", "「乗り越す（のりこす）」专指坐过预定站点，补交票价称为「乗り越し精算」。"],
                    ["4. 站务员回答：", "「改札口の右手にございます（在检票口的右手边）」。"]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "我们来拆解在东京地铁坐过站或卡内没钱时的急救口语。"},
                    {"speaker": "ja", "text": "すみません", "card_idx": 0},
                    {"speaker": "explainer", "text": "向站务员求助发问：不好意思、劳驾。", "card_idx": 0},
                    {"speaker": "ja", "text": "乗り越し", "card_idx": 1},
                    {"speaker": "explainer", "text": "专有名词：乘车坐过站、越站。", "card_idx": 1},
                    {"speaker": "ja", "text": "精算機", "card_idx": 2},
                    {"speaker": "explainer", "text": "名词：自动补票机、结算机。", "card_idx": 2},
                    {"speaker": "ja", "text": "どこ", "card_idx": 3},
                    {"speaker": "explainer", "text": "疑问代词：在哪里。", "card_idx": 3},
                    {"speaker": "ja", "text": "ありますか", "card_idx": 4},
                    {"speaker": "explainer", "text": "非生物存在疑问句：有吗、在吗？", "card_idx": 4},
                    {"speaker": "explainer", "text": "语法精讲：询问某处设施方位的标准公式。", "is_spotlight": True},
                    {"speaker": "ja", "text": "乗り越し精算機はどこにありますか？", "is_spotlight": True},
                    {"speaker": "explainer", "text": "意思是请问补票机在哪里，出站遇阻时直接问站务员。", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "03. 交通卡余额不足与充值",
                "spoken_text": "ICカードの残高が足りません、チャージしたいです。",
                "meaning": "交通卡余额不足，我想充值。",
                "tip": "充值在日语中直接使用外来语「チャージ（Charge）」，极为简单实用。",
                "tokens": [
                    {"orig": "ICカードの", "kana": "あいしーかーどの", "romaji": "aishii-kaado no", "pos": "外来语+助词", "meaning": "交通IC卡的"},
                    {"orig": "残高が", "kana": "ざんだかが", "romaji": "zandaka ga", "pos": "名词+主格", "meaning": "卡内余额"},
                    {"orig": "足りません、", "kana": "たりません", "romaji": "tarimasen,", "pos": "动词否定", "meaning": "不够/不足"},
                    {"orig": "チャージ", "kana": "ちゃーじ", "romaji": "chaaji", "pos": "外来语", "meaning": "充值"},
                    {"orig": "したいです。", "kana": "したいです", "romaji": "shitai desu.", "pos": "愿望句型", "meaning": "想做……"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "04. 余额与充值愿望句型拆解",
                "sentence_ja": "ICカードの残高が足りません、チャージしたいです。",
                "vocab": [
                    {"orig": "ICカード", "kana": "あいしーかーど", "romaji": "aishii kaado", "pos": "名词", "meaning": "Suica/Pasmo"},
                    {"orig": "残高", "kana": "ざんだか", "romaji": "zandaka", "pos": "名词", "meaning": "账户余额"},
                    {"orig": "足りません", "kana": "たりません", "romaji": "tarimasen", "pos": "动词否定", "meaning": "不足/不够"},
                    {"orig": "チャージ", "kana": "ちゃーじ", "romaji": "chaaji", "pos": "名词", "meaning": "充值/加值"},
                    {"orig": "したいです", "kana": "したいです", "romaji": "shitai desu", "pos": "愿望句", "meaning": "想做……"}
                ],
                "grammar_title": "愿望表达：动词ます形词干 + たいです",
                "grammar_bullets": [
                    ["1. 表达自身愿望：", "「动词词干 + たいです」表示第一人称“我想做某事”。"],
                    ["2. 残高（ざんだか）：", "特指账户、银行卡或交通卡的可用余额。"],
                    ["3. 充值设备操作：", "除了精算机，日本各大车站自动售票机均支持1000日元起现金充值。"],
                    ["4. 询问充值位置：", "「チャージはどこでできますか（请问在哪里可以充值？）」。"]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "接下来拆解交通卡余额不足时的充值诉求表达。"},
                    {"speaker": "ja", "text": "ICカード", "card_idx": 0},
                    {"speaker": "explainer", "text": "外来语：西瓜卡、Pasmo等交通IC卡。", "card_idx": 0},
                    {"speaker": "ja", "text": "残高", "card_idx": 1},
                    {"speaker": "explainer", "text": "名词：卡内余额。", "card_idx": 1},
                    {"speaker": "ja", "text": "足りません", "card_idx": 2},
                    {"speaker": "explainer", "text": "动词否定形式：不足、不够。", "card_idx": 2},
                    {"speaker": "ja", "text": "チャージ", "card_idx": 3},
                    {"speaker": "explainer", "text": "外来语名词：充值、加值。", "card_idx": 3},
                    {"speaker": "ja", "text": "したいです", "card_idx": 4},
                    {"speaker": "explainer", "text": "愿望助动词：想要做某事。", "card_idx": 4},
                    {"speaker": "explainer", "text": "语法精讲：表达想要充值的经典句型。", "is_spotlight": True},
                    {"speaker": "ja", "text": "チャージしたいです。", "is_spotlight": True},
                    {"speaker": "explainer", "text": "意思是我想充值，窗口求助时简洁明了。", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "05. 换乘联络通道实战问询",
                "spoken_text": "丸ノ内線への連絡通路はこちらですか？まっすぐお進みください。",
                "meaning": "去丸之内线的换乘通道是走这边吗？请一直往前走。",
                "tip": "在新宿、东京等大站换乘时，找「連絡通路（れんらくつうろ）」标识可快速通达。",
                "tokens": [
                    {"orig": "丸ノ内線への", "kana": "まるのうちせんへの", "romaji": "marunouchi-sen e no", "pos": "专有名词+助词", "meaning": "去丸之内线的"},
                    {"orig": "連絡通路は", "kana": "れんらくつうろは", "romaji": "renraku tsuuro wa", "pos": "名词+提示", "meaning": "换乘联络通道"},
                    {"orig": "こちらですか？", "kana": "こちらですか", "romaji": "kochira desu ka?", "pos": "代词疑问", "meaning": "是这边吗？"},
                    {"orig": "まっすぐ", "kana": "まっすぐ", "romaji": "massugu", "pos": "副词", "meaning": "径直/一直"},
                    {"orig": "お進みください。", "kana": "おすすみください", "romaji": "osusumi kudasai.", "pos": "敬语祈使", "meaning": "请往前走"}
                ]
            },
            {
                "type": "outro",
                "chapter": "06. 关注与练习",
                "spoken_text": "关注 TokyoFlow 日语，欢迎下载 App 一起跟读练习！"
            }
        ]
    },

    # -------------------------------------------------------------------------
    # EP.06: 便利店咖啡机与ATM
    # -------------------------------------------------------------------------
    {
        "episode_number": 6,
        "folder_name": "E06-Kombini_Coffee_ATM-v1.0-zh",
        "slug": "kombini_coffee_atm_zh",
        "locale": "zh",
        "title": "便利店现磨冰咖啡购买与ATM外卡取现",
        "yt_title": "【JLPT N5】便利店咖啡怎么买？冷柜取杯与ATM取现全流程精讲（EP.06）",
        "category": "便利店日常 • 咖啡与ATM",
        "level": "JLPT N5",
        "district": "新宿 (Shinjuku)",
        "bg_image": "tmp/videogen/real_photos/ep06_coffee_1.jpg",
        "cover": {
            "hook": "便利店咖啡秘籍",
            "sub_hook": "冷柜拿杯收银按键",
            "jp_line1": "アイスコーヒーのRを、",
            "jp_line2": "ひとつください！",
            "grammar_tag": "JLPT N5 语法：~のRで / ひとつ（数量词与点单）",
            "translation": "「请给我一杯常规中杯冰咖啡！」",
            "context_note": "日本便利店冰咖啡标准购买口诀与按键指南",
            "location_tag": "场景：便利店咖啡机与Seven Bank ATM",
            "tag": "🇯🇵 便利店实用技能 • 影子跟读"
        },
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. 现磨冰咖啡收银点单",
                "spoken_text": "アイスコーヒーのRを、ひとつください！",
                "meaning": "请给我一杯常规中杯冰咖啡！",
                "tip": "冰咖啡需先去冷冻柜拿装有冰块的杯子，再去收银台结账并到机器前按键。",
                "tokens": [
                    {"orig": "アイスコーヒーの", "kana": "あいすこーひーの", "romaji": "aisu koohii no", "pos": "外来语+助词", "meaning": "冰咖啡的"},
                    {"orig": "Rを、", "kana": "あーるを", "romaji": "aaru o,", "pos": "尺寸代号+宾格", "meaning": "Regular中杯"},
                    {"orig": "ひとつ", "kana": "ひとつ", "romaji": "hitotsu", "pos": "量词", "meaning": "一个/一杯"},
                    {"orig": "ください！", "kana": "ください", "romaji": "kudasai!", "pos": "短语", "meaning": "请给我"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. 咖啡点单尺寸与动线拆解",
                "sentence_ja": "アイスコーヒーのRを、ひとつください！",
                "vocab": [
                    {"orig": "アイスコーヒー", "kana": "あいすこーひー", "romaji": "aisu koohii", "pos": "外来语", "meaning": "冰咖啡"},
                    {"orig": "R", "kana": "あーる", "romaji": "aaru", "pos": "量词", "meaning": "Regular 标准杯"},
                    {"orig": "を", "kana": "を", "romaji": "o", "pos": "助词", "meaning": "宾格助词"},
                    {"orig": "ひとつ", "kana": "ひとつ", "romaji": "hitotsu", "pos": "量词", "meaning": "一个/一份"},
                    {"orig": "ください", "kana": "ください", "romaji": "kudasai", "pos": "祈使短语", "meaning": "请给……"}
                ],
                "grammar_title": "点单公式：物品 + の + 尺寸 + を + 数量 + ください",
                "grammar_bullets": [
                    ["1. 杯型代号辨识：", "R 代表 Regular（标准中杯，约110日元）；L 代表 Large（大杯）。"],
                    ["2. 冷热购买动线差异：", "热咖啡直接在收银台点单拿空纸杯；冰咖啡必须先在冷冻柜自取冰杯。"],
                    ["3. 自助咖啡机操作：", "将撕开封口的冰杯放入机器，按下对应的「アイス（Ice）」与「R」按钮。"],
                    ["4. 数量词复习：", "ひとつ（一个）、ふたつ（两个）、みっつ（三个）。"]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "我们来拆解日本便利店极高性价比的现磨冰咖啡购买技巧。"},
                    {"speaker": "ja", "text": "アイスコーヒー", "card_idx": 0},
                    {"speaker": "explainer", "text": "外来语：冰咖啡。", "card_idx": 0},
                    {"speaker": "ja", "text": "R", "card_idx": 1},
                    {"speaker": "explainer", "text": "杯型读作 aaru，代表标准中杯。", "card_idx": 1},
                    {"speaker": "ja", "text": "を", "card_idx": 2},
                    {"speaker": "explainer", "text": "提示动作对象的宾格助词。", "card_idx": 2},
                    {"speaker": "ja", "text": "ひとつ", "card_idx": 3},
                    {"speaker": "explainer", "text": "和语数量词：一份、一杯。", "card_idx": 3},
                    {"speaker": "ja", "text": "ください", "card_idx": 4},
                    {"speaker": "explainer", "text": "请给我，点单必备表达。", "card_idx": 4},
                    {"speaker": "explainer", "text": "语法精讲：便利店点饮料的标准句型。", "is_spotlight": True},
                    {"speaker": "ja", "text": "アイスコーヒーのRをひとつください。", "is_spotlight": True},
                    {"speaker": "explainer", "text": "意思是请给我一杯标准杯冰咖啡，结账时直接说。", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "03. ATM海外银联卡取款问询",
                "spoken_text": "ATMで海外カードの引き出しは可能ですか？",
                "meaning": "请问在ATM机上可以使用海外卡取现吗？",
                "tip": "7-Eleven 的 Seven Bank ATM 全面支持中文界面与银联/Visa/MasterCard 取日元现金。",
                "tokens": [
                    {"orig": "ATMで", "kana": "えーてぃーえむで", "romaji": "eetiiemu de", "pos": "名词+手段", "meaning": "在ATM上"},
                    {"orig": "海外カードの", "kana": "かいがいかーどの", "romaji": "kaigai kaado no", "pos": "名词+助词", "meaning": "海外银行卡的"},
                    {"orig": "引き出しは", "kana": "ひきだしは", "romaji": "hikidashi wa", "pos": "名词+提示", "meaning": "取款/取现"},
                    {"orig": "可能ですか？", "kana": "かのうですか", "romaji": "kanou desu ka?", "pos": "形容动词疑问", "meaning": "可以吗？"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "04. 银行金融与取款词汇拆解",
                "sentence_ja": "ATMで海外カードの引き出しは可能ですか？",
                "vocab": [
                    {"orig": "ATM", "kana": "えーてぃーえむ", "romaji": "eetiiemu", "pos": "名词", "meaning": "自动柜员机"},
                    {"orig": "海外カード", "kana": "かいがいかーど", "romaji": "kaigai kaado", "pos": "名词", "meaning": "境外发行的卡"},
                    {"orig": "引き出し", "kana": "ひきだし", "romaji": "hikidashi", "pos": "名词", "meaning": "取款/提现"},
                    {"orig": "可能", "kana": "かのう", "romaji": "kanou", "pos": "名词", "meaning": "可行/可能"},
                    {"orig": "ですか", "kana": "ですか", "romaji": "desu ka", "pos": "疑问助词", "meaning": "是……吗"}
                ],
                "grammar_title": "正式询问句型：名词 + は可能ですか",
                "grammar_bullets": [
                    ["1. 语法功能：", "比「できますか」更加书面正式，常用于服务业询问某项业务是否支持。"],
                    ["2. 取款与存款专有名词：", "「お引き出し（取款）」、「お預け入れ（存款）」、「残高照会（查余额）」。"],
                    ["3. 7-Eleven ATM优势：", "插卡后屏幕左上角可直接切换「简体中文」，单笔最高可取10万日元。"],
                    ["4. 找零收据提醒：", "「レシートをお受け取りください（请收好您的小票）」。"]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "接下来拆解在便利店ATM机使用海外卡取现金的实用句型。"},
                    {"speaker": "ja", "text": "ATM", "card_idx": 0},
                    {"speaker": "explainer", "text": "名词读作 eetiiemu，自动取款机。", "card_idx": 0},
                    {"speaker": "ja", "text": "海外カード", "card_idx": 1},
                    {"speaker": "explainer", "text": "名词：海外发行的银联或信用卡。", "card_idx": 1},
                    {"speaker": "ja", "text": "引き出し", "card_idx": 2},
                    {"speaker": "explainer", "text": "名词：取款、提现。", "card_idx": 2},
                    {"speaker": "ja", "text": "可能", "card_idx": 3},
                    {"speaker": "explainer", "text": "名词：可行、能够支持。", "card_idx": 3},
                    {"speaker": "ja", "text": "ですか", "card_idx": 4},
                    {"speaker": "explainer", "text": "礼貌疑问句尾助词。", "card_idx": 4},
                    {"speaker": "explainer", "text": "语法精讲：询问某项金融业务是否支持的高级句型。", "is_spotlight": True},
                    {"speaker": "ja", "text": "海外カードの引き出しは可能ですか？", "is_spotlight": True},
                    {"speaker": "explainer", "text": "意思是支持海外卡取现吗，问店员或客服时非常地道。", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "05. 小票与找零确认",
                "spoken_text": "レシートをお受け取りください。ありがとうございました！",
                "meaning": "请收好您的小票收据。非常感谢！",
                "tip": "购物小票上有退税明细或促销条码，店员一定会双手递上并说这句道谢。",
                "tokens": [
                    {"orig": "レシートを", "kana": "れしーとを", "romaji": "reshiito o", "pos": "外来语+宾格", "meaning": "小票收据"},
                    {"orig": "お受け取り", "kana": "おうけとり", "romaji": "ouketori", "pos": "敬语连用形", "meaning": "收取"},
                    {"orig": "ください。", "kana": "ください", "romaji": "kudasai.", "pos": "祈使短语", "meaning": "请……"},
                    {"orig": "ありがとう", "kana": "ありがとう", "romaji": "arigatou", "pos": "寒暄语", "meaning": "感谢"},
                    {"orig": "ございました！", "kana": "ございました", "romaji": "gozaimashita!", "pos": "敬语过去式", "meaning": "非常感谢"}
                ]
            },
            {
                "type": "outro",
                "chapter": "06. 关注与练习",
                "spoken_text": "关注 TokyoFlow 日语，欢迎下载 App 一起跟读练习！"
            }
        ]
    },

    # -------------------------------------------------------------------------
    # EP.07: 拉面食券机与定制
    # -------------------------------------------------------------------------
    {
        "episode_number": 7,
        "folder_name": "E07-Ramen_Ticket_Vending-v1.0-zh",
        "slug": "ramen_ticket_vending_zh",
        "locale": "zh",
        "title": "东京一兰拉面食券机与面硬汤浓定制黑话",
        "yt_title": "【JLPT N5】像老饕一样吃拉面！食券机点餐与面硬汤浓定制精讲（EP.07）",
        "category": "拉面美食 • 食券与定制",
        "level": "JLPT N5",
        "district": "池袋 (Ikebukuro)",
        "bg_image": "tmp/videogen/real_photos/ep07_ichiran_shinjuku.jpg",
        "cover": {
            "hook": "拉面点单黑话",
            "sub_hook": "面硬汤浓加份面",
            "jp_line1": "麺硬め・味濃いめ、",
            "jp_line2": "替え玉をお願いします！",
            "grammar_tag": "JLPT N5 语法：~め（程度偏向）& 替え玉（加面）",
            "translation": "「面条偏硬、汤底偏浓，再加一份面！」",
            "context_note": "东京博多豚骨与家系拉面店最核心的定制点单口诀",
            "location_tag": "场景：池袋正宗豚骨拉面街 • 吧台前",
            "tag": "🇯🇵 拉面老饕必备 • 影子跟读"
        },
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. 食券机先购票提示",
                "spoken_text": "食券を先にお買い求めください。",
                "meaning": "请先在自动食券机上购买餐券。",
                "tip": "日本拉面店多采用先买票后入座机制，进门先看「券売機（けんばいき）」。",
                "tokens": [
                    {"orig": "食券を", "kana": "しょっけんを", "romaji": "shokken o", "pos": "名词+宾格", "meaning": "餐券/食券"},
                    {"orig": "先に", "kana": "さきに", "romaji": "saki ni", "pos": "副词", "meaning": "先/预先"},
                    {"orig": "お買い求め", "kana": "おかいもとめ", "romaji": "okaimotome", "pos": "敬语连用形", "meaning": "购买"},
                    {"orig": "ください。", "kana": "ください", "romaji": "kudasai.", "pos": "礼貌祈使", "meaning": "请……"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. 拉面店食券购买词汇拆解",
                "sentence_ja": "食券を先にお買い求めください。",
                "vocab": [
                    {"orig": "食券", "kana": "しょっけん", "romaji": "shokken", "pos": "名词", "meaning": "点餐食券"},
                    {"orig": "先に", "kana": "さきに", "romaji": "saki ni", "pos": "副词", "meaning": "首先/预先"},
                    {"orig": "お買い求め", "kana": "おかいもとめ", "romaji": "okaimotome", "pos": "敬语词干", "meaning": "选购/购买"},
                    {"orig": "ください", "kana": "ください", "romaji": "kudasai", "pos": "短语", "meaning": "请……"}
                ],
                "grammar_title": "敬语公式：お + 动词连用形 + ください",
                "grammar_bullets": [
                    ["1. 敬语动词：", "「お買い求め（おかいもとめ）」是「買う（购买）」的典雅敬语形式。"],
                    ["2. 食券机使用动线：", "投入现金/刷IC卡 -> 按下按钮选择拉面与配菜 -> 取出食券与找零。"],
                    ["3. 常见加料按钮：", "「味玉（あじたま，溏心蛋）」、「チャーシュー（叉烧）」、「ネギ（葱花）」。"],
                    ["4. 递券时机：", "入座后将食券放在吧台上方，店员收券时会询问口味定制细节。"]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "我们来拆解日本拉面店进门第一句听到的购票指引。"},
                    {"speaker": "ja", "text": "食券", "card_idx": 0},
                    {"speaker": "explainer", "text": "名词：点餐券、食券。", "card_idx": 0},
                    {"speaker": "ja", "text": "先に", "card_idx": 1},
                    {"speaker": "explainer", "text": "副词：首先、预先。", "card_idx": 1},
                    {"speaker": "ja", "text": "お買い求め", "card_idx": 2},
                    {"speaker": "explainer", "text": "动词買う的高级敬语连用形：选购。", "card_idx": 2},
                    {"speaker": "ja", "text": "ください", "card_idx": 3},
                    {"speaker": "explainer", "text": "请……礼貌祈使表达。", "card_idx": 3},
                    {"speaker": "explainer", "text": "语法精讲：服务人员礼貌引导顾客购买的经典句型。", "is_spotlight": True},
                    {"speaker": "ja", "text": "食券を先にお買い求めください。", "is_spotlight": True},
                    {"speaker": "explainer", "text": "意思是请先购买餐券，排队进店时店员常会引导。", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "03. 面条硬度与加面老饕定制",
                "spoken_text": "麺硬め、味濃いめで、替え玉をお願いします！",
                "meaning": "面条偏硬，汤底偏浓，再加一份面！",
                "tip": "形容词词干后加「め」表示程度偏向（硬め、柔らかめ、多め、少なめ）。",
                "tokens": [
                    {"orig": "麺", "kana": "めん", "romaji": "men", "pos": "名词", "meaning": "面条"},
                    {"orig": "硬め、", "kana": "かため", "romaji": "katame,", "pos": "程度接尾", "meaning": "偏硬"},
                    {"orig": "味", "kana": "あじ", "romaji": "aji", "pos": "名词", "meaning": "味道/汤底"},
                    {"orig": "濃いめで、", "kana": "こいめで", "romaji": "koime de,", "pos": "程度接尾+助词", "meaning": "偏浓"},
                    {"orig": "替え玉を", "kana": "かえだまを", "romaji": "kaedama o", "pos": "名词+宾格", "meaning": "加面/续面"},
                    {"orig": "お願いします！", "kana": "おねがいします", "romaji": "onegaishimasu!", "pos": "短语", "meaning": "拜托了"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "04. 口味倾向与加面黑话拆解",
                "sentence_ja": "麺硬め、味濃いめで、替え玉をお願いします！",
                "vocab": [
                    {"orig": "麺", "kana": "めん", "romaji": "men", "pos": "名词", "meaning": "拉面面条"},
                    {"orig": "硬め", "kana": "かため", "romaji": "katame", "pos": "程度接尾", "meaning": "偏硬/有嚼劲"},
                    {"orig": "濃いめ", "kana": "こいめ", "romaji": "koime", "pos": "程度接尾", "meaning": "汤底偏浓"},
                    {"orig": "替え玉", "kana": "かえだま", "romaji": "kaedama", "pos": "名词", "meaning": "续面/加一份面"},
                    {"orig": "お願いします", "kana": "おねがいします", "romaji": "onegaishimasu", "pos": "短语", "meaning": "请/拜托"}
                ],
                "grammar_title": "程度接尾词：形容词词干 + め（表示倾向）",
                "grammar_bullets": [
                    ["1. 程度倾向公式：", "形容词去掉い + め（硬め = 偏硬，柔らかめ = 偏软，多め = 偏多，少なめ = 偏少）。"],
                    ["2. 替え玉（かえだま）文化：", "博多豚骨拉面保留汤底，向店员加点一份刚煮好的细面（通常100~150日元）。"],
                    ["3. 加面时机技巧：", "第一碗面吃到还剩三分之一且汤底充足时喊「替え玉」，即可无缝衔接。"],
                    ["4. 油量定制词汇：", "「油多め（多油，脂香浓郁）」、「油少なめ（少油，清爽可口）」。"]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "接下来拆解拉面店最受老饕推崇的个性化口味定制口诀。"},
                    {"speaker": "ja", "text": "麺", "card_idx": 0},
                    {"speaker": "explainer", "text": "名词：面条。", "card_idx": 0},
                    {"speaker": "ja", "text": "硬め", "card_idx": 1},
                    {"speaker": "explainer", "text": "形容词词干加接尾词：面条煮得偏硬、有嚼劲。", "card_idx": 1},
                    {"speaker": "ja", "text": "濃いめ", "card_idx": 2},
                    {"speaker": "explainer", "text": "汤底味道偏浓厚。", "card_idx": 2},
                    {"speaker": "ja", "text": "替え玉", "card_idx": 3},
                    {"speaker": "explainer", "text": "专有名词：保留汤底额外加一份面条。", "card_idx": 3},
                    {"speaker": "ja", "text": "お願いします", "card_idx": 4},
                    {"speaker": "explainer", "text": "拜托了、麻烦您。", "card_idx": 4},
                    {"speaker": "explainer", "text": "语法精讲：形容词加め表示程度偏向的实用法则。", "is_spotlight": True},
                    {"speaker": "ja", "text": "麺硬めで、替え玉をお願いします！", "is_spotlight": True},
                    {"speaker": "explainer", "text": "意思是面煮硬一点再加一份面，拉面店地道点单金句。", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "05. 清汤冲淡实战问询",
                "spoken_text": "スープを割りスープで薄めてもらえますか？",
                "meaning": "可以帮我加点清汤把汤底冲淡一点吗？",
                "tip": "吃沾面（つけ麺）吃完后，让店员加「スープ割り（清汤）」可以喝到鲜美高汤。",
                "tokens": [
                    {"orig": "スープを", "kana": "すーぷを", "romaji": "suupu o", "pos": "外来语+宾格", "meaning": "汤底"},
                    {"orig": "割りスープで", "kana": "わりすーぷで", "romaji": "wari-suupu de", "pos": "名词+手段", "meaning": "用稀释高汤"},
                    {"orig": "薄めて", "kana": "うすめて", "romaji": "usumete", "pos": "动词て形", "meaning": "冲淡/稀释"},
                    {"orig": "もらえますか？", "kana": "もらえますか", "romaji": "moraemasu ka?", "pos": "可能请求", "meaning": "能帮我……吗？"}
                ]
            },
            {
                "type": "outro",
                "chapter": "06. 关注与练习",
                "spoken_text": "关注 TokyoFlow 日语，欢迎下载 App 一起跟读练习！"
            }
        ]
    },

    # -------------------------------------------------------------------------
    # EP.08: 银座精品店试衣与免税
    # -------------------------------------------------------------------------
    {
        "episode_number": 8,
        "folder_name": "E08-Ginza_TaxFree_Shopping-v1.0-zh",
        "slug": "ginza_taxfree_shopping_zh",
        "locale": "zh",
        "title": "银座旗舰店优雅试衣与免税退税流程",
        "yt_title": "【JLPT N5】银座购物优雅试衣！试穿与询问尺码精品店日语精讲（EP.08）",
        "category": "银座购物 • 试衣与免税",
        "level": "JLPT N5",
        "district": "银座 (Ginza)",
        "bg_image": "tmp/videogen/real_photos/ep08_ginza_uniqlo.jpg",
        "cover": {
            "hook": "银座购物试衣",
            "sub_hook": "优雅试穿询问句式",
            "jp_line1": "この服を、",
            "jp_line2": "試着してもいいですか？",
            "grammar_tag": "JLPT N5 语法：~てもいいですか（请求许可：可以……吗）",
            "translation": "「我可以试穿一下这件衣服吗？」",
            "context_note": "银座精品店、优衣库旗舰店试衣间前最优雅的标准口语",
            "location_tag": "场景：银座旗舰百货 • 服饰精品专柜",
            "tag": "🇯🇵 银座购物实景 • 影子跟读"
        },
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. 试衣间试穿礼貌请求",
                "spoken_text": "この服を、試着してもいいですか？",
                "meaning": "我可以试穿一下这件衣服吗？",
                "tip": "日本服装店试衣前必须先向店员打招呼，女性试穿套头衣物需佩戴面罩（フェイスカバー）。",
                "tokens": [
                    {"orig": "この", "kana": "この", "romaji": "kono", "pos": "连体词", "meaning": "这个/这件"},
                    {"orig": "服を、", "kana": "ふくを", "romaji": "fuku o,", "pos": "名词+宾格", "meaning": "衣服"},
                    {"orig": "試着して", "kana": "しちゃくして", "romaji": "shichaku shite", "pos": "动词て形", "meaning": "试穿"},
                    {"orig": "もいいですか？", "kana": "もいいですか", "romaji": "mo ii desu ka?", "pos": "许可句型", "meaning": "可以吗？"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. 试穿请求语法与礼仪拆解",
                "sentence_ja": "この服を、試着してもいいですか？",
                "vocab": [
                    {"orig": "この", "kana": "この", "romaji": "kono", "pos": "连体词", "meaning": "这/这件"},
                    {"orig": "服", "kana": "ふく", "romaji": "fuku", "pos": "名词", "meaning": "服装/衣服"},
                    {"orig": "試着", "kana": "しちゃく", "romaji": "shichaku", "pos": "名词/动词", "meaning": "试穿衣服"},
                    {"orig": "して", "kana": "して", "romaji": "shite", "pos": "助动词", "meaning": "做（接续形式）"},
                    {"orig": "もいいですか", "kana": "もいいですか", "romaji": "mo ii desu ka", "pos": "许可句型", "meaning": "可以……吗"}
                ],
                "grammar_title": "请求许可公式：动词て形 + もいいですか",
                "grammar_bullets": [
                    ["1. 语法功能：", "用于向对方征求许可，“我可以做某事吗？”语气客气温和。"],
                    ["2. 试衣间礼仪：", "进入试衣间（試着室，しちゃくしつ）前，店员会询问件数并递上号码牌。"],
                    ["3. 脱鞋规定：", "日本试衣间地面铺有地毯，进入前务必在踏垫前脱鞋。"],
                    ["4. 店员热情回应：", "「どうぞ、試着室へご案内いたします（请，我带您去试衣间）」。"]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "我们来拆解在银座各大服饰百货试穿衣服的标准礼貌句型。"},
                    {"speaker": "ja", "text": "この", "card_idx": 0},
                    {"speaker": "explainer", "text": "指示代词：这件。", "card_idx": 0},
                    {"speaker": "ja", "text": "服", "card_idx": 1},
                    {"speaker": "explainer", "text": "名词读作 fuku，衣服服装。", "card_idx": 1},
                    {"speaker": "ja", "text": "試着", "card_idx": 2},
                    {"speaker": "explainer", "text": "名词读作 shichaku，试穿。", "card_idx": 2},
                    {"speaker": "ja", "text": "して", "card_idx": 3},
                    {"speaker": "explainer", "text": "动词做（する）的接续て形。", "card_idx": 3},
                    {"speaker": "ja", "text": "もいいですか", "card_idx": 4},
                    {"speaker": "explainer", "text": "请求许可短语：可以吗？", "card_idx": 4},
                    {"speaker": "explainer", "text": "语法精讲：征求对方许可的标准句型。", "is_spotlight": True},
                    {"speaker": "ja", "text": "試着してもいいですか？", "is_spotlight": True},
                    {"speaker": "explainer", "text": "意思是我可以试穿一下吗，挑好衣服向店员示意时必说。", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "03. 尺码与颜色差异问询",
                "spoken_text": "サイズ違いや色違いはありますか？Sサイズをお願いします。",
                "meaning": "有其他尺码或者其他颜色吗？麻烦给我拿一件S码。",
                "tip": "在日语中，后缀「〜違い（ちがい）」常用来表达“其他不同种类”。",
                "tokens": [
                    {"orig": "サイズ違いや", "kana": "さいずちがいや", "romaji": "saizu-chigai ya", "pos": "名词+连词", "meaning": "其他尺码或"},
                    {"orig": "色違いは", "kana": "いろちがいは", "romaji": "iro-chigai wa", "pos": "名词+提示", "meaning": "其他颜色"},
                    {"orig": "ありますか？", "kana": "ありますか", "romaji": "arimasu ka?", "pos": "存在动词", "meaning": "有吗？"},
                    {"orig": "Sサイズを", "kana": "えすさいずを", "romaji": "esu-saizu o", "pos": "名词+宾格", "meaning": "S号尺码"},
                    {"orig": "お願いします。", "kana": "おねがいします", "romaji": "onegaishimasu.", "pos": "礼貌短语", "meaning": "麻烦了"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "04. 服饰尺寸与款式词汇拆解",
                "sentence_ja": "サイズ違いや色違いはありますか？Sサイズをお願いします。",
                "vocab": [
                    {"orig": "サイズ違い", "kana": "さいずちがい", "romaji": "saizu chigai", "pos": "名词", "meaning": "不同尺码"},
                    {"orig": "色違い", "kana": "いろちがい", "romaji": "iro chigai", "pos": "名词", "meaning": "不同颜色"},
                    {"orig": "ありますか", "kana": "ありますか", "romaji": "arimasu ka", "pos": "存在动词", "meaning": "有存货吗"},
                    {"orig": "Sサイズ", "kana": "えすさいず", "romaji": "esu saizu", "pos": "外来语", "meaning": "小码 S Size"},
                    {"orig": "お願いします", "kana": "おねがいします", "romaji": "onegaishimasu", "pos": "短语", "meaning": "请拿给我"}
                ],
                "grammar_title": "词汇构成：名词 + 違い（表示不同款式）",
                "grammar_bullets": [
                    ["1. 构词法：", "「サイズ違い（尺码不同）」、「色違い（颜色不同）」、「柄違い（花纹图案不同）」."],
                    ["2. 尺码表达：", "Sサイズ（小码）、Mサイズ（中码）、Lサイズ（大码）、フリーサイズ（均码）."],
                    ["3. 试穿后觉得不合身：", "「少し小さいです / 少し大きいです（稍微有点小 / 稍微有点大）」."],
                    ["4. 决定购买：", "「これにします / これをいただきます（我就要这件了）」."]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "接下来拆解试穿后询问其他尺码与颜色的地道表达。"},
                    {"speaker": "ja", "text": "サイズ違い", "card_idx": 0},
                    {"speaker": "explainer", "text": "名词：其他尺码、不同号码。", "card_idx": 0},
                    {"speaker": "ja", "text": "色違い", "card_idx": 1},
                    {"speaker": "explainer", "text": "名词：其他颜色配色。", "card_idx": 1},
                    {"speaker": "ja", "text": "ありますか", "card_idx": 2},
                    {"speaker": "explainer", "text": "存在动词疑问：有吗？", "card_idx": 2},
                    {"speaker": "ja", "text": "Sサイズ", "card_idx": 3},
                    {"speaker": "explainer", "text": "名词读作 esu-saizu，小号尺码。", "card_idx": 3},
                    {"speaker": "ja", "text": "お願いします", "card_idx": 4},
                    {"speaker": "explainer", "text": "拜托了、麻烦拿给我。", "card_idx": 4},
                    {"speaker": "explainer", "text": "语法精讲：名词加違い表达其他不同款式的构词法。", "is_spotlight": True},
                    {"speaker": "ja", "text": "サイズ違いはありますか？", "is_spotlight": True},
                    {"speaker": "explainer", "text": "意思是请问有别的尺码吗，试衣服时极其高频实用。", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "05. 免税柜台引导问询",
                "spoken_text": "免税専用カウンターへご案内いたします。こちらへどうぞ。",
                "meaning": "我带您前往免税专用柜台。请往这边走。",
                "tip": "在大型百货（如三越、高岛屋），通常需在专门的免税退税楼层统一办理。",
                "tokens": [
                    {"orig": "免税専用", "kana": "めんぜいせんよう", "romaji": "menzei senyou", "pos": "名词", "meaning": "免税专用"},
                    {"orig": "カウンターへ", "kana": "かうんたーへ", "romaji": "kauntaa e", "pos": "名词+方向", "meaning": "前往柜台"},
                    {"orig": "ご案内", "kana": "ごあんない", "romaji": "goannai", "pos": "敬语名词", "meaning": "引导/带路"},
                    {"orig": "いたします。", "kana": "いたします", "romaji": "itashimasu.", "pos": "谦让语", "meaning": "我为您做"},
                    {"orig": "こちらへどうぞ。", "kana": "こちらへどうぞ", "romaji": "kochira e douzo.", "pos": "礼貌短语", "meaning": "请往这边"}
                ]
            },
            {
                "type": "outro",
                "chapter": "06. 关注与练习",
                "spoken_text": "关注 TokyoFlow 日语，欢迎下载 App 一起跟读练习！"
            }
        ]
    },

    # -------------------------------------------------------------------------
    # EP.09: 动漫公司开设芬兰桑拿热点
    # -------------------------------------------------------------------------
    {
        "episode_number": 9,
        "folder_name": "E09-anime_sauna_trend-v1.0-zh",
        "slug": "anime_sauna_trend_zh",
        "locale": "zh",
        "title": "东京动漫公司跨界开设正宗芬兰桑拿热点",
        "yt_title": "【JLPT N5】动漫公司去开桑拿？身心彻底放松「整う」流行语精讲（EP.09）",
        "category": "东京热点 • 桑拿流行语",
        "level": "JLPT N5",
        "district": "秋叶原 (Akihabara)",
        "bg_image": "/Users/kilvonwu/.gemini/antigravity/brain/b34d491c-7bb1-4e81-ab7c-51e66a95dc10/ep09_female_sauna_16_9_1791040719951.jpg",
        "cover": {
            "hook": "动漫公司开桑拿",
            "sub_hook": "身心放松流行语",
            "jp_line1": "本格的なサウナで、",
            "jp_line2": "心身がととのう！",
            "grammar_tag": "JLPT N5 语法：~で（动作场所）& ととのう（桑拿流行语）",
            "translation": "「在正宗桑拿里，身心彻底放松舒畅！」",
            "context_note": "日本全网爆火的桑拿文化流行语与跨界新业态",
            "location_tag": "场景：秋叶原动漫街 • 芬兰桑拿馆",
            "tag": "🇯🇵 东京流行热点 • 影子跟读"
        },
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. 动漫公司跨界新闻速报",
                "spoken_text": "アニメ制作会社が東京で本格的なサウナをオープンしました。",
                "meaning": "动画制作公司在东京开设了一家地道的芬兰桑拿馆。",
                "tip": "「本格的（ほんかくてき）」表示正宗、专业、地道的品质。",
                "tokens": [
                    {"orig": "アニメ制作会社が", "kana": "あにめせいさくがいしゃが", "romaji": "anime seisakugaisha ga", "pos": "名词+主格", "meaning": "动画制作公司"},
                    {"orig": "東京で", "kana": "とうきょうで", "romaji": "toukyou de", "pos": "名词+场所", "meaning": "在东京"},
                    {"orig": "本格的な", "kana": "ほんかくてきな", "romaji": "honkakuteki na", "pos": "形容动词", "meaning": "地道正宗的"},
                    {"orig": "サウナを", "kana": "さうなを", "romaji": "sauna o", "pos": "外来语+宾格", "meaning": "桑拿馆"},
                    {"orig": "オープンしました。", "kana": "おーぷんしました", "romaji": "oopun shimashita.", "pos": "动词过去式", "meaning": "开业了"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. 新闻热点词汇与语法拆解",
                "sentence_ja": "アニメ制作会社が東京で本格的なサウナをオープンしました。",
                "vocab": [
                    {"orig": "アニメ", "kana": "あにめ", "romaji": "anime", "pos": "名词", "meaning": "日本动画"},
                    {"orig": "制作会社", "kana": "せいさくがいしゃ", "romaji": "seisakugaisha", "pos": "名词", "meaning": "制作出品公司"},
                    {"orig": "本格的", "kana": "ほんかくてき", "romaji": "honkakuteki", "pos": "形容动词", "meaning": "正宗地道"},
                    {"orig": "サウナ", "kana": "さうな", "romaji": "sauna", "pos": "外来语", "meaning": "芬兰桑拿浴"},
                    {"orig": "オープン", "kana": "おーぷん", "romaji": "oopun", "pos": "动词", "meaning": "开业/新开张"}
                ],
                "grammar_title": "场所助词：名词（场所）+ で（表示动作发生地）",
                "grammar_bullets": [
                    ["1. 场所助词 で 功能：", "表示某项动态活动或事件发生的地点（如「東京で開く」在东京举办）。"],
                    ["2. 本格的（ほんかくてき）：", "日本社会极受青睐的品质形容词，形容不偷工减料、遵循原产地正统标准。"],
                    ["3. 动漫跨界趋势：", "秋叶原动漫制作工作室将二次元原画展示与芬兰木屋桑拿结合，打造新式体验空间。"],
                    ["4. 开业动词：", "「オープンする（新店开业）」、「リニューアル（翻新升级）」."]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "我们来拆解这条在东京社交网络引发热烈讨论的跨界新闻。"},
                    {"speaker": "ja", "text": "アニメ", "card_idx": 0},
                    {"speaker": "explainer", "text": "名词：日本动画、Anime。", "card_idx": 0},
                    {"speaker": "ja", "text": "制作会社", "card_idx": 1},
                    {"speaker": "explainer", "text": "名词：制作出品公司。", "card_idx": 1},
                    {"speaker": "ja", "text": "本格的", "card_idx": 2},
                    {"speaker": "explainer", "text": "形容动词：正宗地道、原汁原味。", "card_idx": 2},
                    {"speaker": "ja", "text": "サウナ", "card_idx": 3},
                    {"speaker": "explainer", "text": "外来语：芬兰桑拿浴。", "card_idx": 3},
                    {"speaker": "ja", "text": "オープン", "card_idx": 4},
                    {"speaker": "explainer", "text": "开张开业、Open。", "card_idx": 4},
                    {"speaker": "explainer", "text": "语法精讲：表示在某地开展新业务的场所助词用法。", "is_spotlight": True},
                    {"speaker": "ja", "text": "本格的なサウナをオープンしました。", "is_spotlight": True},
                    {"speaker": "explainer", "text": "意思是开设了地道的正宗桑拿馆，新闻标题标准句式。", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "03. 桑拿流行语「整う」深度解析",
                "spoken_text": "ととのうという言葉は、心身がリフレッシュすることを意味します。",
                "meaning": "所谓的「totonou」是指身心得到彻底放松舒畅的状态。",
                "tip": "「ととのう（整う）」是日本全网爆火的桑拿热词，形容冷热水交替后的大脑极度放空。",
                "tokens": [
                    {"orig": "ととのうという", "kana": "ととのうという", "romaji": "totonou to iu", "pos": "引用表达", "meaning": "所谓的totonou"},
                    {"orig": "言葉は、", "kana": "ことばは", "romaji": "kotoba wa,", "pos": "名词+提示", "meaning": "这个词汇"},
                    {"orig": "心身が", "kana": "しんしんが", "romaji": "shinshin ga", "pos": "名词+主格", "meaning": "身心"},
                    {"orig": "リフレッシュする", "kana": "りふれっしゅする", "romaji": "rifuresshu suru", "pos": "动词", "meaning": "彻底放松刷新"},
                    {"orig": "ことを意味します。", "kana": "ことをいみします", "romaji": "koto o imi shimasu.", "pos": "短语", "meaning": "意味着……"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "04. 桑拿流行文化与心理状态剖析",
                "sentence_ja": "ととのうという言葉は、心身がリフレッシュすることを意味します。",
                "vocab": [
                    {"orig": "ととのう", "kana": "ととのう", "romaji": "totonou", "pos": "动词", "meaning": "身心协调舒畅"},
                    {"orig": "言葉", "kana": "ことば", "romaji": "kotoba", "pos": "名词", "meaning": "词汇/语言"},
                    {"orig": "心身", "kana": "しんしん", "romaji": "shinshin", "pos": "名词", "meaning": "身体与心灵"},
                    {"orig": "リフレッシュ", "kana": "りふれっしゅ", "romaji": "rifuresshu", "pos": "动词", "meaning": "恢复活力Refresh"},
                    {"orig": "意味します", "kana": "いみします", "romaji": "imi shimasu", "pos": "动词", "meaning": "意思是/意味着"}
                ],
                "grammar_title": "定义句型：名词 + という言葉は、〜を意味します",
                "grammar_bullets": [
                    ["1. 术语定义公式：", "「A という言葉は B を意味します（所谓 A 这个词，意味着 B）」."],
                    ["2. 「整う（ととのう）」的生理机理：", "桑拿高温蒸发 -> 冷水浴收缩血管 -> 外气浴静坐，产生深度内啡肽分泌."],
                    ["3. 日本年轻人社交文化：", "下班后结伴去「サ活（桑拿活动）」，成为东京都市白领最流行的解压方式."],
                    ["4. 桑拿爱好者专有名词：", "热爱桑拿的人被称为「サウナー（Saunist）」."]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "接下来拆解日本近年来最火热的流行语「整う」的文化背景。"},
                    {"speaker": "ja", "text": "ととのう", "card_idx": 0},
                    {"speaker": "explainer", "text": "动词：身心恢复平衡舒畅。", "card_idx": 0},
                    {"speaker": "ja", "text": "言葉", "card_idx": 1},
                    {"speaker": "explainer", "text": "名词：词语、流行用语。", "card_idx": 1},
                    {"speaker": "ja", "text": "心身", "card_idx": 2},
                    {"speaker": "explainer", "text": "名词读作 shinshin，身心两方面。", "card_idx": 2},
                    {"speaker": "ja", "text": "リフレッシュ", "card_idx": 3},
                    {"speaker": "explainer", "text": "外来语动词：恢复活力、极度放松。", "card_idx": 3},
                    {"speaker": "ja", "text": "意味します", "card_idx": 4},
                    {"speaker": "explainer", "text": "动词：意味着、代表着。", "card_idx": 4},
                    {"speaker": "explainer", "text": "语法精讲：定义某项新兴概念或流行语的标准句式。", "is_spotlight": True},
                    {"speaker": "ja", "text": "心身がリフレッシュすることを意味します。", "is_spotlight": True},
                    {"speaker": "explainer", "text": "意思是代表身心彻底焕然一新，桑拿文化核心关键词。", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "05. 预约制与官网确认",
                "spoken_text": "完全予約制なので、事前に公式サイトで確認してください。",
                "meaning": "因为是完全预约制，请提前在官方网站确认。",
                "tip": "日本高档桑拿通常需提前线上预约，避免现场满员扑空。",
                "tokens": [
                    {"orig": "完全予約制", "kana": "かんぜんよやくせい", "romaji": "kanzen yoyakusei", "pos": "名词", "meaning": "完全预约制"},
                    {"orig": "なので、", "kana": "なので", "romaji": "na no de,", "pos": "原因助词", "meaning": "因为……所以"},
                    {"orig": "事前に", "kana": "じぜんに", "romaji": "jizen ni", "pos": "副词", "meaning": "提前/事先"},
                    {"orig": "公式サイトで", "kana": "こうしきさいとで", "romaji": "koushiki saito de", "pos": "名词+手段", "meaning": "在官方网站"},
                    {"orig": "確認してください。", "kana": "かくにんしてください", "romaji": "kakunin shite kudasai.", "pos": "祈使短语", "meaning": "请确认"}
                ]
            },
            {
                "type": "outro",
                "chapter": "06. 关注与练习",
                "spoken_text": "关注 TokyoFlow 日语，欢迎下载 App 一起跟读练习！"
            }
        ]
    },

    # -------------------------------------------------------------------------
    # EP.10: 绫濑遥天然呆魅力热点
    # -------------------------------------------------------------------------
    {
        "episode_number": 10,
        "folder_name": "E10-ayase_haruka_tennen-v1.0-zh",
        "slug": "ayase_haruka_tennen_zh",
        "locale": "zh",
        "title": "国民女神绫濑遥天然呆反差萌魅力精讲",
        "yt_title": "【JLPT N5】绫濑遥天然呆发言引全场爆笑！日综反差萌流行语精讲（EP.10）",
        "category": "东京娱乐 • 明星流行语",
        "level": "JLPT N5",
        "district": "东京流行文化",
        "bg_image": "docs/youtube_releases/E10-ayase_haruka_tennen-v1.0/thumbnail.jpg",
        "cover": {
            "hook": "绫濑遥天然呆发言",
            "sub_hook": "反差萌国民女神",
            "jp_line1": "綾瀬はるかが会場で、",
            "jp_line2": "天然発言をしました！",
            "grammar_tag": "JLPT N5 语法：~で（动作场所）& 天然（天真纯粹萌点）",
            "translation": "「绫濑遥在现场发表了可爱的天然呆发言！」",
            "context_note": "日本演艺圈最受喜爱的国民级性格标签「天然（てんねん）」",
            "location_tag": "场景：东京电影首映会发布会现场",
            "tag": "🇯🇵 日本演艺圈娱乐精讲 • 影子跟读"
        },
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. 发布会天然呆爆笑现场",
                "spoken_text": "綾瀬はるかが会場で天然発言をして、みんなを笑わせました。",
                "meaning": "绫濑遥在会场发表了可爱的天然呆发言，逗笑了全场观众。",
                "tip": "「天然（てんねん）」在日语流行文化中专指单纯率真、不按常理出牌的可爱性格。",
                "tokens": [
                    {"orig": "綾瀬はるかが", "kana": "あやせはるかが", "romaji": "ayase haruka ga", "pos": "专有名词+主格", "meaning": "绫濑遥"},
                    {"orig": "会場で", "kana": "かいじょうで", "romaji": "kaijou de", "pos": "名词+场所", "meaning": "在会场"},
                    {"orig": "天然発言を", "kana": "てんねんはつげんを", "romaji": "tennen hatsugen o", "pos": "名词+宾格", "meaning": "天然呆发言"},
                    {"orig": "して、", "kana": "して", "romaji": "shite,", "pos": "动词て形", "meaning": "发表了"},
                    {"orig": "みんなを", "kana": "みんなを", "romaji": "minna o", "pos": "代词+宾格", "meaning": "全场大家"},
                    {"orig": "笑わせました。", "kana": "わらわせました", "romaji": "warawasemashita.", "pos": "使役态动词", "meaning": "逗笑了"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. 娱乐新闻与使役态语法拆解",
                "sentence_ja": "綾瀬はるかが会場で天然発言をして、みんなを笑わせました。",
                "vocab": [
                    {"orig": "綾瀬はるか", "kana": "あやせはるか", "romaji": "ayase haruka", "pos": "专有名词", "meaning": "国民女演员绫濑遥"},
                    {"orig": "会場", "kana": "かいじょう", "romaji": "kaijou", "pos": "名词", "meaning": "活动会场"},
                    {"orig": "天然発言", "kana": "てんねんはつげん", "romaji": "tennen hatsugen", "pos": "名词", "meaning": "天然呆出格言论"},
                    {"orig": "みんな", "kana": "みんな", "romaji": "minna", "pos": "名词", "meaning": "大家/观众们"},
                    {"orig": "笑わせました", "kana": "わらわせました", "romaji": "warawasemashita", "pos": "使役态", "meaning": "使大家笑起来"}
                ],
                "grammar_title": "使役动词：动词使役态（让……笑起来）",
                "grammar_bullets": [
                    ["1. 使役态构成：", "一类动词词尾改 a 段 + せる（笑う -> 笑わせる，让某人笑起来）."],
                    ["2. 「天然（てんねん）」文化内涵：", "并非贬义，而是指本人毫无造作伪装、自然流露的呆萌魅力，深受观众喜爱."],
                    ["3. 演艺圈反差萌地位：", "绫濑遥演技精湛但在综艺节目中常有脱线发言，多年蝉联“日本最受欢迎女星”榜首."],
                    ["4. 动词连用形接续：", "「〜をして、〜ました」表示连续发生的前后两个动作."]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "我们来拆解日本娱乐节目最常出现的国民级流行词汇「天然」。"},
                    {"speaker": "ja", "text": "綾瀬はるか", "card_idx": 0},
                    {"speaker": "explainer", "text": "专有名词：日本国民级顶流女演员绫濑遥。", "card_idx": 0},
                    {"speaker": "ja", "text": "会場", "card_idx": 1},
                    {"speaker": "explainer", "text": "名词：电影发布会现场、会场。", "card_idx": 1},
                    {"speaker": "ja", "text": "天然発言", "card_idx": 2},
                    {"speaker": "explainer", "text": "流行词汇：天然呆脱线发言。", "card_idx": 2},
                    {"speaker": "ja", "text": "みんな", "card_idx": 3},
                    {"speaker": "explainer", "text": "代词：大家、现场全员。", "card_idx": 3},
                    {"speaker": "ja", "text": "笑わせました", "card_idx": 4},
                    {"speaker": "explainer", "text": "动词使役态：逗得大家开怀大笑。", "card_idx": 4},
                    {"speaker": "explainer", "text": "语法精讲：使役态让某人产生情绪反应的经典句型。", "is_spotlight": True},
                    {"speaker": "ja", "text": "天然発言をして、みんなを笑わせました。", "is_spotlight": True},
                    {"speaker": "explainer", "text": "意思是发表了天然呆言论逗笑全场，日综最高频表达。", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "03. 自然不做作的性格魅力",
                "spoken_text": "自然体なリアクションが、長年愛されている理由です。",
                "meaning": "真实不做作的自然反应，正是她多年来深受大家喜爱的原因。",
                "tip": "「自然体（しぜんたい）」形容为人处世不装腔作势、保持本真的纯粹状态。",
                "tokens": [
                    {"orig": "自然体な", "kana": "しぜんたいな", "romaji": "shizentai na", "pos": "形容动词", "meaning": "自然不做作的"},
                    {"orig": "リアクションが、", "kana": "りあくしょんが", "romaji": "riakushon ga,", "pos": "外来语+主格", "meaning": "临场反应"},
                    {"orig": "長年", "kana": "ながねん", "romaji": "naganen", "pos": "副词/名词", "meaning": "长年以来"},
                    {"orig": "愛されている", "kana": "あいされている", "romaji": "aisarete iru", "pos": "被动态", "meaning": "被大家深爱"},
                    {"orig": "理由です。", "kana": "りゆうです", "romaji": "riyuu desu.", "pos": "断定句", "meaning": "的原因"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "04. 被动态与原因句型深度拆解",
                "sentence_ja": "自然体なリアクションが、長年愛されている理由です。",
                "vocab": [
                    {"orig": "自然体", "kana": "しぜんたい", "romaji": "shizentai", "pos": "名词", "meaning": "自然不做作"},
                    {"orig": "リアクション", "kana": "りあくしょん", "romaji": "riakushon", "pos": "外来语", "meaning": "情绪反应/Reaction"},
                    {"orig": "長年", "kana": "ながねん", "romaji": "naganen", "pos": "名词", "meaning": "长年累月"},
                    {"orig": "愛されている", "kana": "あいされている", "romaji": "aisarete iru", "pos": "被动态", "meaning": "被深爱着"},
                    {"orig": "理由", "kana": "りゆう", "romaji": "riyuu", "pos": "名词", "meaning": "原因/缘由"}
                ],
                "grammar_title": "被动态表达：动词受身形 + ている（持续被……）",
                "grammar_bullets": [
                    ["1. 被动态构成：", "「愛する -> 愛される -> 愛されている（一直深受大众爱戴）」."],
                    ["2. 说明理由句型：", "「小句（修饰语）+ 理由です（这就是……的原因）」."],
                    ["3. リアクション文化：", "日本综艺极其注重嘉宾的「リアクション（受惊、惊喜等即时反应）」."],
                    ["4. 赞美他人性格：", "「裏表がない（为人表里如一，毫无心机）」."]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "接下来拆解表达某位明星为什么深受大众喜爱的说明句式。"},
                    {"speaker": "ja", "text": "自然体", "card_idx": 0},
                    {"speaker": "explainer", "text": "名词：自然纯真、不做作的状态。", "card_idx": 0},
                    {"speaker": "ja", "text": "リアクション", "card_idx": 1},
                    {"speaker": "explainer", "text": "外来语：现场即时反应、Reaction。", "card_idx": 1},
                    {"speaker": "ja", "text": "長年", "card_idx": 2},
                    {"speaker": "explainer", "text": "时间副词：多年以来。", "card_idx": 2},
                    {"speaker": "ja", "text": "愛されている", "card_idx": 3},
                    {"speaker": "explainer", "text": "动词被动态进行时：持续被大家所喜爱。", "card_idx": 3},
                    {"speaker": "ja", "text": "理由", "card_idx": 4},
                    {"speaker": "explainer", "text": "名词：缘由、原因所在。", "card_idx": 4},
                    {"speaker": "explainer", "text": "语法精讲：用被动态修饰名词说明核心原因的句型。", "is_spotlight": True},
                    {"speaker": "ja", "text": "長年愛されている理由です。", "is_spotlight": True},
                    {"speaker": "explainer", "text": "意思是这就是她多年深受喜爱的原因，评论明星标准表达。", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "05. 暖心治愈感悟表达",
                "spoken_text": "思わずほっこりするエピソードですね。癒やされました！",
                "meaning": "真是让人忍不住会心一笑的暖心小故事呢。太治愈了！",
                "tip": "「ほっこりする」和「癒やされる（いやされる）」是日本年轻人表达“被暖到、被治愈”的最高频词。",
                "tokens": [
                    {"orig": "思わず", "kana": "おもわず", "romaji": "omowazu", "pos": "副词", "meaning": "情不自禁地"},
                    {"orig": "ほっこりする", "kana": "ほっこりする", "romaji": "hokkori suru", "pos": "拟态词动词", "meaning": "心里暖洋洋"},
                    {"orig": "エピソードですね。", "kana": "えぴそーどですね", "romaji": "episoodo desu ne.", "pos": "外来语+感叹", "meaning": "小故事呢"},
                    {"orig": "癒やされました！", "kana": "いやされました", "romaji": "iyasaremashita!", "pos": "动词被动态", "meaning": "被治愈了！"}
                ]
            },
            {
                "type": "outro",
                "chapter": "06. 关注与练习",
                "spoken_text": "关注 TokyoFlow 日语，欢迎下载 App 一起跟读练习！"
            }
        ]
    },

    # -------------------------------------------------------------------------
    # EP.11: 涩谷近未来AI机器人短剧热点
    # -------------------------------------------------------------------------
    {
        "episode_number": 11,
        "folder_name": "E11-shabuya-robot-drama-v1.0-zh",
        "slug": "shibuya_robot_drama_zh",
        "locale": "zh",
        "title": "涩谷街头AI机器人短剧爆火与科技流行语",
        "yt_title": "【JLPT N4】涩谷AI机器人短剧爆火！科技科幻与社交网络热点精讲（EP.11）",
        "category": "东京科技 • 影视热点",
        "level": "JLPT N4",
        "district": "涩谷 (Shibuya)",
        "bg_image": "docs/youtube_releases/E11-shabuya-robot-drama-v1.0/thumbnail.jpg",
        "cover": {
            "hook": "涩谷未来科幻短剧",
            "sub_hook": "AI机器人引发热议",
            "jp_line1": "渋谷の街を舞台にした、",
            "jp_line2": "AIロボットドラマが話題！",
            "grammar_tag": "JLPT N4 语法：~を舞台にする（以……为背景舞台）",
            "translation": "「以涩谷街头为舞台的AI机器人短剧引爆热议！」",
            "context_note": "东京涩谷十字路口未来科技短片在社交媒体引发全网疯传",
            "location_tag": "场景：涩谷十字路口 • 未来科技短剧",
            "tag": "🇯🇵 东京科技影视热点 • 影子跟读"
        },
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. 涩谷科幻微剧热点速报",
                "spoken_text": "渋谷の街を舞台にしたAIロボットの短編ドラマが話題になっています。",
                "meaning": "以涩谷街头为舞台的AI机器人短篇微剧正在引发广泛热议。",
                "tip": "「〜を舞台にする」是影视报道高频短语，表示“以某地或某时期为故事背景”。",
                "tokens": [
                    {"orig": "渋谷の街を", "kana": "しぶやのまちを", "romaji": "shibuya no machi o", "pos": "专有名词+宾格", "meaning": "涩谷的街头"},
                    {"orig": "舞台にした", "kana": "ぶたいにした", "romaji": "butai ni shita", "pos": "短语", "meaning": "以……为舞台"},
                    {"orig": "AIロボットの", "kana": "えーあいろぼっとの", "romaji": "eeai robotto no", "pos": "外来语+助词", "meaning": "AI机器人的"},
                    {"orig": "短編ドラマが", "kana": "たんぺんどらまが", "romaji": "tanpen dorama ga", "pos": "名词+主格", "meaning": "短篇电视剧"},
                    {"orig": "話題に", "kana": "わだいに", "romaji": "wadai ni", "pos": "名词+结果", "meaning": "成为热点话题"},
                    {"orig": "なっています。", "kana": "なっています", "romaji": "natte imasu.", "pos": "动词进行时", "meaning": "正在引发关注"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. 影视报道与话题句型拆解",
                "sentence_ja": "渋谷の街を舞台にしたAIロボットの短編ドラマが話題になっています。",
                "vocab": [
                    {"orig": "渋谷の街", "kana": "しぶやのまち", "romaji": "shibuya no machi", "pos": "名词", "meaning": "涩谷街头市景"},
                    {"orig": "舞台", "kana": "ぶたい", "romaji": "butai", "pos": "名词", "meaning": "舞台/故事背景"},
                    {"orig": "AIロボット", "kana": "えーあいろぼっと", "romaji": "eeai robotto", "pos": "外来语", "meaning": "人工智能机器人"},
                    {"orig": "短編ドラマ", "kana": "たんぺんどらま", "romaji": "tanpen dorama", "pos": "名词", "meaning": "短篇微剧"},
                    {"orig": "話題", "kana": "わだい", "romaji": "wadai", "pos": "名词", "meaning": "热门话题/焦点"}
                ],
                "grammar_title": "经典句型：名词 + を舞台にする（以……为背景）",
                "grammar_bullets": [
                    ["1. 句式用法：", "「A を舞台にした B」用来修饰小说、动漫或电影，“以 A 为舞台背景的 B 作品”."],
                    ["2. 「話題になっている」功能：", "表示某件事物在网络、电视或报刊上持续发酵成为当下热门讨论焦点."],
                    ["3. 涩谷科幻地标：", "涩谷十字路口（スクランブル交差点）因赛博朋克霓虹大屏常被选为未来科幻拍摄地."],
                    ["4. 动词变化：", "「話題になる（成为话题）」->「話題になっている（正成为热门热搜）」."]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "我们来拆解这条讲述东京未来科技影视创作的热门报道。"},
                    {"speaker": "ja", "text": "渋谷の街", "card_idx": 0},
                    {"speaker": "explainer", "text": "专有名词：涩谷繁华街区市景。", "card_idx": 0},
                    {"speaker": "ja", "text": "舞台", "card_idx": 1},
                    {"speaker": "explainer", "text": "名词读作 butai，戏剧舞台、故事背景。", "card_idx": 1},
                    {"speaker": "ja", "text": "AIロボット", "card_idx": 2},
                    {"speaker": "explainer", "text": "外来语：人工智能机器人、AI Robot。", "card_idx": 2},
                    {"speaker": "ja", "text": "短編ドラマ", "card_idx": 3},
                    {"speaker": "explainer", "text": "名词：短篇微短剧、短剧集。", "card_idx": 3},
                    {"speaker": "ja", "text": "話題", "card_idx": 4},
                    {"speaker": "explainer", "text": "名词读作 wadai，热门话题、热搜焦点。", "card_idx": 4},
                    {"speaker": "explainer", "text": "语法精讲：以某地为舞台背景并引发全网热议的标准句型。", "is_spotlight": True},
                    {"speaker": "ja", "text": "短編ドラマが話題になっています。", "is_spotlight": True},
                    {"speaker": "explainer", "text": "意思是这部短剧正在引发热烈讨论，媒体报道标准表达。", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "03. 社交网络病毒式传播",
                "spoken_text": "未来の東京を描いた映像が、SNSで急速に拡散されています。",
                "meaning": "描绘未来东京的科幻画面，在社交媒体上正在被迅速传播转发。",
                "tip": "「拡散される（かくさんされる）」专指在 X（原Twitter）等社交平台上被大量转发扩散。",
                "tokens": [
                    {"orig": "未来の", "kana": "みらいの", "romaji": "mirai no", "pos": "名词+助词", "meaning": "未来的"},
                    {"orig": "東京を", "kana": "とうきょうを", "romaji": "toukyou o", "pos": "名词+宾格", "meaning": "东京"},
                    {"orig": "描いた", "kana": "えがいた", "romaji": "egaita", "pos": "动词过去式", "meaning": "描绘展现的"},
                    {"orig": "映像が、", "kana": "えいぞうが", "romaji": "eizou ga,", "pos": "名词+主格", "meaning": "影像画面"},
                    {"orig": "SNSで", "kana": "えすえぬえすで", "romaji": "esuenuesu de", "pos": "名词+手段", "meaning": "在社交网络上"},
                    {"orig": "急速に", "kana": "きゅうそくに", "romaji": "kyuusoku ni", "pos": "副词", "meaning": "迅速飞快地"},
                    {"orig": "拡散されています。", "kana": "かくさんされています", "romaji": "kakusan sarete imasu.", "pos": "被动态进行时", "meaning": "被大量转发传播"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "04. 社交媒体与网络传播词汇拆解",
                "sentence_ja": "未来の東京を描いた映像が、SNSで急速に拡散されています。",
                "vocab": [
                    {"orig": "未来", "kana": "みらい", "romaji": "mirai", "pos": "名词", "meaning": "近未来/科技未来"},
                    {"orig": "描いた", "kana": "えがいた", "romaji": "egaita", "pos": "动词", "meaning": "描绘/刻画"},
                    {"orig": "映像", "kana": "えいぞう", "romaji": "eizou", "pos": "名词", "meaning": "影像/视频画面"},
                    {"orig": "SNS", "kana": "えすえぬえす", "romaji": "esuenuesu", "pos": "名词", "meaning": "社交网络平台"},
                    {"orig": "拡散", "kana": "かくさん", "romaji": "kakusan", "pos": "动词/名词", "meaning": "扩散/转发"}
                ],
                "grammar_title": "被动进行时：动词被动态 + ている（正在被……）",
                "grammar_bullets": [
                    ["1. 句式构成：", "「拡散する（转发扩散）」->「拡散される（被转发）」->「拡散されている（正在被病毒式疯传）」."],
                    ["2. SNS 在日语中的读法：", "按字母逐字读作「エス・エヌ・エス（指代X、Instagram、TikTok、YouTube等）」."],
                    ["3. 网络爆火词汇：", "「バズる（在网上突然爆火，Buzz）」、「トレンド入り（登上热搜榜首）」."],
                    ["4. 副词急速に（きゅうそくに）：", "形容传播扩散速度极快，短时间内突破百万播放."]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "接下来拆解社交媒体时代形容视频爆火疯传的黄金词汇。"},
                    {"speaker": "ja", "text": "未来", "card_idx": 0},
                    {"speaker": "explainer", "text": "名词：近未来、科技未来世界。", "card_idx": 0},
                    {"speaker": "ja", "text": "描いた", "card_idx": 1},
                    {"speaker": "explainer", "text": "动词描く的过去形：描绘、展现。", "card_idx": 1},
                    {"speaker": "ja", "text": "映像", "card_idx": 2},
                    {"speaker": "explainer", "text": "名词读作 eizou，视频画面、影像。", "card_idx": 2},
                    {"speaker": "ja", "text": "SNS", "card_idx": 3},
                    {"speaker": "explainer", "text": "名词读作 esuenuesu，社交媒体网络平台。", "card_idx": 3},
                    {"speaker": "ja", "text": "拡散", "card_idx": 4},
                    {"speaker": "explainer", "text": "名词读作 kakusan，扩散、转发疯传。", "card_idx": 4},
                    {"speaker": "explainer", "text": "语法精讲：被动进行时态形容事物正在被大量传播的句型。", "is_spotlight": True},
                    {"speaker": "ja", "text": "SNSで急速に拡散されています。", "is_spotlight": True},
                    {"speaker": "explainer", "text": "意思是在社交媒体上正在被飞速疯传，网络热点必备表达。", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "05. 近未来探访愿望表达",
                "spoken_text": "近未来の渋谷に行ってみたいですね！楽しみです。",
                "meaning": "真想去近未来的涩谷亲眼看看呢！太让人期待了。",
                "tip": "「〜てみたい（想去试一试/想去看看）」是表达对新鲜事物憧憬的最高频句式。",
                "tokens": [
                    {"orig": "近未来の", "kana": "きんみらいの", "romaji": "kinmirai no", "pos": "名词+助词", "meaning": "近未来的"},
                    {"orig": "渋谷に", "kana": "しぶやに", "romaji": "shibuya ni", "pos": "专有名词+目的地", "meaning": "去涩谷"},
                    {"orig": "行って", "kana": "いって", "romaji": "itte", "pos": "动词て形", "meaning": "去"},
                    {"orig": "みたいですね！", "kana": "みたいですね", "romaji": "mitai desu ne!", "pos": "尝试愿望", "meaning": "想去看看呢！"},
                    {"orig": "楽しみです。", "kana": "たのしみです", "romaji": "tanoshimi desu.", "pos": "形容动词", "meaning": "很让人期待"}
                ]
            },
            {
                "type": "outro",
                "chapter": "06. 关注与练习",
                "spoken_text": "关注 TokyoFlow 日语，欢迎下载 App 一起跟读练习！"
            }
        ]
    }
]

async def generate_all_chinese_episodes():
    print("==================================================")
    print("🚀 Starting Batch Chinese Episode Producer")
    print(f"Target Queue: {len(EPISODES_CHINESE_DATA)} Episodes (EP.02 ~ EP.11)")
    print("==================================================")
    
    for ep_cfg in EPISODES_CHINESE_DATA:
        ep_num = ep_cfg["episode_number"]
        out_dir = str(RELEASES_DIR / ep_cfg["folder_name"])
        os.makedirs(out_dir, exist_ok=True)
        script_file = os.path.join(out_dir, "script.json")
        
        with open(script_file, "w", encoding="utf-8") as f:
            json.dump(ep_cfg, f, indent=2, ensure_ascii=False)
        print(f"\n📝 Saved Chinese Script: {script_file}")
        
        # Execute Multilingual Producer
        await produce_multilingual_episode(
            script_path=script_file,
            output_dir=out_dir,
            locale_code="zh"
        )

if __name__ == "__main__":
    asyncio.run(generate_all_chinese_episodes())
