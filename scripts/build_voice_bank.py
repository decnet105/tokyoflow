import os
import json
import subprocess
import re

OUTPUT_DIR = "TokyoFlow/Resources/Audio/VoiceBank"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# List of all target pronunciations
KANA_LIST = [
    # Seion (Hiragana & Katakana)
    ("a", "あ", "ア"), ("i", "い", "イ"), ("u", "う", "ウ"), ("e", "え", "エ"), ("o", "お", "オ"),
    ("ka", "か", "カ"), ("ki", "き", "キ"), ("ku", "く", "ク"), ("ke", "け", "ケ"), ("ko", "こ", "コ"),
    ("sa", "さ", "サ"), ("shi", "し", "シ"), ("su", "す", "ス"), ("se", "せ", "セ"), ("so", "そ", "ソ"),
    ("ta", "た", "タ"), ("chi", "ち", "チ"), ("tsu", "つ", "ツ"), ("te", "て", "テ"), ("to", "と", "ト"),
    ("na", "な", "ナ"), ("ni", "に", "ニ"), ("nu", "ぬ", "ヌ"), ("ne", "ね", "ネ"), ("no", "の", "ノ"),
    ("ha", "は", "ハ"), ("hi", "ひ", "ヒ"), ("fu", "ふ", "フ"), ("he", "へ", "ヘ"), ("ho", "ほ", "ホ"),
    ("ma", "ま", "マ"), ("mi", "み", "ミ"), ("mu", "む", "ム"), ("me", "め", "メ"), ("mo", "も", "モ"),
    ("ya", "や", "ヤ"), ("yu", "ゆ", "ユ"), ("yo", "よ", "ヨ"),
    ("ra", "ら", "ラ"), ("ri", "り", "リ"), ("ru", "る", "ル"), ("re", "れ", "レ"), ("ro", "ろ", "ロ"),
    ("wa", "わ", "ワ"), ("wo", "を", "ヲ"), ("n", "ん", "ン"),
    # Dakuon / Handakuon
    ("ga", "が", "ガ"), ("gi", "ぎ", "ギ"), ("gu", "ぐ", "グ"), ("ge", "げ", "ゲ"), ("go", "ご", "ゴ"),
    ("za", "ざ", "ザ"), ("ji", "じ", "ジ"), ("zu", "ず", "ズ"), ("ze", "ぜ", "ゼ"), ("zo", "ぞ", "ゾ"),
    ("da", "だ", "ダ"), ("di", "ぢ", "ヂ"), ("du", "づ", "ヅ"), ("de", "で", "デ"), ("do", "ど", "ド"),
    ("ba", "ば", "バ"), ("bi", "び", "ビ"), ("bu", "ぶ", "ブ"), ("be", "べ", "ベ"), ("bo", "ぼ", "ボ"),
    ("pa", "ぱ", "パ"), ("pi", "ぴ", "ピ"), ("pu", "ぷ", "プ"), ("pe", "ぺ", "ペ"), ("po", "ぽ", "ポ"),
    # Yoon
    ("kya", "きゃ", "キャ"), ("kyu", "きゅ", "キュ"), ("kyo", "きょ", "キョ"),
    ("sha", "しゃ", "シャ"), ("shu", "しゅ", "シュ"), ("sho", "しょ", "ショ"),
    ("cha", "ちゃ", "チャ"), ("chu", "ちゅ", "チュ"), ("cho", "ちょ", "チョ"),
    ("nya", "にゃ", "ニャ"), ("nyu", "にゅ", "ニュ"), ("nyo", "にょ", "ニョ"),
    ("hya", "ひゃ", "ヒャ"), ("hyu", "ひゅ", "ヒュ"), ("hyo", "ひょ", "ヒョ"),
    ("mya", "みゃ", "ミャ"), ("myu", "みゅ", "ミュ"), ("myo", "みょ", "ミョ"),
    ("rya", "りゃ", "リャ"), ("ryu", "りゅ", "リュ"), ("ryo", "りょ", "リョ"),
    ("gya", "ぎゃ", "ギャ"), ("gyu", "ぎゅ", "ギュ"), ("gyo", "ぎょ", "ギョ"),
    ("ja", "じゃ", "ジャ"), ("ju", "じゅ", "ジュ"), ("jo", "じょ", "ジョ"),
    ("bya", "びゃ", "ビャ"), ("byu", "びゅ", "ビュ"), ("byo", "びょ", "ビョ"),
    ("pya", "ぴゃ", "ピャ"), ("pyu", "ぴゅ", "ピュ"), ("pyo", "ぴょ", "ピョ")
]

