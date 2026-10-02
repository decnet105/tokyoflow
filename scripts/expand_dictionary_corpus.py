#!/usr/bin/env python3
"""
expand_dictionary_corpus.py
Expands TokyoFlow's JLPT & Tokyo Life Vocabulary with authentic, practical,
and high-frequency words across N5, N4, N3, N2, and N1.
"""

import json
import os

DICT_PATH = "TokyoFlow/Resources/jlpt_dictionary.json"

NEW_VOCAB_ENTRIES = [
    # --- N5: Metro & Transit Essentials ---
    {
        "id": "n5_exp_001_kaisatsuguchi",
        "kanji": "改札口",
        "reading": "かいさつぐち",
        "romaji": "kaisatsuguchi",
        "pitchAccent": "[3] Nakadaka",
        "level": "N5",
        "partOfSpeech": "Noun",
        "meaning": "Ticket gate, turnstile",
        "exampleJa": "東口の改札口で待ち合わせをしましょう。",
        "exampleFurigana": "ひがしぐちの かいさつぐちで まちあわせを しましょう。",
        "exampleZh": "在东口的检票口集合吧。",
        "exampleEn": "Let's meet up at the east exit ticket gates.",
        "transitivePair": None,
        "collocation": "改札口を通る",
        "examYearNote": "JLPT N5 Core Transit",
        "scenarioTag": "transit"
    },
    {
        "id": "n5_exp_002_norikae",
        "kanji": "乗り換え",
        "reading": "のりかえ",
        "romaji": "norikae",
        "pitchAccent": "[0] Heiban",
        "level": "N5",
        "partOfSpeech": "Noun",
        "meaning": "Transfer, changing trains",
        "exampleJa": "東京駅での乗り換え時間は5分です。",
        "exampleFurigana": "とうきょうえきでの のりかえ じかんは ごふんです。",
        "exampleZh": "在东京站的换乘时间是5分钟。",
        "exampleEn": "The transfer time at Tokyo Station is 5 minutes.",
        "transitivePair": None,
        "collocation": "乗り換え案内",
        "examYearNote": "JLPT N5 Core Transit",
        "scenarioTag": "transit"
    },
    {
        "id": "n5_exp_003_kippu",
        "kanji": "切符",
        "reading": "きっぷ",
        "romaji": "kippu",
        "pitchAccent": "[0] Heiban",
        "level": "N5",
        "partOfSpeech": "Noun",
        "meaning": "Ticket (train, event)",
        "exampleJa": "自動券売機で切符を買いました。",
        "exampleFurigana": "じどうけんばいきで きっぷを かいました。",
        "exampleZh": "在自动售票机买了车票。",
        "exampleEn": "I bought a ticket at the automated ticket machine.",
        "transitivePair": None,
        "collocation": "切符を買う",
        "examYearNote": "JLPT N5 Essential",
        "scenarioTag": "transit"
    },
    {
        "id": "n5_exp_004_deguchi",
        "kanji": "出口",
        "reading": "でぐち",
        "romaji": "deguchi",
        "pitchAccent": "[1] Atamadaka",
        "level": "N5",
        "partOfSpeech": "Noun",
        "meaning": "Exit, way out",
        "exampleJa": "南口の出口を出てすぐ右にあります。",
        "exampleFurigana": "みなみぐちの でぐちを でて すぐ みぎに あります。",
        "exampleZh": "出南口后就在右边。",
        "exampleEn": "It is immediately to the right after leaving the south exit.",
        "transitivePair": "入口 (iriguchi - entrance)",
        "collocation": "出口を出る",
        "examYearNote": "JLPT N5 Direction",
        "scenarioTag": "transit"
    },
    {
        "id": "n5_exp_005_iriguchi",
        "kanji": "入口",
        "reading": "いりぐち",
        "romaji": "iriguchi",
        "pitchAccent": "[0] Heiban",
        "level": "N5",
        "partOfSpeech": "Noun",
        "meaning": "Entrance, entryway",
        "exampleJa": "ビルの入口にアルコール消毒液があります。",
        "exampleFurigana": "びるの いりぐちに あるこーる しょうどくえきが あります。",
        "exampleZh": "大楼入口有酒精消毒液。",
        "exampleEn": "There is hand sanitizer at the building entrance.",
        "transitivePair": "出口 (deguchi - exit)",
        "collocation": "入口に入る",
        "examYearNote": "JLPT N5 Direction",
        "scenarioTag": "daily"
    },
    # --- N5: Convenience Store & Food ---
    {
        "id": "n5_exp_006_onigiri",
        "kanji": "おにぎり",
        "reading": "おにぎり",
        "romaji": "onigiri",
        "pitchAccent": "[2] Nakadaka",
        "level": "N5",
        "partOfSpeech": "Noun",
        "meaning": "Rice ball (Japanese style)",
        "exampleJa": "鮭のおにぎりと緑茶を買いました。",
        "exampleFurigana": "さけの おにぎりと りょくちゃを かいました。",
        "exampleZh": "买了三文鱼饭团和绿茶。",
        "exampleEn": "I bought a salmon onigiri and green tea.",
        "transitivePair": None,
        "collocation": "おにぎりを食べる",
        "examYearNote": "JLPT N5 Daily Life",
        "scenarioTag": "kombini"
    },
    {
        "id": "n5_exp_007_bentou",
        "kanji": "お弁当",
        "reading": "おべんとう",
        "romaji": "obentou",
        "pitchAccent": "[0] Heiban",
        "level": "N5",
        "partOfSpeech": "Noun",
        "meaning": "Bento lunchbox",
        "exampleJa": "お弁当を温めてもらえますか？",
        "exampleFurigana": "おべんとうを あたためて もらえますか？",
        "exampleZh": "可以帮我把便当加热一下吗？",
        "exampleEn": "Could you please warm up this bento?",
        "transitivePair": None,
        "collocation": "お弁当を温める",
        "examYearNote": "JLPT N5 Daily Food",
        "scenarioTag": "kombini"
    },
    {
        "id": "n5_exp_008_kaikei",
        "kanji": "会計",
        "reading": "かいけい",
        "romaji": "kaikei",
        "pitchAccent": "[0] Heiban",
        "level": "N5",
        "partOfSpeech": "Noun",
        "meaning": "Bill, checkout, paying the check",
        "exampleJa": "お会計は別々でお願いします。",
        "exampleFurigana": "おかいけいは べつべつで おねがいします。",
        "exampleZh": "买单请分开付。",
        "exampleEn": "Please split the bill for payment.",
        "transitivePair": None,
        "collocation": "お会計をお願いする",
        "examYearNote": "JLPT N5 Payment",
        "scenarioTag": "dining"
    },
    {
        "id": "n5_exp_009_menrui",
        "kanji": "麺類",
        "reading": "めんるい",
        "romaji": "menrui",
        "pitchAccent": "[1] Atamadaka",
        "level": "N5",
        "partOfSpeech": "Noun",
        "meaning": "Noodles, noodle dishes",
        "exampleJa": "ラーメンやうどんなどの麺類が好きです。",
        "exampleFurigana": "らーめんや うどんなどの めんるいが すきです。",
        "exampleZh": "喜欢拉面和乌冬等面类。",
        "exampleEn": "I like noodle dishes like ramen and udon.",
        "transitivePair": None,
        "collocation": "麺類を注文する",
        "examYearNote": "JLPT N5 Food",
        "scenarioTag": "dining"
    },
    {
        "id": "n5_exp_010_kanpai",
        "kanji": "乾杯",
        "reading": "かんぱい",
        "romaji": "kanpai",
        "pitchAccent": "[0] Heiban",
        "level": "N5",
        "partOfSpeech": "Noun / Suru-Verb",
        "meaning": "Cheers, toast (drinking)",
        "exampleJa": "みんなでビールを持って乾杯しました。",
        "exampleFurigana": "みんなで びーるを もって かんぱい しました。",
        "exampleZh": "大家举着啤酒干杯了。",
        "exampleEn": "Everyone held their beers and made a toast.",
        "transitivePair": None,
        "collocation": "乾杯をする",
        "examYearNote": "JLPT N5 Social",
        "scenarioTag": "izakaya"
    },

    # --- N4: Practical Japanese & Real Situations ---
    {
        "id": "n4_exp_001_shiteiseki",
        "kanji": "指定席",
        "reading": "していせき",
        "romaji": "shiteiseki",
        "pitchAccent": "[2] Nakadaka",
        "level": "N4",
        "partOfSpeech": "Noun",
        "meaning": "Reserved seat",
        "exampleJa": "新幹線の指定席を事前にネットで予約しました。",
        "exampleFurigana": "しんかんせんの していせきを じぜんに ねっとで よやくしました。",
        "exampleZh": "提前在网上预订了新干线的指定席。",
        "exampleEn": "I reserved a designated seat on the Shinkansen online in advance.",
        "transitivePair": "自由席 (jiyuuseki - unreserved seat)",
        "collocation": "指定席を予約する",
        "examYearNote": "JLPT N4 Transit",
        "scenarioTag": "transit"
    },
    {
        "id": "n4_exp_002_jiyuuseki",
        "kanji": "自由席",
        "reading": "じゆうせき",
        "romaji": "jiyuuseki",
        "pitchAccent": "[2] Nakadaka",
        "level": "N4",
        "partOfSpeech": "Noun",
        "meaning": "Non-reserved seat, unreserved car",
        "exampleJa": "自由席の特急券を買ってホームで並びました。",
        "exampleFurigana": "じゆうせきの とっきゅうけんを かって ほーむで ならびました。",
        "exampleZh": "买了自由席特急券并在站台排队。",
        "exampleEn": "I bought an unreserved express ticket and lined up on the platform.",
        "transitivePair": "指定席 (shiteiseki - reserved seat)",
        "collocation": "自由席に乗る",
        "examYearNote": "JLPT N4 Transit",
        "scenarioTag": "transit"
    },
    {
        "id": "n4_exp_003_furikomi",
        "kanji": "振込",
        "reading": "ふりこみ",
        "romaji": "furikomi",
        "pitchAccent": "[0] Heiban",
        "level": "N4",
        "partOfSpeech": "Noun / Suru-Verb",
        "meaning": "Bank transfer, account deposit payment",
        "exampleJa": "家賃の支払いは毎月銀行振込で行います。",
        "exampleFurigana": "やちんの しはらいは まいつき ぎんこう ふりこみで おこないます。",
        "exampleZh": "房租支付每月通过银行转账进行。",
        "exampleEn": "Rent payment is made via bank transfer every month.",
        "transitivePair": None,
        "collocation": "口座に振り込む",
        "examYearNote": "JLPT N4 Daily Life",
        "scenarioTag": "daily"
    },
    {
        "id": "n4_exp_004_menzei",
        "kanji": "免税",
        "reading": "めんぜい",
        "romaji": "menzei",
        "pitchAccent": "[0] Heiban",
        "level": "N4",
        "partOfSpeech": "Noun / Suru-Verb",
        "meaning": "Tax exemption, duty-free shopping",
        "exampleJa": "合計5000円以上購入すると免税になります。",
        "exampleFurigana": "ごうけい ごせんえんいじょう こうにゅうすると めんぜいに なります。",
        "exampleZh": "合计购买5000日元以上可免税。",
        "exampleEn": "Purchases of 5,000 yen or more qualify for tax exemption.",
        "transitivePair": None,
        "collocation": "免税手続き",
        "examYearNote": "JLPT N4 Shopping",
        "scenarioTag": "shopping"
    },
    {
        "id": "n4_exp_005_ryoushuusho",
        "kanji": "領収書",
        "reading": "りょうしゅうしょ",
        "romaji": "ryoushuusho",
        "pitchAccent": "[0] Heiban",
        "level": "N4",
        "partOfSpeech": "Noun",
        "meaning": "Official receipt (for business reimbursement)",
        "exampleJa": "会社の経費にするため領収書を宛名付きで頼みました。",
        "exampleFurigana": "かいしゃの けいひにするため りょうしゅうしょを あてなつきで たのみました。",
        "exampleZh": "为了报销公司经费，要求开具带抬头的正式发票。",
        "exampleEn": "I requested an official receipt with addressee name for company expense filing.",
        "transitivePair": "レシート (reshiito - register slip)",
        "collocation": "領収書を発行する",
        "examYearNote": "JLPT N4 Business/Dining",
        "scenarioTag": "business"
    },

    # --- N3: Intermediate Conversational & Scenario Vocabulary ---
    {
        "id": "n3_exp_001_gentei",
        "kanji": "限定",
        "reading": "げんてい",
        "romaji": "gentei",
        "pitchAccent": "[0] Heiban",
        "level": "N3",
        "partOfSpeech": "Noun / Suru-Verb",
        "meaning": "Limited edition, restriction, exclusive",
        "exampleJa": "秋葉原店限定のフィギュアを購入しました。",
        "exampleFurigana": "あきはばらてん げんていの ふぃぎゅあを こうにゅうしました。",
        "exampleZh": "购买了秋叶原店限定手办。",
        "exampleEn": "I bought the Akihabara store exclusive figure.",
        "transitivePair": None,
        "collocation": "期間限定",
        "examYearNote": "JLPT N3 Commercial",
        "scenarioTag": "anime"
    },
    {
        "id": "n3_exp_002_tokuten",
        "kanji": "特典",
        "reading": "とくてん",
        "romaji": "tokuten",
        "pitchAccent": "[0] Heiban",
        "level": "N3",
        "partOfSpeech": "Noun",
        "meaning": "Special benefit, buyer bonus, privilege perk",
        "exampleJa": "Blu-rayの予約特典として描き下ろしポスターが付いてきます。",
        "exampleFurigana": "ぶるーれいの よやく とくてんとして えがきおろし ぽすたーが ついてきます。",
        "exampleZh": "作为蓝光预订特权附送特别绘制海报。",
        "exampleEn": "An exclusive illustrated poster is included as a pre-order bonus for the Blu-ray.",
        "transitivePair": None,
        "collocation": "購入特典",
        "examYearNote": "JLPT N3 Media",
        "scenarioTag": "anime"
    },
    {
        "id": "n3_exp_003_enryo",
        "kanji": "遠慮",
        "reading": "えんりょ",
        "romaji": "enryo",
        "pitchAccent": "[0] Heiban",
        "level": "N3",
        "partOfSpeech": "Noun / Suru-Verb",
        "meaning": "Restraint, hesitation, holding back politely",
        "exampleJa": "質問があれば遠慮なくいつでもお尋ねください。",
        "exampleFurigana": "しつもんが あれば えんりょなく いつでも おたずねください。",
        "exampleZh": "如果有问题请随时尽管提问，不要客气。",
        "exampleEn": "Please don't hesitate to ask anytime if you have any questions.",
        "transitivePair": None,
        "collocation": "遠慮なく",
        "examYearNote": "JLPT N3 Social Manner",
        "scenarioTag": "social"
    },
    {
        "id": "n3_exp_004_teinei",
        "kanji": "丁寧",
        "reading": "ていねい",
        "romaji": "teinei",
        "pitchAccent": "[1] Atamadaka",
        "level": "N3",
        "partOfSpeech": "Na-Adjective",
        "meaning": "Polite, courteous, meticulous, careful",
        "exampleJa": "店員さんがとても丁寧な言葉遣いで対応してくれました。",
        "exampleFurigana": "てんいんさんが とても ていねいな ことばづかいで たいおうしてくれました。",
        "exampleZh": "店员用非常礼貌的措辞接待了我。",
        "exampleEn": "The store staff assisted me with very polite and respectful phrasing.",
        "transitivePair": "乱暴 (ranbou - rough)",
        "collocation": "丁寧な対応",
        "examYearNote": "JLPT N3 Culture",
        "scenarioTag": "service"
    },

    # --- N2: Advanced Business & Expressive Nuances ---
    {
        "id": "n2_exp_001_shouchi",
        "kanji": "承知",
        "reading": "しょうち",
        "romaji": "shouchi",
        "pitchAccent": "[0] Heiban",
        "level": "N2",
        "partOfSpeech": "Noun / Suru-Verb",
        "meaning": "Acknowledgement, consent, fully aware (Kenjougo)",
        "exampleJa": "ご依頼の件、承知いたしました。直ちに着手します。",
        "exampleFurigana": "ごいらいの けん、しょうち いたしました。ただちに ちゃくしゅします。",
        "exampleZh": "您委托的事项已知悉，我立即着手处理。",
        "exampleEn": "Understood regarding your request. I will begin working on it immediately.",
        "transitivePair": None,
        "collocation": "承知いたしました",
        "examYearNote": "JLPT N2 Business Keigo",
        "scenarioTag": "business"
    },
    {
        "id": "n2_exp_002_kyoushuku",
        "kanji": "恐縮",
        "reading": "きょうしゅく",
        "romaji": "kyoushuku",
        "pitchAccent": "[0] Heiban",
        "level": "N2",
        "partOfSpeech": "Noun / Suru-Verb",
        "meaning": "Extremely obliged, feeling apologetic/grateful for someone's trouble",
        "exampleJa": "お忙しいところご足労いただき大変恐縮です。",
        "exampleFurigana": "おいそがしい ところ ごそくろう いただき たいへん きょうしゅくです。",
        "exampleZh": "百忙之中让您特意跑一趟，十分过意不去。",
        "exampleEn": "I am terribly obliged and grateful for you taking the time to come all the way here amidst your busy schedule.",
        "transitivePair": None,
        "collocation": "大変恐縮です",
        "examYearNote": "JLPT N2 Business Etiquette",
        "scenarioTag": "business"
    },
    {
        "id": "n2_exp_003_chousei",
        "kanji": "調整",
        "reading": "ちょうせい",
        "romaji": "chousei",
        "pitchAccent": "[0] Heiban",
        "level": "N2",
        "partOfSpeech": "Noun / Suru-Verb",
        "meaning": "Adjustment, coordination, fine-tuning schedule",
        "exampleJa": "来週のミーティング日程をクライアントと調整中です。",
        "exampleFurigana": "らいしゅうの みーてぃんぐ にっていを くらいあんとと ちょうせいちゅうです。",
        "exampleZh": "正在与客户协调下周的会议日程。",
        "exampleEn": "Currently coordinating next week's meeting schedule with the client.",
        "transitivePair": None,
        "collocation": "日程を調整する",
        "examYearNote": "JLPT N2 Business",
        "scenarioTag": "business"
    },

    # --- N1: Elite Tokyo Lexicon & Literary Depth ---
    {
        "id": "n1_exp_001_sashitsukaenai",
        "kanji": "差し支えない",
        "reading": "さしつかえない",
        "romaji": "sashitsukaenai",
        "pitchAccent": "[5] Nakadaka",
        "level": "N1",
        "partOfSpeech": "I-Adjective Phrase",
        "meaning": "Acceptable, causes no hindrance / inconvenience, fine to proceed",
        "exampleJa": "もし差し支えなければ、詳しい連絡先をお教えいただけますか？",
        "exampleFurigana": "もし さしつかえなければ、くわしい れんらくさきを おしえいただけますか？",
        "exampleZh": "如果不便之处不存在（方便的话），能否告知详细联系方式？",
        "exampleEn": "If it causes no inconvenience, could you please provide your detailed contact information?",
        "transitivePair": None,
        "collocation": "差し支えなければ",
        "examYearNote": "JLPT N1 Keigo Elite",
        "scenarioTag": "business"
    },
    {
        "id": "n1_exp_002_sessen",
        "kanji": "折衝",
        "reading": "せっしょう",
        "romaji": "sesshou",
        "pitchAccent": "[0] Heiban",
        "level": "N1",
        "partOfSpeech": "Noun / Suru-Verb",
        "meaning": "High-level negotiation, diplomatic parley, bargaining compromise",
        "exampleJa": "両国代表団は深夜まで激しい外交折衝を重ねました。",
        "exampleFurigana": "りょうこく だいひょうだんは しんやまで はげしい がいこう せっしょうを かさねました。",
        "exampleZh": "两国代表团持续进行了激烈的外交谈判直至深夜。",
        "exampleEn": "The delegation of both countries engaged in intense diplomatic negotiations late into the night.",
        "transitivePair": None,
        "collocation": "外交折衝",
        "examYearNote": "JLPT N1 Political/Commercial",
        "scenarioTag": "news"
    },
    {
        "id": "n1_exp_003_yuyo",
        "kanji": "猶予",
        "reading": "ゆうよ",
        "romaji": "yuuyo",
        "pitchAccent": "[1] Atamadaka",
        "level": "N1",
        "partOfSpeech": "Noun / Suru-Verb",
        "meaning": "Grace period, postponement, reprieve, delay",
        "exampleJa": "事態の悪化により、もはや一刻の猶予も許されない状況です。",
        "exampleFurigana": "じたいの あっかにより、もはや いっこくの ゆうよも ゆるされない じょうきょうです。",
        "exampleZh": "随着事态恶化，已是刻不容缓的局面。",
        "exampleEn": "With the worsening situation, not a single moment of delay can be afforded.",
        "transitivePair": None,
        "collocation": "一刻の猶予もない",
        "examYearNote": "JLPT N1 Media / Essay",
        "scenarioTag": "news"
    }
]

