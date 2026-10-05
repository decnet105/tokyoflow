#!/usr/bin/env python3
"""
TokyoFlow Japanese Website Builder & Redesign Engine
Builds bilingual, SEO/GEO-optimized, high-conversion static website for TokyoFlow.
Enforces strict ZERO EMOJI rule across all output files.
"""

import os
import re
import json
import shutil

# Emoji regex for strict validation
EMOJI_REGEX = re.compile(
    r"[\U00010000-\U0010ffff\u2600-\u26ff\u2700-\u27bf\u2300-\u23ff\u2b50\u2b55\u303d\u3297\u3299]"
)

def assert_zero_emoji(text: str, context_name: str = ""):
    matches = EMOJI_REGEX.findall(text)
    if matches:
        raise ValueError(f"[ZERO EMOJI VIOLATION] Found forbidden emojis in {context_name}: {matches}")

# 21 Long-Form Masterclasses / Compilations with Exact Scheduled/Live Timestamps
MASTERCLASSES = [
    {
        "id": "E01",
        "category": "transit",
        "jlpt": "[JLPT N4-N3]",
        "jlpt_zh": "【JLPT N4-N3】",
        "district_en": "Shinjuku (新宿)",
        "district_zh": "新宿站 (2号站台)",
        "duration": "12 Min",
        "title_en": "EP.01 • Tokyo Metro & Yamanote Platform Announcements Decoded",
        "title_zh": "EP.01 • 听懂东京山手线报站！新宿站发车音与盲道提示",
        "desc_en": "Deconstruct Shinjuku Station morning rush departure melodies, tactile yellow paving warnings, inner/outer loop announcements, and natural wayfinding phrases.",
        "desc_zh": "深度拆解新宿站早高峰发车音乐、黄色盲道安全广播、内外环线区分及找站务员极速问路黄金句。",
        "key_phrase": "黄色い点字ブロックの内側までお下がりください。",
        "key_meaning_en": "Please wait behind the yellow tactile braille blocks.",
        "key_meaning_zh": "请退至黄色盲道内侧等候列车进站。",
        "thumb_en": "/assets/thumbnails/E01-Yamanote_Transit_thumb.jpg",
        "thumb_zh": "/assets/thumbnails/E01-Yamanote_Transit_zh_thumb.jpg",
        "yt_url_en": "https://youtu.be/yN6dTC-LBz8",
        "yt_url_zh": "https://youtu.be/6JRuW-U_KsQ",
        "yt_id_en": "yN6dTC-LBz8",
        "yt_id_zh": "6JRuW-U_KsQ",
        "is_live_en": True,
        "is_live_zh": False,
        "schedule_en": "LIVE NOW",
        "schedule_zh": "首播时间：2026年10月05日 20:00 EDT"
    },
    {
        "id": "E02",
        "category": "daily",
        "jlpt": "[JLPT N5-N4]",
        "jlpt_zh": "【JLPT N5-N4】",
        "district_en": "Shibuya (渋谷)",
        "district_zh": "涩谷中心街 7-Eleven",
        "duration": "10 Min",
        "title_en": "EP.02 • Survive Tokyo 7-Eleven Checkout! Rapid Register Japanese",
        "title_zh": "EP.02 • 听懂东京7-Eleven结账！便利店3秒极速收银全通关",
        "desc_en": "Master the 3-second rapid register dialogue at Tokyo convenience stores: microwave heating, bag options, receipt requests, and Suica tap.",
        "desc_zh": "秒懂东京便利店收银台连环问：便当加热、筷子餐具、塑料袋尺寸选择、发票与Suica刷卡支付。",
        "key_phrase": "お弁当温めますか？レジ袋はご利用ですか？",
        "key_meaning_en": "Would you like your bento warmed? Do you need a plastic bag?",
        "key_meaning_zh": "便当需要帮您加热吗？需要使用塑料购物袋吗？",
        "thumb_en": "/assets/thumbnails/E02-Kombini_Checkout_thumb.jpg",
        "thumb_zh": "/assets/thumbnails/E02-Kombini_Checkout_zh_thumb.jpg",
        "yt_url_en": "https://youtu.be/6er1tWAH_oQ",
        "yt_url_zh": "https://youtu.be/SweaDZEQlpo",
        "yt_id_en": "6er1tWAH_oQ",
        "yt_id_zh": "SweaDZEQlpo",
        "is_live_en": True,
        "is_live_zh": False,
        "schedule_en": "LIVE NOW",
        "schedule_zh": "首播时间：2026年10月07日 20:00 EDT"
    },
    {
        "id": "E03",
        "category": "food",
        "jlpt": "[JLPT N5-N4]",
        "jlpt_zh": "【JLPT N5-N4】",
        "district_en": "Omoide Yokocho (思い出横丁)",
        "district_zh": "回忆横丁 居酒屋小巷",
        "duration": "14 Min",
        "title_en": "EP.03 • Order Like a Tokyo Local at an Izakaya! Toriaezu Nama Explained",
        "title_zh": "EP.03 • 像东京本地人一样进居酒屋！先来生啤开场与烤串点单",
        "desc_en": "Order authentic yakitori, understand 'Otoshi' appetizer customs, order draft beers seamlessly, and request the bill like a native Tokyoite.",
        "desc_zh": "掌握先来杯生啤（とりあえず生）、开胃小菜（お通し）规矩、盐烤与酱烤区别及顺畅买单手势。",
        "key_phrase": "とりあえず生二つ、焼き鳥盛り合わせ塩で！",
        "key_meaning_en": "First two draft beers, and a salt-grilled yakitori platter please!",
        "key_meaning_zh": "先来两杯生啤酒，再来一份盐烤烤鸡串拼盘！",
        "thumb_en": "/assets/thumbnails/E03-Izakaya_Night_thumb.jpg",
        "thumb_zh": "/assets/thumbnails/E03-Izakaya_Night_zh_thumb.jpg",
        "yt_url_en": "https://youtu.be/B4sN_BkLcOw",
        "yt_url_zh": "https://youtu.be/P9wLC803VF4",
        "yt_id_en": "B4sN_BkLcOw",
        "yt_id_zh": "P9wLC803VF4",
        "is_live_en": True,
        "is_live_zh": False,
        "schedule_en": "LIVE NOW",
        "schedule_zh": "首播时间：2026年10月09日 20:00 EDT"
    },
    {
        "id": "E04",
        "category": "culture",
        "jlpt": "[JLPT N5-N4]",
        "jlpt_zh": "【JLPT N5-N4】",
        "district_en": "Akihabara (秋葉原)",
        "district_zh": "秋叶原 无线电会馆",
        "duration": "15 Min",
        "title_en": "EP.04 • Akihabara Anime & Figure Shopping! Tax-Free and Rare Merch",
        "title_zh": "EP.04 • 秋叶原淘手办必学！免税退税与找未开封新品实用口语",
        "desc_en": "Navigate Akihabara Radio Kaikan, ask shop clerks for mint unopened items, handle duty-free tax exemption, and decode manga slang.",
        "desc_zh": "逛遍秋叶原无线电会馆与二手神店，向店员询问未开封箱规、办理免税退税手续并掌握原版漫画口吻。",
        "key_phrase": "すみません、この限定フィギュアの未開封品は在庫ありますか？",
        "key_meaning_en": "Excuse me, is this limited edition figure in mint unopened condition in stock?",
        "key_meaning_zh": "请问这款限定手办的未开封新品还有库存吗？",
        "thumb_en": "/assets/thumbnails/E04-Akiba_Pilgrimage_thumb.jpg",
        "thumb_zh": "/assets/thumbnails/E04-Akiba_Pilgrimage_zh_thumb.jpg",
        "yt_url_en": "https://youtu.be/iaGo6ey75Ws",
        "yt_url_zh": "https://youtu.be/Hf8aLBN1iEw",
        "yt_id_en": "iaGo6ey75Ws",
        "yt_id_zh": "Hf8aLBN1iEw",
        "is_live_en": True,
        "is_live_zh": False,
        "schedule_en": "LIVE NOW",
        "schedule_zh": "首播时间：2026年10月13日 20:00 EDT"
    },
    {
        "id": "E05",
        "category": "transit",
        "jlpt": "[JLPT N4-N3]",
        "jlpt_zh": "【JLPT N4-N3】",
        "district_en": "Otemachi / Ginza (大手町 / 銀座)",
        "district_zh": "大手町 / 银座 地铁枢纽",
        "duration": "11 Min",
        "title_en": "EP.05 • Survive Tokyo Subway Rush! Rapid vs Local & Fare Adjustment",
        "title_zh": "EP.05 • 东京地铁坐过站或余额不足？精算机补票与快速换乘实景精讲",
        "desc_en": "Master subway line transfers, express vs local trains, fare adjustment machines (Seisanki), and overcoming locked gate passes.",
        "desc_zh": "搞懂急行与各停列车区别、IC卡出站余额不足精算机补票流程及早高峰换乘指引。",
        "key_phrase": "精算機で乗り越し精算をしたいのですが、どこですか？",
        "key_meaning_en": "I want to adjust my fare at the fare adjustment machine; where is it?",
        "key_meaning_zh": "我想在精算机办理坐过站补票，请问机器在哪里？",
        "thumb_en": "/assets/thumbnails/E05-Tokyo_Subway_Rush_thumb.jpg",
        "thumb_zh": "/assets/thumbnails/E05-Tokyo_Subway_Rush_zh_thumb.jpg",
        "yt_url_en": "https://youtu.be/71K0XIHNZLs",
        "yt_url_zh": "https://youtu.be/odIHpboH1A0",
        "yt_id_en": "71K0XIHNZLs",
        "yt_id_zh": "odIHpboH1A0",
        "is_live_en": True,
        "is_live_zh": False,
        "schedule_en": "LIVE NOW",
        "schedule_zh": "首播时间：2026年10月15日 20:00 EDT"
    },
    {
        "id": "E06",
        "category": "daily",
        "jlpt": "[JLPT N5-N4]",
        "jlpt_zh": "【JLPT N5-N4】",
        "district_en": "Roppongi (六本木)",
        "district_zh": "六本木 便利店与ATM",
        "duration": "10 Min",
        "title_en": "EP.06 • Order Kombini Machine Coffee & Use Seven Bank ATM Like a Local",
        "title_zh": "EP.06 • 便利店咖啡怎么买？冷柜取冰杯与ATM国际取现全流程精讲",
        "desc_en": "Grab freezer ice cups, designate sizes at the register, operate automated espresso machines, and withdraw JPY cash at Seven Bank ATMs.",
        "desc_zh": "冷柜自取冰杯结账、咖啡机操作全步骤，以及在便利店ATM使用海外银行卡提取日元现金。",
        "key_phrase": "アイスコーヒーのレギュラーサイズをお願いします。",
        "key_meaning_en": "One regular-size iced coffee, please.",
        "key_meaning_zh": "请给我一杯常规杯型（R）的冰咖啡。",
        "thumb_en": "/assets/thumbnails/E06-Kombini_Coffee_ATM_thumb.jpg",
        "thumb_zh": "/assets/thumbnails/E06-Kombini_Coffee_ATM_zh_thumb.jpg",
        "yt_url_en": "https://youtu.be/kPXKS2r3o8w",
        "yt_url_zh": "https://youtu.be/C9qHbhafnqc",
        "yt_id_en": "kPXKS2r3o8w",
        "yt_id_zh": "C9qHbhafnqc",
        "is_live_en": True,
        "is_live_zh": False,
        "schedule_en": "LIVE NOW",
        "schedule_zh": "首播时间：2026年10月19日 20:00 EDT"
    },
    {
        "id": "E07",
        "category": "food",
        "jlpt": "[JLPT N5-N4]",
        "jlpt_zh": "【JLPT N5-N4】",
        "district_en": "Ikebukuro (池袋)",
        "district_zh": "池袋 激战区拉面店",
        "duration": "12 Min",
        "title_en": "EP.07 • Order Ramen Like a Tokyo Pro! Ticket Machine & Custom Broth Hacks",
        "title_zh": "EP.07 • 像老饕一样吃拉面！食券机点餐与面硬汤浓定制精讲",
        "desc_en": "Buy tickets on automated vending machines, customize noodle hardness (Katame), broth richness (Koime), and order Kaedama noodle refills.",
        "desc_zh": "熟练操作拉面食券机、定制面条软硬度与汤头浓淡度口诀，并顺畅追加替玉（加面）。",
        "key_phrase": "麺硬め、味濃いめ、油少なめでお願いします。替え玉も！",
        "key_meaning_en": "Noodles firm, flavor rich, light oil please. Also one noodle refill!",
        "key_meaning_zh": "面要硬一些、汤头浓郁、少放油，再加一份替玉（加面）！",
        "thumb_en": "/assets/thumbnails/E07-Ramen_Ticket_Vending_thumb.jpg",
        "thumb_zh": "/assets/thumbnails/E07-Ramen_Ticket_Vending_zh_thumb.jpg",
        "yt_url_en": "https://youtu.be/jB4I3CicHrs",
        "yt_url_zh": "https://youtu.be/ipyktZrqHgQ",
        "yt_id_en": "jB4I3CicHrs",
        "yt_id_zh": "ipyktZrqHgQ",
        "is_live_en": True,
        "is_live_zh": False,
        "schedule_en": "LIVE NOW",
        "schedule_zh": "首播时间：2026年10月21日 20:00 EDT"
    },
    {
        "id": "E08",
        "category": "culture",
        "jlpt": "[JLPT N5-N4]",
        "jlpt_zh": "【JLPT N5-N4】",
        "district_en": "Ginza (銀座)",
        "district_zh": "银座 百货与品牌店",
        "duration": "13 Min",
        "title_en": "EP.08 • Shop Like a Tokyo Stylist! Fitting Rooms, Sizes & Tax-Free Hacks",
        "title_zh": "EP.08 • 银座购物优雅试衣！试穿许可与询问尺码精品店日语精讲",
        "desc_en": "Ask for fitting room access, request different sizes and colors, check inventory, and process duty-free refund receipts in Ginza.",
        "desc_zh": "掌握试衣间许可请求、询问其他尺码与颜色、确认库存及办理商场退税柜台手续。",
        "key_phrase": "試着してみてもいいですか？ワンサイズ大きいものはありますか？",
        "key_meaning_en": "May I try this on? Do you have one size larger?",
        "key_meaning_zh": "请问可以试穿一下吗？有再大一个号的尺码吗？",
        "thumb_en": "/assets/thumbnails/E08-Ginza_TaxFree_Shopping_thumb.jpg",
        "thumb_zh": "/assets/thumbnails/E08-Ginza_TaxFree_Shopping_zh_thumb.jpg",
        "yt_url_en": "https://youtu.be/9GOBcaATRjE",
        "yt_url_zh": "https://youtu.be/WQ1mqBP0gN0",
        "yt_id_en": "9GOBcaATRjE",
        "yt_id_zh": "WQ1mqBP0gN0",
        "is_live_en": True,
        "is_live_zh": False,
        "schedule_en": "LIVE NOW",
        "schedule_zh": "首播时间：2026年10月23日 20:00 EDT"
    },
    {
        "id": "E09",
        "category": "culture",
        "jlpt": "[JLPT N5-N4]",
        "jlpt_zh": "【JLPT N5-N4】",
        "district_en": "Kanda / Akiba (神田 / 秋葉原)",
        "district_zh": "神田 动漫桑拿会馆",
        "duration": "10 Min",
        "title_en": "EP.09 • Anime Studio Opens Real Sauna in Tokyo! Trend & Totonou Breakdown",
        "title_zh": "EP.09 • 动漫公司开桑拿？身心彻底放松「整う」流行语精讲",
        "desc_en": "Break down viral pop news: an anime production studio opens a Finnish cedar sauna in Tokyo. Learn relaxation slang 'Totonou' and wellness vocabulary.",
        "desc_zh": "拆解东京热门文化资讯：知名动漫制作社在神田打造芬兰式桑拿房，学习极度放松流行语「整う」及日常语法。",
        "key_phrase": "サウナに入って心身ともに整いました。",
        "key_meaning_en": "After the sauna session, my body and mind are totally rejuvenated.",
        "key_meaning_zh": "泡完桑拿后，身心彻底进入了放松通透的绝佳状态。",
        "thumb_en": "/assets/thumbnails/E09-anime_sauna_trend_thumb.jpg",
        "thumb_zh": "/assets/thumbnails/E09-anime_sauna_trend_zh_thumb.jpg",
        "yt_url_en": "https://youtu.be/fXJMz9_CGCs",
        "yt_url_zh": "https://youtu.be/28N9m0VcL50",
        "yt_id_en": "fXJMz9_CGCs",
        "yt_id_zh": "28N9m0VcL50",
        "is_live_en": False,
        "is_live_zh": False,
        "schedule_en": "Scheduled: Oct 05, 08:00 AM EDT",
        "schedule_zh": "首播时间：2026年10月27日 20:00 EDT"
    },
    {
        "id": "E10",
        "category": "culture",
        "jlpt": "[JLPT N5-N4]",
        "jlpt_zh": "【JLPT N5-N4】",
        "district_en": "Roppongi Hills (六本木ヒルズ)",
        "district_zh": "六本木 电影发布会",
        "duration": "11 Min",
        "title_en": "EP.10 • Ayase Haruka's Natural Charm at Press Stage! Tennen Japanese Breakdown",
        "title_zh": "EP.10 • 绫濑遥天然呆发言引全场爆笑！日综反差萌流行语精讲",
        "desc_en": "Analyze live press conference interactions, understand the beloved Japanese personality trait 'Tennen', and master conversational humor.",
        "desc_zh": "精读东京新片发布会现场原声，深入理解日本独特的「天然（呆）」性格概念与综艺访谈应答。",
        "key_phrase": "天然な性格でみんなを笑顔にさせました。",
        "key_meaning_en": "Her natural, charming quirkiness brought smiles to everyone in the hall.",
        "key_meaning_zh": "她那天然萌的可爱性格让全场观众都露出了笑容。",
        "thumb_en": "/assets/thumbnails/E10-ayase_haruka_tennen_thumb.jpg",
        "thumb_zh": "/assets/thumbnails/E10-ayase_haruka_tennen_zh_thumb.jpg",
        "yt_url_en": "https://youtu.be/CCUSAjlHbYQ",
        "yt_url_zh": "https://youtu.be/y1zQQA0Tmfs",
        "yt_id_en": "CCUSAjlHbYQ",
        "yt_id_zh": "y1zQQA0Tmfs",
        "is_live_en": False,
        "is_live_zh": False,
        "schedule_en": "Scheduled: Oct 06, 08:00 AM EDT",
        "schedule_zh": "首播时间：2026年10月29日 20:00 EDT"
    },
    {
        "id": "E11",
        "category": "culture",
        "jlpt": "[JLPT N5-N4]",
        "jlpt_zh": "【JLPT N5-N4】",
        "district_en": "Shibuya (渋谷)",
        "district_zh": "涩谷 智能餐饮店",
        "duration": "10 Min",
        "title_en": "EP.11 • Shibuya AI Cat Robot Waiter Drama! Real Restaurant Tech Breakdown",
        "title_zh": "EP.11 • 涩谷AI机器人短剧爆火！科技科幻与现代餐饮热点精讲",
        "desc_en": "Explore high-tech dining in Shibuya where robotic servers deliver hot-pot wagyu. Learn future technology verbs and restaurant expressions.",
        "desc_zh": "探讨涩谷全自动配餐机器人送餐热点，掌握前沿科技词汇、餐饮动词与短剧对话。",
        "key_phrase": "配膳ロボットが席までお肉を運んできました。",
        "key_meaning_en": "The delivery robot brought the beef dishes straight to our table.",
        "key_meaning_zh": "智能送餐机器人把新鲜肉品直接送到了我们的座位上。",
        "thumb_en": "/assets/thumbnails/E11-shabuya-robot-drama_thumb.jpg",
        "thumb_zh": "/assets/thumbnails/E11-shabuya-robot-drama_zh_thumb.jpg",
        "yt_url_en": "https://youtu.be/tIFJcJFxSi4",
        "yt_url_zh": "https://youtu.be/OkPi4X-K8u4",
        "yt_id_en": "tIFJcJFxSi4",
        "yt_id_zh": "OkPi4X-K8u4",
        "is_live_en": False,
        "is_live_zh": False,
        "schedule_en": "Scheduled: Oct 07, 08:00 AM EDT",
        "schedule_zh": "首播时间：2026年11月02日 20:00 EST"
    },
    {
        "id": "E12",
        "category": "culture",
        "jlpt": "[JLPT N5-N4]",
        "jlpt_zh": "【JLPT N5-N4】",
        "district_en": "Tokyo Tech (東京)",
        "district_zh": "东京 科技与社会",
        "duration": "10 Min",
        "title_en": "EP.12 • Apple's Suicide Prevention Request | Tech News Breakdown",
        "title_zh": "EP.12 • 苹果系统防自杀提示更新 | 科技社会热点精讲",
        "desc_en": "Break down official iOS safety notifications, public support hotline vocabulary, and formal technical announcements in Japan.",
        "desc_zh": "精读科技热点官方公告，学习公共咨询窗口求助表达与规范书面语表达。",
        "key_phrase": "相談窓口への案内機能が追加されました。",
        "key_meaning_en": "A guidance feature directing users to consultation hotlines has been added.",
        "key_meaning_zh": "系统中已新增引导用户联系官方心理咨询窗口的支持功能。",
        "thumb_en": "/assets/thumbnails/E12-apple-suicide-prevention_thumb.jpg",
        "thumb_zh": "/assets/thumbnails/E12-apple-suicide-prevention_thumb.jpg",
        "yt_url_en": "https://youtu.be/nVD1G__Yj6U",
        "yt_url_zh": "https://youtu.be/nVD1G__Yj6U",
        "yt_id_en": "nVD1G__Yj6U",
        "yt_id_zh": "nVD1G__Yj6U",
        "is_live_en": False,
        "is_live_zh": False,
        "schedule_en": "Scheduled: Oct 08, 08:00 AM EDT",
        "schedule_zh": "首播时间：2026年11月04日 20:00 EST (排期预告)"
    },
    {
        "id": "E13",
        "category": "food",
        "jlpt": "[JLPT N5-N4]",
        "jlpt_zh": "【JLPT N5-N4】",
        "district_en": "Shinbashi (新橋)",
        "district_zh": "新桥 吉野家牛肉饭",
        "duration": "11 Min",
        "title_en": "EP.13 • Order Gyudon Like a Local! Yoshinoya Tsuyudaku & Set Hacks",
        "title_zh": "EP.13 • 吉野家点单达人！汁多（つゆだく）与套餐定制技巧",
        "desc_en": "Master rapid-fire beef bowl customization: extra sauce (Tsuyudaku), negidaku onions, raw egg sets, and quick lunch rush commands.",
        "desc_zh": "掌握经典牛肉饭点单暗号：汁多（つゆだく）、葱多、生鸡蛋小菜套餐及快节奏出餐应答。",
        "key_phrase": "牛丼並盛、つゆだくで生卵とお新香セットをつけてください。",
        "key_meaning_en": "Standard gyudon with extra sauce, plus raw egg and pickle set please.",
        "key_meaning_zh": "来一份中碗牛肉饭，要多汁（つゆだく），加一份生鸡蛋和腌菜套餐。",
        "thumb_en": "/assets/thumbnails/E13-Gyudon_Customization_thumb.jpg",
        "thumb_zh": "/assets/thumbnails/E13-Gyudon_Customization_thumb.jpg",
        "yt_url_en": "https://youtu.be/JoM1Ht4rsm0",
        "yt_url_zh": "https://youtu.be/JoM1Ht4rsm0",
        "yt_id_en": "JoM1Ht4rsm0",
        "yt_id_zh": "JoM1Ht4rsm0",
        "is_live_en": False,
        "is_live_zh": False,
        "schedule_en": "Scheduled: Oct 09, 08:00 AM EDT",
        "schedule_zh": "首播时间：2026年11月06日 20:00 EST (排期预告)"
    },
    {
        "id": "E14",
        "category": "daily",
        "jlpt": "[JLPT N4-N3]",
        "jlpt_zh": "【JLPT N4-N3】",
        "district_en": "Nakano (中野)",
        "district_zh": "中野 日本邮政物流",
        "duration": "12 Min",
        "title_en": "EP.14 • Never Miss Japanese Mail! Redelivery Slips & Delivery Hacks",
        "title_zh": "EP.14 • 日本邮政不在票处理！再投递申请全流程攻略",
        "desc_en": "Read delivery attempt notices (Fuzai Renrakuhyō), book specific delivery time slots online, and receive parcels at home without stress.",
        "desc_zh": "看懂日本快递不在联络票关键信息、手机扫码预约指定时间段再投递与签收礼仪。",
        "key_phrase": "ご不在連絡票の追跡番号で再配達をお願いしたいです。",
        "key_meaning_en": "I'd like to request redelivery using the tracking number on my absence slip.",
        "key_meaning_zh": "我想用不在联络票上的单号申请重新预约配送。",
        "thumb_en": "/assets/thumbnails/E14-JapanPost_Redelivery_thumb.jpg",
        "thumb_zh": "/assets/thumbnails/E14-JapanPost_Redelivery_thumb.jpg",
        "yt_url_en": "https://youtu.be/hMpbydnmDzE",
        "yt_url_zh": "https://youtu.be/hMpbydnmDzE",
        "yt_id_en": "hMpbydnmDzE",
        "yt_id_zh": "hMpbydnmDzE",
        "is_live_en": False,
        "is_live_zh": False,
        "schedule_en": "Scheduled: Oct 12, 08:00 AM EDT",
        "schedule_zh": "首播时间：2026年11月09日 20:00 EST (排期预告)"
    },
    {
        "id": "E15",
        "category": "daily",
        "jlpt": "[JLPT N5-N4]",
        "jlpt_zh": "【JLPT N5-N4】",
        "district_en": "Koenji (高円寺)",
        "district_zh": "高圆寺 社区生鲜超市",
        "duration": "12 Min",
        "title_en": "EP.15 • Tokyo Supermarket 8 PM Half-Price Hunt! Hangaku Bento & Sashimi",
        "title_zh": "EP.15 • 东京超市晚8点半价大作战！便当刺身抢购法则",
        "desc_en": "Identify discount stickers (Hangaku, 20% off), time your visits to Tokyo neighborhood supermarkets, and save big on fresh sashimi.",
        "desc_zh": "识别超市降价贴纸（半額、2割引）、掌握晚间贴标折扣规律与生鲜食品地道词汇。",
        "key_phrase": "このお刺身、半額シールが貼ってありますね！",
        "key_meaning_en": "Look, this sashimi platter has a half-price sticker on it!",
        "key_meaning_zh": "你看，这份生鱼片已经贴上了半价折扣标签！",
        "thumb_en": "/assets/thumbnails/E15-Supermarket_HalfPrice_Rush_thumb.jpg",
        "thumb_zh": "/assets/thumbnails/E15-Supermarket_HalfPrice_Rush_thumb.jpg",
        "yt_url_en": "https://youtu.be/SYTMgRcyycQ",
        "yt_url_zh": "https://youtu.be/SYTMgRcyycQ",
        "yt_id_en": "SYTMgRcyycQ",
        "yt_id_zh": "SYTMgRcyycQ",
        "is_live_en": False,
        "is_live_zh": False,
        "schedule_en": "Scheduled: Oct 13, 08:00 AM EDT",
        "schedule_zh": "首播时间：2026年11月11日 20:00 EST (排期预告)"
    },
    {
        "id": "E16",
        "category": "daily",
        "jlpt": "[JLPT N5-N4]",
        "jlpt_zh": "【JLPT N5-N4】",
        "district_en": "Shinjuku Drugstore (薬局)",
        "district_zh": "新宿 松本清药妆店",
        "duration": "12 Min",
        "title_en": "EP.16 • Tokyo Drugstore Survival! Buying Painkillers & Explaining Symptoms",
        "title_zh": "EP.16 • 东京药妆店救急！止痛药选购与症状准确描述",
        "desc_en": "Ask pharmacists for pain relievers (EVE, Loxonin), describe headaches, stomach issues, and fever accurately in Japanese.",
        "desc_zh": "准确向药剂师描述头痛、发热、胃痛症状，选购温和不伤胃的止痛药与常备药。",
        "key_phrase": "頭痛がひどいので、胃に優しい鎮痛薬を探しています。",
        "key_meaning_en": "I have a severe headache, so I'm looking for a painkiller that is gentle on the stomach.",
        "key_meaning_zh": "我头痛得厉害，想找一种不刺激胃的温和止痛药。",
        "thumb_en": "/assets/thumbnails/E16-Drugstore_Medicine_thumb.jpg",
        "thumb_zh": "/assets/thumbnails/E16-Drugstore_Medicine_thumb.jpg",
        "yt_url_en": "https://youtu.be/jOlIP0S4TJI",
        "yt_url_zh": "https://youtu.be/jOlIP0S4TJI",
        "yt_id_en": "jOlIP0S4TJI",
        "yt_id_zh": "jOlIP0S4TJI",
        "is_live_en": False,
        "is_live_zh": False,
        "schedule_en": "Scheduled: Oct 14, 08:00 AM EDT",
        "schedule_zh": "首播时间：2026年11月13日 20:00 EST (排期预告)"
    },
    {
        "id": "E17",
        "category": "culture",
        "jlpt": "[JLPT N5-N4]",
        "jlpt_zh": "【JLPT N5-N4】",
        "district_en": "Asakusa Sento (浅草 銭湯)",
        "district_zh": "浅草 传统日式钱汤",
        "duration": "13 Min",
        "title_en": "EP.17 • Tokyo Public Bath & Onsen Etiquette! Washing Rules & Towel Manners",
        "title_zh": "EP.17 • 东京钱汤与温泉礼仪！入浴清洗与毛巾规范",
        "desc_en": "Master sento entry, shoe locker keys, washing stool protocols (Kakeyu), tub rules, and locker room etiquette like a native.",
        "desc_zh": "掌握传统钱汤番台购票、鞋柜钥匙、入池前淋浴冲洗（かけ湯）规范及更衣室礼仪。",
        "key_phrase": "湯船に入る前に、かけ湯で体を綺麗に洗いましょう。",
        "key_meaning_en": "Before entering the bathtub, let's rinse and wash our body clean with warm water.",
        "key_meaning_zh": "进入温泉汤池之前，请务必先冲洗身体清洁干净。",
        "thumb_en": "/assets/thumbnails/E17-Onsen_Sento_Etiquette_thumb.jpg",
        "thumb_zh": "/assets/thumbnails/E17-Onsen_Sento_Etiquette_thumb.jpg",
        "yt_url_en": "https://youtu.be/NvxHyVZ0XSY",
        "yt_url_zh": "https://youtu.be/NvxHyVZ0XSY",
        "yt_id_en": "NvxHyVZ0XSY",
        "yt_id_zh": "NvxHyVZ0XSY",
        "is_live_en": False,
        "is_live_zh": False,
        "schedule_en": "Scheduled: Oct 15, 08:00 AM EDT",
        "schedule_zh": "首播时间：2026年11月16日 20:00 EST (排期预告)"
    },
    {
        "id": "E18",
        "category": "food",
        "jlpt": "[JLPT N5-N4]",
        "jlpt_zh": "【JLPT N5-N4】",
        "district_en": "Omotesando Cafe (表参道)",
        "district_zh": "表参道 / 代官山 精品咖啡馆",
        "duration": "11 Min",
        "title_en": "EP.18 • Order Coffee & Custom Drinks in Tokyo! Takeout, Milk & Size Hacks",
        "title_zh": "EP.18 • 东京咖啡馆个性定制！外带与换奶定制指南",
        "desc_en": "Order specialty drip coffee, specify oat/soy milk swaps, choose ice levels, and clarify dine-in (Tennai) vs takeout (Omochikaeri) taxes.",
        "desc_zh": "精品咖啡手冲点单、更换燕麦奶或低脂奶、指定少冰及区分店内享用与外带消费税。",
        "key_phrase": "オーツミルクに変更で、持ち帰りでお願いします。",
        "key_meaning_en": "Please substitute oat milk, and make it for takeout.",
        "key_meaning_zh": "请帮我换成燕麦奶，这杯麻烦打包带走。",
        "thumb_en": "/assets/thumbnails/E18-Tokyo_Cafe_Ordering_thumb.jpg",
        "thumb_zh": "/assets/thumbnails/E18-Tokyo_Cafe_Ordering_thumb.jpg",
        "yt_url_en": "https://youtu.be/rY3KT6Lk1uA",
        "yt_url_zh": "https://youtu.be/rY3KT6Lk1uA",
        "yt_id_en": "rY3KT6Lk1uA",
        "yt_id_zh": "rY3KT6Lk1uA",
        "is_live_en": False,
        "is_live_zh": False,
        "schedule_en": "Scheduled: Oct 16, 08:00 AM EDT",
        "schedule_zh": "首播时间：2026年11月18日 20:00 EST (排期预告)"
    },
    {
        "id": "E19",
        "category": "transit",
        "jlpt": "[JLPT N4-N3]",
        "jlpt_zh": "【JLPT N4-N3】",
        "district_en": "Tokyo Station (東京駅)",
        "district_zh": "东京站 新干线绿色窗口",
        "duration": "13 Min",
        "title_en": "EP.19 • Book Shinkansen Bullet Train Tickets! Reserved Seats & Mt. Fuji View",
        "title_zh": "EP.19 • 新干线订票指南！指定席与富士山侧选座技巧",
        "desc_en": "Buy Nozomi/Hikari bullet train tickets at Midori-no-Madoguchi, choose Row E window seats for Mt. Fuji views, and manage oversized baggage.",
        "desc_zh": "在绿色窗口购买希望号/光号车票、挑选E排靠窗富士山景观位及大件行李预约规则。",
        "key_phrase": "富士山が見える側の指定席を一枚予約したいのですが。",
        "key_meaning_en": "I'd like to book one reserved seat on the side with the Mt. Fuji view.",
        "key_meaning_zh": "我想预订一张能看到富士山那一侧的靠窗指定席车票。",
        "thumb_en": "/assets/thumbnails/E19-Shinkansen_BulletTrain_Tickets_thumb.jpg",
        "thumb_zh": "/assets/thumbnails/E19-Shinkansen_BulletTrain_Tickets_thumb.jpg",
        "yt_url_en": "https://youtu.be/OeVMipTfon0",
        "yt_url_zh": "https://youtu.be/OeVMipTfon0",
        "yt_id_en": "OeVMipTfon0",
        "yt_id_zh": "OeVMipTfon0",
        "is_live_en": False,
        "is_live_zh": False,
        "schedule_en": "Scheduled: Oct 19, 08:00 AM EDT",
        "schedule_zh": "首播时间：2026年11月20日 20:00 EST (排期预告)"
    },
    {
        "id": "WL01",
        "category": "compilation",
        "jlpt": "[JLPT N5-N2]",
        "jlpt_zh": "【JLPT N5-N2】",
        "district_en": "Cinema Immersion (映画)",
        "district_zh": "日本院线电影沉浸",
        "duration": "18 Min",
        "title_en": "WL.01 • Last Mile Cinema Masterclass | Master Real Japanese Through Film",
        "title_zh": "WL.01 • 电影《最后的里程》影视沉浸精讲 | 电影级高语境深度解析",
        "desc_en": "Comprehensive 18-minute masterclass decoding Japan's 2024 blockbuster movie 'Last Mile': logistics terminology, workplace nuances, and pitch accuracy.",
        "desc_zh": "18分钟深度解析2024年日本现象级电影《Last Mile》：物流社会学、职场潜台词、敬语反转与纯正语调。",
        "key_phrase": "映画のリアルなセリフから高コンテクストな日本語を深く学ぶ。",
        "key_meaning_en": "Deeply learn high-context living Japanese through authentic cinematic dialogues.",
        "key_meaning_zh": "从真实电影台词中深度汲取高语境地道日语与社会文化精髓。",
        "thumb_en": "/assets/thumbnails/WL01-last-mile-masterclass_thumb.jpg",
        "thumb_zh": "/assets/thumbnails/WL01-last-mile-masterclass_zh_thumb.jpg",
        "yt_url_en": "https://youtu.be/-KFRtoLDNVU",
        "yt_url_zh": "https://youtu.be/qVNR2duZWqQ",
        "yt_id_en": "-KFRtoLDNVU",
        "yt_id_zh": "qVNR2duZWqQ",
        "is_live_en": True,
        "is_live_zh": True,
        "schedule_en": "LIVE NOW",
        "schedule_zh": "已公开上线 • 立即观看"
    },
    {
        "id": "WM01",
        "category": "compilation",
        "jlpt": "[JLPT N5-N3]",
        "jlpt_zh": "【JLPT N5-N3】",
        "district_en": "Tokyo 360 Mega",
        "district_zh": "东京全景生活大合集",
        "duration": "28 Min",
        "title_en": "WM.01 • Monday to Friday Tokyo Survival All-in-One + Culture Marathon",
        "title_zh": "WM.01 • 周一到周五东京生活全景大合集（28分钟超长沉浸精讲）",
        "desc_en": "The ultimate 28-minute Japanese learning compilation covering 10 real scenarios from transit and 7-Eleven to izakayas, sento, and ramen.",
        "desc_zh": "28分钟东京独立生活终极合集：涵盖电车、便利店、居酒屋、秋叶原、拉面机、钱汤等10大核心实景。",
        "key_phrase": "月曜日から金曜日までの東京リアル生活を完全攻略！",
        "key_meaning_en": "Complete conquest of authentic Tokyo living from Monday through Friday!",
        "key_meaning_zh": "一站式通关周一到周五东京独立生活全部核心口语与高频语法！",
        "thumb_en": "/assets/thumbnails/WM01-weekday_survival_mega_compilation_thumb.jpg",
        "thumb_zh": "/assets/thumbnails/WM01-weekday_survival_mega_compilation_zh_thumb.jpg",
        "yt_url_en": "https://youtu.be/mV7J6OKutj0",
        "yt_url_zh": "https://youtu.be/D99vmCoeymc",
        "yt_id_en": "mV7J6OKutj0",
        "yt_id_zh": "D99vmCoeymc",
        "is_live_en": True,
        "is_live_zh": True,
        "schedule_en": "LIVE NOW",
        "schedule_zh": "已公开上线 • 立即观看"
    }
]