KANA_WORDS = [
    # Seion words
    ("arigatou", "ありがとう"), ("inu", "いぬ"), ("inu_kanji", "犬"), ("udon", "うどん"), 
    ("eki", "えき"), ("eki_kanji", "駅"), ("onigiri", "おにぎり"),
    ("kawaii", "かわいい"), ("kippu", "きっぷ"), ("kippu_kanji", "切符"), 
    ("kuruma", "くるま"), ("kuruma_kanji", "車"), ("keitai", "けいたい"), ("keitai_kanji", "携帯"),
    ("konbini", "コンビニ"),
    ("sakura", "さくら"), ("sakura_kanji", "桜"), ("shinjuku", "しんじゅく"), ("shinjuku_kanji", "新宿"),
    ("suika", "すいか"), ("suika_eng", "Suica"), ("sensei", "せんせい"), ("sensei_kanji", "先生"),
    ("soba", "そば"),
    ("takoyaki", "たこやき"), ("chikatetsu", "ちかてつ"), ("chikatetsu_kanji", "地下鉄"),
    ("tsuki", "つき"), ("tsuki_kanji", "月"), ("tenpura", "てんぷら"),
    ("toukyou", "とうきょう"), ("toukyou_kanji", "東京"),
    ("natsu", "なつ"), ("natsu_kanji", "夏"), ("nihon", "にほん"), ("nihon_kanji", "日本"),
    ("nuigurumi", "ぬいぐるみ"), ("neko", "ねこ"), ("neko_kanji", "猫"),
    ("nomimono", "のみもの"), ("nomimono_kanji", "飲み物"),
    ("hanabi", "はなび"), ("hanabi_kanji", "花火"), ("hikari", "ひかり"), ("hikari_kanji", "光"),
    ("fujisan", "ふじさん"), ("fujisan_kanji", "富士山"), ("heya", "へや"), ("heya_kanji", "部屋"),
    ("hon", "ほん"), ("hon_kanji", "本"),
    ("manga", "まんが"), ("manga_kanji", "漫画"), ("mizu", "みず"), ("mizu_kanji", "水"),
    ("muryou", "むりょう"), ("muryou_kanji", "無料"), ("megane", "めがね"), ("megane_kanji", "眼鏡"),
    ("mouichido", "もういちど"),
    ("yama", "やま"), ("yama_kanji", "山"), ("yume", "ゆめ"), ("yume_kanji", "夢"),
    ("yoru", "よる"), ("yoru_kanji", "夜"),
    ("raamen", "ラーメン"), ("ringo", "りんご"), ("ringo_kanji", "林檎"),
    ("rusuban", "るすばん"), ("rusuban_kanji", "留守番"),
    ("ressha", "れっしゃ"), ("ressha_kanji", "列車"), ("rousoku", "ろうそく"),
    ("wasabi", "わさび"), ("okudasai", "をください"),
    # Dakuon & Handakuon words
    ("gakkou", "がっこう"), ("gakkou_kanji", "学校"),
    ("gyuudon", "ぎゅうどん"), ("gyuudon_kanji", "牛丼"),
    ("gunma", "ぐんま"), ("gunma_kanji", "群馬"),
    ("genki", "げんき"), ("genki_kanji", "元気"),
    ("gohan", "ごはん"), ("gohan_kanji", "ご飯"),
    ("zasshi", "ざっし"), ("zasshi_kanji", "雑誌"),
    ("jikan", "じかん"), ("jikan_kanji", "時間"),
    ("zutto", "ずっと"),
    ("zenbu", "ぜんぶ"), ("zenbu_kanji", "全部"),
    ("zou", "ぞう"), ("zou_kanji", "象"),
    ("daijoubu", "だいじょうぶ"), ("daijoubu_kanji", "大丈夫"),
    ("densha", "でんしゃ"), ("densha_kanji", "電車"),
    ("doko", "どこ"),
    ("basho", "ばしょ"), ("basho_kanji", "場所"),
    ("biiru", "ビール"),
    ("bunka", "ぶんか"), ("bunka_kanji", "文化"),
    ("benri", "べんり"), ("benri_kanji", "便利"),
    ("boku", "ぼく"), ("boku_kanji", "僕"),
    ("pan", "パン"),
    ("pinku", "ピンク"),
    ("purin", "プリン"),
    ("pen", "ペン"),
    ("posuto", "ポスト"),
    # Yoon words
    ("kyaku", "きゃく"), ("kyaku_kanji", "客"),
    ("kyuukou", "きゅうこう"), ("kyuukou_kanji", "急行"),
    ("kyou", "きょう"), ("kyou_kanji", "今日"),
    ("shashin", "しゃしん"), ("shashin_kanji", "写真"),
    ("shuuden", "しゅうでん"), ("shuuden_kanji", "終電"),
    ("shouhin", "しょうひん"), ("shouhin_kanji", "商品"),
    ("ocha", "おちゃ"), ("ocha_kanji", "お茶"),
    ("chuumon", "ちゅうもん"), ("chuumon_kanji", "注文"),
    ("chotto", "ちょっと"),
    ("nyanko", "にゃんこ"),
    ("ryoushuusho", "りょうしゅうしょ"), ("ryoushuusho_kanji", "領収書")
]

