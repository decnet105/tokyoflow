import asyncio
import os
import json
import subprocess
import edge_tts
import time

VOICEBANK_DIR = "TokyoFlow/Resources/Audio/VoiceBank"
MANIFEST_PATH = os.path.join(VOICEBANK_DIR, "voice_bank_manifest.json")
JLPT_PATH = "TokyoFlow/Resources/jlpt_dictionary.json"

SAMPLE_RATE = 44100
VOICE_FEMALE = "ja-JP-NanamiNeural"
FEMALE_EQ_FILTER = "equalizer=f=300:t=q:w=1.2:g=1.5,equalizer=f=4000:t=q:w=1.5:g=1.0,equalizer=f=8000:t=q:w=2.0:g=-3.0,lowpass=f=9500,aresample=44100"

async def synth_voice_file(text: str, out_m4a: str):
    temp_wav = out_m4a.replace(".m4a", ".wav")
    temp_mp3 = out_m4a.replace(".m4a", ".mp3")
    comm = edge_tts.Communicate(text, VOICE_FEMALE, rate="-10%", pitch="+4Hz")
    await comm.save(temp_mp3)
    subprocess.run([
        "/opt/homebrew/bin/ffmpeg", "-y", "-i", temp_mp3,
        "-af", FEMALE_EQ_FILTER,
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        out_m4a
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(temp_mp3): os.remove(temp_mp3)
    if os.path.exists(temp_wav): os.remove(temp_wav)

# Comprehensive Junior-High School Graduate Vocabulary Matrix
expanded_lexicon = [
    # --- N5 (Elementary / Life Basics) ---
    {"id": "n5_021", "kanji": "朝", "reading": "あさ", "romaji": "asa", "pitchAccent": "① (頭高)", "level": "N5", "partOfSpeech": "名詞", "meaning": "早上 / Morning", "exampleJa": "毎朝7時に起きます。", "exampleFurigana": "まいあさ しちじに おきます。", "exampleZh": "每天早上7点起床。", "exampleEn": "I wake up at 7 every morning."},
    {"id": "n5_022", "kanji": "夜", "reading": "よる", "romaji": "yoru", "pitchAccent": "① (頭高)", "level": "N5", "partOfSpeech": "名詞", "meaning": "夜晚 / Night", "exampleJa": "夜の東京タワーはとても綺麗です。", "exampleFurigana": "よるの とうきょうたわーは とても きれいです。", "exampleZh": "晚上的东京铁塔非常漂亮。", "exampleEn": "Tokyo Tower is very beautiful at night."},
    {"id": "n5_023", "kanji": "学校", "reading": "がっこう", "romaji": "gakkou", "pitchAccent": "⓪ (平板)", "level": "N5", "partOfSpeech": "名詞", "meaning": "学校 / School", "exampleJa": "地下鉄で学校に通っています。", "exampleFurigana": "ちかてつで がっこうに かよっています。", "exampleZh": "坐地铁上学。", "exampleEn": "I commute to school by subway."},
    {"id": "n5_024", "kanji": "先生", "reading": "せんせい", "romaji": "sensei", "pitchAccent": "③ (尾高)", "level": "N5", "partOfSpeech": "名詞", "meaning": "老师 / Teacher", "exampleJa": "日本語の先生に質問しました。", "exampleFurigana": "にほんごの せんせいに しつもんしました。", "exampleZh": "向日语老师提问。", "exampleEn": "I asked a question to my Japanese teacher."},
    {"id": "n5_025", "kanji": "話す", "reading": "はなす", "romaji": "hanasu", "pitchAccent": "② (中高)", "level": "N5", "partOfSpeech": "動詞", "meaning": "说话 / To speak", "exampleJa": "店員さんと日本語で話しました。", "exampleFurigana": "てんいんさんと にほんごで はなしました。", "exampleZh": "和店员用日语交谈。", "exampleEn": "Spoke in Japanese with the store clerk."},
    {"id": "n5_026", "kanji": "聞く", "reading": "きく", "romaji": "kiku", "pitchAccent": "⓪ (平板)", "level": "N5", "partOfSpeech": "動詞", "meaning": "听 / To listen, hear", "exampleJa": "毎日NHKラジオニュースを聞きます。", "exampleFurigana": "まいにち えぬえいちけー らじおにゅーすを ききます。", "exampleZh": "每天听NHK广播新闻。", "exampleEn": "I listen to NHK radio news every day."},
    {"id": "n5_027", "kanji": "書く", "reading": "かく", "romaji": "kaku", "pitchAccent": "① (頭高)", "level": "N5", "partOfSpeech": "動詞", "meaning": "写 / To write", "exampleJa": "ノートに新しい漢字を書く。", "exampleFurigana": "のーとに あたらしい かんじを かく。", "exampleZh": "在笔记本上写新汉字。", "exampleEn": "Write new kanji in the notebook."},
    {"id": "n5_028", "kanji": "読む", "reading": "よむ", "romaji": "yomu", "pitchAccent": "① (頭高)", "level": "N5", "partOfSpeech": "動詞", "meaning": "读 / To read", "exampleJa": "電車の広告を読んでみる。", "exampleFurigana": "でんしゃの こうこくを よんでみる。", "exampleZh": "试着阅读电车上的广告。", "exampleEn": "Try reading the train advertisements."},
    {"id": "n5_029", "kanji": "買う", "reading": "かう", "romaji": "kau", "pitchAccent": "⓪ (平板)", "level": "N5", "partOfSpeech": "動詞", "meaning": "买 / To buy", "exampleJa": "お土産に抹茶のお菓子を買いました。", "exampleFurigana": "おみやげに まっちゃの おかしを かいました。", "exampleZh": "买了抹茶点心作为伴手礼。", "exampleEn": "Bought matcha sweets as souvenirs."},
    {"id": "n5_030", "kanji": "待つ", "reading": "まつ", "romaji": "matsu", "pitchAccent": "① (頭高)", "level": "N5", "partOfSpeech": "動詞", "meaning": "等 / To wait", "exampleJa": "ハチ公前で友達を待っています。", "exampleFurigana": "はちこうまえで ともだちを まっています。", "exampleZh": "在八公像前等朋友。", "exampleEn": "Waiting for a friend in front of Hachiko."},

    # --- N4 (Everyday Immersion & Practical Situations) ---
    {"id": "n4_011", "kanji": "急行", "reading": "きゅうこう", "romaji": "kyuukou", "pitchAccent": "⓪ (平板)", "level": "N4", "partOfSpeech": "名詞", "meaning": "急行列车、快车 / Express train", "exampleJa": "この電車は急行なので次の主要駅に停まります。", "exampleFurigana": "この でんしゃは きゅうこうなので つぎの しゅようえきに とまります。", "exampleZh": "这趟电车是快车，停靠下一个主要车站。", "exampleEn": "This train is an express, stopping at the next major station."},
    {"id": "n4_012", "kanji": "温める", "reading": "あたためる", "romaji": "atatameru", "pitchAccent": "④ (中高)", "level": "N4", "partOfSpeech": "動詞", "meaning": "加热 / To warm up", "exampleJa": "お弁当をレンジで温めていただけますか？", "exampleFurigana": "おべんとうを れんじで あたためて いただけますか？", "exampleZh": "可以帮我用微波炉加热便当吗？", "exampleEn": "Could you please warm up the bento in the microwave?"},
    {"id": "n4_013", "kanji": "会計", "reading": "かいけい", "romaji": "kaikei", "pitchAccent": "⓪ (平板)", "level": "N4", "partOfSpeech": "名詞", "meaning": "结账、买单 / Bill, checkout", "exampleJa": "お会計は別々でお願いします。", "exampleFurigana": "おかいけいは べつべつで おねがいします。", "exampleZh": "结账请分开付。", "exampleEn": "We would like to pay separately, please."},
    {"id": "n4_014", "kanji": "袋", "reading": "ふくろ", "romaji": "fukuro", "pitchAccent": "③ (尾高)", "level": "N4", "partOfSpeech": "名詞", "meaning": "袋子 / Bag", "exampleJa": "レジ袋は大丈夫です、マイバッグがあります。", "exampleFurigana": "れじぶくろは だいじょうぶです、まいばっぐが あります。", "exampleZh": "不用塑料袋了，我有自带环保袋。", "exampleEn": "I don't need a plastic bag; I have my own reusable bag."},
    {"id": "n4_015", "kanji": "準備", "reading": "じゅんび", "romaji": "junbi", "pitchAccent": "① (頭高)", "level": "N4", "partOfSpeech": "名詞/動詞", "meaning": "准备 / Preparation", "exampleJa": "明日のお出かけの準備を済ませました。", "exampleFurigana": "あしたの おでかけの じゅんびを すませました。", "exampleZh": "做好了明天出门的准备。", "exampleEn": "Finished preparations for going out tomorrow."},

    # --- N3 (Intermediate Conversation & Japanese Culture) ---
    {"id": "n3_011", "kanji": "満員", "reading": "まんいん", "romaji": "man'in", "pitchAccent": "⓪ (平板)", "level": "N3", "partOfSpeech": "名詞", "meaning": "客满、满员 / Packed, crowded full", "exampleJa": "朝のラッシュ時の山手線は超満員です。", "exampleFurigana": "あさの らっしゅじの やまのてせんは ちょうまんいんです。", "exampleZh": "早高峰的山手线人满为患。", "exampleEn": "The Yamanote Line is packed to capacity during morning rush hour."},
    {"id": "n3_012", "kanji": "お通し", "reading": "おとおし", "romaji": "otooshi", "pitchAccent": "⓪ (平板)", "level": "N3", "partOfSpeech": "名詞", "meaning": "居酒屋开胃小菜 / Appetizer cover charge", "exampleJa": "居酒屋に着席すると、すぐにお通しが運ばれてきた。", "exampleFurigana": "いざかやに ちゃくせきすると、すぐに おとおしが はこばれてきた。", "exampleZh": "在居酒屋就座后，开胃小菜马上端了上来。", "exampleEn": "As soon as we sat down at the izakaya, the table appetizer was served."},
    {"id": "n3_013", "kanji": "乾杯", "reading": "かんぱい", "romaji": "kanpai", "pitchAccent": "⓪ (平板)", "level": "N3", "partOfSpeech": "名詞/動詞", "meaning": "干杯 / Cheers, toast", "exampleJa": "「お疲れ様でした！」とみんなで生ビールで乾杯した。", "exampleFurigana": "「おつかれさまでした！」と みんなで なまびーるで かんぱいした。", "exampleZh": "大家一起说着“辛苦了！”用生啤干杯。", "exampleEn": "Everyone toasted with draft beer, saying 'Cheers for your hard work!'"},
    {"id": "n3_014", "kanji": "改札", "reading": "かいさつ", "romaji": "kaisatsu", "pitchAccent": "⓪ (平板)", "level": "N3", "partOfSpeech": "名詞", "meaning": "检票口 / Ticket gate", "exampleJa": "スマホを改札機にかざすだけでスムーズに通れます。", "exampleFurigana": "すまほを かいさつきに かざすだけで すむーずに とおります。", "exampleZh": "只需将手机贴近检票机即可顺畅通过。", "exampleEn": "Simply hold your smartphone over the gate to pass smoothly."},
    {"id": "n3_015", "kanji": "優先席", "reading": "ゆうせんせき", "romaji": "yuusenseki", "pitchAccent": "③ (中高)", "level": "N3", "partOfSpeech": "名詞", "meaning": "爱心专座、优先席 / Priority seating", "exampleJa": "お年寄りや妊婦さんのために優先席を譲りましょう。", "exampleFurigana": "おとしよりや にんぷさんの ために ゆうせんせきを ゆずりましょう。", "exampleZh": "请为老人和孕妇让出爱心专座。", "exampleEn": "Let's yield priority seats to the elderly and pregnant women."},

    # --- N2 (Advanced Expression & Social Media/Business) ---
    {"id": "n2_007", "kanji": "問い合わせ", "reading": "といあわせ", "romaji": "toiawase", "pitchAccent": "⓪ (平板)", "level": "N2", "partOfSpeech": "名詞", "meaning": "咨询、询问 / Inquiry", "exampleJa": "落とし物センターに忘れ物の問い合わせをした。", "exampleFurigana": "おとしものせんたーに わすれものの といあわせを した。", "exampleZh": "向失物招领中心咨询了遗落物品。", "exampleEn": "I made an inquiry about lost property at the lost and found center."},
    {"id": "n2_008", "kanji": "柔軟", "reading": "じゅうなん", "romaji": "juunan", "pitchAccent": "⓪ (平板)", "level": "N2", "partOfSpeech": "形容動詞", "meaning": "灵活、柔软 / Flexible, adaptable", "exampleJa": "予期せぬトラブルにも柔軟に対応できる姿勢が大切です。", "exampleFurigana": "よきせぬ とらぶるにも じゅうなんに たいおうできる しせいが たいせつです。", "exampleZh": "面对意料之外的问题，能灵活应对的姿态至关重要。", "exampleEn": "A flexible attitude to handle unexpected issues is essential."},
    {"id": "n2_009", "kanji": "推進", "reading": "すいしん", "romaji": "suishin", "pitchAccent": "⓪ (平板)", "level": "N2", "partOfSpeech": "名詞/動詞", "meaning": "推进、倡导 / Promotion, drive forward", "exampleJa": "東京都はキャッシュレス決済の普及を推進しています。", "exampleFurigana": "とうきょうとは きゃっしゅれすけっさいの ふきゅうを すいしんしています。", "exampleZh": "东京都正大力推进无现金支付的普及。", "exampleEn": "The Tokyo Metropolitan Government is actively promoting cashless payments."},
    {"id": "n2_010", "kanji": "効率的", "reading": "こうりつてき", "romaji": "kouritsuteki", "pitchAccent": "⓪ (平板)", "level": "N2", "partOfSpeech": "形容動詞", "meaning": "高效率的 / Efficient", "exampleJa": "スキマ時間を活用して効率的に語彙力を強化する。", "exampleFurigana": "すきまじかんを かつようして こうりつてきに ごいりょくを きょうかする。", "exampleZh": "利用碎片时间高效率强化词汇量。", "exampleEn": "Leveraging spare moments to efficiently boost vocabulary."},

    # --- N1 (Nuanced Mastery & Formal Media) ---
    {"id": "n1_006", "kanji": "如実", "reading": "にょじつ", "romaji": "nyojitsu", "pitchAccent": "⓪ (平板)", "level": "N1", "partOfSpeech": "形容動詞", "meaning": "真实、如实 / Vividly, authentically", "exampleJa": "観光客の増加は日本文化の人気を如実に物語っている。", "exampleFurigana": "かんこうきゃくの ぞうかは にほんぶんかの にんきを にょじつに ものがたっている。", "exampleZh": "游客的增长如实反映了日本文化的超高人气。", "exampleEn": "The increase in tourists authentically reflects the popularity of Japanese culture."},
    {"id": "n1_007", "kanji": "申し分ない", "reading": "もうしぶんない", "romaji": "moushibunnai", "pitchAccent": "⑤ (中高)", "level": "N1", "partOfSpeech": "形容詞", "meaning": "无可挑剔、十全十美 / Beyond reproach, flawless", "exampleJa": "最新のスマートフォンは性能も画質も申し分ない。", "exampleFurigana": "さいしんの すまーとふぉんは せいのうも がしつも もうしぶんない。", "exampleZh": "最新的智能手机在性能与画质上都无可挑剔。", "exampleEn": "The newest smartphone is flawless in both performance and image quality."},
    {"id": "n1_008", "kanji": "克明", "reading": "こくめい", "romaji": "kokumei", "pitchAccent": "⓪ (平板)", "level": "N1", "partOfSpeech": "形容動詞", "meaning": "详尽、细致入微 / Minute, detailed", "exampleJa": "ニュース番組では台風の被害状況が克明に報じられた。", "exampleFurigana": "にゅーすばんぐみでは たいふうの ひがいじょうきょうが こくめいに ほうじられた。", "exampleZh": "新闻节目详尽细致地报道了台风的受灾情况。", "exampleEn": "The news program reported the typhoon damages in minute detail."}
]

# Load existing JLPT database and merge
with open(JLPT_PATH, "r", encoding="utf-8") as f:
    existing = json.load(f)

existing_ids = {w["id"] for w in existing}
for w in expanded_lexicon:
    if w["id"] not in existing_ids:
        existing.append(w)

with open(JLPT_PATH, "w", encoding="utf-8") as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

print(f"📖 Complete JLPT dictionary now contains {len(existing)} comprehensive entries!")

# Update manifest and synthesize audio for all words
with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
    manifest = json.load(f)

new_files_to_synth = {}
for w in existing:
    if w["kanji"]:
        fn_k = f"jlpt_{w['id']}_kanji.m4a"
        manifest[w["kanji"]] = fn_k
        manifest[w["kanji"].lower()] = fn_k
        new_files_to_synth[fn_k] = w["kanji"]
    if w["reading"]:
        fn_r = f"jlpt_{w['id']}_reading.m4a"
        manifest[w["reading"]] = fn_r
        new_files_to_synth[fn_r] = w["reading"]
    if w["exampleJa"]:
        fn_e = f"jlpt_{w['id']}_ex.m4a"
        manifest[w["exampleJa"]] = fn_e
        new_files_to_synth[fn_e] = w["exampleJa"]

with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"🎙️ Total VoiceBank indexed keys: {len(manifest)}. Checking and synthesizing missing files...")

sem = asyncio.Semaphore(16)
done = 0
total = len(new_files_to_synth)

async def synth_item(fn, text):
    global done
    out_path = os.path.join(VOICEBANK_DIR, fn)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        done += 1
        return
    async with sem:
        try:
            await synth_voice_file(text, out_path)
            done += 1
        except Exception as e:
            print(f"Error {fn}: {e}")

async def main():
    t0 = time.time()
    tasks = [synth_item(fn, txt) for fn, txt in new_files_to_synth.items()]
    await asyncio.gather(*tasks)
    t1 = time.time()
    print(f"🎉 All {done}/{total} dictionary audio files ready in {t1-t0:.2f}s!")

if __name__ == "__main__":
    asyncio.run(main())