# Top Vertical Shorts for Rapid Shadowing Drills
SHORTS_ZH = [
    {
        "id": "WS.01",
        "jlpt": "【JLPT N3】",
        "title": "电影《最后的里程》高光台词跟读！2.7m/s绝不停运？",
        "yt_url": "https://youtu.be/XVbg-f8s7F0",
        "yt_id": "XVbg-f8s7F0",
        "focus": "满岛光电影原声与~わけにはいかない",
        "is_live": True,
        "schedule": "已公开上线 • 立即跟读"
    },
    {
        "id": "WS.02",
        "jlpt": "【JLPT N4】",
        "title": "听懂山手线站台广播！黄色盲道退后提示与自谦语精讲",
        "yt_url": "https://youtu.be/PSynUxU1zy4",
        "yt_id": "PSynUxU1zy4",
        "focus": "山手线站台广播与自谦语mairimasu",
        "is_live": True,
        "schedule": "已公开上线 • 立即跟读"
    },
    {
        "id": "SH.00",
        "jlpt": "【中文首发】",
        "title": "告别死板教科书！每天1分钟搞定东京地道实景日语",
        "yt_url": "https://youtu.be/XUWDCPU0Tog",
        "yt_id": "XUWDCPU0Tog",
        "focus": "东京地道实景日语全景导学",
        "is_live": True,
        "schedule": "已公开上线 • 立即跟读"
    },
    {
        "id": "SH.01",
        "jlpt": "【JLPT N4】",
        "title": "听懂东京山手线报站！1分钟实景原声跟读挑战",
        "yt_url": "https://youtu.be/7CPqE_Y4nYA",
        "yt_id": "7CPqE_Y4nYA",
        "focus": "山手线发车音与盲道黄线",
        "is_live": False,
        "schedule": "首播时间：10月06日 20:00 EDT"
    },
    {
        "id": "SH.02",
        "jlpt": "【JLPT N5】",
        "title": "便利店买便当必听！收银台原声跟读挑战",
        "yt_url": "https://youtu.be/qnW1x0AMq5Y",
        "yt_id": "qnW1x0AMq5Y",
        "focus": "便当加热与购物袋选择",
        "is_live": False,
        "schedule": "首播时间：10月08日 20:00 EDT"
    },
    {
        "id": "SH.03",
        "jlpt": "【JLPT N5】",
        "title": "像本地人一样进居酒屋！先来生啤原声跟读",
        "yt_url": "https://youtu.be/RdE2fQdcQnw",
        "yt_id": "RdE2fQdcQnw",
        "focus": "先来生啤与烤串拼盘",
        "is_live": False,
        "schedule": "首播时间：10月12日 20:00 EDT"
    },
    {
        "id": "SH.04",
        "jlpt": "【JLPT N5】",
        "title": "秋叶原淘手办必学！免税退税1分钟原声跟读",
        "yt_url": "https://youtu.be/Sxb_NET07Io",
        "yt_id": "Sxb_NET07Io",
        "focus": "免税退税与未开封正品",
        "is_live": False,
        "schedule": "首播时间：10月14日 20:00 EDT"
    },
    {
        "id": "SH.05",
        "jlpt": "【JLPT N4】",
        "title": "东京地铁坐过站/余额不足？精算机补票跟读",
        "yt_url": "https://youtu.be/DqzlmsrCWO4",
        "yt_id": "DqzlmsrCWO4",
        "focus": "精算机补票与换乘指引",
        "is_live": False,
        "schedule": "首播时间：10月16日 20:00 EDT"
    },
    {
        "id": "SH.06",
        "jlpt": "【JLPT N5】",
        "title": "日本便利店冰咖啡怎么买？冷柜取杯与点单跟读",
        "yt_url": "https://youtu.be/8Whu9ozLB6Y",
        "yt_id": "8Whu9ozLB6Y",
        "focus": "冷柜自取冰杯与咖啡机",
        "is_live": False,
        "schedule": "首播时间：10月20日 20:00 EDT"
    },
    {
        "id": "SH.07",
        "jlpt": "【JLPT N5】",
        "title": "像老饕一样吃拉面！面硬汤浓加面口诀原声跟读",
        "yt_url": "https://youtu.be/jCqHgSzkYNY",
        "yt_id": "jCqHgSzkYNY",
        "focus": "面硬汤浓定制口诀与替玉",
        "is_live": False,
        "schedule": "首播时间：10月22日 20:00 EDT"
    },
    {
        "id": "SH.08",
        "jlpt": "【JLPT N5】",
        "title": "银座买衣服优雅试穿！试衣间许可请求跟读",
        "yt_url": "https://youtu.be/tOwEtT7ftMA",
        "yt_id": "tOwEtT7ftMA",
        "focus": "试衣间许可与尺码询问",
        "is_live": False,
        "schedule": "首播时间：10月26日 20:00 EDT"
    },
    {
        "id": "SH.09",
        "jlpt": "【JLPT N5】",
        "title": "动漫公司开桑拿？身心放松「整う」流行语跟读",
        "yt_url": "https://youtu.be/EHnxZQyZCJY",
        "yt_id": "EHnxZQyZCJY",
        "focus": "芬兰桑拿与放松口诀",
        "is_live": False,
        "schedule": "首播时间：10月28日 20:00 EDT"
    },
    {
        "id": "SH.10",
        "jlpt": "【JLPT N5】",
        "title": "绫濑遥天然呆引爆笑！日综反差萌流行语跟读",
        "yt_url": "https://youtu.be/7QO41aDb5dU",
        "yt_id": "7QO41aDb5dU",
        "focus": "天然呆性格与综艺对话",
        "is_live": False,
        "schedule": "首播时间：10月30日 20:00 EDT"
    },
    {
        "id": "SH.11",
        "jlpt": "【JLPT N4】",
        "title": "涩谷AI机器人微剧爆火！近未来科技热点跟读",
        "yt_url": "https://youtu.be/zoFHEf-Ir2c",
        "yt_id": "zoFHEf-Ir2c",
        "focus": "送餐机器人与餐饮动词",
        "is_live": False,
        "schedule": "首播时间：11月03日 20:00 EST"
    }
]