PHRASES_AND_VOCAB = [
    # Survival Expressions
    ("phrase_atatamete", "温めてください"),
    ("phrase_atatame_masuka", "温めますか？"),
    ("phrase_fukuro_daijoubu", "袋は大丈夫です"),
    ("phrase_daijoubu", "大丈夫です"),
    ("phrase_issho_de_ii", "一緒でいいです"),
    ("phrase_toriaezu_nama", "とりあえず生で！"),
    ("phrase_okaikei", "お会計お願いします"),
    ("phrase_okanjou", "お勘定お願いします"),
    ("phrase_arerugii", "アレルギーがあります"),
    ("phrase_shichaku", "試着してもいいですか？"),
    ("phrase_menzei", "免税できますか？"),
    ("phrase_fuzaihyou", "不在票が入っていました"),
    ("phrase_kyuukyuusha", "救急車をお願いします"),
    ("phrase_nanbansen", "〜は何番線ですか？"),
    ("phrase_nanbansen_short", "何番線ですか？"),
    ("phrase_tacchi_dekimasen", "タッチできませんでした"),
    ("phrase_irasshaimase", "いらっしゃいませ！"),
    ("phrase_arigatou_gozaimasu", "ありがとうございます"),
    ("phrase_arigatou_gozaimashita", "ありがとうございました"),
    ("phrase_sumimasen", "すみません"),
    ("phrase_gochisousama", "ごちそうさまでした"),
    ("phrase_itadakimasu", "いただきます"),
    ("phrase_kore_kudasai", "これください"),
    ("phrase_ikura_desuka", "いくらですか"),
    ("phrase_ryoushuusho", "領収書をお願いします"),
    ("phrase_chaaji", "チャージをお願いします"),
    ("phrase_oomori", "大盛りでお願いします"),
    ("phrase_osusume", "おすすめは何ですか"),
    ("phrase_suica_de", "Suicaでお願いします"),
    ("phrase_kaado_de", "カードで払えますか"),
    ("phrase_toire", "トイレはどこですか"),
    ("phrase_eigo_menyuu", "英語のメニューはありますか"),
    ("phrase_shashin", "写真を撮ってもらえますか"),
    ("phrase_shuuden", "終電は何時ですか"),
    ("phrase_norikae", "乗り換えはどこですか"),
    ("phrase_yamanote", "山手線はどちらですか"),
    
    # Key Tokyo Vocabulary
    ("vocab_suica", "Suica"),
    ("vocab_pasmo", "Pasmo"),
    ("vocab_kippu", "切符"),
    ("vocab_seisan", "精算"),
    ("vocab_kaisatsuguchi", "改札口"),
    ("vocab_norikae_single", "乗り換え"),
    ("vocab_shuuden_single", "終電"),
    ("vocab_obentou", "お弁当"),
    ("vocab_onigiri", "おにぎり"),
    ("vocab_hashi", "箸"),
    ("vocab_supuun", "スプーン"),
    ("vocab_fooku", "フォーク"),
    ("vocab_rejibukuro", "レジ袋"),
    ("vocab_atatame", "温め"),
    ("vocab_ramen", "ラーメン"),
    ("vocab_men_katasa", "麺のかたさ"),
    ("vocab_kaedama", "替玉"),
    ("vocab_suupu", "スープ"),
    ("vocab_izakaya", "居酒屋"),
    ("vocab_namabiiru", "生ビール"),
    ("vocab_haibooru", "ハイボール"),
    ("vocab_uuroncha", "烏龍茶"),
    ("vocab_edamame", "枝豆"),
    ("vocab_yakitori", "焼き鳥"),
    ("vocab_kanpai", "乾杯"),
    ("vocab_kissaten", "喫茶店"),
    ("vocab_burendo", "ブレンドコーヒー"),
    ("vocab_aisukoohii", "アイスコーヒー"),
    ("vocab_chuumon", "注文"),
    ("vocab_ohiya", "お冷"),
    ("vocab_oshibori", "おしぼり"),
    ("vocab_ryoushuusho_single", "領収書"),
    ("vocab_reshiito", "レシート"),
    ("vocab_shinjuku", "新宿"),
    ("vocab_shibuya", "渋谷"),
    ("vocab_akihabara", "秋葉原"),
    ("vocab_asakusa", "浅草"),
    ("vocab_ginza", "銀座"),
    ("vocab_roppongi", "六本木"),
    ("vocab_ueno", "上野"),
    ("vocab_tokyo_station", "東京駅"),
    ("vocab_ikebukuro", "池袋"),
    ("vocab_harajuku", "原宿"),

    # Manga SFX
    ("sfx_dokidoki", "ドキドキ"),
    ("sfx_zawazawa", "ざわ… ざわ…"),
    ("sfx_don", "ドンッ！"),
    ("sfx_sakusaku", "サクサク"),
    ("sfx_juwa", "ジュワッ"),
    ("sfx_giragira", "ギラギラ"),
    ("sfx_nikoniko", "ニコニコ"),
    ("sfx_iraira", "イライラ"),
    ("sfx_zaazaa", "ザーザー"),
    ("sfx_kosokoso", "コソコソ"),

    # Tokyo Persona Greetings
    ("persona_sakura", "ヤッホー！今日渋谷で何か面白いことあった？"),
    ("persona_kenji", "いらっしゃい！何杯飲む？今日のおすすめはマグロだよ！"),
    ("persona_tanaka", "ご案内いたします。どちらの方面へお出かけですか？"),
    ("persona_ren", "今期の新作アニメもう観た？原作マンガもめっちゃ熱いよ！")
]

