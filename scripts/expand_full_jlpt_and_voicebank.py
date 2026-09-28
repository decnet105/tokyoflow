import asyncio
import os
import json
import subprocess
import wave
import edge_tts
import re
import time

AUDIO_DIR = "TokyoFlow/Resources/Audio"
VOICEBANK_DIR = "TokyoFlow/Resources/Audio/VoiceBank"
MANIFEST_PATH = os.path.join(VOICEBANK_DIR, "voice_bank_manifest.json")
JLPT_PATH = "TokyoFlow/Resources/jlpt_dictionary.json"
RADIO_FILE = os.path.join(AUDIO_DIR, "nhk_journal_55min.m4a")

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(VOICEBANK_DIR, exist_ok=True)

SAMPLE_RATE = 44100
VOICE_FEMALE = "ja-JP-NanamiNeural"  # Sweet, soothing, authentic NHK female
VOICE_MALE = "ja-JP-KeitaNeural"    # Warm broadcast male

# Filter for male voice to remove any metallic/scratchy digital residue and add warmth
MALE_EQ_FILTER = "equalizer=f=230:t=q:w=1.2:g=3.8,equalizer=f=3200:t=q:w=1.8:g=-2.5,equalizer=f=6500:t=q:w=2.0:g=-6.0,lowpass=f=8200,aresample=44100"
# Filter for female voice for pleasant clarity and sweetness
FEMALE_EQ_FILTER = "equalizer=f=300:t=q:w=1.2:g=1.5,equalizer=f=4000:t=q:w=1.5:g=1.0,equalizer=f=8000:t=q:w=2.0:g=-3.0,lowpass=f=9500,aresample=44100"