SHORTS_EN = [
    {
        "id": "SH.01",
        "jlpt": "[JLPT N4]",
        "title": "What Tokyo Train Stations ACTUALLY Announce!",
        "yt_url": "https://youtu.be/luY_kYPz5Bo",
        "yt_id": "luY_kYPz5Bo",
        "focus": "Yamanote Train Arrival & Braille Block",
        "is_live": True,
        "schedule": "LIVE NOW"
    },
    {
        "id": "SH.02",
        "jlpt": "[JLPT N5]",
        "title": "How to Survive Tokyo 7-Eleven Checkout in 30s",
        "yt_url": "https://youtu.be/npUV2_Ilid8",
        "yt_id": "npUV2_Ilid8",
        "focus": "Bento Heating & Bag Choices",
        "is_live": True,
        "schedule": "LIVE NOW"
    },
    {
        "id": "SH.03",
        "jlpt": "[JLPT N5]",
        "title": "How Locals Order at a Tokyo Izakaya",
        "yt_url": "https://youtu.be/9gMYd5lRwtI",
        "yt_id": "9gMYd5lRwtI",
        "focus": "Toriaezu Nama & Yakitori",
        "is_live": True,
        "schedule": "LIVE NOW"
    },
    {
        "id": "SH.04",
        "jlpt": "[JLPT N5]",
        "title": "How to Buy Anime Figures in Akihabara Tax-Free!",
        "yt_url": "https://youtu.be/GerQ2oL84o8",
        "yt_id": "GerQ2oL84o8",
        "focus": "Duty-Free & Mint Condition",
        "is_live": True,
        "schedule": "LIVE NOW"
    },
    {
        "id": "SH.05",
        "jlpt": "[JLPT N4]",
        "title": "Never Get Lost on the Tokyo Subway!",
        "yt_url": "https://youtu.be/K8E-XXJFu3I",
        "yt_id": "K8E-XXJFu3I",
        "focus": "Fare Adjustment & Transfers",
        "is_live": True,
        "schedule": "LIVE NOW"
    },
    {
        "id": "SH.06",
        "jlpt": "[JLPT N5]",
        "title": "How to Order Coffee at Japanese Convenience Stores",
        "yt_url": "https://youtu.be/fj-Yto1FF3U",
        "yt_id": "fj-Yto1FF3U",
        "focus": "Freezer Ice Cup & Machine",
        "is_live": True,
        "schedule": "LIVE NOW"
    },
    {
        "id": "SH.07",
        "jlpt": "[JLPT N5]",
        "title": "How to Order Ramen Like a Tokyo Master",
        "yt_url": "https://youtu.be/4nH8UUKeEDA",
        "yt_id": "4nH8UUKeEDA",
        "focus": "Noodle Hardness & Kaedama",
        "is_live": True,
        "schedule": "LIVE NOW"
    },
    {
        "id": "SH.08",
        "jlpt": "[JLPT N5]",
        "title": "How to Shop Clothes in Tokyo Ginza!",
        "yt_url": "https://youtu.be/O2FjmMOFWgM",
        "yt_id": "O2FjmMOFWgM",
        "focus": "Fitting Room & Size Request",
        "is_live": True,
        "schedule": "LIVE NOW"
    },
    {
        "id": "SH.09",
        "jlpt": "[JLPT N5]",
        "title": "Anime Studio Made a SAUNA in Tokyo?!",
        "yt_url": "https://youtu.be/nLSoKy3DFFI",
        "yt_id": "nLSoKy3DFFI",
        "focus": "Finnish Sauna & Totonou Slang",
        "is_live": False,
        "schedule": "Scheduled: Oct 05, 05:00 PM EDT"
    },
    {
        "id": "SH.10",
        "jlpt": "[JLPT N5]",
        "title": "Ayase Haruka's Natural Charm!",
        "yt_url": "https://youtu.be/gkl9fCKjkyQ",
        "yt_id": "gkl9fCKjkyQ",
        "focus": "Natural Personality Trait (Tennen)",
        "is_live": False,
        "schedule": "Scheduled: Oct 06, 05:00 PM EDT"
    },
    {
        "id": "SH.11",
        "jlpt": "[JLPT N5]",
        "title": "Shabu-ya Robot Drama!",
        "yt_url": "https://youtu.be/DiGmCYF_ZNI",
        "yt_id": "DiGmCYF_ZNI",
        "focus": "Restaurant Cat Robot Server",
        "is_live": False,
        "schedule": "Scheduled: Oct 07, 08:00 AM EDT"
    },
    {
        "id": "SH.13",
        "jlpt": "[JLPT N5]",
        "title": "How to Order Gyudon at Yoshinoya Like a Pro",
        "yt_url": "https://youtu.be/aXDKg4hwK2I",
        "yt_id": "aXDKg4hwK2I",
        "focus": "Tsuyudaku & Set Customization",
        "is_live": False,
        "schedule": "Scheduled: Oct 09, 08:00 AM EDT"
    }
]

def build_schema_json(lang="zh"):
    if lang == "zh":
        faq_items = [
            {
                "@type": "Question",
                "name": "TokyoFlow 和传统教科书（如《大家日语》《新标日》）有什么区别？",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "传统教科书多采用孤立脱节的句型和生硬的人造录音，缺少真实日本高语境（Ba）的空气感。TokyoFlow 采用东京实景驱动体系，内置 4,170+ 本地真人原声、山手线站台发车音乐、便利店3秒极速收银、居酒屋点单、声调高低走向图谱及 3-tier 振假名卡拉OK高亮，帮助学习者建立自然脱口而出的听说直觉。"
                }
            },
            {
                "@type": "Question",
                "name": "TokyoFlow 的视频剧集和学习路径是如何规划的？",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "TokyoFlow 遵循 Japan Foundation (CEFR-J A1 至 B2) 与 JLPT N5 至 N1 标准，构建了 365 日年间独立生活进阶路线。内容涵盖 16:9 长篇影视化深度精讲（Micro-lessons）、9:16 沉浸影子跟读（Shorts）、超长生活全景合集（Mega-compilations）与院线电影沉浸精析，并在官方 YouTube 频道（@TokyoFlowJapan）保持稳定更新。"
                }
            },
            {
                "@type": "Question",
                "name": "什么是东京标准声调走向图谱（Pitch Accent）？为什么对听说极其重要？",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "日语是典型的音高重音（Pitch Accent）语言。相同的假名组合（如「雨 ame」和「飴 ame」），音调高低走向不同含义完全相反。TokyoFlow 将头高型、中高型、尾高型和平板型声调全部视觉化为平滑高低曲线，并配合本地原声示范，彻底根除外国学习者的平调发音。"
                }
            },
            {
                "@type": "Question",
                "name": "如何通过 YouTube 频道与 TokyoFlow App 进行高效结合学习？",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "在 YouTube 频道观看 16:9 长视频精读文化背景与语法拆解，使用 9:16 短视频进行每日 1 分钟原声影子跟读（Shadowing）；随后在 TokyoFlow App 中进行 SuperMemo SM-2 科学间隔复习、声调比对与实景任务闯关，实现快速听说飞跃。"
                }
            }
        ]
    else:
        faq_items = [
            {
                "@type": "Question",
                "name": "How does TokyoFlow differ from traditional Japanese textbooks like Genki or Minna no Nihongo?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Traditional textbooks rely on artificial grammar drills and robotic synthesized voices disconnected from high-context Japanese culture. TokyoFlow is built on real-world Tokyo situations with 4,170+ native audio tracks, Yamanote Line announcements, 7-Eleven register speed drills, and visual pitch accent curves that rewire your instinctive speaking fluency."
                }
            },
            {
                "@type": "Question",
                "name": "How is the TokyoFlow curriculum and video catalog structured?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "TokyoFlow is aligned with the Japan Foundation Standard (CEFR-J A1 to B2) and JLPT N5 through N1. It features a 365-Day Living Blueprint across 16:9 In-Depth Masterclasses, 9:16 Rapid Shadowing Shorts, Mega Compilations, and Cinema Immersion lessons published on the official YouTube Channel (@TokyoFlowJapan)."
                }
            },
            {
                "@type": "Question",
                "name": "Why is visual Pitch Accent essential for speaking natural Japanese?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Japanese is a pitch-accent language where pitch contours differentiate meanings (such as 'ame' for rain vs 'ame' for candy). TokyoFlow visualizes all four pitch patterns (Atamadaka, Nakadaka, Odaka, Heiban) with real-time waveform and pitch curves to eliminate monotone accents."
                }
            },
            {
                "@type": "Question",
                "name": "How can I combine TokyoFlow YouTube videos and the interactive mobile app?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Watch our 16:9 masterclasses and 9:16 shadowing shorts on YouTube (@TokyoFlowJapan) for immersive comprehension, then use the TokyoFlow iOS app for SuperMemo SM-2 spaced repetition, pitch matching, and hands-on scenario challenges."
                }
            }
        ]

    # Create VideoObject list
    video_objects = []
    for item in MASTERCLASSES[:12]:
        thumb = item["thumb_zh"] if lang == "zh" else item["thumb_en"]
        yt_url = item["yt_url_zh"] if lang == "zh" else item["yt_url_en"]
        yt_id = item["yt_id_zh"] if lang == "zh" else item["yt_id_en"]
        video_objects.append({
            "@type": "VideoObject",
            "name": item["title_zh"] if lang == "zh" else item["title_en"],
            "description": item["desc_zh"] if lang == "zh" else item["desc_en"],
            "thumbnailUrl": f"https://tokyoflow.app{thumb}",
            "uploadDate": "2026-10-01T08:00:00+09:00",
            "contentUrl": yt_url,
            "embedUrl": f"https://www.youtube-nocookie.com/embed/{yt_id}",
            "publisher": {
                "@type": "Organization",
                "name": "TokyoFlow",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://tokyoflow.app/assets/app_icon.jpg"
                }
            }
        })

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": "https://tokyoflow.app/#organization",
                "name": "TokyoFlow",
                "alternateName": ["TokyoFlow Japanese", "東京フロウ"],
                "url": "https://tokyoflow.app/",
                "logo": "https://tokyoflow.app/assets/app_icon.jpg",
                "sameAs": [
                    "https://www.youtube.com/@TokyoFlowJapan"
                ]
            },
            {
                "@type": "WebSite",
                "@id": f"https://tokyoflow.app/{'' if lang == 'zh' else 'en/'}#website",
                "url": f"https://tokyoflow.app/{'' if lang == 'zh' else 'en/'}",
                "name": "TokyoFlow Japanese",
                "publisher": { "@id": "https://tokyoflow.app/#organization" },
                "inLanguage": ["zh-Hans", "en"] if lang == "zh" else ["en", "zh-Hans"]
            },
            {
                "@type": "MobileApplication",
                "@id": "https://tokyoflow.app/#app",
                "name": "TokyoFlow - Japanese Speaking",
                "operatingSystem": "iOS 17.0 or later",
                "applicationCategory": "EducationalApplication",
                "publisher": { "@id": "https://tokyoflow.app/#organization" },
                "image": "https://tokyoflow.app/assets/app_icon.jpg",
                "description": "Tokyo context-driven Japanese mastery system featuring 4,170+ native audio tracks, pitch accent curves, and scenario simulations.",
                "offers": {
                    "@type": "Offer",
                    "price": "0",
                    "priceCurrency": "USD"
                }
            },
            {
                "@type": "Course",
                "@id": f"https://tokyoflow.app/{'' if lang == 'zh' else 'en/'}#course",
                "name": "Tokyo Situational Japanese Living Masterclass" if lang == "en" else "东京实景高语境日语大师课",
                "description": "Master living Japanese in Tokyo's authentic atmosphere with 20+ scenarios, 4,170+ native audio tracks, and JLPT N5-N1 vocabulary.",
                "provider": { "@id": "https://tokyoflow.app/#organization" }
            },
            {
                "@type": "FAQPage",
                "@id": f"https://tokyoflow.app/{'' if lang == 'zh' else 'en/'}#faq",
                "mainEntity": faq_items
            },
            {
                "@type": "ItemList",
                "@id": f"https://tokyoflow.app/{'' if lang == 'zh' else 'en/'}#videolist",
                "name": "TokyoFlow Japanese Video Academy Episodes",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": idx + 1,
                        "item": v_obj
                    }
                    for idx, v_obj in enumerate(video_objects)
                ]
            }
        ]
    }
    return json.dumps(schema, ensure_ascii=False, indent=2)

