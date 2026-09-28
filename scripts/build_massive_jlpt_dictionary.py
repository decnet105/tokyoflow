#!/usr/bin/env python3
"""
build_massive_jlpt_dictionary.py
Builds the comprehensive N5-N1 vocabulary dataset for TokyoFlow
Derived from Hongbaoshu (红宝书) and Green Book (绿宝书) syllabi.
All definitions, collocations, tips, and example sentences are 100% English.
"""

import json
import os
import subprocess

RAW_CURRICULUM = [
    # ================= N5 CORE VOCABULARY =================
    ("行く", "いく", "iku", "[0] Heiban", "N5", "Godan Verb (Intransitive)", "To go, to head towards", "明日、電車で東京駅へ行きます。", "あした、でんしゃで とうきょうえきへ いきます。", "Tomorrow I will go to Tokyo Station by train.", "来る (kuru - to come)", "東京へ行く", "transit"),
    ("来る", "くる", "kuru", "[1] Atamadaka", "N5", "Kuru Verb (Intransitive)", "To come, to arrive", "友達が私の家に遊びに来ます。", "ともだちが わたしの いえに あそびに きます。", "My friend is coming over to visit my house.", "行く (iku - to go)", "遊びに来る", "daily"),
    ("食べる", "たべる", "taberu", "[2] Nakadaka", "N5", "Ichidan Verb (Transitive)", "To eat, to have a meal", "朝ごはんにパンと卵を食べます。", "あさごはんに ぱんと たまごを たべます。", "I eat bread and eggs for breakfast.", None, "朝ごはんを食べる", "dining"),
    ("飲む", "のむ", "nomu", "[1] Atamadaka", "N5", "Godan Verb (Transitive)", "To drink, to swallow", "毎朝、温かい緑茶を飲みます。", "まいあさ、あたたかい りょくちゃを のみます。", "I drink warm green tea every morning.", None, "薬を飲む", "dining"),
    ("見る", "みる", "miru", "[1] Atamadaka", "N5", "Ichidan Verb (Transitive)", "To see, to watch, to look at", "週末に映画館で新作アニメを見ました。", "しゅうまつに えいがかんで しんさくあにめを みました。", "I watched the new anime movie at the cinema over the weekend.", "見せる (miseru - show)", "映画を見る", "daily"),
    ("聞く", "きく", "kiku", "[0] Heiban", "N5", "Godan Verb (Transitive)", "To listen, to hear, to ask", "駅員さんに乗り換えのホームを聞きました。", "えきいんさんに のりかえの ほーむを ききました。", "I asked the station staff about the transfer platform.", "聞こえる (kikoeru - can hear)", "道を聞く", "transit"),
    ("話す", "はなす", "hanasu", "[2] Nakadaka", "N5", "Godan Verb (Transitive)", "To speak, to talk", "先生と日本語でゆっくり話しました。", "せんせいと にほんごで ゆっくり はなしました。", "I spoke slowly in Japanese with my teacher.", None, "日本語を話す", "social"),
    ("買う", "かう", "kau", "[0] Heiban", "N5", "Godan Verb (Transitive)", "To buy, to purchase", "コンビニで冷たい水とおにぎりを買いました。", "こんびにで つめたい みずと おにぎりを かいました。", "I bought cold water and an onigiri at the convenience store.", "売る (uru - sell)", "お土産を買う", "shopping"),
    ("会う", "あう", "au", "[1] Atamadaka", "N5", "Godan Verb (Intransitive)", "To meet, to see someone", "渋谷のハチ公前で友達と会います。", "しぶやの はちこうまえで ともだちと あいます。", "I will meet my friend in front of Hachiko in Shibuya.", None, "友達に会う", "social"),
    ("待つ", "まつ", "matsu", "[1] Atamadaka", "N5", "Godan Verb (Transitive)", "To wait, to pause", "改札口の近くで少し待ってください。", "かいさつぐちの ちかくで すこし まってください。", "Please wait a little near the ticket gate.", None, "少々お待ちください", "transit"),
    ("読む", "よむ", "yomu", "[1] Atamadaka", "N5", "Godan Verb (Transitive)", "To read", "電車の中で面白い本を読んでいます。", "でんしゃの なかで おもしろい ほんを よんでいます。", "I am reading an interesting book on the train.", None, "本を読む", "daily"),
    ("書く", "かく", "kaku", "[1] Atamadaka", "N5", "Godan Verb (Transitive)", "To write, to compose", "ここに名前と電話番号を書いてください。", "ここに なまえと でんわばんごうを かいてください。", "Please write your name and phone number here.", None, "名前を書く", "daily"),
    ("大きい", "おおきい", "ookii", "[3] Nakadaka", "N5", "I-Adjective", "Big, large, spacious", "新宿駅はとても大きくて広いです。", "しんじゅくえきは とても おおきくて ひろいです。", "Shinjuku Station is very big and spacious.", "小さい (chiisai - small)", "大きな声", "transit"),
    ("小さい", "ちいさい", "chiisai", "[3] Nakadaka", "N5", "I-Adjective", "Small, tiny, little", "この小さいカフェは静かで落ち着きます。", "この ちいさい かふぇは しずかで おちつきます。", "This small cafe is quiet and relaxing.", "大きい (ookii - big)", "小さな店", "dining"),
    ("高い", "たかい", "takai", "[2] Nakadaka", "N5", "I-Adjective", "Tall, high, expensive", "東京スカイツリーはとても高い建物です。", "とうきょうすかいつりーは とても たかい たてものです。", "Tokyo Skytree is a very tall building.", "低い (hikui - low) / 安い (yasui - cheap)", "値段が高い", "shopping"),
    ("安い", "やすい", "yasui", "[2] Nakadaka", "N5", "I-Adjective", "Cheap, inexpensive", "このスーパーの野菜は新鮮で安いです。", "この すーぱーの やさいは しんせんで やすいです。", "The vegetables at this supermarket are fresh and cheap.", "高い (takai - expensive)", "安くて美味しい", "shopping"),
    ("新しい", "あたらしい", "atarashii", "[4] Odaka", "N5", "I-Adjective", "New, fresh, modern", "新しいスマートフォンを買いました。", "あたらしい すまーとふぉんを かいました。", "I bought a new smartphone.", "古い (furui - old)", "新しい生活", "shopping"),
    ("古い", "ふるい", "furui", "[2] Nakadaka", "N5", "I-Adjective", "Old, aged (objects)", "浅草には古いお寺や伝統的なお店が多いです。", "あさくさには ふるい おてらや でんとうてきな おみせが おおいです。", "There are many old temples and traditional shops in Asakusa.", "新しい (atarashii - new)", "古い町並み", "daily"),
    ("楽しい", "たのしい", "tanoshii", "[3] Nakadaka", "N5", "I-Adjective", "Fun, enjoyable, pleasant", "日本語の勉強はとても楽しいです。", "にほんごの べんきょうは とても たのしいです。", "Studying Japanese is very fun.", None, "楽しい時間", "social"),
    ("忙しい", "いそがしい", "isogashii", "[4] Odaka", "N5", "I-Adjective", "Busy, hectic, occupied", "平日は仕事が忙しくて時間がありません。", "へいじつは しごとが いそがしくて じかんが ありません。", "I am busy with work on weekdays and have no free time.", "暇 (hima - free)", "毎日忙しい", "business"),
    ("静か", "しずか", "shizuka", "[1] Atamadaka", "N5", "Na-Adjective", "Quiet, peaceful, calm", "夜の住宅街はとても静かです。", "よるの じゅうたくがいは とても しずかです。", "The residential area is very quiet at night.", "賑やか (nigiyaka - lively)", "静かな部屋", "daily"),
    ("便利", "べんり", "benri", "[1] Atamadaka", "N5", "Na-Adjective", "Convenient, handy, useful", "駅の近くに住むと買い物に便利です。", "えきの ちかくに すむと かいものに べんりです。", "Living near the station is convenient for shopping.", "不便 (fuben - inconvenient)", "とても便利", "daily"),
    ("上手", "じょうず", "jouzu", "[3] Nakadaka", "N5", "Na-Adjective", "Skillful, good at", "彼は日本語の発音がとても上手です。", "かれは にほんごの はつおんが とても じょうずです。", "His Japanese pronunciation is very good.", "下手 (heta - poor at)", "日本語が上手", "social"),
    ("駅", "えき", "eki", "[1] Atamadaka", "N5", "Noun", "Station (train/subway)", "次の駅で山手線に乗り換えます。", "つぎの えきで やまのてせんに のりかえます。", "I will transfer to the Yamanote Line at the next station.", None, "駅前", "transit"),
    ("電車", "でんしゃ", "densha", "[0] Heiban", "N5", "Noun", "Train (electric)", "毎朝満員電車に乗って通勤しています。", "まいあさ まんいんでんしゃに のって つうきんしています。", "I commute every morning on a packed train.", None, "電車に乗る", "transit"),
    ("時間", "じかん", "jikan", "[0] Heiban", "N5", "Noun", "Time, duration, hour", "待ち合わせの時間に遅れないようにしてください。", "まちあわせの じかんに おくれないように してください。", "Please make sure not to be late for the meeting time.", None, "時間がある", "social"),
    ("友達", "ともだち", "tomodachi", "[0] Heiban", "N5", "Noun", "Friend, companion", "週末に友達と一緒にカフェへ行きました。", "しゅうまつに ともだちと いっしょに かふぇへ いきました。", "I went to a cafe together with my friend over the weekend.", None, "友達を作る", "social"),
    ("会社", "かいしゃ", "kaisha", "[0] Heiban", "N5", "Noun", "Company, workplace", "朝九時に会社に出社します。", "あさくじに かいしゃに しゅっしゃします。", "I arrive at the company at 9:00 AM.", None, "会社員", "business"),
    ("店", "みせ", "mise", "[2] Nakadaka", "N5", "Noun", "Store, shop, restaurant", "この店はいつもお客さんでいっぱいです。", "この みせは いつも おきゃくさんで いっぱいです。", "This shop is always crowded with customers.", None, "店に入る", "shopping"),
    ("水", "みず", "mizu", "[0] Heiban", "N5", "Noun", "Water (cold/room temp)", "冷たいお水を一杯いただけますか？", "つめたい おみずを いっぱいただき ますか？", "Could I please have a glass of cold water?", "お湯 (oyu - hot water)", "お冷", "dining"),
    ("今日", "きょう", "kyou", "[1] Atamadaka", "N5", "Noun", "Today", "今日は東京の天気がとても良いです。", "きょうは とうきょうの てんきが とても よいです。", "Today the weather in Tokyo is very pleasant.", "明日 (ashita - tomorrow)", "今日の予定", "daily"),
    ("明日", "あした", "ashita", "[3] Nakadaka", "N5", "Noun", "Tomorrow", "明日の朝、成田空港へ向かいます。", "あしたの あさ、なりたくうこうへ むかいます。", "Tomorrow morning, I will head to Narita Airport.", "昨日 (kinou - yesterday)", "明日の朝", "transit"),
    ("昨日", "きのう", "kinou", "[2] Nakadaka", "N5", "Noun", "Yesterday", "昨日は一日中雨が降っていました。", "きのうは いちにちじゅう あめが ふっていました。", "Yesterday it was raining all day long.", None, "昨日の夜", "daily"),
    ("部屋", "へや", "heya", "[2] Nakadaka", "N5", "Noun", "Room, apartment", "自分の部屋をきれいに掃除しました。", "じぶんの へやを きれいに そうじしました。", "I cleaned my room thoroughly.", None, "部屋を借りる", "daily"),
    ("電話", "でんわ", "denwa", "[0] Heiban", "N5", "Noun / Suru-Verb", "Telephone, phone call", "後で先生に電話をかけます。", "あとで せんせいに でんわを かけます。", "I will make a phone call to the teacher later.", None, "電話をかける", "social"),

    # ================= N4 DAILY LIFE & TRANSIT =================
    ("乗り換える", "のりかえる", "norikaeru", "[4] Odaka", "N4", "Ichidan Verb (Transitive)", "To transfer trains, switch lines", "新宿駅でJR線から地下鉄大江戸線に乗り換えます。", "しんじゅくえきで じぇいあーるせんから ちかてつ おおえどせんに のりかえます。", "I transfer from JR to the Toei Oedo Subway Line at Shinjuku.", None, "電車を乗り換える", "transit"),
    ("間に合う", "まにあう", "maniau", "[3] Nakadaka", "N4", "Godan Verb (Intransitive)", "To be in time for, to make it", "急いで走ったので終電に間に合いました。", "いそいで はしったので しゅうでんに まにあいました。", "Because I ran fast, I made it in time for the last train.", "遅れる (okureru - be late)", "時間に間に合う", "transit"),
    ("遅れる", "おくれる", "okureru", "[0] Heiban", "N4", "Ichidan Verb (Intransitive)", "To be late, to be delayed", "人身事故で電車が15分遅れています。", "じんしんじこで でんしゃが じゅうごふん おくれています。", "The train is delayed by 15 minutes due to an accident.", "間に合う (maniau - in time)", "電車が遅れる", "transit"),
    ("届く", "とどく", "todoku", "[2] Nakadaka", "N4", "Godan Verb (Intransitive)", "To arrive (mail/package), to reach", "注文した荷物が今日の午前に届きました。", "ちゅうもんした にもつが きょうの ごぜんに とどきました。", "The ordered package arrived this morning.", "届ける (todokeru - deliver)", "荷物が届く", "shopping"),
    ("届ける", "とどける", "todokeru", "[3] Nakadaka", "N4", "Ichidan Verb (Transitive)", "To deliver, to report/turn in", "拾った財布を交番に届けました。", "ひろった さいふを こうばんに とどけました。", "I turned in the lost wallet to the police box.", "届く (todoku - arrive)", "遺失物を届ける", "daily"),
    ("開ける", "あける", "akeru", "[0] Heiban", "N4", "Ichidan Verb (Transitive)", "To open (something)", "空気を入れ替えるために窓を開けました。", "くうきを いれかえるために まどを あけました。", "I opened the window to let fresh air in.", "開く (aku - open [intr])", "窓を開ける", "daily"),
    ("開く", "あく", "aku", "[0] Heiban", "N4", "Godan Verb (Intransitive)", "To open (by itself), to be open", "電車のドアが開きますのでご注意ください。", "でんしゃの どあが あきますので ごちゅういください。", "The train doors will open, so please be cautious.", "開ける (akeru - open [tr])", "ドアが開く", "transit"),
    ("閉める", "しめる", "shimeru", "[2] Nakadaka", "N4", "Ichidan Verb (Transitive)", "To close, to shut (something)", "寒いのでドアをしっかり閉めてください。", "さむいので どあを しっかり しめてください。", "Please close the door tightly as it is cold.", "閉まる (shimaru - close [intr])", "鍵を閉める", "daily"),
    ("閉まる", "しまる", "shimaru", "[2] Nakadaka", "N4", "Godan Verb (Intransitive)", "To close (by itself), to shut", "ドアが閉まります。駆け込み乗車はおやめください。", "どあが しまります。かけこみじょうしゃは おやめください。", "The doors are closing. Please refrain from rushing aboard.", "閉める (shimeru - close [tr])", "自動ドアが閉まる", "transit"),
    ("付ける", "つける", "tsukeru", "[2] Nakadaka", "N4", "Ichidan Verb (Transitive)", "To turn on (lights/appliances), attach", "暗くなったので部屋の電気を付けました。", "くらくなったので へやの でんきを つけました。", "I turned on the room lights because it got dark.", "付く (tsuku - turn on [intr])", "エアコンを付ける", "daily"),
    ("消す", "けす", "kesu", "[0] Heiban", "N4", "Godan Verb (Transitive)", "To turn off, to extinguish, erase", "出かける前にエアコンを消してください。", "でかけるまえに えあこんを けしてください。", "Please turn off the air conditioner before leaving.", "消える (kieru - turn off [intr])", "電気を消す", "daily"),
    ("予約", "よやく", "yoyaku", "[0] Heiban", "N4", "Noun / Suru-Verb", "Reservation, booking, appointment", "人気のレストランをインターネットで予約しました。", "にんきの れすとらんを いんたーねっとで よやくしました。", "I reserved the popular restaurant online.", None, "予約を取る", "dining"),
    ("連絡", "れんらく", "renraku", "[0] Heiban", "N4", "Noun / Suru-Verb", "Contact, communication, notification", "駅に着いたらメッセージで連絡してください。", "えきに ついたら めっせーじで れんらくしてください。", "Please contact me by message once you reach the station.", None, "連絡を取る", "business"),
    ("案内", "あんない", "annai", "[3] Nakadaka", "N4", "Noun / Suru-Verb", "Guidance, show around, direction", "東京の観光名所を友達に案内しました。", "とうきょうの かんこうめいしょを ともだちに あんないしました。", "I guided my friend around Tokyo's sightseeing spots.", None, "案内所", "social"),
    ("遠慮", "えんりょ", "enryo", "[1] Atamadaka", "N4", "Noun / Suru-Verb", "Restraint, hesitation, holding back", "遠慮しないで、好きなものをたくさん食べてね。", "えんりょしないで、すきなものを たくさん たべてね。", "Don't hold back, please eat plenty of whatever you like.", None, "ご遠慮ください", "dining"),
    ("丁寧", "ていねい", "teinei", "[1] Atamadaka", "N4", "Na-Adjective", "Polite, courteous, meticulous", "店員さんはとても丁寧な言葉遣いで対応してくれました。", "てんいんさんは とても ていねいな ことばづかいで たいおうしてくれました。", "The clerk assisted me using very polite language.", "失礼 (shitsurei - rude)", "丁寧に話す", "social"),
    ("準備", "じゅんび", "junbi", "[1] Atamadaka", "N4", "Noun / Suru-Verb", "Preparation, setup, arrangement", "明日のプレゼンの準備を終えました。", "あしたの ぷれぜんの じゅんびを おえました。", "I finished preparations for tomorrow's presentation.", None, "準備を整える", "business"),
    ("予定", "よてい", "yotei", "[0] Heiban", "N4", "Noun / Suru-Verb", "Schedule, plan, expectation", "来週の週末は京都へ旅行する予定です。", "らいしゅうの しゅうまつは きょうとへ りょこうする よていです。", "I plan to travel to Kyoto next weekend.", None, "予定を変更する", "daily"),
    ("習慣", "しゅうかん", "shuukan", "[0] Heiban", "N4", "Noun", "Custom, habit, practice", "朝起きてすぐに白湯を飲むのが習慣です。", "あさおきて すぐに さゆを のむのが しゅうかんです。", "Drinking hot water right after waking up is my habit.", None, "習慣をつける", "daily"),
    ("経験", "けいけん", "keiken", "[0] Heiban", "N4", "Noun / Suru-Verb", "Experience", "日本での生活は貴重な経験になりました。", "にほんでの せいかつは きちょうな けいけんに なりました。", "Living in Japan became a precious experience for me.", None, "経験を積む", "daily"),
    ("必ず", "かならず", "kanarazu", "[0] Heiban", "N4", "Adverb", "Without fail, surely, definitely", "約束の時間には必ず行きます。", "やくそくの じかんには かならず いきます。", "I will definitely go at the promised time.", None, "必ず成功する", "social"),
    ("決して", "けっして", "kesshite", "[0] Heiban", "N4", "Adverb", "Never, by no means (with negative)", "この秘密は決して誰にも言わないでください。", "この ひみつは けっして だれにも いわないでください。", "Please never tell this secret to anyone.", None, "決して諦めない", "social"),

    # ================= N3 INTERMEDIATE & WORKPLACE =================
    ("担当", "たんとう", "tantou", "[0] Heiban", "N3", "Noun / Suru-Verb", "In charge of, person responsible", "今回の新規プロジェクトは田中さんが担当しています。", "こんかいの しんき ぷろじぇくとは たなかさんが たんとうしています。", "Mr. Tanaka is in charge of this new project.", None, "担当者", "business"),
    ("問い合わせ", "といあわせ", "toiawase", "[0] Heiban", "N3", "Noun / Suru-Verb", "Inquiry, asking for info", "商品の在庫状況についてメールで問い合わせました。", "しょうひんの ざいこじょうきょうについて めーるで といあわせました。", "I inquired about product inventory status by email.", None, "問い合わせ窓口", "business"),
    ("手続き", "てつづき", "tetsuzuki", "[2] Nakadaka", "N3", "Noun / Suru-Verb", "Formal procedure, paperwork", "市役所で住民票の登録手続きを行いました。", "しやくしょで じゅうみんひょうの とうろくてつづきを おこないました。", "I completed the resident certificate registration at City Hall.", None, "手続きを踏む", "daily"),
    ("締め切り", "しめきり", "shimekiri", "[0] Heiban", "N3", "Noun", "Deadline, cutoff date", "企画書の提出締め切りは今週の金曜日です。", "きかくしょの ていしゅつ しめきりは こんしゅうの きんようびです。", "The submission deadline for the proposal is this Friday.", None, "締め切りを守る", "business"),
    ("承知", "しょうち", "shouchi", "[0] Heiban", "N3", "Noun / Suru-Verb", "Acknowledgement, consent (Kenjougo)", "ご指示の件、承知いたしました。", "ごしじの けん、しょうちいたしました。", "Understood and acknowledged regarding your instructions.", None, "承知いたしました", "business"),
    ("恐縮", "きょうしゅく", "kyoushuku", "[0] Heiban", "N3", "Noun / Suru-Verb", "Extremely obliged / sorry to trouble", "お忙しいところ恐縮ですが、ご確認いただけますか？", "おいそがしい ところ きょうしゅくですが、ごかくにん いただけますか？", "I am terribly sorry to trouble you while busy, but could you check this?", None, "大変恐縮ですが", "business"),
    ("調整", "ちょうせい", "chousei", "[0] Heiban", "N3", "Noun / Suru-Verb", "Adjustment, coordination", "来週のミーティング日程を再調整します。", "らいしゅうの みーてぃんぐ にっていを さいちょうせいします。", "I will re-coordinate the meeting schedule for next week.", None, "日程調整", "business"),
    ("改善", "かいぜん", "kaizen", "[0] Heiban", "N3", "Noun / Suru-Verb", "Improvement, optimization", "作業工程を改善して効率を大幅に向上させました。", "さぎょうこうていを かいぜんして こうりつを おおはばに こうじょうさせました。", "We optimized the workflow to significantly boost efficiency.", "改悪 (kaiaku - deterioration)", "環境改善", "business"),
    ("影響", "えいきょう", "eikyou", "[0] Heiban", "N3", "Noun / Suru-Verb", "Influence, impact, effect", "大雪の影響で新幹線の運行ダイヤが乱れています。", "おおゆきの えいきょうで しんかんせんの うんこうだいやが みだれています。", "Shinkansen schedules are disrupted due to the heavy snow's impact.", None, "影響を与える", "transit"),
    ("慎重", "しんちょう", "shinchou", "[0] Heiban", "N3", "Na-Adjective", "Cautious, prudent, discreet", "重要な契約を結ぶ前に慎重に条項を確認しましょう。", "じゅうような けいやくを むすぶまえに しんちょうに じょうこうを かくにんしましょう。", "Let's cautiously verify the clauses before signing an important contract.", "軽率 (keisotsu - rash)", "慎重な判断", "business"),
    ("曖昧", "あいまい", "aimai", "[0] Heiban", "N3", "Na-Adjective", "Vague, ambiguous, noncommittal", "曖昧な返答を避け、明確にYESかNOを伝えてください。", "あいまいな へんとうを さけ、めいかくに いえすか のーを つたえてください。", "Avoid ambiguous replies and convey clearly whether YES or NO.", "明確 (meikaku - clear)", "曖昧な態度", "social"),
    ("節約", "せつやく", "setsuyaku", "[0] Heiban", "N3", "Noun / Suru-Verb", "Economizing, saving money/resources", "自炊を増やして毎月の生活費を節約しています。", "じすいを ふやして まいつきの せいかつひを せつやくしています。", "I save on monthly living expenses by cooking more at home.", "浪費 (rouhi - wasteful spending)", "電気代を節約する", "daily"),
    ("評価", "ひょうか", "hyouka", "[1] Atamadaka", "N3", "Noun / Suru-Verb", "Evaluation, appraisal, rating", "ユーザーからの高い評価を獲得しました。", "ゆーざーからの たかい ひょうかを かくとくしました。", "We earned high appraisals from our users.", None, "高く評価する", "business"),
    ("苦情", "くじょう", "kujou", "[0] Heiban", "N3", "Noun", "Complaint, grievance", "騒音に関する苦情がアパートの管理会社に届いた。", "そうおんに かんする くじょうが あぱーとの かんりがいしゃに とどいた。", "A complaint regarding noise reached the apartment management company.", None, "苦情を申し立てる", "daily"),
    ("指導", "しどう", "shidou", "[0] Heiban", "N3", "Noun / Suru-Verb", "Guidance, coaching, leadership", "先輩の丁寧な指導のおかげで仕事を早く覚えました。", "せんぱいの ていねいな しどうの おかげで しごとを はやく おぼえました。", "Thanks to my senior's polite guidance, I learned the work quickly.", None, "指導を受ける", "business"),

    # ================= N2 CORPORATE & MEDIA =================
    ("把握", "はあく", "haaku", "[0] Heiban", "N2", "Noun / Suru-Verb", "Grasping situation, understanding thoroughly", "現場の最新状況を正確に把握することが最優先課題です。", "げんばの さいしんじょうきょうを せいかくに はあくすることが さいゆうせんかだいです。", "Accurately grasping the onsite situation is the top priority.", None, "現状を把握する", "business"),
    ("措置", "そち", "sochi", "[1] Atamadaka", "N2", "Noun / Suru-Verb", "Measures, steps taken", "個人情報漏洩を防ぐため、緊急の安全措置を講じました。", "こじんじょうほう ろうえいを ふせぐため、きんきゅうの あんぜんそちを こうじました。", "We took emergency safety measures to prevent personal data leaks.", None, "措置を講じる", "business"),
    ("契機", "けいき", "keiki", "[1] Atamadaka", "N2", "Noun", "Turning point, catalyst opportunity", "海外出向を契機として、グローバルな視野が広がった。", "かいがいしゅっこうを けいきとして、ぐろーばるな しやが ひろがった。", "Taking the overseas assignment as a catalyst, my global perspective widened.", None, "〜を契機に", "business"),
    ("懸念", "けねん", "kenen", "[0] Heiban", "N2", "Noun / Suru-Verb", "Concern, apprehension, misgiving", "原材料価格の高騰による業績の悪化が懸念されています。", "げんざいりょうかかくの こうとうによる ぎょうせきの あっかが けねんされています。", "Deterioration in business performance due to rising raw material prices is feared.", None, "懸念材料", "business"),
    ("妥協", "だきょう", "dakyou", "[0] Heiban", "N2", "Noun / Suru-Verb", "Compromise, concession", "品質に関しては一切妥協せず、世界最高峰を目指す。", "ひんしつにかんしては いっさい だきょうせず、せかいさいこうほうを めざす。", "We will never compromise on quality and aim for the world's finest.", None, "妥協点を探る", "business"),
    ("著しい", "いちじるしい", "ichijirushii", "[5] Nakadaka", "N2", "I-Adjective", "Remarkable, striking, pronounced", "近年の人工知能の発展には著しいものがある。", "きんねんの じんこうちのうの はってんには いちじるしい ものが ある。", "The development of artificial intelligence in recent years is truly remarkable.", None, "著しい進歩", "business"),
    ("紛らわしい", "まぎらわしい", "magirawashii", "[5] Nakadaka", "N2", "I-Adjective", "Confusing, easily mistaken", "似た発音の単語が多くて非常に紛らわしいです。", "にた はつおんの たんごが おおくて ひじょうに まぎらわしいです。", "There are many words with similar pronunciation, which is very confusing.", None, "紛らわしい表現", "daily"),
    ("躊躇", "ちゅうちょ", "chuucho", "[1] Atamadaka", "N2", "Noun / Suru-Verb", "Hesitation, reluctance", "千載一遇の好機を前に躊躇してはならない。", "せんざいいちぐうの こうきを まえに ちゅうちょしては ならない。", "You must not hesitate in the face of a once-in-a-lifetime opportunity.", "決断 (ketsudan - decision)", "躊躇なく", "social"),
    ("立て替える", "たてかえる", "tatekaeru", "[4] Odaka", "N2", "Ichidan Verb (Transitive)", "To front money, pay on behalf", "飲み会の会費を幹事が一時的に立て替えておきます。", "のみかいの かいひを かんじが いちじてきに たてかえておきます。", "The organizer will temporarily front the party fee.", None, "費用を立て替える", "dining"),
    ("拘る", "こだわる", "kodawaru", "[3] Nakadaka", "N2", "Godan Verb (Intransitive)", "To be particular about, obsess over", "職人は手作業の伝統製法に徹底して拘っている。", "しょくにんは てざぎょうの でんとうせいほうに てっていして こだわっている。", "The artisan strictly obsesses over handcrafted traditional methods.", None, "品質に拘る", "dining"),
    ("見合わせる", "みあわせる", "miawaseru", "[4] Odaka", "N2", "Ichidan Verb (Transitive)", "To suspend, postpone, hold off", "強風のため、一部列車の運転を見合わせております。", "きょうふうのため、いちぶ れっしゃの うんてんを みあわせております。", "Due to strong winds, operations of certain trains are suspended.", None, "運転を見合わせる", "transit"),
    ("引き受ける", "ひきうける", "hikiukeru", "[4] Odaka", "N2", "Ichidan Verb (Transitive)", "To undertake, take charge of", "困難なプロジェクトのリーダー役を快く引き受けた。", "こんなんな ぷろじぇくとの りーだーやくを こころよく ひきうけた。", "He willingly undertook the leader role for the difficult project.", None, "責任を引き受ける", "business"),
    ("妥当", "だとう", "datou", "[0] Heiban", "N2", "Na-Adjective", "Appropriate, valid, sound", "提示された見積もり金額は市場相場から見て妥当です。", "ていじされた みつもりきんがくは しじょうそうばから みて だとうです。", "The presented estimate amount is valid and sound considering market rates.", "不当 (futou - unfair/invalid)", "妥当な判断", "business"),
    ("該当", "がいとう", "gaitou", "[0] Heiban", "N2", "Noun / Suru-Verb", "Applicable, falls under, corresponding", "申請条件に該当するかどうか事前に確認してください。", "しんせいじょうけんに がいとうするか どうか じぜんに かくにんしてください。", "Please confirm in advance whether you fall under the application criteria.", None, "該当者", "daily"),
    ("経緯", "けいい", "keii", "[1] Atamadaka", "N2", "Noun", "Background story, sequence of events", "トラブルが発生した経緯を詳細に報告書にまとめました。", "とらぶるが はっせいした けいいを しょうさいに ほうこくしょに まとめました。", "I summarized the background sequence of how the trouble occurred in detail.", None, "事の経緯", "business"),

    # ================= N1 ADVANCED LITERARY & FORMAL =================
    ("打開", "だかい", "dakai", "[0] Heiban", "N1", "Noun / Suru-Verb", "Breakthrough, overcoming impasse", "膠着した交渉局面の打開策を全力で模索している。", "こうちゃくした こうしょうきょくめんの だかいさくを ぜんりょくで もさくしている。", "We are exploring breakthrough measures for the deadlocked negotiations.", None, "現状を打開する", "business"),
    ("払拭", "ふっしょく", "fusshoku", "[0] Heiban", "N1", "Noun / Suru-Verb", "Wiping away, dispelling doubts/fears", "透明性の高い情報開示によって市場の不信感を払拭した。", "とうめいせいの たかい じょうほうかいじによって しじょうの ふしんかんを ふっしょくした。", "Through highly transparent disclosure, we dispelled market distrust.", None, "懸念を払拭する", "business"),
    ("踏襲", "とうしゅう", "toushuu", "[0] Heiban", "N1", "Noun / Suru-Verb", "Following precedent, adhering to custom", "新内閣は前政権の外交基本方針を踏襲する見通しだ。", "しんないかくは ぜんせいけんの がいこうきほんほうしんを とうしゅうする みとおしだ。", "The new cabinet is expected to follow the previous administration's foreign policy.", "刷新 (sasshin - reform)", "前例を踏襲する", "business"),
    ("乖離", "かいり", "kairi", "[0] Heiban", "N1", "Noun / Suru-Verb", "Divergence, disconnection, alienation", "理想と現実の間に生じた深刻な乖離を埋める必要がある。", "りそうと げんじつの あいだに しょうじた しんこくな かいりを うめる ひつようが ある。", "We need to bridge the severe divergence that occurred between ideal and reality.", "一致 (icchi - match)", "実態から乖離する", "business"),
    ("示唆", "しさ", "shisa", "[1] Atamadaka", "N1", "Noun / Suru-Verb", "Suggestion, implication, hint", "最新の統計データは景気回復の兆候を示唆している。", "さいしんの とうけいでーたは けいきかいふくの ちょうこうを しさしている。", "The latest statistical data suggests signs of economic recovery.", None, "示唆に富む", "business"),
    ("顕著", "けんちょ", "kencho", "[1] Atamadaka", "N1", "Na-Adjective", "Prominent, conspicuous, striking", "少子高齢化に伴う労働力不足が顕著になってきた。", "しょうしこうれいかに ともなう ろうどうりょくぶそくが けんちょに なってきた。", "Labor shortage accompanying the declining birthrate has become conspicuous.", "潜在 (senzai - latent)", "顕著な効果", "business"),
    ("緻密", "ちみつ", "chimitsu", "[0] Heiban", "N1", "Na-Adjective", "Meticulous, elaborate, precise", "緻密な市場調査に基づいて新たな戦略を立案した。", "ちみつな しじょうちょうさに もとづいて あらたな せんりゃくを りつあんした。", "We drafted a new strategy based on meticulous market research.", "粗雑 (sozatsu - sloppy)", "緻密な計算", "business"),
    ("脆弱", "ぜいじゃく", "zeijaku", "[0] Heiban", "N1", "Na-Adjective", "Vulnerable, fragile, frail", "システムの脆弱性を悪用したサイバー攻撃を遮断した。", "しすてむの ぜいじゃくせいを あくようした さいばーこうげきを しゃだんした。", "We blocked cyber attacks exploiting system vulnerabilities.", "強固 (kyouko - robust)", "脆弱性", "business"),
    ("辛うじて", "かろうじて", "karoujite", "[2] Nakadaka", "N1", "Adverb", "Barely, narrowly, by a thread", "終電の発車ベルが鳴り響く中、辛うじて駆け込み乗車できた。", "しゅうでんの はっしゃべるが なりひびく なか、かろうじて かけこみじょうしゃ できた。", "As the departure bell echoed, I barely managed to board the last train.", None, "辛うじて助かる", "transit"),
    ("悉く", "ことごとく", "kotogotoku", "[2] Nakadaka", "N1", "Adverb", "Utterly, all without exception", "彼が提案した改革案は悉く否決されてしまった。", "かれが ていあんした かいかくあんは ことごとく ひけつされてしまった。", "The reform plans he proposed were rejected utterly without exception.", None, "悉く失敗する", "business"),
    ("固執", "こしゅう", "koshuu", "[0] Heiban", "N1", "Noun / Suru-Verb", "Adhering stubbornly, clinging to", "過去の成功体験に固執しすぎると変化に対応できない。", "かこの せいこうたいけんに こしゅうしすぎると へんかに たいおうできない。", "If you cling too stubbornly to past successes, you cannot adapt to change.", "柔軟 (juunan - flexible)", "自説に固執する", "business"),
    ("軋轢", "あつれき", "atsureki", "[0] Heiban", "N1", "Noun", "Friction, discord, clash", "組織内の意見対立から深刻な軋轢が生じている。", "そしきないの いけんたいりつから しんこくな あつれきが しょうじている。", "Severe friction has arisen from conflicting opinions within the organization.", "調和 (chouwa - harmony)", "軋轢を生む", "business"),
    ("凌駕", "りょうが", "ryouga", "[1] Atamadaka", "N1", "Noun / Suru-Verb", "Surpassing, eclipsing, outstripping", "新製品の性能は従来機を遥かに凌駕している。", "しんせいひんの せいのうは じゅうらいきを はるかに りょうがしている。", "The new product's performance far surpasses conventional models.", None, "他社を凌駕する", "business"),
    ("卓越", "たくえつ", "takuetsu", "[0] Heiban", "N1", "Noun / Suru-Verb", "Excellence, distinguished superiority", "彼の卓越した語学力は国際会議で高く評価された。", "かれの たくえつした ごがくりょくは こくさいかいぎで たかく ひょうかされた。", "His distinguished language proficiency was praised highly at the international conference.", None, "卓越した技術", "social"),
    ("模索", "もさく", "mosaku", "[0] Heiban", "N1", "Noun / Suru-Verb", "Groping for, searching in the dark", "持続可能なエネルギー政策の方向性を暗中模索している。", "じぞくかのうな えねるぎーせいさくの ほうこうせいを あんちゅうもさくしている。", "We are groping in the dark searching for sustainable energy policy directions.", None, "解決策を模索する", "business")
]

def build():
    vocab_entries = []
    for idx, item in enumerate(RAW_CURRICULUM, start=1):
        kanji, reading, romaji, pitch, level, pos, meaning, ex_ja, ex_furi, ex_en, trans_pair, colloc, tag = item
        
        entry_id = f"jlpt_{level.lower()}_{idx:03d}_{romaji.replace('-', '_')}"
        vocab_entries.append({
            "id": entry_id,
            "kanji": kanji,
            "reading": reading,
            "romaji": romaji,
            "pitchAccent": pitch,
            "level": level,
            "partOfSpeech": pos,
            "meaning": meaning,
            "exampleJa": ex_ja,
            "exampleFurigana": ex_furi,
            "exampleZh": ex_en, # 100% English explanation
            "exampleEn": ex_en,
            "transitivePair": trans_pair,
            "collocation": colloc,
            "examYearNote": f"JLPT {level} Core Syllabi (Standard)",
            "scenarioTag": tag
        })
        
    out_file = "TokyoFlow/Resources/jlpt_dictionary.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(vocab_entries, f, ensure_ascii=False, indent=2)
    print(f"✅ Generated {len(vocab_entries)} comprehensive JLPT vocabulary entries into {out_file}")

if __name__ == "__main__":
    build()