async def synth_to_wav(text: str, voice: str, out_wav: str, is_male: bool = False, slow: bool = True):
    temp_mp3 = out_wav + ".mp3"
    rate_str = "-12%" if slow else "-5%"
    pitch_str = "-2Hz" if is_male else "+4Hz"
    
    comm = edge_tts.Communicate(text, voice, rate=rate_str, pitch=pitch_str)
    await comm.save(temp_mp3)

    filt = MALE_EQ_FILTER if is_male else FEMALE_EQ_FILTER
    subprocess.run([
        "/opt/homebrew/bin/ffmpeg", "-y", "-i", temp_mp3,
        "-af", filt,
        "-ar", str(SAMPLE_RATE), "-ac", "2", "-c:a", "pcm_s16le",
        out_wav
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if os.path.exists(temp_mp3):
        os.remove(temp_mp3)

def create_silence_bytes(duration_sec: float) -> bytes:
    n_samples = int(duration_sec * SAMPLE_RATE)
    return b'\x00\x00\x00\x00' * n_samples

# ==============================================================================
# 1. EXPANDED JLPT N5-N1 & DAILY TOKYO SCENARIO VOCABULARY (~Junior High Graduate)
# ==============================================================================
jlpt_core_database = [
    # --- N5: Foundations & Essential Daily Life ---
    {"id": "n5_001", "kanji": "私", "reading": "わたし", "romaji": "watashi", "pitchAccent": "⓪ (平板)", "level": "N5", "partOfSpeech": "代名詞", "meaning": "我 / I, me", "exampleJa": "私は東京に住んでいます。", "exampleFurigana": "わたしは とうきょうに すんでいます。", "exampleZh": "我住在东京。", "exampleEn": "I live in Tokyo."},
    {"id": "n5_002", "kanji": "駅", "reading": "えき", "romaji": "eki", "pitchAccent": "① (頭高)", "level": "N5", "partOfSpeech": "名詞", "meaning": "车站 / Station", "exampleJa": "新宿駅で山手線に乗り換えます。", "exampleFurigana": "しんじゅくえきで やまのてせんに のりかえます。", "exampleZh": "在新宿站换乘山手线。", "exampleEn": "Transfer to the Yamanote Line at Shinjuku Station."},
    {"id": "n5_003", "kanji": "行く", "reading": "いく", "romaji": "iku", "pitchAccent": "⓪ (平板)", "level": "N5", "partOfSpeech": "動詞", "meaning": "去 / To go", "exampleJa": "明日秋葉原へ行きます。", "exampleFurigana": "あした あきはばらへ いきます。", "exampleZh": "明天去秋叶原。", "exampleEn": "I am going to Akihabara tomorrow."},
    {"id": "n5_004", "kanji": "食べる", "reading": "たべる", "romaji": "taberu", "pitchAccent": "② (中高)", "level": "N5", "partOfSpeech": "動詞", "meaning": "吃 / To eat", "exampleJa": "お昼ご飯に牛丼を食べます。", "exampleFurigana": "おひるごはんに ぎゅうどんを たべます。", "exampleZh": "午饭吃牛肉饭。", "exampleEn": "I eat beef bowl for lunch."},
    {"id": "n5_005", "kanji": "飲む", "reading": "のむ", "romaji": "nomu", "pitchAccent": "① (頭高)", "level": "N5", "partOfSpeech": "動詞", "meaning": "喝 / To drink", "exampleJa": "喫茶店で冷たいアイスラテを飲む。", "exampleFurigana": "きっさてんで つめたい あいすらてを のむ。", "exampleZh": "在咖啡厅喝冰拿铁。", "exampleEn": "Drink iced latte at the cafe."},
    {"id": "n5_006", "kanji": "買う", "reading": "かう", "romaji": "kau", "pitchAccent": "⓪ (平板)", "level": "N5", "partOfSpeech": "動詞", "meaning": "买 / To buy", "exampleJa": "コンビニでおにぎりを二つ買いました。", "exampleFurigana": "こんびにで おにぎりを ふたつ かいました。", "exampleZh": "在便利店买了两个饭团。", "exampleEn": "Bought two rice balls at the convenience store."},
    {"id": "n5_007", "kanji": "本", "reading": "ほん", "romaji": "hon", "pitchAccent": "① (頭高)", "level": "N5", "partOfSpeech": "名詞", "meaning": "书 / Book", "exampleJa": "本屋で日本のマンガを買いました。", "exampleFurigana": "ほんやで にほんの まんがを かいました。", "exampleZh": "在书店买了日本漫画。", "exampleEn": "Bought Japanese manga at the bookstore."},
    {"id": "n5_008", "kanji": "見る", "reading": "みる", "romaji": "miru", "pitchAccent": "① (頭高)", "level": "N5", "partOfSpeech": "動詞", "meaning": "看 / To see, watch", "exampleJa": "今夜新作のアニメを見ます。", "exampleFurigana": "こんや しんさくの あにめを みます。", "exampleZh": "今晚看新动画。", "exampleEn": "I will watch new anime tonight."},
    {"id": "n5_009", "kanji": "時間", "reading": "じかん", "romaji": "jikan", "pitchAccent": "⓪ (平板)", "level": "N5", "partOfSpeech": "名詞", "meaning": "时间 / Time", "exampleJa": "電車の時間を確認してください。", "exampleFurigana": "でんしゃの じかんを かくにんしてください。", "exampleZh": "请确认电车时间。", "exampleEn": "Please check the train time."},
    {"id": "n5_010", "kanji": "電車", "reading": "でんしゃ", "romaji": "densha", "pitchAccent": "⓪ (平板)", "level": "N5", "partOfSpeech": "名詞", "meaning": "电车 / Train", "exampleJa": "朝の電車はとても混んでいます。", "exampleFurigana": "あさの でんしゃは とても こんでいます。", "exampleZh": "早上的电车非常拥挤。", "exampleEn": "The morning train is very crowded."},
    {"id": "n5_011", "kanji": "水", "reading": "みず", "romaji": "mizu", "pitchAccent": "⓪ (平板)", "level": "N5", "partOfSpeech": "名詞", "meaning": "水 / Water", "exampleJa": "冷たいお水を一杯ください。", "exampleFurigana": "つめたい おみずを いっぱいくダさい。", "exampleZh": "请给我一杯冰水。", "exampleEn": "Please give me a glass of cold water."},
    {"id": "n5_012", "kanji": "大きい", "reading": "おおきい", "romaji": "ookii", "pitchAccent": "③ (中高)", "level": "N5", "partOfSpeech": "形容詞", "meaning": "大的 / Big, large", "exampleJa": "東京ドームはとても大きいです。", "exampleFurigana": "とうきょうどーむは とても おおきいです。", "exampleZh": "东京巨蛋非常大。", "exampleEn": "Tokyo Dome is very big."},
    {"id": "n5_013", "kanji": "小さい", "reading": "ちいさい", "romaji": "chiisai", "pitchAccent": "③ (中高)", "level": "N5", "partOfSpeech": "形容詞", "meaning": "小的 / Small", "exampleJa": "小さいカバンを持って出かけます。", "exampleFurigana": "ちいさい かばんを もって でかけます。", "exampleZh": "拿着小包出门。", "exampleEn": "Going out carrying a small bag."},
    {"id": "n5_014", "kanji": "新しい", "reading": "あたらしい", "romaji": "atarashii", "pitchAccent": "④ (中高)", "level": "N5", "partOfSpeech": "形容詞", "meaning": "新的 / New", "exampleJa": "新しいスマホを買いました。", "exampleFurigana": "あたらしい すまほを かいました。", "exampleZh": "买了新智能手机。", "exampleEn": "I bought a new smartphone."},
    {"id": "n5_015", "kanji": "古い", "reading": "ふるい", "romaji": "furui", "pitchAccent": "② (中高)", "level": "N5", "partOfSpeech": "形容詞", "meaning": "旧的、古老的 / Old", "exampleJa": "浅草には古いお寺がたくさんあります。", "exampleFurigana": "あさくさには ふるい おてらが たくさん あります。", "exampleZh": "浅草有很多古老的寺庙。", "exampleEn": "There are many old temples in Asakusa."},
    {"id": "n5_016", "kanji": "友達", "reading": "ともだち", "romaji": "tomodachi", "pitchAccent": "⓪ (平板)", "level": "N5", "partOfSpeech": "名詞", "meaning": "朋友 / Friend", "exampleJa": "週末に友達と渋谷で会います。", "exampleFurigana": "しゅうまつに ともだちと しぶやで あいます。", "exampleZh": "周末和朋友在涩谷见面。", "exampleEn": "Meeting friends in Shibuya this weekend."},
    {"id": "n5_017", "kanji": "今日", "reading": "きょう", "romaji": "kyou", "pitchAccent": "① (頭高)", "level": "N5", "partOfSpeech": "名詞", "meaning": "今天 / Today", "exampleJa": "今日の天気は晴れです。", "exampleFurigana": "きょうの てんきは はれです。", "exampleZh": "今天天气晴朗。", "exampleEn": "Today's weather is sunny."},
    {"id": "n5_018", "kanji": "明日", "reading": "あした", "romaji": "ashita", "pitchAccent": "③ (尾高)", "level": "N5", "partOfSpeech": "名詞", "meaning": "明天 / Tomorrow", "exampleJa": "明日は朝早く起きます。", "exampleFurigana": "あしたは あさはやく おきます。", "exampleZh": "明天早上早起。", "exampleEn": "I will wake up early tomorrow morning."},
    {"id": "n5_019", "kanji": "何", "reading": "なに", "romaji": "nani", "pitchAccent": "① (頭高)", "level": "N5", "partOfSpeech": "代名詞", "meaning": "什么 / What", "exampleJa": "おすすめのメニューは何ですか？", "exampleFurigana": "おすすめの めにゅーは なんですか？", "exampleZh": "推荐的菜单是什么？", "exampleEn": "What is the recommended menu item?"},
    {"id": "n5_020", "kanji": "日本語", "reading": "にほんご", "romaji": "nihongo", "pitchAccent": "⓪ (平板)", "level": "N5", "partOfSpeech": "名詞", "meaning": "日语 / Japanese language", "exampleJa": "毎日アプリで日本語を練習しています。", "exampleFurigana": "まいにち あぷりで にほんごを れんしゅうしています。", "exampleZh": "每天在App上练习日语。", "exampleEn": "I practice Japanese on the app every day."},

    # --- N4: Practical Daily Travel & Conversations ---
    {"id": "n4_001", "kanji": "乗り換える", "reading": "のりかえる", "romaji": "norikaeru", "pitchAccent": "④ (中高)", "level": "N4", "partOfSpeech": "動詞", "meaning": "换乘 / To transfer trains", "exampleJa": "大手町駅で半蔵門線に乗り換えてください。", "exampleFurigana": "おおてまちえきで はんぞうもんせんに のりかえてください。", "exampleZh": "请在大手町站换乘半藏门线。", "exampleEn": "Please transfer to the Hanzomon Line at Otemachi Station."},
    {"id": "n4_002", "kanji": "遅れる", "reading": "おくれる", "romaji": "okureru", "pitchAccent": "⓪ (平板)", "level": "N4", "partOfSpeech": "動詞", "meaning": "迟到、延误 / To be late, delayed", "exampleJa": "人身事故で中央線が10分遅れています。", "exampleFurigana": "じんしんじこで ちゅうおうせんが じゅっぷん おくれています。", "exampleZh": "因事故中央线延误了10分钟。", "exampleEn": "The Chuo Line is delayed by 10 minutes due to an incident."},
    {"id": "n4_003", "kanji": "案内", "reading": "あんない", "romaji": "annai", "pitchAccent": "③ (尾高)", "level": "N4", "partOfSpeech": "名詞", "meaning": "引导、指引 / Guidance, guide", "exampleJa": "店員さんが試着室へ案内してくれた。", "exampleFurigana": "てんいんさんが しちゃくしつへ あんないしてくれた。", "exampleZh": "店员引导我去了试衣间。", "exampleEn": "The clerk guided me to the fitting room."},
    {"id": "n4_004", "kanji": "都合", "reading": "つごう", "romaji": "tsugou", "pitchAccent": "⓪ (平板)", "level": "N4", "partOfSpeech": "名詞", "meaning": "情况、方便 / Convenience, circumstances", "exampleJa": "明日の午後はご都合よろしいですか？", "exampleFurigana": "あしたの ごごは ごつごう よろしいですか？", "exampleZh": "明天下午您方便吗？", "exampleEn": "Is tomorrow afternoon convenient for you?"},
    {"id": "n4_005", "kanji": "注文", "reading": "ちゅうもん", "romaji": "chuumon", "pitchAccent": "⓪ (平板)", "level": "N4", "partOfSpeech": "名詞/動詞", "meaning": "点餐、订购 / Order", "exampleJa": "タッチパネルでラーメンを注文しました。", "exampleFurigana": "たっちぱねるで らーめんを ちゅうもんしました。", "exampleZh": "用触控屏点了拉面。", "exampleEn": "Ordered ramen on the touch panel."},
    {"id": "n4_006", "kanji": "割引", "reading": "わりびき", "romaji": "waribiki", "pitchAccent": "⓪ (平板)", "level": "N4", "partOfSpeech": "名詞", "meaning": "打折、折扣 / Discount", "exampleJa": "夜8時以降は弁当が3割引になります。", "exampleFurigana": "よる はちじいこうは べんとうが さんわりびきに なります。", "exampleZh": "晚上8点后便当打7折。", "exampleEn": "Bentos get a 30% discount after 8 PM."},
    {"id": "n4_007", "kanji": "両替", "reading": "りょうがえ", "romaji": "ryougae", "pitchAccent": "⓪ (平板)", "level": "N4", "partOfSpeech": "名詞/動詞", "meaning": "兑换货币、换零钱 / Money exchange", "exampleJa": "券売機で千円札を両替できますか？", "exampleFurigana": "けんばいきで せんえんさつを りょうがえできますか？", "exampleZh": "能在自动售票机上换千元纸币吗？", "exampleEn": "Can I exchange a 1,000 yen bill at the ticket machine?"},
    {"id": "n4_008", "kanji": "連絡", "reading": "れんらく", "romaji": "renraku", "pitchAccent": "⓪ (平板)", "level": "N4", "partOfSpeech": "名詞/動詞", "meaning": "联络、通知 / Contact, reach out", "exampleJa": "遅れる時は必ず事前に連絡してください。", "exampleFurigana": "おくれるときは かならず じぜんに れんらくしてください。", "exampleZh": "迟到时请务必提前联络。", "exampleEn": "Please always contact in advance if you will be late."},
    {"id": "n4_009", "kanji": "遠慮", "reading": "えんりょ", "romaji": "enryo", "pitchAccent": "① (頭高)", "level": "N4", "partOfSpeech": "名詞/動詞", "meaning": "客气、顾虑 / Hesitation, reserve", "exampleJa": "どうぞ遠慮しないでたくさん食べてください。", "exampleFurigana": "どうぞ えんりょしないで たくさん たべてください。", "exampleZh": "请不要客气，多吃点。", "exampleEn": "Please do not hesitate and eat as much as you like."},
    {"id": "n4_010", "kanji": "無料", "reading": "むりょう", "romaji": "muryou", "pitchAccent": "⓪ (平板)", "level": "N4", "partOfSpeech": "名詞", "meaning": "免费 / Free of charge", "exampleJa": "店内ではフリーWi-Fiが無料で使えます。", "exampleFurigana": "てんないでは ふりーわいふぁいが むりょうで つかえます。", "exampleZh": "店内可以免费使用公共Wi-Fi。", "exampleEn": "Free Wi-Fi is available in the store at no charge."},

    # --- N3: Intermediate Immersion & Tokyo Living ---
    {"id": "n3_001", "kanji": "終電", "reading": "しゅうでん", "romaji": "shuuden", "pitchAccent": "⓪ (平板)", "level": "N3", "partOfSpeech": "名詞", "meaning": "末班车 / Last train", "exampleJa": "終電を逃して近くのカプセルホテルに泊まった。", "exampleFurigana": "しゅうでんを のがして ちかくの かぷせるほてるに とまった。", "exampleZh": "错过了末班车，住在附近的胶囊旅馆。", "exampleEn": "Missed the last train and stayed at a nearby capsule hotel."},
    {"id": "n3_002", "kanji": "消費期限", "reading": "しょうひきげん", "romaji": "shouhikigen", "pitchAccent": "④ (中高)", "level": "N3", "partOfSpeech": "名詞", "meaning": "保质期（新鲜食品使用期限） / Expiration date", "exampleJa": "消費期限が今日までなので早めに食べましょう。", "exampleFurigana": "しょうひきげんが きょうまでなので はやめに たべましょう。", "exampleZh": "保质期到今天为止，赶紧吃了吧。", "exampleEn": "The expiration date is today, so let's eat it soon."},
    {"id": "n3_003", "kanji": "手続き", "reading": "てつづき", "romaji": "tetsuzuki", "pitchAccent": "② (中高)", "level": "N3", "partOfSpeech": "名詞", "meaning": "手续 / Procedure, formalities", "exampleJa": "区役所で住民票の発行手続きを行いました。", "exampleFurigana": "くやくしょで じゅうみんひょうの はっこうてつづきを おこないました。", "exampleZh": "在区役所办理了住民票开具手续。", "exampleEn": "I completed the procedure to issue a resident record at the ward office."},
    {"id": "n3_004", "kanji": "見切り品", "reading": "みきりひん", "romaji": "mikirihin", "pitchAccent": "⓪ (平板)", "level": "N3", "partOfSpeech": "名詞", "meaning": "打折临期商品 / Discounted clearance food", "exampleJa": "夜のスーパーで見切り品の刺身を安く購入した。", "exampleFurigana": "よるの すーぱーで みきりひんの さしみをお やすく こうにゅうした。", "exampleZh": "在晚上的超市低价买了打折临期的刺身。", "exampleEn": "Bought discounted clearance sashimi cheaply at the supermarket at night."},
    {"id": "n3_005", "kanji": "領収書", "reading": "りょうしゅうしょ", "romaji": "ryoushuusho", "pitchAccent": "⓪ (平板)", "level": "N3", "partOfSpeech": "名詞", "meaning": "发票、收据 / Formal receipt", "exampleJa": "会社の経費で落とすため、宛名入りの領収書をお願いした。", "exampleFurigana": "かいしゃの けいひで おとすため、あてないりの りょうしゅうしょを おねがいした。", "exampleZh": "为了报销公司经费，要了带抬头的正式发票。", "exampleEn": "I requested a addressed receipt to expense it to the company."},
    {"id": "n3_006", "kanji": "限定", "reading": "げんてい", "romaji": "gentei", "pitchAccent": "⓪ (平板)", "level": "N3", "partOfSpeech": "名詞/動詞", "meaning": "限定 / Limited edition", "exampleJa": "秋葉原のイベントで会場限定フィギュアを手に入れた。", "exampleFurigana": "あきはばらの いべんとで かいじょうげんてい ふぃぎゅあを てにいれた。", "exampleZh": "在秋叶原的活动中入手了会场限定手办。", "exampleEn": "Acquired a venue-limited figure at the Akihabara event."},
    {"id": "n3_007", "kanji": "削減", "reading": "さくげん", "romaji": "sakugen", "pitchAccent": "⓪ (平板)", "level": "N3", "partOfSpeech": "名詞/動詞", "meaning": "削减、减少 / Reduction, cut down", "exampleJa": "コンビニ各社が食品ロス削減に向けた値引きを推進している。", "exampleFurigana": "こんびにかくしゃが しょくひんろすさくげんに むけた ねびきを すいしんしている。", "exampleZh": "各便利店正推进旨在削减食物浪费的打折措施。", "exampleEn": "Convenience store chains are promoting discounts to cut food loss."},
    {"id": "n3_008", "kanji": "工夫", "reading": "くふう", "romaji": "kufuu", "pitchAccent": "⓪ (平板)", "level": "N3", "partOfSpeech": "名詞/動詞", "meaning": "下功夫、巧妙构思 / Ingenuity, devise ways", "exampleJa": "短いスキマ時間を有効に使うよう工夫しています。", "exampleFurigana": "みじかい すきまじかんを ゆうこうに つかうよう くふうしています。", "exampleZh": "巧妙构思如何有效利用短暂的碎片时间。", "exampleEn": "I devise ways to use short spare moments effectively."},
    {"id": "n3_009", "kanji": "節約", "reading": "せつやく", "romaji": "setsuyaku", "pitchAccent": "⓪ (平板)", "level": "N3", "partOfSpeech": "名詞/動詞", "meaning": "节约、省钱 / Saving, economizing", "exampleJa": "自炊を増やして毎月の食費を節約しています。", "exampleFurigana": "じすいを ふやして まいつきの しょくひを せつやくしています。", "exampleZh": "增加自己做饭来节省每月的伙食费。", "exampleEn": "I cook more at home to save on monthly food expenses."},
    {"id": "n3_010", "kanji": "雰囲気", "reading": "ふんいき", "romaji": "fun'iki", "pitchAccent": "③ (中高)", "level": "N3", "partOfSpeech": "名詞", "meaning": "气氛、氛围 / Atmosphere, ambiance", "exampleJa": "この居酒屋はレトロな昭和の雰囲気が漂っている。", "exampleFurigana": "この いざかやは れとろな しょうわの ふんいきが ただよっている。", "exampleZh": "这家居酒屋洋溢着怀旧的昭和氛围。", "exampleEn": "This izakaya has a retro Showa-era ambiance."},

    # --- N2: Advanced Nuance & Business/Societal Reading ---
    {"id": "n2_001", "kanji": "ダイヤ改正", "reading": "だいやかいせい", "romaji": "daiyakaisei", "pitchAccent": "④ (中高)", "level": "N2", "partOfSpeech": "名詞", "meaning": "运行时刻表调整 / Timetable revision", "exampleJa": "春のダイヤ改正に伴い、終電の時刻が繰り上げられます。", "exampleFurigana": "はるの だいやかいせいに ともない、しゅうでんの じこくが くりあげられます。", "exampleZh": "伴随春季时刻表调整，末班车时刻提前。", "exampleEn": "With the spring timetable revision, final train departure times will be moved up."},
    {"id": "n2_002", "kanji": "配慮", "reading": "はいりょ", "romaji": "hairyo", "pitchAccent": "① (頭高)", "level": "N2", "partOfSpeech": "名詞/動詞", "meaning": "关照、顾及 / Consideration, concern for others", "exampleJa": "満員電車ではリュックサックを前に抱える配慮が求められる。", "exampleFurigana": "まんいんでんしゃでは りゅっくさっくを まえにかかえる はいりょが もとめられる。", "exampleZh": "在满员电车中需要注意把双肩包抱在胸前的体贴礼仪。", "exampleEn": "Holding backpacks in front is expected courtesy on crowded trains."},
    {"id": "n2_003", "kanji": "把握", "reading": "はあく", "romaji": "haaku", "pitchAccent": "⓪ (平板)", "level": "N2", "partOfSpeech": "名詞/動詞", "meaning": "掌握、领会 / Grasp, understand thoroughly", "exampleJa": "台風の進路と運行状況を正確に把握しておく必要がある。", "exampleFurigana": "たいふうの しんろと うんこうじょうきょうを せいかくに はあくしておく ひつようがある。", "exampleZh": "必须准确掌握台风路径和电车运行状况。", "exampleEn": "It is necessary to thoroughly grasp typhoon routes and transit status."},
    {"id": "n2_004", "kanji": "契機", "reading": "けいき", "romaji": "keiki", "pitchAccent": "① (頭高)", "level": "N2", "partOfSpeech": "名詞", "meaning": "契机、转机 / Opportunity, trigger", "exampleJa": "東京への旅行を契機に本格的な日本語学習を始めた。", "exampleFurigana": "とうきょうへの りょこうを けいきに ほんかくてきな にほんごがくしゅうを はじめた。", "exampleZh": "以去东京旅行受启发为契机，开始了系统学习日语。", "exampleEn": "A trip to Tokyo served as the trigger to begin serious Japanese studies."},
    {"id": "n2_005", "kanji": "臨機応変", "reading": "りんきおうへん", "romaji": "rinkiouhen", "pitchAccent": "⑤ (中高)", "level": "N2", "partOfSpeech": "四字熟語/形容動詞", "meaning": "随机应变 / Adapting flexibly to circumstances", "exampleJa": "列車の運休時には臨機応変に迂回ルートを選択する。", "exampleFurigana": "れっしゃの うんきゅうじには りんきおうへんに うかいるーとを せんたくする。", "exampleZh": "列车停运时要随机应变选择迂回路线。", "exampleEn": "Select detour routes flexibly when train services are suspended."},
    {"id": "n2_006", "kanji": "一環", "reading": "いっかん", "romaji": "ikkan", "pitchAccent": "⓪ (平板)", "level": "N2", "partOfSpeech": "名詞", "meaning": "一个环节 / Part of, link in a chain", "exampleJa": "環境保全の一環として、マイバッグ持参が定着している。", "exampleFurigana": "かんきょうほぜんの いっかんとして、まいばっぐじさんが ていちゃくしている。", "exampleZh": "作为环境保护的一环，自带购物袋已成为日常常态。", "exampleEn": "Bringing reusable shopping bags has caught on as part of environmental conservation."},

    # --- N1: Editorial, Broadcast & High Nuance Mastery ---
    {"id": "n1_001", "kanji": "余儀なくされる", "reading": "よぎなくされる", "romaji": "yoginakusareru", "pitchAccent": "⑥ (中高)", "level": "N1", "partOfSpeech": "連語/動詞", "meaning": "被迫、不得已 / Forced to, compelled to", "exampleJa": "大雨の影響で首都圏の交通網は運休を余儀なくされた。", "exampleFurigana": "おおあめの えいきょうで しゅとけんの こうつうもうは うんきゅうを よぎなくされた。", "exampleZh": "受大雨影响首都圈交通网络被迫停运。", "exampleEn": "The metropolitan transit network was forced to suspend operations due to heavy rainfall."},
    {"id": "n1_002", "kanji": "踏まえる", "reading": "ふまえる", "romaji": "fumaeru", "pitchAccent": "③ (中高)", "level": "N1", "partOfSpeech": "動詞", "meaning": "立足于、依据 / Based upon, taking into account", "exampleJa": "過去の台風被害を踏まえ、防犯・防災対策が強化されている。", "exampleFurigana": "かこの たいふうひがいを ふまえ、ぼうはん・ぼうさいたいさくが きょうかされている。", "exampleZh": "基于以往的台风灾害经验，防灾措施得到了进一步加强。", "exampleEn": "Disaster prevention measures are strengthened based on past typhoon damages."},
    {"id": "n1_003", "kanji": "目覚ましい", "reading": "めざましい", "romaji": "mezamashii", "pitchAccent": "④ (中高)", "level": "N1", "partOfSpeech": "形容詞", "meaning": "显著的、惊人的 / Remarkable, striking", "exampleJa": "AI自動運転技術の実用化は目覚ましい進歩を遂げている。", "exampleFurigana": "えーあい じどううんてんぎじゅつの じつようかは めざましい しんぽを とげている。", "exampleZh": "AI自动驾驶技术的实用化取得了令人瞩目的飞跃。", "exampleEn": "Practical application of AI autonomous driving technology has made remarkable strides."},
    {"id": "n1_004", "kanji": "巧みに", "reading": "たくみに", "romaji": "takumi ni", "pitchAccent": "② (中高)", "level": "N1", "partOfSpeech": "副詞", "meaning": "巧妙地 / Skillfully, cleverly", "exampleJa": "職人が伝統技術を巧みに操り、現代アートへと昇華させた。", "exampleFurigana": "しょくにんが でんとうぎじゅつを たくみに あやつり、げんだいあーとへと しょうかさせた。", "exampleZh": "匠人巧妙运用传统技艺，将其升华为当代艺术。", "exampleEn": "Artisans skillfully wield traditional techniques, sublimating them into contemporary art."},
    {"id": "n1_005", "kanji": "一概に", "reading": "いちがいに", "romaji": "ichigai ni", "pitchAccent": "⓪ (平板)", "level": "N1", "partOfSpeech": "副詞", "meaning": "一概、一概而论 / Sweepingly, unconditionally", "exampleJa": "言葉の使い分けは文脈によるため、一概には決められない。", "exampleFurigana": "ことばの つかいわけは ぶんみゃくによるため、いちがいには きめられない。", "exampleZh": "词汇用法的区分因语境而异，不能一概而论。", "exampleEn": "Distinguishing word usage depends on context and cannot be sweepingly generalized."}
]

# Write out jlpt_dictionary.json
with open(JLPT_PATH, "w", encoding="utf-8") as f:
    json.dump(jlpt_core_database, f, ensure_ascii=False, indent=2)

print(f"✅ Saved {len(jlpt_core_database)} JLPT core dictionary entries to {JLPT_PATH}")

# ==============================================================================
# 2. STUDIO NHK RADIO WITH COMFORTABLE SLOW CADENCE & PRECISE TIMESTAMPS
# ==============================================================================
broadcast_chapters = [
    {
        "id": "c1",
        "title": "Headlines & Opening",
        "titleJa": "オープニング・全国の主要ニュース",
        "description": "Opening signature broadcast chimes and national headlines.",
        "sentences": [
            {
                "id": "r1_1",
                "japanese": "皆様こんばんは。NHKジャーナル、夜の総合ニュースです。",
                "furigana": "みなさまこんばんは。えぬえいちけーじゃーなる、よるのそうごうにゅーすです。",
                "english": "Good evening everyone. This is NHK Journal with tonight's comprehensive evening news."
            },
            {
                "id": "r1_2",
                "japanese": "今夜の主なニュースをお伝えいたします。",
                "furigana": "こんやのおもなにゅーすをおつたえいたします。",
                "english": "We bring you tonight's major headlines."
            },
            {
                "id": "r1_3",
                "japanese": "JR東日本は、東京やその近くを走る電車の終電の時間を早めると発表しました。",
                "furigana": "じぇいあーるひがしにほんは、とうきょうやそのちかくをはしるでんしゃのしゅうでんのじかんをはやめるとはっぴょうしました。",
                "english": "JR East announced that it will advance the last train times for trains operating in and around Tokyo."
            },
            {
                "id": "r1_4",
                "japanese": "山手線や中央線など多くの主要路線で、終電が15分から30分程度早くなります。",
                "furigana": "やまのてせいやちゅうおうせんなどおおくのしゅようろせんで、しゅうでんがじゅうごふんからさんじゅっぷんていどはやくなります。",
                "english": "On major lines including the Yamanote and Chuo Lines, final departures will be 15 to 30 minutes earlier."
            },
            {
                "id": "r1_5",
                "japanese": "深夜に線路を点検・修繕する作業員の安全と働く時間を確保するための措置です。",
                "furigana": "しんやにせんろをてんけん・しゅうぜんするさぎょういんのあんぜんとはたらくじかんをかくほするためのそちです。",
                "english": "This measure is to secure safe working hours for crews inspecting and repairing tracks overnight."
            }
        ]
    },
    {
        "id": "c2",
        "title": "Tokyo Weather & Climate",
        "titleJa": "台風・首都圏の気象情報",
        "description": "Detailed Tokyo weather forecast, typhoon alerts, and transit operations.",
        "sentences": [
            {
                "id": "r2_1",
                "japanese": "続いて、気象庁からの首都圏の気象情報をお伝えします。",
                "furigana": "つづいて、きしょうちょうからのしゅとけんのきしょうじょうほうをおつたえします。",
                "english": "Next is the metropolitan weather update from the Japan Meteorological Agency."
            },
            {
                "id": "r2_2",
                "japanese": "南の海上に発生した大型の台風が、明日の夜にかけて関東地方に接近する見込みです。",
                "furigana": "みなみのかいじょうにはっせいしたおおがたのたいふうが、あすのよるにかけてかんとうちほうにせっきんするみこみです。",
                "english": "A large typhoon formed over southern waters is expected to approach the Kanto region by tomorrow evening."
            },
            {
                "id": "r2_3",
                "japanese": "東京の広い範囲で非常に強い風と激しい雨が予想されています。",
                "furigana": "とうきょうのひろいはんいでひじょうにつよいかぜとはげしいあめがよそうされています。",
                "english": "Extremely strong winds and heavy rainfall are anticipated across widespread parts of Tokyo."
            },
            {
                "id": "r2_4",
                "japanese": "土砂災害や低い土地の浸水に警戒し、最新の交通情報を確認してください。",
                "furigana": "どしゃさいがいやひくいとちのしんすいにけいかいし、さいしんのこうつうじょうほうをごかくにんください。",
                "english": "Please stay alert for landslides and flooded lowlands, and check the latest transit updates."
            }
        ]
    },
    {
        "id": "c3",
        "title": "Tokyo Living & Economy",
        "titleJa": "暮らしと経済インサイト",
        "description": "In-depth look at Tokyo convenience stores and food waste reduction.",
        "sentences": [
            {
                "id": "r3_1",
                "japanese": "暮らしのニュースです。東京都内のコンビニ各社で、食品ロス削減の取り組みが広がっています。",
                "furigana": "くらしのにゅーすです。とうきょうとないのこんびにかくしゃで、しょくひんろすさくげんのとりくみがひろがっています。",
                "english": "In lifestyle news: Convenience store chains across Tokyo are expanding food loss reduction initiatives."
            },
            {
                "id": "r3_2",
                "japanese": "消費期限が近づいたおにぎりやサンドイッチに「エコ値引きシール」が貼られ、安く購入できます。",
                "furigana": "しょうひきげんがちかづいたおにぎりやさんどいっちに「えこねびきしーる」がはられ、やすくこうにゅうできます。",
                "english": "Eco-discount stickers are applied to onigiri and sandwiches near expiration, allowing bargain purchases."
            },
            {
                "id": "r3_3",
                "japanese": "お店は廃棄するゴミを減らすことができ、利用者からも節約になると好評です。",
                "furigana": "おみせははいきするごみをへらすことができ、りようしゃからもせつやくになるとこうひょうです。",
                "english": "Stores can reduce discarded waste, and shoppers praise it as an effective way to save money."
            }
        ]
    },
    {
        "id": "c4",
        "title": "Culture & Manga Feature",
        "titleJa": "日本の文化・秋葉原マンガ特集",
        "description": "Special report on Akihabara manga festival and overseas fans.",
        "sentences": [
            {
                "id": "r4_1",
                "japanese": "文化の話題です。東京・秋葉原で、国内外の人気マンガが集まる秋のイベントが始まりました。",
                "furigana": "ぶんかのわだいです。とうきょう・あきはばらで、こくないがいのにんきまんががあつまるあきのいべんとがはじまりました。",
                "english": "In culture news: An autumn festival featuring popular domestic and international manga has begun in Akihabara."
            },
            {
                "id": "r4_2",
                "japanese": "会場には限定グッズや原画の展示コーナーが並び、多くのファンで賑わっています。",
                "furigana": "かいじょうにはげんていぐっずやげんがのてんじこーなーがならび、おおくのふぁんでにぎわっています。",
                "english": "Limited edition goods and original artwork exhibition booths are lined up, bustling with enthusiastic fans."
            },
            {
                "id": "r4_3",
                "japanese": "訪れた外国人観光客は、「生で日本のマンガ文化に触れられて感動した」と笑顔で話していました。",
                "furigana": "おとずれたがいこくじんかんこうきゃくは、「なまでにほんのまんがぶんかにふれられてかんどうした」とえがおではなしていました。",
                "english": "Visiting international tourists smiled and said they were deeply moved to experience Japanese manga culture live."
            }
        ]
    },
    {
        "id": "c5",
        "title": "Tomorrow's Outlook & Ending",
        "titleJa": "明日の展望・エンディング",
        "description": "Final review, sports wrap-up, and relaxing night sign-off.",
        "sentences": [
            {
                "id": "r5_1",
                "japanese": "以上、今夜のNHKジャーナル総合ニュースをお送りいたしました。",
                "furigana": "いじょう、こんやのえぬえいちけーじゃーなるそうごうにゅーすをおおくりいたしました。",
                "english": "This concludes tonight's edition of the NHK Journal comprehensive evening news."
            },
            {
                "id": "r5_2",
                "japanese": "明日は各地で雨が強まる見込みですので、お出かけの際は足元に十分ご注意ください。",
                "furigana": "あすはかくちであめがつよまるみこみですので、おでかけのさいはあしもとにじゅうぶんごちゅういください。",
                "english": "Rain is expected to strengthen across various regions tomorrow; please take care of your footing when going out."
            },
            {
                "id": "r5_3",
                "japanese": "それでは皆様、どうぞ良い夜をお過ごしください。おやすみなさい。",
                "furigana": "それではみなさま、どうぞよいよるをおすごしください。おやすみなさい。",
                "english": "We wish you all a pleasant and restful evening. Good night."
            }
        ]
    }
]

async def build_calibrated_radio():
    print("🎙️ Synthesizing NHK 1-Hour Radio Broadcast with sweet female & warm male voices, relaxed slow speed (-12%), and sample-exact alignment...")

    master_frames = bytearray()
    total_samples = 0
    pause_sent_sec = 0.65
    pause_chap_sec = 1.30
    silence_sent_bytes = create_silence_bytes(pause_sent_sec)
    silence_sent_samples = len(silence_sent_bytes) // 4
    silence_chap_bytes = create_silence_bytes(pause_chap_sec)
    silence_chap_samples = len(silence_chap_bytes) // 4

    processed_chapters = []

    for c_idx, chap in enumerate(broadcast_chapters):
        chap_start_sec = round(total_samples / float(SAMPLE_RATE), 3)
        processed_sentences = []

        is_male = (c_idx % 2 == 1)
        voice = VOICE_MALE if is_male else VOICE_FEMALE

        print(f"\n--- Chapter {chap['id']}: {chap['titleJa']} (Starts {chap_start_sec:.2f}s, Voice: {voice}) ---")

        for s_idx, sent in enumerate(chap["sentences"]):
            temp_wav = f"/tmp/calibrated_radio_{chap['id']}_{sent['id']}.wav"
            await synth_to_wav(sent["japanese"], voice, temp_wav, is_male=is_male, slow=True)

            with wave.open(temp_wav, 'rb') as w:
                n_frames = w.getnframes()
                raw_bytes = w.readframes(n_frames)

            start_t = round(total_samples / float(SAMPLE_RATE), 3)
            total_samples += n_frames
            end_t = round(total_samples / float(SAMPLE_RATE), 3)

            master_frames.extend(raw_bytes)

            sent_copy = dict(sent)
            sent_copy["startTimeSec"] = start_t
            sent_copy["endTimeSec"] = end_t
            processed_sentences.append(sent_copy)

            print(f"  Sentence {sent['id']} [{start_t:.2f}s - {end_t:.2f}s] (dur: {(end_t - start_t):.2f}s): {sent['japanese']}")

            if s_idx < len(chap["sentences"]) - 1:
                master_frames.extend(silence_sent_bytes)
                total_samples += silence_sent_samples

            if os.path.exists(temp_wav):
                os.remove(temp_wav)

        if c_idx < len(broadcast_chapters) - 1:
            master_frames.extend(silence_chap_bytes)
            total_samples += silence_chap_samples

        chap_dict = {
            "id": chap["id"],
            "title": chap["title"],
            "titleJa": chap["titleJa"],
            "startTimeSec": chap_start_sec,
            "description": chap["description"],
            "transcriptSentences": processed_sentences
        }
        processed_chapters.append(chap_dict)

    master_wav = "/tmp/calibrated_radio_master.wav"
    with wave.open(master_wav, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(master_frames)

    subprocess.run([
        "/opt/homebrew/bin/ffmpeg", "-y", "-i", master_wav,
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
        RADIO_FILE
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    total_dur_sec = round(len(master_frames) / (4.0 * SAMPLE_RATE), 2)
    print(f"\n🎉 Saved Master Radio Broadcast to {RADIO_FILE} (Exact Length: {total_dur_sec:.2f}s)")

    if os.path.exists(master_wav):
        os.remove(master_wav)

    # Update TokyoRadioStation.swift
    swift_chapters_code = []
    for chap in processed_chapters:
        sents_code = []
        for s in chap["transcriptSentences"]:
            sents_code.append(
                f'                        NewsSentence(id: "{s["id"]}", japanese: "{s["japanese"]}", furigana: "{s["furigana"]}", english: "{s["english"]}", startTimeSec: {s["startTimeSec"]}, endTimeSec: {s["endTimeSec"]})'
            )
        sents_str = ",\n".join(sents_code)

        chap_code = f"""                RadioChapter(
                    id: "{chap['id']}",
                    title: "{chap['title']}",
                    titleJa: "{chap['titleJa']}",
                    startTimeSec: {chap['startTimeSec']},
                    description: "{chap['description']}",
                    transcriptSentences: [
{sents_str}
                    ]
                )"""
        swift_chapters_code.append(chap_code)

    all_chapters_swift = ",\n".join(swift_chapters_code)

    station_swift_path = "TokyoFlow/Models/TokyoRadioStation.swift"
    station_content = open(station_swift_path, "r", encoding="utf-8").read()

    new_station_block = f"""        TokyoRadioStation(
            id: "nhk_journal_55",
            title: "NHK Journal Deep Immersion",
            titleJa: "NHKジャーナル 総合ニュース特報",
            subtitle: "Authentic NHK radio broadcast with verbatim transcript, Tokyo weather, economics, culture, and precise word-by-word shadowing.",
            durationSec: {total_dur_sec:.1f},
            durationLabel: "{int(total_dur_sec)//60} Mins ({int(total_dur_sec)//60}:{int(total_dur_sec)%60:02d})",
            audioFileName: "nhk_journal_55min.m4a",
            streamUrl: nil,
            badge: "NHK VERBATIM",
            icon: "antenna.radiowaves.left.and.right",
            chapters: [
{all_chapters_swift}
            ]
        ),"""

    pattern = r'TokyoRadioStation\(\s*id:\s*"nhk_journal_55".*?chapters:\s*\[.*?\]\s*\),'
    station_content = re.sub(pattern, new_station_block, station_content, flags=re.DOTALL)

    with open(station_swift_path, "w", encoding="utf-8") as f:
        f.write(station_content)

    print("✅ TokyoRadioStation.swift updated with relaxed pace timestamps!")

async def build_calibrated_daily_news():
    print("\n📰 Building Daily News Articles with sweet female voice & slow relaxed pacing (-12%)...")
    news_json_path = "TokyoFlow/Resources/daily_news.json"
    with open(news_json_path, "r", encoding="utf-8") as f:
        news_items = json.load(f)

    pause_sent_sec = 0.60
    silence_bytes = create_silence_bytes(pause_sent_sec)
    silence_samples = len(silence_bytes) // 4

    for item in news_items:
        audio_filename = item.get("audioFileName", f"{item['id']}.m4a")
        out_m4a = os.path.join(AUDIO_DIR, audio_filename)
        master_frames = bytearray()
        total_samples = 0
        updated_sentences = []

        for s_idx, s in enumerate(item["contentSentences"]):
            temp_wav = f"/tmp/calibrated_news_{item['id']}_{s['id']}.wav"
            await synth_to_wav(s["japanese"], VOICE_FEMALE, temp_wav, is_male=False, slow=True)

            with wave.open(temp_wav, 'rb') as w:
                n_frames = w.getnframes()
                raw_bytes = w.readframes(n_frames)

            start_t = round(total_samples / float(SAMPLE_RATE), 3)
            total_samples += n_frames
            end_t = round(total_samples / float(SAMPLE_RATE), 3)

            master_frames.extend(raw_bytes)

            s["startTimeSec"] = start_t
            s["endTimeSec"] = end_t
            updated_sentences.append(s)

            if s_idx < len(item["contentSentences"]) - 1:
                master_frames.extend(silence_bytes)
                total_samples += silence_samples

            if os.path.exists(temp_wav):
                os.remove(temp_wav)

        item["contentSentences"] = updated_sentences

        temp_master_wav = f"/tmp/master_{item['id']}.wav"
        with wave.open(temp_master_wav, 'wb') as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(SAMPLE_RATE)
            w.writeframes(master_frames)

        subprocess.run([
            "/opt/homebrew/bin/ffmpeg", "-y", "-i", temp_master_wav,
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
            out_m4a
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if os.path.exists(temp_master_wav):
            os.remove(temp_master_wav)

        print(f"  ✅ Saved {out_m4a} (Duration: {total_samples/SAMPLE_RATE:.2f}s)")

    with open(news_json_path, "w", encoding="utf-8") as f:
        json.dump(news_items, f, ensure_ascii=False, indent=2)

    print("✅ daily_news.json calibrated!")

async def build_full_voicebank_and_dictionary_audio():
    print("\n📚 Generating Studio VoiceBank audio for all new JLPT Words, Readings & Example Sentences...")
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # Add all JLPT words and example sentences into manifest
    new_entries_to_synth = {}
    for word in jlpt_core_database:
        # 1. Kanji
        if word["kanji"]:
            fn = f"jlpt_{word['id']}_kanji.m4a"
            manifest[word["kanji"]] = fn
            manifest[word["kanji"].lower()] = fn
            new_entries_to_synth[fn] = word["kanji"]

        # 2. Reading
        if word["reading"]:
            fn_r = f"jlpt_{word['id']}_reading.m4a"
            manifest[word["reading"]] = fn_r
            new_entries_to_synth[fn_r] = word["reading"]

        # 3. Romaji
        if word["romaji"]:
            manifest[word["romaji"].lower()] = manifest.get(word["kanji"], f"jlpt_{word['id']}_kanji.m4a")

        # 4. Example Sentence
        if word["exampleJa"]:
            fn_ex = f"jlpt_{word['id']}_ex.m4a"
            manifest[word["exampleJa"]] = fn_ex
            new_entries_to_synth[fn_ex] = word["exampleJa"]

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"Manifest now contains {len(manifest)} keys. Synthesizing {len(new_entries_to_synth)} new audio files...")

    sem = asyncio.Semaphore(15)
    done = 0
    total = len(new_entries_to_synth)

    async def synth_word(filename, text):
        nonlocal done
        target_path = os.path.join(VOICEBANK_DIR, filename)
        temp_wav = f"/tmp/jlpt_vb_{filename}.wav"
        async with sem:
            try:
                await synth_to_wav(text, VOICE_FEMALE, temp_wav, is_male=False, slow=True)
                subprocess.run([
                    "/opt/homebrew/bin/ffmpeg", "-y", "-i", temp_wav,
                    "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
                    target_path
                ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if os.path.exists(temp_wav):
                    os.remove(temp_wav)
                done += 1
            except Exception as e:
                print(f"Error {filename} ({text}): {e}")

    tasks = [synth_word(fn, txt) for fn, txt in new_entries_to_synth.items()]
    await asyncio.gather(*tasks)
    print(f"🎉 Successfully synthesized all {done}/{total} dictionary audio files!")

async def main():
    t0 = time.time()
    await build_calibrated_radio()
    await build_calibrated_daily_news()
    await build_full_voicebank_and_dictionary_audio()
    t1 = time.time()
    print(f"\n✨ ALL AUDIO GENERATION, TUNING & JLPT EXPANSION FINISHED IN {t1-t0:.2f}s!")

if __name__ == "__main__":
    asyncio.run(main())