def generate_video_cards_html(lang="zh"):
    cards_html = []
    for ep in MASTERCLASSES:
        title = ep["title_zh"] if lang == "zh" else ep["title_en"]
        desc = ep["desc_zh"] if lang == "zh" else ep["desc_en"]
        district = ep["district_zh"] if lang == "zh" else ep["district_en"]
        jlpt = ep["jlpt_zh"] if lang == "zh" else ep["jlpt"]
        yt_url = ep["yt_url_zh"] if lang == "zh" else ep["yt_url_en"]
        thumb = ep["thumb_zh"] if lang == "zh" else ep["thumb_en"]
        key_meaning = ep["key_meaning_zh"] if lang == "zh" else ep["key_meaning_en"]
        takeaway_label = "核心实景金句" if lang == "zh" else "Key Survival Phrase"
        
        is_live = ep["is_live_zh"] if lang == "zh" else ep["is_live_en"]
        schedule_text = ep["schedule_zh"] if lang == "zh" else ep["schedule_en"]

        if is_live:
            status_badge_class = "status-badge-live"
            status_badge_text = "[已公开上线 • 立即观看]" if lang == "zh" else "[LIVE NOW]"
            btn_text = "在 YouTube 观看精讲" if lang == "zh" else "Watch on YouTube"
        else:
            status_badge_class = "status-badge-scheduled"
            status_badge_text = f"[{schedule_text}]"
            btn_text = "前往 YouTube 预约首播提醒" if lang == "zh" else "Set Premiere Reminder"

        card = f"""
        <article class="video-card-item" data-category="{ep['category']}">
          <a href="{yt_url}" target="_blank" rel="noopener" class="video-card-link" aria-label="{title}">
            <div class="video-thumb-wrap">
              <img src="{thumb}" alt="{title}" class="video-thumb-img" loading="lazy" width="640" height="360">
              <div class="video-badge-group">
                <span class="badge-jlpt">{jlpt}</span>
                <span class="badge-duration">{ep['duration']}</span>
              </div>
              <div class="video-status-overlay">
                <span class="{status_badge_class}">{status_badge_text}</span>
              </div>
              <div class="video-play-overlay">
                <div class="play-circle">
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
                </div>
              </div>
            </div>
            <div class="video-content-body">
              <div class="video-location-row">
                <span class="loc-tag">[ {district} ]</span>
                <span class="ep-tag">{ep['id']}</span>
              </div>
              <h3 class="video-item-title">{title}</h3>
              <p class="video-item-desc">{desc}</p>
              
              <div class="video-takeaway-box">
                <div class="takeaway-label">{takeaway_label}</div>
                <div class="takeaway-jp">{ep['key_phrase']}</div>
                <div class="takeaway-trans">{key_meaning}</div>
              </div>

              <div class="video-yt-action">
                <div class="video-schedule-row">
                  <span class="schedule-label">{"发布状态" if lang == "zh" else "Release Status"}:</span>
                  <span class="schedule-val {status_badge_class}">{schedule_text}</span>
                </div>
                <span class="yt-action-btn">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                  <span>{btn_text}</span>
                  <span class="arrow-icon">›</span>
                </span>
              </div>
            </div>
          </a>
        </article>
        """
        cards_html.append(card)
    return "\n".join(cards_html)

def generate_shorts_cards_html(lang="zh"):
    cards_html = []
    shorts_list = SHORTS_ZH if lang == "zh" else SHORTS_EN
    for sh in shorts_list:
        title = sh["title"]
        focus = sh["focus"]
        jlpt = sh["jlpt"]
        is_live = sh["is_live"]
        schedule = sh["schedule"]
        
        if is_live:
            badge_class = "status-badge-live"
            btn_text = "立即跟读挑战" if lang == "zh" else "Start Shadowing Drill"
        else:
            badge_class = "status-badge-scheduled"
            btn_text = "预约首播跟读" if lang == "zh" else "Set Reminder"

        card = f"""
        <div class="short-card-item">
          <a href="{sh['yt_url']}" target="_blank" rel="noopener" class="short-card-link" aria-label="{title}">
            <div class="short-top-bar">
              <span class="short-badge">{jlpt}</span>
              <span class="short-ep">{sh['id']}</span>
            </div>
            <h4 class="short-title">{title}</h4>
            <div class="short-focus-box">
              <span class="short-focus-label">{"跟读要点" if lang == "zh" else "Drill Focus"}:</span>
              <span class="short-focus-text">{focus}</span>
            </div>
            <div class="short-schedule-tag {badge_class}">
              <span>{schedule}</span>
            </div>
            <div class="short-btn-bar">
              <span class="short-action-link">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
                <span>{btn_text}</span>
              </span>
            </div>
          </a>
        </div>
        """
        cards_html.append(card)
    return "\n".join(cards_html)

def generate_faq_html(lang="zh"):
    if lang == "zh":
        faqs = [
            ("TokyoFlow 和传统教科书（如《大家的日语》《新标日》）有什么核心区别？",
             "传统教科书主要围绕语法规则和人造例句展开，缺少真实日本高语境（Ba）的空气感与即时反应。TokyoFlow 采用东京实景驱动体系，内置 4,170+ 本地真人原声、山手线发车铃声与站台广播、便利店3秒极速收银、居酒屋点单、声调高低走向图谱及 3-tier 假名卡拉OK高亮，帮助学习者直接建立肌肉记忆与脱口而出的听说反射。"),
            ("TokyoFlow 的视频剧集发布时间与排期规划是怎样的？",
             "TokyoFlow 中文解说专区定于美东时间每晚 20:00（北京时间次日 08:00）首播，目前已排期发布 EP.01 至 EP.11 完整长视频与跟读短片；全球英文版定于美东时间每日 08:00 AM 首播。页面上每个专集卡片均明确标注了【已公开上线】或【预约首播时间】，方便学习者提前在 YouTube 设定开播提醒。"),
            ("什么是东京标准声调走向图谱（Pitch Accent）？为什么对听说极其重要？",
             "日语是典型的音高重音（Pitch Accent）语言。相同的假名组合（如「雨 ame」和「飴 ame」），音调高低走向不同含义完全相反。TokyoFlow 将头高型、中高型、尾高型和平板型声调全部视觉化为平滑高低曲线，并配合本地真人原声示范，彻底根除外国学习者的平调发音。"),
            ("零基础学习者可以从 TokyoFlow 开始学习吗？",
             "完全可以。TokyoFlow 提供从五十音图发音、汉字笔顺动画到 JLPT N5 基础生活实景（电车刷卡、便利店购物、拉面食券机点单）的阶梯式教学，每句对话均配有 3-tier 振假名、罗马音及精准中文翻译，零基础亦能轻松跟读入门。"),
            ("如何结合 YouTube 视频与 TokyoFlow App 进行高效复习？",
             "建议在 YouTube 频道观看 16:9 长视频精读文化背景与语法拆解，使用 9:16 短视频进行每日 1 分钟原声影子跟读（Shadowing）；随后在 TokyoFlow App 中进行 SuperMemo SM-2 科学间隔复习、声调比对与实景任务闯关，实现快速听说飞跃。")
        ]
    else:
        faqs = [
            ("How does TokyoFlow differ from traditional textbooks like Genki or Minna no Nihongo?",
             "Traditional textbooks rely on artificial grammar drills and robotic synthesized voices disconnected from high-context Japanese culture. TokyoFlow is built on real-world Tokyo situations with 4,170+ native audio tracks, Yamanote Line announcements, 7-Eleven register speed drills, and visual pitch accent curves that rewire your instinctive speaking fluency."),
            ("What is the YouTube release cadence and schedule for TokyoFlow episodes?",
             "TokyoFlow Global English edition drops daily at 08:00 AM EDT (21:00 JST), while Chinese Edition drops at 20:00 EDT (08:00 AM CST next day). Each video card on our website explicitly displays whether the episode is [LIVE NOW] or its exact [Scheduled Premiere Date & Time] with one-click YouTube reminder integration."),
            ("Why is visual Pitch Accent essential for speaking natural Japanese?",
             "Japanese is a pitch-accent language where pitch contours differentiate meanings (such as 'ame' for rain vs 'ame' for candy). TokyoFlow visualizes all four pitch patterns (Atamadaka, Nakadaka, Odaka, Heiban) with real-time waveform and pitch curves to eliminate monotone accents."),
            ("Can complete beginners start learning with TokyoFlow?",
             "Yes. TokyoFlow provides a gentle onboarding curve starting from Kana pronunciation and essential N5 survival scenarios (transit Suica gates, 7-Eleven heating, ramen ticket machines) with 3-tier Ruby, Romaji, and English breakdowns."),
            ("How do I maximize learning between YouTube and the mobile app?",
             "Watch our 16:9 masterclasses and 9:16 shadowing shorts on YouTube (@TokyoFlowJapan) for immersive comprehension, then use the TokyoFlow iOS app for SuperMemo SM-2 spaced repetition, pitch matching, and hands-on scenario challenges.")
        ]

    items_html = []
    for idx, (q, a) in enumerate(faqs):
        open_attr = 'open' if idx == 0 else ''
        items_html.append(f"""
        <details class="faq-item" {open_attr}>
          <summary class="faq-question">
            <span class="faq-q-text">{q}</span>
            <span class="faq-toggle-icon">+</span>
          </summary>
          <div class="faq-answer">
            <p>{a}</p>
          </div>
        </details>
        """)
    return "\n".join(items_html)

def build_chinese_page():
    video_cards = generate_video_cards_html("zh")
    shorts_cards = generate_shorts_cards_html("zh")
    faq_html = generate_faq_html("zh")
    schema_json = build_schema_json("zh")

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <title>TokyoFlow — 東京を、生きる日本語。| 真实东京高语境日语学习系统与影视学院</title>
  <meta name="description" content="打破生硬脱节的语法教科书。TokyoFlow 是专为日本生活与深度文化探索打造的场景驱动日语学习系统。内置 4,170+ 本地真人原声、山手线站台广播、便利店极速收银、居酒屋点单、声调走向图谱与 365 日年间进阶路线。">
  <meta name="keywords" content="TokyoFlow, 拾得, 日语学习, 东京日语, 山手线广播, 声调走向图, 日本生活日语, 日语口语影子跟读, 漫画拟声词, JLPT N5 N4 N3 N2 N1, YouTube 日语学习, Japanese Fluency">
  <meta name="author" content="TokyoFlow Team">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="theme-color" content="#F8F6F0">
  <link rel="canonical" href="https://tokyoflow.app/">

  <!-- GEO & Multi-Language Hreflang Tags -->
  <link rel="alternate" hreflang="zh-Hans" href="https://tokyoflow.app/">
  <link rel="alternate" hreflang="zh-CN" href="https://tokyoflow.app/">
  <link rel="alternate" hreflang="en" href="https://tokyoflow.app/en/">
  <link rel="alternate" hreflang="x-default" href="https://tokyoflow.app/">

  <!-- Open Graph / WeChat / Social Meta -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="TokyoFlow">
  <meta property="og:url" content="https://tokyoflow.app/">
  <meta property="og:title" content="TokyoFlow · 東京を、生きる日本語。">
  <meta property="og:description" content="在 4,170+ 真实东京真人原声与生活场景中，掌握真正鲜活的高语境日语。涵盖山手线广播、7-Eleven收银、居酒屋点单与中文解说视频专区。">
  <meta property="og:image" content="https://tokyoflow.app/assets/app_icon.jpg">
  <meta property="og:locale" content="zh_CN">
  <meta property="og:locale:alternate" content="en_US">

  <!-- Twitter Cards -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="TokyoFlow — Master Real-World Tokyo Japanese">
  <meta name="twitter:description" content="Immerse in authentic Tokyo situations. 4,170+ native human voices, pitch accent curves, video masterclasses, and scenario drills.">
  <meta name="twitter:image" content="https://tokyoflow.app/assets/app_icon.jpg">

  <!-- Favicon & Typography -->
  <link rel="icon" href="/assets/app_icon.jpg">
  <link rel="apple-touch-icon" href="/assets/app_icon.jpg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Shippori+Mincho:wght@500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  
  <link rel="stylesheet" href="/styles.css">

  <!-- JSON-LD Structured Data for Google SEO & GEO -->
  <script type="application/ld+json">
{schema_json}
  </script>