manifest = {}

def sanitize_key(text):
    return re.sub(r'[\s\n\r\t・、。！？!?「」()（）…#]+', '', text).strip()

def generate_voice_file(file_id, text, voice="Kyoko"):
    out_m4a = os.path.join(OUTPUT_DIR, f"{file_id}.m4a")
    if os.path.exists(out_m4a) and os.path.getsize(out_m4a) > 0:
        return f"{file_id}.m4a"
    tmp_aiff = f"/tmp/{file_id}.aiff"
    
    # Generate high fidelity master AIFF
    subprocess.run(["say", "-v", voice, "-r", "165", "-o", tmp_aiff, text], check=True)
    
    # Convert and filter to broadcast quality AAC m4a
    subprocess.run([
        "ffmpeg", "-y", "-i", tmp_aiff,
        "-af", "highpass=f=80,lowpass=f=12000,dynaudnorm=f=50:m=3.0",
        "-c:a", "aac", "-b:a", "128k",
        out_m4a
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    if os.path.exists(tmp_aiff):
        os.remove(tmp_aiff)
    
    return f"{file_id}.m4a"

print("Starting Native Voice Bank Generation...")

# 1. Process Kana
for romaji, hira, kata in KANA_LIST:
    file_id = f"kana_{romaji}"
    fn = generate_voice_file(file_id, hira, voice="Kyoko")
    manifest[hira] = fn
    manifest[kata] = fn
    manifest[romaji] = fn
    manifest[sanitize_key(hira)] = fn
    manifest[sanitize_key(kata)] = fn

# 2. Process Kana Example Words
for file_id, word in KANA_WORDS:
    fn = generate_voice_file(f"word_{file_id}", word, voice="Kyoko")
    manifest[word] = fn
    manifest[sanitize_key(word)] = fn

# 3. Process Phrases, Scenarios, Vocabulary & SFX
for file_id, text in PHRASES_AND_VOCAB:
    voice = "Kyoko"
    if "kenji" in file_id or "tanaka" in file_id or "ren" in file_id:
        voice = "Kyoko" # or native male/female
    fn = generate_voice_file(file_id, text, voice=voice)
    manifest[text] = fn
    manifest[sanitize_key(text)] = fn

# Save manifest
manifest_path = os.path.join(OUTPUT_DIR, "voice_bank_manifest.json")
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"Generated {len(set(manifest.values()))} native audio assets and {len(manifest)} mapped dictionary keys.")
print(f"Manifest written to {manifest_path}")