def main():
    if not os.path.exists(DICT_PATH):
        print(f"Error: {DICT_PATH} not found!")
        return

    with open(DICT_PATH, "r", encoding="utf-8") as f:
        existing_words = json.load(f)

    existing_keys = set((w.get("kanji") or w.get("reading"), w.get("reading")) for w in existing_words)
    existing_ids = set(w.get("id") for w in existing_words)

    added_count = 0
    for entry in NEW_VOCAB_ENTRIES:
        key = (entry.get("kanji") or entry.get("reading"), entry.get("reading"))
        if key not in existing_keys and entry["id"] not in existing_ids:
            existing_words.append(entry)
            existing_keys.add(key)
            existing_ids.add(entry["id"])
            added_count += 1

    # Save cleanly back
    with open(DICT_PATH, "w", encoding="utf-8") as f:
        json.dump(existing_words, f, ensure_ascii=False, indent=2)

    print(f"✓ Successfully enriched dictionary!")
    print(f"  • New additions: +{added_count}")
    print(f"  • Total words in {DICT_PATH}: {len(existing_words)}")

    # Distribution stats
    levels = {}
    for w in existing_words:
        lvl = w.get("level", "Unknown")
        levels[lvl] = levels.get(lvl, 0) + 1
    print(f"  • Level distribution: {levels}")

if __name__ == "__main__":
    main()