</head>
<body>

  <!-- Navigation Bar -->
  <header class="navbar">
    <div class="container nav-inner">
      <a href="/" class="brand-mark">
        <img src="/assets/app_icon.jpg" alt="TokyoFlow Icon" class="brand-icon" width="38" height="38">
        <div class="brand-text-group">
          <div class="brand-title">TOKYO<span>FLOW</span></div>
          <span class="brand-kanji">東京・文脈主導の日本語</span>
        </div>
      </a>

      <ul class="nav-links">
        <li><a href="#showcase">/01 现场实境</a></li>
        <li><a href="#academy">/02 中文影视专区</a></li>
        <li><a href="#pillars">/03 四大体系</a></li>
        <li><a href="#curriculum">/04 年间路线</a></li>
        <li><a href="#materials">/05 学习材料</a></li>
        <li><a href="#faq">/06 常见问题</a></li>
      </ul>

      <div class="nav-actions">
        <!-- Language Switcher -->
        <a href="/en/" class="lang-switch-btn" title="Switch to English Edition">
          <span class="lang-code-tag">[EN]</span>
          <span>English</span>
        </a>

        <div class="tokyo-live-badge">
          <span class="pulse-dot"></span>
          <span id="tokyo-clock">TOKYO --:-- JST</span>
        </div>

        <a href="https://www.youtube.com/@TokyoFlowJapan" target="_blank" rel="noopener" class="btn-nav-yt" title="前往 YouTube 官方频道">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
          <span>YouTube 频道</span>
        </a>

        <a href="#download" class="btn-nav-primary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 6.37c.61-.75 1.04-1.8 1.01-2.87-.96.04-2.13.65-2.79 1.43-.58.67-1.08 1.74-.95 2.78 1.07.08 2.14-.58 2.73-1.34z"/></svg>
          <span>下载 App</span>
          <span class="arrow-glyph">›</span>
        </a>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="hero">
    <div class="container">
      <div class="hero-header">
        <div class="hero-kicker-pill">
          <span>東京実境 · 現場情境リアルタイム</span>
        </div>

        <h1 class="hero-title-jp">東京を、<span>生きる日本語。</span></h1>
        
        <h2 class="hero-title-en">
          走出脱离语境的句式，在 <strong>东京真实空气</strong> 中掌握地道表达。
        </h2>

        <p class="hero-description">
          从山手线发车铃声与站台广播，到深夜居酒屋的热气与漫画拟声词。4,170+ 原声声库、标准声调高低走向图谱、中文解说影视专区与真实生活任务，全面重塑你的日语直觉。
        </p>

        <div class="hero-cta-group">
          <a href="https://www.youtube.com/@TokyoFlowJapan" target="_blank" rel="noopener" class="btn-hero-yt">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
            <span>订阅 YouTube 官方频道 (每日美东 20:00 中文首播)</span>
          </a>

          <a href="#academy" class="btn-hero-secondary">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M4 6h16v12H4z M2 4v16h20V4H2z M10 9v6l5-3z"/></svg>
            <span>浏览中文解说影视专区</span>
          </a>

          <a href="#download" class="btn-hero-appstore">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 6.37c.61-.75 1.04-1.8 1.01-2.87-.96.04-2.13.65-2.79 1.43-.58.67-1.08 1.74-.95 2.78 1.07.08 2.14-.58 2.73-1.34z"/></svg>
            <span>下载 iOS 版 App</span>
          </a>
        </div>

        <!-- Metrics Overview -->
        <div class="hero-metrics-bar">
          <div class="metric-item">
            <span class="metric-num">4,170+</span>
            <span class="metric-label">东京真人原声音频</span>
          </div>
          <div class="metric-item">
            <span class="metric-num">21+ 专集</span>
            <span class="metric-label">中文实景影视长片</span>
          </div>
          <div class="metric-item">
            <span class="metric-num">20:00 EDT</span>
            <span class="metric-label">中文频道每日定时首播</span>
          </div>
          <div class="metric-item">
            <span class="metric-num">N5 → N1</span>
            <span class="metric-label">JLPT 10,000+ 核心词库</span>
          </div>
          <div class="metric-item">
            <span class="metric-num">365 日</span>
            <span class="metric-label">CEFR-J 独立生活进阶</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Interactive Scenario Showcase -->
  <section id="showcase" class="showcase-section">
    <div class="container">
      <div class="showcase-wrapper">
        
        <!-- Left: Scenario Selector -->
        <div class="showcase-info">
          <div class="section-label-group">
            <span class="section-stamp">现场实境</span>
            <span class="mono-tag">实境与声调走向实验室</span>
          </div>

          <h3 class="showcase-title">
            随时置身于东京的空气与声音中。
          </h3>
          <p class="showcase-desc">
            点击下方不同场景，实时在右侧模拟机体验标准声调走向（平板/头高/中高/尾高）、敬语与口语语域切换及原生语速节奏。
          </p>

          <div class="scenario-selector">
            <div class="scenario-tab active" data-scenario="densha" onclick="switchScenario('densha')">
              <div class="tab-left">
                <div class="tab-icon-box">[电车]</div>
                <div class="tab-title-wrap">
                  <div class="tab-title">山手线站台广播</div>
                  <div class="tab-subtitle">新宿站 • 2号站台发车与黄线提示</div>
                </div>
              </div>
              <span class="tab-tag">敬语 · 站台</span>
            </div>

            <div class="scenario-tab" data-scenario="kombini" onclick="switchScenario('kombini')">
              <div class="tab-left">
                <div class="tab-icon-box">[便利店]</div>
                <div class="tab-title-wrap">
                  <div class="tab-title">便利店3秒极速收银</div>
                  <div class="tab-subtitle">涩谷中心街 • 加热与袋子选择</div>
                </div>
              </div>
              <span class="tab-tag">接客 · 礼貌</span>
            </div>

            <div class="scenario-tab" data-scenario="izakaya" onclick="switchScenario('izakaya')">
              <div class="tab-left">
                <div class="tab-icon-box">[酒场]</div>
                <div class="tab-title-wrap">
                  <div class="tab-title">回忆横丁居酒屋点单</div>
                  <div class="tab-subtitle">昭和小巷 • 烤鸡串与生啤开场</div>
                </div>
              </div>
              <span class="tab-tag">日常 · 口语</span>
            </div>

            <div class="scenario-tab" data-scenario="akiba" onclick="switchScenario('akiba')">
              <div class="tab-left">
                <div class="tab-icon-box">[动漫]</div>
                <div class="tab-title-wrap">
                  <div class="tab-title">秋叶原模型与漫画拟声词</div>
                  <div class="tab-subtitle">无线电会馆 • 展柜询问与原版阅读</div>
                </div>
              </div>
              <span class="tab-tag">兴趣 · 俗语</span>
            </div>
          </div>
        </div>

        <!-- Right: Interactive iPhone Mockup -->
        <div class="phone-mockup-wrapper">
          <div class="iphone-frame">
            <div class="dynamic-island">
              <div class="camera-lens"></div>
              <div class="island-mic"></div>
            </div>

            <div class="phone-screen" id="phoneScreen">
              <div class="app-top-header">
                <span class="app-badge-level" id="appLevel">JLPT N4-N3 • 交通实境</span>
                <span class="app-register-tag" id="appRegister">敬语（Keigo）</span>
              </div>

              <div class="app-scenario-card">
                <div class="app-district-row">
                  <span class="district-marker">[地点]</span>
                  <span id="appDistrictName">新宿站 • 2号站台</span>
                </div>

                <div class="app-japanese-phrase" id="appJpText">
                  まもなく、2番線に山手線がまいります。黄色い点字ブロックの内侧までお下がりください。
                </div>

                <div class="app-romaji-phrase" id="appRomajiText">
                  Mamonaku, ni-ban-sen ni Yamanote-sen ga mairimasu.
                </div>

                <div class="app-english-phrase" id="appEnText">
                  山手线电车即将到达2号站台，请退至黄色盲道内侧等候。
                </div>

                <!-- Pitch Accent Curve -->
                <div class="pitch-accent-box">
                  <div class="pitch-label">
                    <span>标准东京声调走向</span>
                    <span id="pitchPatternName">中高型（高音落在中间）</span>
                  </div>
                  <svg class="pitch-curve-svg" viewBox="0 0 200 30" preserveAspectRatio="none">
                    <path id="pitchPath" d="M 10 20 Q 50 5 100 8 T 190 22" fill="none" stroke="#BC382C" stroke-width="2.5" stroke-linecap="round"/>
                    <circle id="pitchDot1" cx="20" cy="18" r="3.5" fill="#fff" stroke="#BC382C" stroke-width="1.5"/>
                    <circle id="pitchDot2" cx="70" cy="8" r="3.5" fill="#BC382C"/>
                    <circle id="pitchDot3" cx="130" cy="12" r="3.5" fill="#BC382C"/>
                    <circle id="pitchDot4" cx="180" cy="22" r="3.5" fill="#fff" stroke="#BC382C" stroke-width="1.5"/>
                  </svg>
                </div>
              </div>

              <!-- Waveform -->
              <div class="app-waveform-bar" id="waveformContainer">
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
              </div>

              <!-- Play Button -->
              <button class="app-play-button" id="appPlayBtn" onclick="playActiveScenarioAudio()">
                <span id="appPlayIcon">▶</span>
                <span id="appPlayLabel">试听东京真人原声音频</span>
              </button>
            </div>
          </div>
        </div>

      </div>
    </div>
  </section>

  <!-- YouTube Academy & Playlist Hub (Chinese Edition) -->
  <section id="academy" class="academy-section">
    <div class="container">
      
      <!-- YouTube Channel Spotlight Banner -->
      <div class="yt-channel-banner">
        <div class="yt-banner-left">
          <div class="yt-live-pill">
            <span class="pulse-dot"></span>
            <span>YOUTUBE 官方中文专区 · 每日 20:00 EDT 首播</span>
          </div>
          <h2 class="yt-banner-title">TokyoFlow 日语实景影视专区【中文解说版】</h2>
          <p class="yt-banner-desc">
            全网首创东京实景影视级精讲。结合 4K 真实街景、纯正东京真人原声与 3-tier 振假名卡拉OK高亮。所有中文专集均已同步排期，支持在 YouTube 设定开播提醒。
          </p>
          <div class="yt-schedule-tags">
            <span class="sched-tag">美东 20:00 (北京次日 08:00) 定时首播</span>
            <span class="sched-tag">中文地道语法与文化解说</span>
            <span class="sched-tag">4K 现场实景照片背景</span>
            <span class="sched-tag">3-Tier 振假名对照</span>
          </div>
        </div>
        <div class="yt-banner-right">
          <a href="https://www.youtube.com/@TokyoFlowJapan?sub_confirmation=1" target="_blank" rel="noopener" class="btn-yt-subscribe">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
            <span>一键订阅 YouTube 频道 (开启铃铛)</span>
          </a>
        </div>
      </div>

      <!-- Release Schedule Notice -->
      <div class="schedule-notice-bar">
        <span class="notice-badge">[首播排期说明]</span>
        <span class="notice-text">下方专集卡片均已接入官方中文版 YouTube 链接与中文 4K 封面。<strong>已公开视频</strong>可直接播放，<strong>排期首播视频</strong>显示具体公映日期与时间，点击可前往 YouTube 预约开播提醒！</span>
      </div>

      <!-- Playlist Filter Bar -->
      <div class="playlist-filter-bar">
        <button class="filter-pill active" data-filter="all" onclick="filterAcademy('all')">全部专集 ({len(MASTERCLASSES)})</button>
        <button class="filter-pill" data-filter="transit" onclick="filterAcademy('transit')">交通出行 [山手线/地铁/新干线]</button>
        <button class="filter-pill" data-filter="daily" onclick="filterAcademy('daily')">生活便利 [便利店/快递/超市/药妆]</button>
        <button class="filter-pill" data-filter="food" onclick="filterAcademy('food')">美食酒场 [居酒屋/拉面/吉野家/咖啡]</button>
        <button class="filter-pill" data-filter="culture" onclick="filterAcademy('culture')">文化兴趣 [秋叶原/银座/桑拿/钱汤]</button>
        <button class="filter-pill" data-filter="compilation" onclick="filterAcademy('compilation')">全景合辑 & 电影大师课</button>
      </div>

      <!-- Masterclasses Grid -->
      <div class="video-cards-grid" id="videoGrid">
{video_cards}
      </div>

      <!-- Shorts Shadowing Showcase (Chinese Edition) -->
      <div class="shorts-section-wrap">
        <div class="shorts-header">
          <div>
            <div class="section-stamp">快速跟读</div>
            <h3 class="shorts-title">9:16 竖屏影子跟读挑战【中文解说版】</h3>
            <p class="shorts-desc">每天 30 秒，跟随东京原声极速跟读，校准音调与脱口直觉。点击直达中文 Shorts 播放与排期页面。</p>
          </div>
          <a href="https://www.youtube.com/@TokyoFlowJapan/shorts" target="_blank" rel="noopener" class="btn-shorts-all">
            <span>浏览全部 YouTube Shorts</span>
            <span>›</span>
          </a>
        </div>

        <div class="shorts-grid">
{shorts_cards}
        </div>
      </div>

    </div>
  </section>

  <!-- Four Core Learning Pillars -->
  <section id="pillars" class="pillars-section">
    <div class="container">
      <div class="editorial-header">
        <div class="mono-tag">[ 四大核心学习体系 ]</div>
        <h2 class="editorial-heading">TokyoFlow 四大学习体系</h2>
        <p class="hero-description">专为真正掌握日本实用口语与文化融入设计的四大核心支柱。</p>
      </div>

      <div class="pillars-grid">
        <div class="pillar-card">
          <div class="pillar-top">
            <span class="pillar-number">体系 01</span>
            <span class="pillar-stamp">[声库走向]</span>
          </div>
          <div>
            <div class="pillar-title-jp">4,170+ 本地真人原声与声调走向图</div>
            <div class="pillar-title-en">东京本地真人高保真声库与 Pitch Accent 可视化</div>
            <p class="pillar-desc">
              每一个词汇与生活对话均由东京本地人录制，配合精确到假名音节的高低音走向图谱（頭高、中高、尾高、平板），彻底根除外国学习者的平调发音。
            </p>
          </div>
          <div class="pillar-tags">
            <span class="pillar-tag">东京标准音调</span>
            <span class="pillar-tag">高低走向曲线</span>
            <span class="pillar-tag">毫秒级卡拉OK高亮</span>
          </div>
        </div>

        <div class="pillar-card">
          <div class="pillar-top">
            <span class="pillar-number">体系 02</span>
            <span class="pillar-stamp">[电台影子]</span>
          </div>
          <div>
            <div class="pillar-title-jp">NHK 新闻与电台影子跟读播放器</div>
            <div class="pillar-title-en">真实广播流与多档变速影子跟读</div>
            <p class="pillar-desc">
              沉浸式听取地道新闻广播。词词对照的振假名标注、点击即查释义与 0.8x 至 1.5x 多档变速听力理解诊断。
            </p>
          </div>
          <div class="pillar-tags">
            <span class="pillar-tag">多档变速 (0.8x - 1.5x)</span>
            <span class="pillar-tag">无障碍影子跟读</span>
            <span class="pillar-tag">每日高频更新</span>
          </div>
        </div>

        <div class="pillar-card">
          <div class="pillar-top">
            <span class="pillar-number">体系 03</span>
            <span class="pillar-stamp">[漫画拟声]</span>
          </div>
          <div>
            <div class="pillar-title-jp">漫画拟声词与拟态语实验室</div>
            <div class="pillar-title-en">500+ 漫画拟声拟态与文化音效互动板</div>
            <p class="pillar-desc">
              收录 500+ 漫画情感与动作音效（ドキドキ、ざわ…、ドドド），轻松读懂少年、青年原版单行本与动画台词。
            </p>
          </div>
          <div class="pillar-tags">
            <span class="pillar-tag">文化媒体艺术库</span>
            <span class="pillar-tag">拟声拟态分类</span>
            <span class="pillar-tag">交互式音效板</span>
          </div>
        </div>

        <div class="pillar-card">
          <div class="pillar-top">
            <span class="pillar-number">体系 04</span>
            <span class="pillar-stamp">[记忆算法]</span>
          </div>
          <div>
            <div class="pillar-title-jp">JLPT [N5-N1] SuperMemo SM-2 记忆引擎</div>
            <div class="pillar-title-en">10,000+ 核心词汇与科学间隔遗忘曲线</div>
            <p class="pillar-desc">
              基于 SuperMemo SM-2 算法的闪卡复习系统，智能捕捉弱项词汇并自动安排回捞复习，汉字笔顺动画一应俱全。
            </p>
          </div>
          <div class="pillar-tags">
            <span class="pillar-tag">N5-N1 全量词库</span>
            <span class="pillar-tag">汉字笔顺演示</span>
            <span class="pillar-tag">SM-2 遗忘曲线</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 1-Year Curriculum Roadmap -->
  <section id="curriculum" class="roadmap-section">
    <div class="container">
      <div class="editorial-header">
        <div class="mono-tag">[ 365 日独立生活进阶路线 ]</div>
        <h2 class="editorial-heading">Japan Foundation (CEFR-J) 年间学习路线</h2>
        <p class="hero-description">以在东京独立生活与顺畅沟通为目标的阶段进阶指南。</p>
      </div>

      <div class="roadmap-grid">
        <div class="roadmap-card">
          <span class="roadmap-q-badge">第一季度 • DAYS 1–90</span>
          <div class="roadmap-level-title">JF A1 • [JLPT N5]</div>
          <div class="roadmap-level-sub">东京生存必备 · 抵日安居</div>
          <ul class="roadmap-list">
            <li>交通：Suica 充值与闸机应对</li>
            <li>便利店：便当加热与购物袋选择</li>
            <li>餐饮：拉面自动贩卖机与个性定制</li>
            <li>漫画：基础热血音效与拟声词</li>
          </ul>
        </div>

        <div class="roadmap-card">
          <span class="roadmap-q-badge">第二季度 • DAYS 91–180</span>
          <div class="roadmap-level-title">JF A2 • [JLPT N4]</div>
          <div class="roadmap-level-sub">城市探索 · 日常交往与生活习惯</div>
          <ul class="roadmap-list">
            <li>百货：试衣、退税与尺码咨询</li>
            <li>出行：地铁各停急行与精算机补票</li>
            <li>咖啡：席位预约与换奶定制</li>
            <li>物流：日本邮政不在票再投递</li>
          </ul>
        </div>

        <div class="roadmap-card">
          <span class="roadmap-q-badge">第三季度 • DAYS 181–270</span>
          <div class="roadmap-level-title">JF A2-B1 • [JLPT N3]</div>
          <div class="roadmap-level-sub">深度融入 · 公共办事与社交文化</div>
          <ul class="roadmap-list">
            <li>居酒屋：烤串生啤开场与顺畅买单</li>
            <li>公共：传统钱汤与温泉入浴礼仪</li>
            <li>交通：新干线富士山侧指定席订票</li>
            <li>医疗：药妆店止痛药与症状描述</li>
          </ul>
        </div>

        <div class="roadmap-card">
          <span class="roadmap-q-badge">第四季度 • DAYS 271–365</span>
          <div class="roadmap-level-title">JF B1-B2 • [JLPT N2-N1]</div>
          <div class="roadmap-level-sub">独立自如 · 影视鉴赏与深度理解</div>
          <ul class="roadmap-list">
            <li>影视：院线电影深度台词鉴赏</li>
            <li>新闻：NHK 原生广播与时事速递</li>
            <li>职场：常用商务寒暄与敬语分寸</li>
            <li>漫画：无振假名单行本顺畅通读</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- Study Materials Section -->
  <section id="materials" class="materials-section">
    <div class="container">
      <div class="editorial-header">
        <div class="mono-tag">[ 学习材料与核心资源 ]</div>
        <h2 class="editorial-heading">TokyoFlow 学习资料与精讲包</h2>
        <p class="hero-description">配合 YouTube 剧集与 App 的核心学习材料，提供完整的假名对照与声调走向图。</p>
      </div>

      <div class="materials-grid">
        <div class="material-card">
          <div class="material-tag">[PDF 讲义]</div>
          <h3 class="material-title">东京实景对话精讲台本 (EP.01 - EP.19)</h3>
          <p class="material-desc">包含 19 个实景对话的 3-tier 振假名、罗马音、语法剖析与词汇清单。</p>
          <a href="https://www.youtube.com/@TokyoFlowJapan" target="_blank" rel="noopener" class="btn-material-link">
            <span>在 YouTube 视频简介区查看</span>
            <span>›</span>
          </a>
        </div>

        <div class="material-card">
          <div class="material-tag">[音调图谱]</div>
          <h3 class="material-title">东京标准声调走向核心手册 (4大模式)</h3>
          <p class="material-desc">头高型、中高型、尾高型与平板型完整走向规律与真人发音比对表。</p>
          <a href="#showcase" class="btn-material-link">
            <span>在上方模拟器体验</span>
            <span>›</span>
          </a>
        </div>

        <div class="material-card">
          <div class="material-tag">[词库体系]</div>
          <h3 class="material-title">JLPT N5-N1 10,000+ 高频词库闪卡</h3>
          <p class="material-desc">基于 SM-2 科学间隔曲线，包含例句真人音频、汉字笔顺动画与高频考点。</p>
          <a href="#download" class="btn-material-link">
            <span>在 TokyoFlow App 中复习</span>
            <span>›</span>
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- FAQ Section (GEO / SEO Schema Rich Snippets) -->
  <section id="faq" class="faq-section">
    <div class="container">
      <div class="editorial-header">
        <div class="mono-tag">[ 常见问题解答 ]</div>
        <h2 class="editorial-heading">关于 TokyoFlow 的常见疑问</h2>
        <p class="hero-description">了解高语境学习法、声调走向图与影视化学习的核心原理。</p>
      </div>

      <div class="faq-container">
{faq_html}
      </div>
    </div>
  </section>

  <!-- Download & Subscribe Dual CTA Section -->
  <section id="download" class="download-section">
    <div class="container">
      <div class="download-box">
        <div class="download-box-inner">
          <div class="section-stamp" style="display: inline-block; margin-bottom: 1.5rem;">TOKYOFLOW</div>
          <h2 class="download-box-title">東京の息遣いを、あなたの手の中に。</h2>
          <p class="download-box-p">
            前往 Apple App Store 下载 TokyoFlow，并在 YouTube 订阅每日视频更新。在 4,170+ 本地真人原声与真实东京场景中，开启鲜活的日语之旅。
          </p>

          <div class="download-actions-wrap">
            <a href="https://www.youtube.com/@TokyoFlowJapan?sub_confirmation=1" target="_blank" rel="noopener" class="btn-hero-yt">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
              <span>订阅 YouTube 频道 (开启首播通知)</span>
            </a>

            <a href="#" class="btn-hero-appstore">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 6.37c.61-.75 1.04-1.8 1.01-2.87-.96.04-2.13.65-2.79 1.43-.58.67-1.08 1.74-.95 2.78 1.07.08 2.14-.58 2.73-1.34z"/></svg>
              <span>下载 iOS App</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Site Footer -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-inner">
        <div class="footer-brand-info">
          <div class="footer-brand-title">TokyoFlow · 東京フロウ</div>
          <div class="footer-brand-tagline">东京高语境实景日语学习体系 · 中文解说影视专区</div>
        </div>

        <div class="footer-links-group">
          <a href="/privacy/">隐私政策</a>
          <a href="/terms/">服务条款</a>
          <a href="/support/">技术支持</a>
          <a href="/en/">English Edition</a>
          <a href="https://www.youtube.com/@TokyoFlowJapan" target="_blank" rel="noopener">YouTube 频道</a>
          <a href="mailto:support@tokyoflow.app">联系我们</a>
        </div>

        <div class="footer-copyright">
          <span>© 2026 TokyoFlow. 传承 · 创新 · 语境驱动</span>
          <span>Tokyo Cultural Living Japanese & Video Academy</span>
        </div>
      </div>
    </div>
  </footer>

  <script src="/app.js"></script>
</body>
</html>
"""
    assert_zero_emoji(html, "site/index.html")
    return html

def build_english_page():
    video_cards = generate_video_cards_html("en")
    shorts_cards = generate_shorts_cards_html("en")
    faq_html = generate_faq_html("en")
    schema_json = build_schema_json("en")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <title>TokyoFlow — Master Living Japanese in Tokyo's Living Atmosphere | Video Academy</title>
  <meta name="description" content="Move beyond decontextualized textbook Japanese. TokyoFlow is a situational, high-context Japanese mastery system with 4,170+ native audio tracks, Yamanote Line broadcasts, 7-Eleven register speed drills, and visual pitch accent curves.">
  <meta name="keywords" content="TokyoFlow, Learn Japanese, Tokyo Japanese, Japanese Shadowing, Pitch Accent, Yamanote Line, Japanese Audio, JLPT N5 N4 N3 N2 N1, Japanese Immersion, YouTube Japanese">
  <meta name="author" content="TokyoFlow Team">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="theme-color" content="#F8F6F0">
  <link rel="canonical" href="https://tokyoflow.app/en/">

  <!-- GEO & Multi-Language Hreflang Tags -->
  <link rel="alternate" hreflang="zh-Hans" href="https://tokyoflow.app/">
  <link rel="alternate" hreflang="zh-CN" href="https://tokyoflow.app/">
  <link rel="alternate" hreflang="en" href="https://tokyoflow.app/en/">
  <link rel="alternate" hreflang="x-default" href="https://tokyoflow.app/">

  <!-- Open Graph / Social Meta -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="TokyoFlow">
  <meta property="og:url" content="https://tokyoflow.app/en/">
  <meta property="og:title" content="TokyoFlow · Master Living Japanese in Context">
  <meta property="og:description" content="Immerse in authentic Tokyo situations. 4,170+ native human voices, visual pitch accent curves, video masterclasses, and real-world audio.">
  <meta property="og:image" content="https://tokyoflow.app/assets/app_icon.jpg">
  <meta property="og:locale" content="en_US">
  <meta property="og:locale:alternate" content="zh_CN">

  <!-- Twitter Cards -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="TokyoFlow — Master Real-World Tokyo Japanese">
  <meta name="twitter:description" content="Immerse in authentic Tokyo situations. 4,170+ native human voices, pitch accent curves, and scenario drills.">
  <meta name="twitter:image" content="https://tokyoflow.app/assets/app_icon.jpg">

  <!-- Favicon & Typography -->
  <link rel="icon" href="/assets/app_icon.jpg">
  <link rel="apple-touch-icon" href="/assets/app_icon.jpg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Shippori+Mincho:wght@500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  
  <link rel="stylesheet" href="/styles.css">

  <!-- JSON-LD Structured Data for Google SEO & GEO -->
  <script type="application/ld+json">
{schema_json}
  </script>
</head>
<body>

  <!-- Navigation Bar -->
  <header class="navbar">
    <div class="container nav-inner">
      <a href="/en/" class="brand-mark">
        <img src="/assets/app_icon.jpg" alt="TokyoFlow Icon" class="brand-icon" width="38" height="38">
        <div class="brand-text-group">
          <div class="brand-title">TOKYO<span>FLOW</span></div>
          <span class="brand-kanji">東京・文脈主导の日本語</span>
        </div>
      </a>

      <ul class="nav-links">
        <li><a href="#showcase">/01 Situations</a></li>
        <li><a href="#academy">/02 Video Academy</a></li>
        <li><a href="#pillars">/03 Core System</a></li>
        <li><a href="#curriculum">/04 Roadmap</a></li>
        <li><a href="#materials">/05 Materials</a></li>
        <li><a href="#faq">/06 FAQ</a></li>
      </ul>

      <div class="nav-actions">
        <!-- Language Switcher -->
        <a href="/" class="lang-switch-btn" title="切换到中文版">
          <span class="lang-code-tag">[ZH]</span>
          <span>中文</span>
        </a>

        <div class="tokyo-live-badge">
          <span class="pulse-dot"></span>
          <span id="tokyo-clock">TOKYO --:-- JST</span>
        </div>

        <a href="https://www.youtube.com/@TokyoFlowJapan" target="_blank" rel="noopener" class="btn-nav-yt" title="TokyoFlow on YouTube">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
          <span>YouTube</span>
        </a>

        <a href="#download" class="btn-nav-primary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 6.37c.61-.75 1.04-1.8 1.01-2.87-.96.04-2.13.65-2.79 1.43-.58.67-1.08 1.74-.95 2.78 1.07.08 2.14-.58 2.73-1.34z"/></svg>
          <span>Download App</span>
          <span class="arrow-glyph">›</span>
        </a>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="hero">
    <div class="container">
      <div class="hero-header">
        <div class="hero-kicker-pill">
          <span>TOKYO LIVING · HIGH-CONTEXT IMMERSION</span>
        </div>

        <h1 class="hero-title-jp">東京を、<span>生きる日本語。</span></h1>
        
        <h2 class="hero-title-en">
          Step beyond artificial textbook dialogues. Master living Japanese in <strong>Tokyo's authentic atmosphere</strong>.
        </h2>

        <p class="hero-description">
          From Yamanote Line departure melodies to late-night izakayas and manga sound effects. 4,170+ native audio tracks, visual pitch accent curves, video masterclasses, and real-life missions designed to rewire your natural speaking reflex.
        </p>

        <div class="hero-cta-group">
          <a href="https://www.youtube.com/@TokyoFlowJapan" target="_blank" rel="noopener" class="btn-hero-yt">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
            <span>Subscribe on YouTube (Daily 08:00 AM EDT Releases)</span>
          </a>

          <a href="#academy" class="btn-hero-secondary">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M4 6h16v12H4z M2 4v16h20V4H2z M10 9v6l5-3z"/></svg>
            <span>Explore Video Academy</span>
          </a>

          <a href="#download" class="btn-hero-appstore">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 6.37c.61-.75 1.04-1.8 1.01-2.87-.96.04-2.13.65-2.79 1.43-.58.67-1.08 1.74-.95 2.78 1.07.08 2.14-.58 2.73-1.34z"/></svg>
            <span>Download for iOS</span>
          </a>
        </div>

        <!-- Metrics Overview -->
        <div class="hero-metrics-bar">
          <div class="metric-item">
            <span class="metric-num">4,170+</span>
            <span class="metric-label">Tokyo Native Audio Tracks</span>
          </div>
          <div class="metric-item">
            <span class="metric-num">21+ Masterclasses</span>
            <span class="metric-label">Cinematic Video Lessons</span>
          </div>
          <div class="metric-item">
            <span class="metric-num">08:00 AM EDT</span>
            <span class="metric-label">Daily Global Premieres</span>
          </div>
          <div class="metric-item">
            <span class="metric-num">N5 → N1</span>
            <span class="metric-label">JLPT 10,000+ Core Lexicon</span>
          </div>
          <div class="metric-item">
            <span class="metric-num">365 Days</span>
            <span class="metric-label">CEFR-J Living Curriculum</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Interactive Scenario Showcase -->
  <section id="showcase" class="showcase-section">
    <div class="container">
      <div class="showcase-wrapper">
        
        <!-- Left: Scenario Selector -->
        <div class="showcase-info">
          <div class="section-label-group">
            <span class="section-stamp">LIVE LAB</span>
            <span class="mono-tag">Situational Pitch Accent Laboratory</span>
          </div>

          <h3 class="showcase-title">
            Immerse in Tokyo's Living Voice and Atmosphere.
          </h3>
          <p class="showcase-desc">
            Select a real scenario below to experience standard Tokyo pitch accent curves (Heiban / Atamadaka / Nakadaka / Odaka), register switching, and native cadence on the interactive device.
          </p>

          <div class="scenario-selector">
            <div class="scenario-tab active" data-scenario="densha" onclick="switchScenario('densha')">
              <div class="tab-left">
                <div class="tab-icon-box">[Transit]</div>
                <div class="tab-title-wrap">
                  <div class="tab-title">Yamanote Line Platform</div>
                  <div class="tab-subtitle">Shinjuku Station • Track 2 Melody & Braille Line</div>
                </div>
              </div>
              <span class="tab-tag">Keigo · Platform</span>
            </div>

            <div class="scenario-tab" data-scenario="kombini" onclick="switchScenario('kombini')">
              <div class="tab-left">
                <div class="tab-icon-box">[Kombini]</div>
                <div class="tab-title-wrap">
                  <div class="tab-title">7-Eleven Rapid Checkout</div>
                  <div class="tab-subtitle">Shibuya Center-Gai • Microwave & Bag Options</div>
                </div>
              </div>
              <span class="tab-tag">Service · Polite</span>
            </div>

            <div class="scenario-tab" data-scenario="izakaya" onclick="switchScenario('izakaya')">
              <div class="tab-left">
                <div class="tab-icon-box">[Izakaya]</div>
                <div class="tab-title-wrap">
                  <div class="tab-title">Omoide Yokocho Izakaya</div>
                  <div class="tab-subtitle">Showa Alley • Toriaezu Nama & Yakitori</div>
                </div>
              </div>
              <span class="tab-tag">Casual · Colloquial</span>
            </div>

            <div class="scenario-tab" data-scenario="akiba" onclick="switchScenario('akiba')">
              <div class="tab-left">
                <div class="tab-icon-box">[Anime]</div>
                <div class="tab-title-wrap">
                  <div class="tab-title">Akihabara Figure & Manga SFX</div>
                  <div class="tab-subtitle">Radio Kaikan • Stock Inquiry & Onomatopoeia</div>
                </div>
              </div>
              <span class="tab-tag">Pop · Slang</span>
            </div>
          </div>
        </div>

        <!-- Right: Interactive iPhone Mockup -->
        <div class="phone-mockup-wrapper">
          <div class="iphone-frame">
            <div class="dynamic-island">
              <div class="camera-lens"></div>
              <div class="island-mic"></div>
            </div>

            <div class="phone-screen" id="phoneScreen">
              <div class="app-top-header">
                <span class="app-badge-level" id="appLevel">JLPT N4-N3 • TRANSIT</span>
                <span class="app-register-tag" id="appRegister">Keigo (Honorific)</span>
              </div>

              <div class="app-scenario-card">
                <div class="app-district-row">
                  <span class="district-marker">[LOCATION]</span>
                  <span id="appDistrictName">Shinjuku Station • Track 2</span>
                </div>

                <div class="app-japanese-phrase" id="appJpText">
                  まもなく、2番線に山手線がまいります。黄色い点字ブロックの内側までお下がりください。
                </div>

                <div class="app-romaji-phrase" id="appRomajiText">
                  Mamonaku, ni-ban-sen ni Yamanote-sen ga mairimasu.
                </div>

                <div class="app-english-phrase" id="appEnText">
                  The Yamanote Line train will soon arrive at Track 2. Please wait behind the yellow line.
                </div>

                <!-- Pitch Accent Curve -->
                <div class="pitch-accent-box">
                  <div class="pitch-label">
                    <span>Standard Tokyo Pitch Contour</span>
                    <span id="pitchPatternName">Nakadaka (Mid-High Peak)</span>
                  </div>
                  <svg class="pitch-curve-svg" viewBox="0 0 200 30" preserveAspectRatio="none">
                    <path id="pitchPath" d="M 10 20 Q 50 5 100 8 T 190 22" fill="none" stroke="#BC382C" stroke-width="2.5" stroke-linecap="round"/>
                    <circle id="pitchDot1" cx="20" cy="18" r="3.5" fill="#fff" stroke="#BC382C" stroke-width="1.5"/>
                    <circle id="pitchDot2" cx="70" cy="8" r="3.5" fill="#BC382C"/>
                    <circle id="pitchDot3" cx="130" cy="12" r="3.5" fill="#BC382C"/>
                    <circle id="pitchDot4" cx="180" cy="22" r="3.5" fill="#fff" stroke="#BC382C" stroke-width="1.5"/>
                  </svg>
                </div>
              </div>

              <!-- Waveform -->
              <div class="app-waveform-bar" id="waveformContainer">
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
              </div>

              <!-- Play Button -->
              <button class="app-play-button" id="appPlayBtn" onclick="playActiveScenarioAudio()">
                <span id="appPlayIcon">▶</span>
                <span id="appPlayLabel">Play Tokyo Native Audio</span>
              </button>
            </div>
          </div>
        </div>

      </div>
    </div>
  </section>

  <!-- YouTube Academy & Playlist Hub -->
  <section id="academy" class="academy-section">
    <div class="container">
      
      <!-- YouTube Channel Spotlight Banner -->
      <div class="yt-channel-banner">
        <div class="yt-banner-left">
          <div class="yt-live-pill">
            <span class="pulse-dot"></span>
            <span>OFFICIAL YOUTUBE CHANNEL · DAILY 08:00 AM EDT RELEASES</span>
          </div>
          <h2 class="yt-banner-title">TokyoFlow Video Academy [Global Edition]</h2>
          <p class="yt-banner-desc">
            Cinematic Japanese lessons filmed and deconstructed across real Tokyo districts. Full HD 1080p, 3-tier Ruby karaoke alignment, and native pitch accent breakdowns.
          </p>
          <div class="yt-schedule-tags">
            <span class="sched-tag">08:00 AM EDT Daily Release</span>
            <span class="sched-tag">1080p 60fps Master Quality</span>
            <span class="sched-tag">3-Tier Ruby Transcripts</span>
          </div>
        </div>
        <div class="yt-banner-right">
          <a href="https://www.youtube.com/@TokyoFlowJapan?sub_confirmation=1" target="_blank" rel="noopener" class="btn-yt-subscribe">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
            <span>Subscribe on YouTube</span>
          </a>
        </div>
      </div>

      <!-- Schedule Notice -->
      <div class="schedule-notice-bar">
        <span class="notice-badge">[RELEASE SCHEDULE]</span>
        <span class="notice-text">Each lesson card indicates whether it is <strong>LIVE NOW</strong> or displays its <strong>Scheduled Premiere Date & Time</strong>. Click any card to watch now or set a premiere reminder on YouTube.</span>
      </div>

      <!-- Playlist Filter Bar -->
      <div class="playlist-filter-bar">
        <button class="filter-pill active" data-filter="all" onclick="filterAcademy('all')">All Episodes ({len(MASTERCLASSES)})</button>
        <button class="filter-pill" data-filter="transit" onclick="filterAcademy('transit')">Transit [Yamanote / Subway / Shinkansen]</button>
        <button class="filter-pill" data-filter="daily" onclick="filterAcademy('daily')">Daily Survival [Kombini / Mail / Supermarket / Pharmacy]</button>
        <button class="filter-pill" data-filter="food" onclick="filterAcademy('food')">Dining & Izakaya [Ramen / Yakitori / Gyudon / Cafe]</button>
        <button class="filter-pill" data-filter="culture" onclick="filterAcademy('culture')">Culture & Etiquette [Akiba / Ginza / Sauna / Onsen]</button>
        <button class="filter-pill" data-filter="compilation" onclick="filterAcademy('compilation')">Mega Marathons & Cinema</button>
      </div>

      <!-- Masterclasses Grid -->
      <div class="video-cards-grid" id="videoGrid">
{video_cards}
      </div>

      <!-- Shorts Shadowing Showcase -->
      <div class="shorts-section-wrap">
        <div class="shorts-header">
          <div>
            <div class="section-stamp">SHADOWING HUB</div>
            <h3 class="shorts-title">9:16 Vertical Interactive Shorts [English Edition]</h3>
            <p class="shorts-desc">30-second rapid shadowing callouts with native Tokyo pronunciation.</p>
          </div>
          <a href="https://www.youtube.com/@TokyoFlowJapan/shorts" target="_blank" rel="noopener" class="btn-shorts-all">
            <span>Explore All YouTube Shorts</span>
            <span>›</span>
          </a>
        </div>

        <div class="shorts-grid">
{shorts_cards}
        </div>
      </div>

    </div>
  </section>

  <!-- Four Core Learning Pillars -->
  <section id="pillars" class="pillars-section">
    <div class="container">
      <div class="editorial-header">
        <div class="mono-tag">[ SYSTEM ARCHITECTURE ]</div>
        <h2 class="editorial-heading">The Four Core Learning Pillars</h2>
        <p class="hero-description">Four foundational disciplines engineered to transition you from textbook rules to instinctive speaking.</p>
      </div>

      <div class="pillars-grid">
        <div class="pillar-card">
          <div class="pillar-top">
            <span class="pillar-number">PILLAR 01</span>
            <span class="pillar-stamp">[PITCH ENGINE]</span>
          </div>
          <div>
            <div class="pillar-title-jp">4,170+ Native Voicebank & Pitch Visualizer</div>
            <div class="pillar-title-en">Tokyo Native Human Voicebank with Pitch Accent Contours</div>
            <p class="pillar-desc">
              Every phrase is voiced by Tokyo natives and mapped to visual pitch accent curves (Atamadaka, Nakadaka, Odaka, Heiban), eliminating flat unnatural intonations.
            </p>
          </div>
          <div class="pillar-tags">
            <span class="pillar-tag">Standard Tokyo Intonation</span>
            <span class="pillar-tag">Visual Pitch Curves</span>
            <span class="pillar-tag">Millisecond Karaoke Alignment</span>
          </div>
        </div>

        <div class="pillar-card">
          <div class="pillar-top">
            <span class="pillar-number">PILLAR 02</span>
            <span class="pillar-stamp">[NHK RADIO]</span>
          </div>
          <div>
            <div class="pillar-title-jp">NHK News & Studio Radio Shadowing Player</div>
            <div class="pillar-title-en">Authentic Broadcast Streams with Multi-Speed Control</div>
            <p class="pillar-desc">
              Immerse in daily news broadcasts with real-time furigana annotations, instant dictionary lookups, and 0.8x to 1.5x variable speed shadowing.
            </p>
          </div>
          <div class="pillar-tags">
            <span class="pillar-tag">Variable Speed (0.8x - 1.5x)</span>
            <span class="pillar-tag">Shadowing Engine</span>
            <span class="pillar-tag">Daily Updates</span>
          </div>
        </div>

        <div class="pillar-card">
          <div class="pillar-top">
            <span class="pillar-number">PILLAR 03</span>
            <span class="pillar-stamp">[MANGA SFX]</span>
          </div>
          <div>
            <div class="pillar-title-jp">Manga Onomatopoeia & Soundboard Lab</div>
            <div class="pillar-title-en">500+ Manga SFX, Emotional Cues & Cultural Audio</div>
            <p class="pillar-desc">
              Decode over 500 manga action and emotion sounds (Doki-Doki, Zawa..., Dododo) with an interactive soundboard to read raw Japanese manga with ease.
            </p>
          </div>
          <div class="pillar-tags">
            <span class="pillar-tag">Cultural Sound Library</span>
            <span class="pillar-tag">Onomatopoeia Categories</span>
            <span class="pillar-tag">Interactive Soundboard</span>
          </div>
        </div>

        <div class="pillar-card">
          <div class="pillar-top">
            <span class="pillar-number">PILLAR 04</span>
            <span class="pillar-stamp">[SM-2 RECALL]</span>
          </div>
          <div>
            <div class="pillar-title-jp">JLPT [N5-N1] SuperMemo SM-2 Memory Engine</div>
            <div class="pillar-title-en">10,000+ Core Words with Spaced Repetition Scheduling</div>
            <p class="pillar-desc">
              SuperMemo SM-2 spaced repetition flashcards algorithmically prioritize weak words, reinforced with Kanji stroke orders and native example audio.
            </p>
          </div>
          <div class="pillar-tags">
            <span class="pillar-tag">N5-N1 Full Lexicon</span>
            <span class="pillar-tag">Kanji Stroke Order</span>
            <span class="pillar-tag">SM-2 Algorithm</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 1-Year Curriculum Roadmap -->
  <section id="curriculum" class="roadmap-section">
    <div class="container">
      <div class="editorial-header">
        <div class="mono-tag">[ 365-DAY LIVING BLUEPRINT ]</div>
        <h2 class="editorial-heading">Japan Foundation (CEFR-J) Annual Roadmap</h2>
        <p class="hero-description">A phased roadmap engineered for independent living and confident communication in Tokyo.</p>
      </div>

      <div class="roadmap-grid">
        <div class="roadmap-card">
          <span class="roadmap-q-badge">QUARTER 1 • DAYS 1–90</span>
          <div class="roadmap-level-title">JF A1 • [JLPT N5]</div>
          <div class="roadmap-level-sub">Tokyo Arrival & Daily Survival</div>
          <ul class="roadmap-list">
            <li>Transit: Suica recharge & gate errors</li>
            <li>Kombini: Microwave heating & bag selection</li>
            <li>Dining: Ramen ticket machines & custom orders</li>
            <li>Manga: Basic battle onomatopoeia & SFX</li>
          </ul>
        </div>

        <div class="roadmap-card">
          <span class="roadmap-q-badge">QUARTER 2 • DAYS 91–180</span>
          <div class="roadmap-level-title">JF A2 • [JLPT N4]</div>
          <div class="roadmap-level-sub">City Exploration & Everyday Mobility</div>
          <ul class="roadmap-list">
            <li>Shopping: Fitting room permits & tax refunds</li>
            <li>Transit: Express trains & fare adjustment</li>
            <li>Cafe: Seating requests & milk substitutions</li>
            <li>Mail: Japan Post absence slips & redelivery</li>
          </ul>
        </div>

        <div class="roadmap-card">
          <span class="roadmap-q-badge">QUARTER 3 • DAYS 181–270</span>
          <div class="roadmap-level-title">JF A2-B1 • [JLPT N3]</div>
          <div class="roadmap-level-sub">Cultural Immersion & Conversational Depth</div>
          <ul class="roadmap-list">
            <li>Izakaya: Yakitori ordering & bill requests</li>
            <li>Public: Traditional sento & onsen etiquette</li>
            <li>Transit: Shinkansen Mt. Fuji window seat booking</li>
            <li>Health: Drugstore painkiller & symptom descriptions</li>
          </ul>
        </div>

        <div class="roadmap-card">
          <span class="roadmap-q-badge">QUARTER 4 • DAYS 271–365</span>
          <div class="roadmap-level-title">JF B1-B2 • [JLPT N2-N1]</div>
          <div class="roadmap-level-sub">Complete Independence & Nuanced Fluency</div>
          <ul class="roadmap-list">
            <li>Cinema: Blockbuster movie dialogue analysis</li>
            <li>News: Live NHK radio & current affairs</li>
            <li>Workplace: Natural business greetings & honorifics</li>
            <li>Manga: Raw unassisted tankōbon reading</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- Study Materials Section -->
  <section id="materials" class="materials-section">
    <div class="container">
      <div class="editorial-header">
        <div class="mono-tag">[ STUDY PACKS & DOWNLOADS ]</div>
        <h2 class="editorial-heading">TokyoFlow Learning Resources</h2>
        <p class="hero-description">Comprehensive companion guides, 3-tier ruby transcripts, and pitch accent references.</p>
      </div>

      <div class="materials-grid">
        <div class="material-card">
          <div class="material-tag">[PDF GUIDE]</div>
          <h3 class="material-title">Tokyo Scenario Dialogue Scripts (EP.01 - EP.19)</h3>
          <p class="material-desc">Complete 3-tier Ruby transcripts, Romaji, grammar points, and vocabulary lists for all 19 episodes.</p>
          <a href="https://www.youtube.com/@TokyoFlowJapan" target="_blank" rel="noopener" class="btn-material-link">
            <span>Available on YouTube Video Descriptions</span>
            <span>›</span>
          </a>
        </div>

        <div class="material-card">
          <div class="material-tag">[PITCH CHARTS]</div>
          <h3 class="material-title">Tokyo Standard Pitch Accent Reference Guide</h3>
          <p class="material-desc">Comprehensive pitch contour guide covering Heiban, Atamadaka, Nakadaka, and Odaka patterns.</p>
          <a href="#showcase" class="btn-material-link">
            <span>Test in Interactive Simulator</span>
            <span>›</span>
          </a>
        </div>

        <div class="material-card">
          <div class="material-tag">[JLPT DECKS]</div>
          <h3 class="material-title">JLPT N5-N1 10,000+ Flashcard Deck</h3>
          <p class="material-desc">Powered by SuperMemo SM-2 algorithm with native human audio, stroke order, and context sentences.</p>
          <a href="#download" class="btn-material-link">
            <span>Practice in TokyoFlow App</span>
            <span>›</span>
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- FAQ Section (GEO / SEO Schema Rich Snippets) -->
  <section id="faq" class="faq-section">
    <div class="container">
      <div class="editorial-header">
        <div class="mono-tag">[ FREQUENTLY ASKED QUESTIONS ]</div>
        <h2 class="editorial-heading">Questions About TokyoFlow</h2>
        <p class="hero-description">Learn about high-context learning, visual pitch contours, and our video academy workflow.</p>
      </div>

      <div class="faq-container">
{faq_html}
      </div>
    </div>
  </section>

  <!-- Download & Subscribe Dual CTA Section -->
  <section id="download" class="download-section">
    <div class="container">
      <div class="download-box">
        <div class="download-box-inner">
          <div class="section-stamp" style="display: inline-block; margin-bottom: 1.5rem;">TOKYOFLOW</div>
          <h2 class="download-box-title">Tokyo's Living Atmosphere, in Your Hands.</h2>
          <p class="download-box-p">
            Download TokyoFlow on the Apple App Store and subscribe to our daily video releases on YouTube. Master living Japanese in 4,170+ native audio tracks and real-world scenes.
          </p>

          <div class="download-actions-wrap">
            <a href="https://www.youtube.com/@TokyoFlowJapan?sub_confirmation=1" target="_blank" rel="noopener" class="btn-hero-yt">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
              <span>Subscribe on YouTube</span>
            </a>

            <a href="#" class="btn-hero-appstore">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 6.37c.61-.75 1.04-1.8 1.01-2.87-.96.04-2.13.65-2.79 1.43-.58.67-1.08 1.74-.95 2.78 1.07.08 2.14-.58 2.73-1.34z"/></svg>
              <span>Download for iOS</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Site Footer -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-inner">
        <div class="footer-brand-info">
          <div class="footer-brand-title">TokyoFlow · 東京フロウ</div>
          <div class="footer-brand-tagline">Tokyo Living Japanese Learning System & Video Academy</div>
        </div>

        <div class="footer-links-group">
          <a href="/en/privacy/">Privacy Policy</a>
          <a href="/en/terms/">Terms of Service</a>
          <a href="/en/support/">Support</a>
          <a href="/">中文版 (Chinese)</a>
          <a href="https://www.youtube.com/@TokyoFlowJapan" target="_blank" rel="noopener">YouTube Channel</a>
          <a href="mailto:support@tokyoflow.app">Contact Us</a>
        </div>

        <div class="footer-copyright">
          <span>© 2026 TokyoFlow. Heritage · Innovation · Context-Driven</span>
          <span>Tokyo Cultural Living Japanese & Video Academy</span>
        </div>
      </div>
    </div>
  </footer>

  <script src="/app.js"></script>
</body>
</html>
"""
    assert_zero_emoji(html, "site/en/index.html")
    return html

def build_app_js():
    js_content = """// TokyoFlow Interactive Experience Engine
// Zero Emoji Discipline Enforced

const SCENARIO_DATA = {
  zh: {
    densha: {
      level: "JLPT N4-N3 • 交通实境",
      register: "敬语・站台广播",
      districtName: "新宿站 • 2号站台",
      jpText: "まもなく、2番線に山手線がまいります。黄色い点字ブロックの内側までお下がりください。",
      romajiText: "Mamonaku, ni-ban-sen ni Yamanote-sen ga mairimasu.",
      translationText: "山手线电车即将到达2号站台，请退至黄色盲道内侧等候。",
      pitchName: "中高型（高音落在中间）",
      pitchPath: "M 10 20 Q 50 5 100 8 T 190 22",
      dots: [
        { cx: 20, cy: 18, fill: "#fff", stroke: "#BC382C" },
        { cx: 70, cy: 8, fill: "#BC382C" },
        { cx: 130, cy: 12, fill: "#BC382C" },
        { cx: 180, cy: 22, fill: "#fff", stroke: "#BC382C" }
      ],
      playBtnDefault: "试听东京真人原声音频",
      playBtnPlaying: "正在播放东京真人原声..."
    },
    kombini: {
      level: "JLPT N5-N4 • 便利店实境",
      register: "接客・礼貌语",
      districtName: "涩谷中心街 • 7-Eleven",
      jpText: "お弁当温めますか？レジ袋はご利用ですか？",
      romajiText: "Obento atatamemasu ka? Reji-bukuro wa go-riyo desu ka?",
      translationText: "便当需要帮您加热吗？需要使用塑料购物袋吗？",
      pitchName: "平板型（平直无跌落）",
      pitchPath: "M 10 22 Q 40 8 100 8 L 190 8",
      dots: [
        { cx: 20, cy: 22, fill: "#fff", stroke: "#BC382C" },
        { cx: 60, cy: 8, fill: "#BC382C" },
        { cx: 120, cy: 8, fill: "#BC382C" },
        { cx: 180, cy: 8, fill: "#BC382C" }
      ],
      playBtnDefault: "试听东京真人原声音频",
      playBtnPlaying: "正在播放东京真人原声..."
    },
    izakaya: {
      level: "JLPT N5-N4 • 昭和居酒屋",
      register: "日常・自然口语",
      districtName: "回忆横丁 • 烤鸡串小巷",
      jpText: "とりあえず生ビール二つ、焼き鳥盛り合わせ塩で！",
      romajiText: "Toriaezu nama biiru futatsu, yakitori moriawase shio de!",
      translationText: "先来两杯生啤酒，再来一份盐烤烤鸡串拼盘！",
      pitchName: "头高型（高音落在首拍）",
      pitchPath: "M 10 6 Q 40 22 100 22 L 190 22",
      dots: [
        { cx: 20, cy: 6, fill: "#BC382C" },
        { cx: 60, cy: 22, fill: "#fff", stroke: "#BC382C" },
        { cx: 120, cy: 22, fill: "#fff", stroke: "#BC382C" },
        { cx: 180, cy: 22, fill: "#fff", stroke: "#BC382C" }
      ],
      playBtnDefault: "试听东京真人原声音频",
      playBtnPlaying: "正在播放东京真人原声..."
    },
    akiba: {
      level: "JLPT N5-N4 • 动漫模型店",
      register: "兴趣・流行俗语",
      districtName: "无线电会馆 • 秋叶原",
      jpText: "すみません、この限定フィギュアの未開封品は在庫ありますか？",
      romajiText: "Sumimasen, kono gentei figyua no mikaihin wa zaiko arimasu ka?",
      translationText: "请问这款限定手办的未开封新品还有库存吗？",
      pitchName: "尾高型（词尾后发生跌落）",
      pitchPath: "M 10 22 Q 60 8 150 8 T 190 22",
      dots: [
        { cx: 20, cy: 22, fill: "#fff", stroke: "#BC382C" },
        { cx: 70, cy: 8, fill: "#BC382C" },
        { cx: 140, cy: 8, fill: "#BC382C" },
        { cx: 185, cy: 22, fill: "#fff", stroke: "#BC382C" }
      ],
      playBtnDefault: "试听东京真人原声音频",
      playBtnPlaying: "正在播放东京真人原声..."
    }
  },
  en: {
    densha: {
      level: "JLPT N4-N3 • TRANSIT",
      register: "Keigo (Honorific)",
      districtName: "Shinjuku Station • Track 2",
      jpText: "まもなく、2番線に山手線がまいります。黄色い点字ブロックの内側までお下がりください。",
      romajiText: "Mamonaku, ni-ban-sen ni Yamanote-sen ga mairimasu.",
      translationText: "The Yamanote Line train will soon arrive at Track 2. Please wait behind the yellow line.",
      pitchName: "Nakadaka (Mid-High Peak)",
      pitchPath: "M 10 20 Q 50 5 100 8 T 190 22",
      dots: [
        { cx: 20, cy: 18, fill: "#fff", stroke: "#BC382C" },
        { cx: 70, cy: 8, fill: "#BC382C" },
        { cx: 130, cy: 12, fill: "#BC382C" },
        { cx: 180, cy: 22, fill: "#fff", stroke: "#BC382C" }
      ],
      playBtnDefault: "Play Tokyo Native Audio",
      playBtnPlaying: "Playing Native Voice..."
    },
    kombini: {
      level: "JLPT N5-N4 • KOMBINI",
      register: "Teineigo (Polite Register)",
      districtName: "Shibuya Center-Gai • 7-Eleven",
      jpText: "お弁当温めますか？レジ袋はご利用ですか？",
      romajiText: "Obento atatamemasu ka? Reji-bukuro wa go-riyo desu ka?",
      translationText: "Would you like your bento warmed? Do you need a plastic shopping bag?",
      pitchName: "Heiban (Flat / Pitch Plateau)",
      pitchPath: "M 10 22 Q 40 8 100 8 L 190 8",
      dots: [
        { cx: 20, cy: 22, fill: "#fff", stroke: "#BC382C" },
        { cx: 60, cy: 8, fill: "#BC382C" },
        { cx: 120, cy: 8, fill: "#BC382C" },
        { cx: 180, cy: 8, fill: "#BC382C" }
      ],
      playBtnDefault: "Play Tokyo Native Audio",
      playBtnPlaying: "Playing Native Voice..."
    },
    izakaya: {
      level: "JLPT N5-N4 • IZAKAYA",
      register: "Tameguchi (Casual Living)",
      districtName: "Omoide Yokocho • Yakitori Alley",
      jpText: "とりあえず生ビール二つ、焼き鳥盛り合わせ塩で！",
      romajiText: "Toriaezu nama biiru futatsu, yakitori moriawase shio de!",
      translationText: "First two draft beers, and a salt-grilled yakitori platter please!",
      pitchName: "Atamadaka (Initial Peak)",
      pitchPath: "M 10 6 Q 40 22 100 22 L 190 22",
      dots: [
        { cx: 20, cy: 6, fill: "#BC382C" },
        { cx: 60, cy: 22, fill: "#fff", stroke: "#BC382C" },
        { cx: 120, cy: 22, fill: "#fff", stroke: "#BC382C" },
        { cx: 180, cy: 22, fill: "#fff", stroke: "#BC382C" }
      ],
      playBtnDefault: "Play Tokyo Native Audio",
      playBtnPlaying: "Playing Native Voice..."
    },
    akiba: {
      level: "JLPT N5-N4 • ANIME & SFX",
      register: "Pop Culture & Slang",
      districtName: "Radio Kaikan • Akihabara",
      jpText: "すみません、この限定フィギュアの未開封品は在庫ありますか？",
      romajiText: "Sumimasen, kono gentei figyua no mikaihin wa zaiko arimasu ka?",
      translationText: "Excuse me, is this limited figure in mint unopened condition in stock?",
      pitchName: "Odaka (Final Pitch Drop)",
      pitchPath: "M 10 22 Q 60 8 150 8 T 190 22",
      dots: [
        { cx: 20, cy: 22, fill: "#fff", stroke: "#BC382C" },
        { cx: 70, cy: 8, fill: "#BC382C" },
        { cx: 140, cy: 8, fill: "#BC382C" },
        { cx: 185, cy: 22, fill: "#fff", stroke: "#BC382C" }
      ],
      playBtnDefault: "Play Tokyo Native Audio",
      playBtnPlaying: "Playing Native Voice..."
    }
  }
};

const AUDIO_FILES = {
  densha: "/assets/audio/densha.mp3",
  kombini: "/assets/audio/kombini.mp3",
  izakaya: "/assets/audio/izakaya.mp3",
  akiba: "/assets/audio/akiba.mp3"
};

let currentScenarioKey = 'densha';
let activeAudio = null;

function getPageLanguage() {
  return document.documentElement.lang.startsWith('zh') ? 'zh' : 'en';
}

function updateTokyoClock() {
  const clockEl = document.getElementById('tokyo-clock');
  if (!clockEl) return;
  const now = new Date();
  const options = {
    timeZone: 'Asia/Tokyo',
    hour12: false,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  };
  const timeStr = new Intl.DateTimeFormat('en-US', options).format(now);
  clockEl.textContent = 'TOKYO ' + timeStr + ' JST';
}

function switchScenario(key) {
  currentScenarioKey = key;
  const lang = getPageLanguage();
  const data = SCENARIO_DATA[lang][key];
  if (!data) return;

  // Stop any active audio
  if (activeAudio) {
    activeAudio.pause();
    activeAudio.currentTime = 0;
    activeAudio = null;
    document.getElementById('waveformContainer')?.classList.remove('is-playing');
  }

  // Update scenario tabs active state
  document.querySelectorAll('.scenario-tab').forEach(tab => {
    tab.classList.toggle('active', tab.getAttribute('data-scenario') === key);
  });

  // Update screen content
  const levelEl = document.getElementById('appLevel');
  const regEl = document.getElementById('appRegister');
  const distEl = document.getElementById('appDistrictName');
  const jpEl = document.getElementById('appJpText');
  const romajiEl = document.getElementById('appRomajiText');
  const enEl = document.getElementById('appEnText');
  const pitchNameEl = document.getElementById('pitchPatternName');
  const pitchPathEl = document.getElementById('pitchPath');
  const playLabelEl = document.getElementById('appPlayLabel');
  const playIconEl = document.getElementById('appPlayIcon');

  if (levelEl) levelEl.textContent = data.level;
  if (regEl) regEl.textContent = data.register;
  if (distEl) distEl.textContent = data.districtName;
  if (jpEl) jpEl.textContent = data.jpText;
  if (romajiEl) romajiEl.textContent = data.romajiText;
  if (enEl) enEl.textContent = data.translationText;
  if (pitchNameEl) pitchNameEl.textContent = data.pitchName;
  if (pitchPathEl) pitchPathEl.setAttribute('d', data.pitchPath);
  if (playLabelEl) playLabelEl.textContent = data.playBtnDefault;
  if (playIconEl) playIconEl.textContent = '▶';

  // Update dots
  const dot1 = document.getElementById('pitchDot1');
  const dot2 = document.getElementById('pitchDot2');
  const dot3 = document.getElementById('pitchDot3');
  const dot4 = document.getElementById('pitchDot4');
  const dots = [dot1, dot2, dot3, dot4];

  data.dots.forEach((dotData, idx) => {
    if (dots[idx]) {
      dots[idx].setAttribute('cx', dotData.cx);
      dots[idx].setAttribute('cy', dotData.cy);
      dots[idx].setAttribute('fill', dotData.fill);
      if (dotData.stroke) {
        dots[idx].setAttribute('stroke', dotData.stroke);
      }
    }
  });
}

function playActiveScenarioAudio() {
  const audioSrc = AUDIO_FILES[currentScenarioKey];
  const lang = getPageLanguage();
  const data = SCENARIO_DATA[lang][currentScenarioKey];
  const waveContainer = document.getElementById('waveformContainer');
  const playLabelEl = document.getElementById('appPlayLabel');
  const playIconEl = document.getElementById('appPlayIcon');

  if (activeAudio) {
    activeAudio.pause();
    activeAudio.currentTime = 0;
    activeAudio = null;
    if (waveContainer) waveContainer.classList.remove('is-playing');
    if (playLabelEl) playLabelEl.textContent = data.playBtnDefault;
    if (playIconEl) playIconEl.textContent = '▶';
    return;
  }

  activeAudio = new Audio(audioSrc);
  if (waveContainer) waveContainer.classList.add('is-playing');
  if (playLabelEl) playLabelEl.textContent = data.playBtnPlaying;
  if (playIconEl) playIconEl.textContent = '■';

  activeAudio.play().catch(e => {
    console.log('Audio autoplay prevented:', e);
  });

  activeAudio.onended = function() {
    activeAudio = null;
    if (waveContainer) waveContainer.classList.remove('is-playing');
    if (playLabelEl) playLabelEl.textContent = data.playBtnDefault;
    if (playIconEl) playIconEl.textContent = '▶';
  };
}

function filterAcademy(category) {
  // Update button active state
  document.querySelectorAll('.filter-pill').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-filter') === category);
  });

  // Filter video cards
  document.querySelectorAll('.video-card-item').forEach(card => {
    const cardCat = card.getAttribute('data-category');
    if (category === 'all' || cardCat === category) {
      card.style.display = 'flex';
    } else {
      card.style.display = 'none';
    }
  });
}

// Initializations on DOM Load
document.addEventListener('DOMContentLoaded', () => {
  updateTokyoClock();
  setInterval(updateTokyoClock, 1000);
});
"""
    assert_zero_emoji(js_content, "site/app.js")
    return js_content

def build_extended_css():
    # Read existing base CSS and append custom styles for Academy, Shorts, Materials, and FAQ
    with open("site/styles.css") as f:
        existing = f.read()

    new_section = """
/* ==========================================================================
   ENHANCED YOUTUBE ACADEMY & CONVERSION STYLES
   ========================================================================== */

/* YouTube Spotlight Banner */
.yt-channel-banner {
  background: linear-gradient(135deg, #181B22 0%, #0F1115 100%);
  border: 1px solid rgba(197, 160, 89, 0.4);
  border-radius: var(--radius-xl);
  padding: 3rem 3.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2.5rem;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.25);
  margin-bottom: 2rem;
  color: #FFFFFF;
}

.yt-banner-left {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 680px;
}

.yt-live-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(224, 72, 56, 0.15);
  border: 1px solid rgba(224, 72, 56, 0.4);
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 700;
  color: #FF5A4E;
  letter-spacing: 0.1em;
  width: fit-content;
}

.yt-banner-title {
  font-family: var(--font-serif);
  font-size: 2.2rem;
  font-weight: 700;
  color: #FFFFFF;
  line-height: 1.25;
}

.yt-banner-desc {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.78);
  line-height: 1.7;
}

.yt-schedule-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  margin-top: 0.25rem;
}

.sched-tag {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  padding: 4px 10px;
  border-radius: 6px;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: #E8D5A3;
}

.btn-yt-subscribe {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: #FF0000;
  color: #FFFFFF;
  padding: 1.1rem 2rem;
  border-radius: var(--radius-md);
  text-decoration: none;
  font-weight: 700;
  font-size: 1rem;
  font-family: var(--font-mono);
  box-shadow: 0 8px 25px rgba(255, 0, 0, 0.35);
  transition: all 0.25s ease;
  white-space: nowrap;
}

.btn-yt-subscribe:hover {
  background: #E60000;
  transform: translateY(-2px);
  box-shadow: 0 12px 30px rgba(255, 0, 0, 0.45);
}

/* Schedule Notice Bar */
.schedule-notice-bar {
  background: rgba(197, 160, 89, 0.12);
  border: 1px solid rgba(197, 160, 89, 0.4);
  border-radius: var(--radius-md);
  padding: 0.85rem 1.25rem;
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.86rem;
  color: var(--navy);
  font-family: var(--font-serif);
}

.notice-badge {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--cinnabar);
  background: rgba(188, 56, 44, 0.1);
  padding: 2px 8px;
  border-radius: 4px;
  white-space: nowrap;
}

.notice-text {
  flex: 1;
  line-height: 1.5;
}

/* Playlist Filter Bar */
.playlist-filter-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  margin-bottom: 2.5rem;
  justify-content: center;
}

.filter-pill {
  padding: 0.6rem 1.2rem;
  border-radius: var(--radius-full);
  background: #FFFFFF;
  border: 1px solid var(--border-gold-subtle);
  color: var(--ink-sub);
  font-family: var(--font-mono);
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(18, 54, 94, 0.04);
}

.filter-pill:hover {
  border-color: var(--gold);
  color: var(--navy);
}

.filter-pill.active {
  background: var(--cinnabar);
  color: #FFFFFF;
  border-color: var(--cinnabar);
  box-shadow: 0 4px 14px rgba(188, 56, 44, 0.3);
}

/* Video Cards Grid */
.video-cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-bottom: 4rem;
}

.video-card-item {
  display: flex;
  flex-direction: column;
}

.video-card-link {
  background: var(--bg-paper-card);
  border: 1px solid var(--border-gold);
  border-radius: var(--radius-lg);
  overflow: hidden;
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  height: 100%;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: var(--shadow-card);
}

.video-card-link:hover {
  border-color: var(--cinnabar);
  transform: translateY(-5px);
  box-shadow: var(--shadow-hover);
  background: #FFFFFF;
}

.video-thumb-wrap {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  background: #0F1115;
  overflow: hidden;
}

.video-thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.video-card-link:hover .video-thumb-img {
  transform: scale(1.04);
}

.video-badge-group {
  position: absolute;
  top: 10px;
  left: 10px;
  display: flex;
  gap: 6px;
  z-index: 2;
}

.badge-jlpt {
  background: rgba(188, 56, 44, 0.92);
  color: #FFFFFF;
  padding: 3px 8px;
  border-radius: 4px;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  font-weight: 700;
}

.badge-duration {
  background: rgba(18, 54, 94, 0.9);
  color: #FFFFFF;
  padding: 3px 8px;
  border-radius: 4px;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  font-weight: 700;
}

.video-status-overlay {
  position: absolute;
  bottom: 8px;
  left: 10px;
  right: 10px;
  z-index: 2;
  display: flex;
}

.status-badge-live {
  background: rgba(16, 185, 129, 0.92);
  color: #FFFFFF;
  padding: 3px 8px;
  border-radius: 4px;
  font-family: var(--font-mono);
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.status-badge-scheduled {
  background: rgba(18, 54, 94, 0.92);
  color: #FBBF24;
  padding: 3px 8px;
  border-radius: 4px;
  font-family: var(--font-mono);
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  border: 1px solid rgba(251, 191, 36, 0.4);
}

.video-play-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.2);
  opacity: 0;
  transition: opacity 0.25s ease;
}

.video-card-link:hover .video-play-overlay {
  opacity: 1;
}

.play-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--cinnabar);
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(188, 56, 44, 0.4);
}

.video-content-body {
  padding: 1.4rem 1.5rem;
  display: flex;
  flex-direction: column;
  flex: 1;
  gap: 0.6rem;
}

.video-location-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: var(--font-mono);
  font-size: 0.74rem;
}

.loc-tag {
  color: var(--gold-deep);
  font-weight: 700;
}

.ep-tag {
  color: var(--ink-muted);
}

.video-item-title {
  font-family: var(--font-serif);
  font-size: 1.12rem;
  font-weight: 700;
  color: var(--navy);
  line-height: 1.35;
}

.video-item-desc {
  font-family: var(--font-serif);
  font-size: 0.88rem;
  color: var(--ink-sub);
  line-height: 1.6;
  flex: 1;
}

.video-takeaway-box {
  background: var(--bg-paper-tint);
  border: 1px solid var(--border-gold-subtle);
  border-radius: 8px;
  padding: 8px 10px;
  margin-top: 0.4rem;
}

.takeaway-label {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  color: var(--cinnabar);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 700;
  margin-bottom: 2px;
}

.takeaway-jp {
  font-family: var(--font-serif);
  font-size: 0.84rem;
  color: var(--navy);
  font-weight: 600;
  line-height: 1.35;
}

.takeaway-trans {
  font-size: 0.74rem;
  color: var(--ink-sub);
  margin-top: 2px;
}

.video-yt-action {
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--border-gold-subtle);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.video-schedule-row {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.74rem;
}

.schedule-label {
  font-family: var(--font-mono);
  color: var(--ink-muted);
  font-weight: 600;
}

.schedule-val {
  font-size: 0.7rem;
  padding: 2px 6px;
  border-radius: 4px;
}

.yt-action-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-mono);
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--cinnabar);
  transition: gap 0.2s ease;
  margin-top: 0.2rem;
}

.video-card-link:hover .yt-action-btn {
  gap: 10px;
}

/* Shorts Showcase */
.shorts-section-wrap {
  background: var(--bg-paper-card);
  border: 1px solid var(--border-gold);
  border-radius: var(--radius-xl);
  padding: 3rem;
  margin-top: 2rem;
  box-shadow: var(--shadow-luxury);
}

.shorts-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 2rem;
  gap: 1.5rem;
}

.shorts-title {
  font-family: var(--font-serif);
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--navy);
  margin-top: 0.3rem;
}

.shorts-desc {
  font-family: var(--font-serif);
  color: var(--ink-sub);
  font-size: 0.92rem;
}

.btn-shorts-all {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #FFFFFF;
  border: 1px solid var(--border-gold);
  padding: 0.65rem 1.25rem;
  border-radius: var(--radius-md);
  font-family: var(--font-mono);
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--navy);
  text-decoration: none;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.btn-shorts-all:hover {
  border-color: var(--cinnabar);
  color: var(--cinnabar);
  transform: translateY(-1px);
}

.shorts-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem;
}

.short-card-item {
  display: flex;
}

.short-card-link {
  background: #FFFFFF;
  border: 1px solid var(--border-gold-subtle);
  border-radius: var(--radius-md);
  padding: 1.2rem;
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 100%;
  transition: all 0.25s ease;
}

.short-card-link:hover {
  border-color: var(--cinnabar);
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(188, 56, 44, 0.12);
}

.short-top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.6rem;
}

.short-badge {
  background: rgba(188, 56, 44, 0.1);
  color: var(--cinnabar);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: var(--font-mono);
  font-size: 0.68rem;
  font-weight: 700;
}

.short-ep {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--ink-muted);
}

.short-title {
  font-family: var(--font-serif);
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--navy);
  line-height: 1.35;
  margin-bottom: 0.6rem;
}

.short-focus-box {
  font-size: 0.76rem;
  color: var(--ink-sub);
  margin-bottom: 0.6rem;
}

.short-focus-label {
  font-family: var(--font-mono);
  font-weight: 600;
  color: var(--gold-deep);
}

.short-schedule-tag {
  font-size: 0.68rem;
  padding: 2px 6px;
  border-radius: 4px;
  margin-bottom: 0.6rem;
  width: fit-content;
}

.short-btn-bar {
  margin-top: auto;
  padding-top: 0.6rem;
  border-top: 1px dashed var(--border-gold-subtle);
}

.short-action-link {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--cinnabar);
}

/* Materials Section */
.materials-section {
  padding: 5rem 0;
  border-top: 1px solid var(--border-gold-subtle);
}

.materials-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.material-card {
  background: var(--bg-paper-card);
  border: 1px solid var(--border-gold);
  border-radius: var(--radius-lg);
  padding: 2.25rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: var(--shadow-card);
  transition: all 0.25s ease;
}

.material-card:hover {
  border-color: var(--cinnabar);
  transform: translateY(-3px);
  box-shadow: var(--shadow-hover);
}

.material-tag {
  font-family: var(--font-mono);
  font-size: 0.74rem;
  font-weight: 700;
  color: var(--cinnabar);
  margin-bottom: 0.75rem;
}

.material-title {
  font-family: var(--font-serif);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--navy);
  line-height: 1.35;
  margin-bottom: 0.6rem;
}

.material-desc {
  font-family: var(--font-serif);
  font-size: 0.9rem;
  color: var(--ink-sub);
  line-height: 1.65;
  margin-bottom: 1.5rem;
}

.btn-material-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-mono);
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--navy);
  text-decoration: none;
  transition: gap 0.2s ease;
}

.btn-material-link:hover {
  color: var(--cinnabar);
  gap: 10px;
}

/* FAQ Section */
.faq-section {
  padding: 5rem 0;
  border-top: 1px solid var(--border-gold-subtle);
}

.faq-container {
  max-width: 860px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.faq-item {
  background: var(--bg-paper-card);
  border: 1px solid var(--border-gold-subtle);
  border-radius: var(--radius-md);
  overflow: hidden;
  transition: all 0.25s ease;
}

.faq-item[open] {
  border-color: var(--gold);
  background: #FFFFFF;
  box-shadow: 0 4px 18px rgba(18, 54, 94, 0.05);
}

.faq-question {
  padding: 1.25rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  list-style: none;
  font-family: var(--font-serif);
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--navy);
  user-select: none;
}

.faq-question::-webkit-details-marker {
  display: none;
}

.faq-toggle-icon {
  font-family: var(--font-mono);
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--gold-deep);
  transition: transform 0.2s ease;
}

.faq-item[open] .faq-toggle-icon {
  transform: rotate(45deg);
  color: var(--cinnabar);
}

.faq-answer {
  padding: 0 1.5rem 1.25rem;
  font-family: var(--font-serif);
  font-size: 0.94rem;
  color: var(--ink-sub);
  line-height: 1.75;
}

/* Navigation buttons refined */
.lang-code-tag {
  font-family: var(--font-mono);
  font-weight: 700;
  margin-right: 4px;
}

.btn-nav-yt {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: var(--radius-md);
  background: rgba(255, 0, 0, 0.08);
  border: 1px solid rgba(255, 0, 0, 0.25);
  color: #CC0000;
  text-decoration: none;
  font-family: var(--font-mono);
  font-size: 0.8rem;
  font-weight: 700;
  transition: all 0.2s ease;
}

.btn-nav-yt:hover {
  background: #FF0000;
  color: #FFFFFF;
  border-color: #FF0000;
}

.btn-hero-secondary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #FFFFFF;
  border: 1px solid var(--border-gold);
  color: var(--navy);
  padding: 1rem 1.6rem;
  border-radius: var(--radius-md);
  text-decoration: none;
  font-family: var(--font-mono);
  font-size: 0.92rem;
  font-weight: 700;
  box-shadow: 0 4px 15px rgba(18, 54, 94, 0.06);
  transition: all 0.25s ease;
}

.btn-hero-secondary:hover {
  border-color: var(--cinnabar);
  color: var(--cinnabar);
  transform: translateY(-2px);
}

.pillar-stamp {
  font-family: var(--font-mono);
  font-size: 0.74rem;
  color: var(--gold-deep);
  font-weight: 700;
}

.district-marker {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--cinnabar);
  font-weight: 700;
}

.arrow-glyph {
  font-size: 1.1rem;
  line-height: 1;
  opacity: 0.9;
}

/* Responsive adjustments */
@media (max-width: 1024px) {
  .video-cards-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .shorts-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .materials-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .yt-channel-banner {
    flex-direction: column;
    align-items: flex-start;
    padding: 2.5rem;
  }
}

@media (max-width: 640px) {
  .video-cards-grid {
    grid-template-columns: 1fr;
  }
  .shorts-grid {
    grid-template-columns: 1fr;
  }
  .materials-grid {
    grid-template-columns: 1fr;
  }
  .shorts-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
"""
    assert_zero_emoji(new_section, "extended CSS")
    # Avoid duplicating if already present
    if "ENHANCED YOUTUBE ACADEMY" in existing:
        # replace the appended section
        base = existing.split("/* ==========================================================================\n   ENHANCED YOUTUBE ACADEMY")[0]
        return base + new_section
    return existing + "\n" + new_section

def build_sitemap_xml():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml"
        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
  
  <!-- Chinese Homepage (Canonical Root) -->
  <url>
    <loc>https://tokyoflow.app/</loc>
    <lastmod>2026-10-04</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
    <xhtml:link rel="alternate" hreflang="zh-Hans" href="https://tokyoflow.app/" />
    <xhtml:link rel="alternate" hreflang="zh-CN" href="https://tokyoflow.app/" />
    <xhtml:link rel="alternate" hreflang="en" href="https://tokyoflow.app/en/" />
    <xhtml:link rel="alternate" hreflang="x-default" href="https://tokyoflow.app/" />
  </url>

  <!-- English Homepage -->
  <url>
    <loc>https://tokyoflow.app/en/</loc>
    <lastmod>2026-10-04</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.95</priority>
    <xhtml:link rel="alternate" hreflang="en" href="https://tokyoflow.app/en/" />
    <xhtml:link rel="alternate" hreflang="zh-Hans" href="https://tokyoflow.app/" />
    <xhtml:link rel="alternate" hreflang="zh-CN" href="https://tokyoflow.app/" />
    <xhtml:link rel="alternate" hreflang="x-default" href="https://tokyoflow.app/" />
  </url>

  <!-- Legal & Support Pages -->
  <url>
    <loc>https://tokyoflow.app/privacy/</loc>
    <lastmod>2026-10-04</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>

  <url>
    <loc>https://tokyoflow.app/terms/</loc>
    <lastmod>2026-10-04</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>

  <url>
    <loc>https://tokyoflow.app/support/</loc>
    <lastmod>2026-10-04</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>

  <url>
    <loc>https://tokyoflow.app/en/privacy/</loc>
    <lastmod>2026-10-04</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>

  <url>
    <loc>https://tokyoflow.app/en/terms/</loc>
    <lastmod>2026-10-04</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>

  <url>
    <loc>https://tokyoflow.app/en/support/</loc>
    <lastmod>2026-10-04</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>

</urlset>
"""
    assert_zero_emoji(xml, "sitemap.xml")
    return xml

def build_robots_txt():
    txt = """User-agent: *
Allow: /
Disallow: /tmp/
Disallow: /build/
Disallow: /build_sim/

Sitemap: https://tokyoflow.app/sitemap.xml
"""
    assert_zero_emoji(txt, "robots.txt")
    return txt

def main():
    print("Building TokyoFlow Redesigned Bilingual Website with Accurate Chinese YouTube URLs & Schedule Badges...")

    zh_html = build_chinese_page()
    en_html = build_english_page()
    app_js = build_app_js()
    styles_css = build_extended_css()
    sitemap_xml = build_sitemap_xml()
    robots_txt = build_robots_txt()

    # Write to site/
    os.makedirs("site/en", exist_ok=True)
    os.makedirs("site/assets/thumbnails", exist_ok=True)
    os.makedirs("site/privacy", exist_ok=True)
    os.makedirs("site/terms", exist_ok=True)
    os.makedirs("site/support", exist_ok=True)
    os.makedirs("site/en/privacy", exist_ok=True)
    os.makedirs("site/en/terms", exist_ok=True)
    os.makedirs("site/en/support", exist_ok=True)

    with open("site/index.html", "w", encoding="utf-8") as f:
        f.write(zh_html)
    with open("site/en/index.html", "w", encoding="utf-8") as f:
        f.write(en_html)
    with open("site/app.js", "w", encoding="utf-8") as f:
        f.write(app_js)
    with open("site/styles.css", "w", encoding="utf-8") as f:
        f.write(styles_css)
    with open("site/sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_xml)
    with open("site/robots.txt", "w", encoding="utf-8") as f:
        f.write(robots_txt)

    # Sync entire site to docs/site for GitHub Pages / docs deployment
    os.makedirs("docs/site", exist_ok=True)
    for root, dirs, files in os.walk("site"):
        rel_path = os.path.relpath(root, "site")
        dest_dir = os.path.join("docs/site", rel_path) if rel_path != "." else "docs/site"
        os.makedirs(dest_dir, exist_ok=True)
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dest_dir, file)
            shutil.copy2(src_file, dst_file)

    # Sync entire site to repo root for Cloudflare Pages / Workers deployment
    for root, dirs, files in os.walk("site"):
        rel_path = os.path.relpath(root, "site")
        dest_dir = os.path.join(".", rel_path) if rel_path != "." else "."
        os.makedirs(dest_dir, exist_ok=True)
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dest_dir, file)
            shutil.copy2(src_file, dst_file)

    print("TokyoFlow Website generated and synchronized to site/, docs/site/, and repo root!")
    print("Zero Emoji Verification Passed on all files.")

if __name__ == "__main__":
    main()
