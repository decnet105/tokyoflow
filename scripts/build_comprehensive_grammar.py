import json
import os

# Comprehensive JLPT Grammar Database (N5 ~ N1) with 100% English Explanations
grammars = [
    # --- N5 Grammar Points ---
    {
        "id": "g_n5_001",
        "title": "〜てください / 〜ないでください",
        "level": "N5",
        "romaji": "~te kudasai / ~naide kudasai",
        "meaningZh": "请…… / 请不要……",
        "meaningEn": "Please do / Please do not do (polite request)",
        "connectionRule": "V[て-form] + ください / V[ない-form] + でください",
        "nuanceExplanation": "Used in daily service or public situations to make a polite instruction or request. When speaking to superiors or elders, use '〜ていただけませんか' for deeper respect.",
        "scenarioTag": "transit",
        "examTip": "Key exam pitfall: check correct te-form and nai-form conjugation rules (e.g. 立って, 読んで, 入らないで).",
        "sentences": [
            {
                "id": "s_g_n5_001_1",
                "japanese": "白線の内側までお下がりください。",
                "furigana": "はくせんの うちがわまで おさがりください。",
                "english": "Please step back behind the white line.",
                "chinese": "请退到白线内侧。",
                "audioKey": "白線の内側までお下がりください。"
            },
            {
                "id": "s_g_n5_001_2",
                "japanese": "車内での通話はご遠慮ください。",
                "furigana": "しゃないでの つうわは ごえんりょください。",
                "english": "Please refrain from making phone calls on the train.",
                "chinese": "车厢内请勿通话。",
                "audioKey": "車内での通話はご遠慮ください。"
            }
        ],
        "quiz": {
            "question": "危ないですから、ここに___ください。",
            "questionFurigana": "あぶないですから、ここに___ください。",
            "options": ["入らないで", "入らなくて", "入らない", "入って"],
            "correctIndex": 0,
            "explanationZh": "表示『请不要进入』，接续为动词ない形 + で + ください。",
            "explanationEn": "Negative polite request formula requires V[nai] + de + kudasai ('入らないでください')."
        }
    },
    {
        "id": "g_n5_002",
        "title": "〜てもいいですか / 〜てはいけません",
        "level": "N5",
        "romaji": "~te mo ii desu ka / ~te wa ikemasen",
        "meaningZh": "可以……吗？ / 不可以……",
        "meaningEn": "May I...? (Permission) / You must not... (Prohibition)",
        "connectionRule": "V[て-form] + もいいですか / V[て-form] + はいけません",
        "nuanceExplanation": "'〜てもいいですか' is the golden formula for asking permission when traveling. '〜てはいけません' sounds strict and commonly appears on warning signs and regulations.",
        "scenarioTag": "shopping",
        "examTip": "Frequently tested together with obligation patterns like '〜なければなりません' (must do).",
        "sentences": [
            {
                "id": "s_g_n5_002_1",
                "japanese": "写真を撮ってもいいですか？",
                "furigana": "しゃしんを とっても いいですか？",
                "english": "May I take a photo here?",
                "chinese": "可以拍照吗？",
                "audioKey": "写真を撮ってもいいですか？"
            },
            {
                "id": "s_g_n5_002_2",
                "japanese": "ここでタバコを吸ってはいけません。",
                "furigana": "ここで たばこを すってはいけません。",
                "english": "Smoking is strictly prohibited here.",
                "chinese": "这里严禁吸烟。",
                "audioKey": "ここでタバコを吸ってはいけません。"
            }
        ],
        "quiz": {
            "question": "美術館の中で写真を___。",
            "questionFurigana": "びじゅつかんの なかで しゃしんを___。",
            "options": ["撮ってはいけません", "撮ってもいいです", "撮らなければなりません", "撮りません"],
            "correctIndex": 0,
            "explanationZh": "美术馆内通常禁止拍照，表达禁止用『〜てはいけません』。",
            "explanationEn": "Prohibition in public venues is expressed with V[te] + wa ikemasen ('撮ってはいけません')."
        }
    },
    {
        "id": "g_n5_003",
        "title": "〜たことがある / 〜たことがない",
        "level": "N5",
        "romaji": "~ta koto ga aru / ~ta koto ga nai",
        "meaningZh": "曾经……过 / 从未……过",
        "meaningEn": "Have the experience of doing / Have never done",
        "connectionRule": "V[た-form] + ことがある / ない",
        "nuanceExplanation": "Exclusively used for life milestones and past experiences. Cannot be used for routine actions that occurred this morning or recently.",
        "scenarioTag": "dining",
        "examTip": "Common trap: Must precede with verb past plain form (た-form), never dictionary form.",
        "sentences": [
            {
                "id": "s_g_n5_003_1",
                "japanese": "納豆を食べたことがありますか？",
                "furigana": "なっとうを たべたことが ありますか？",
                "english": "Have you ever tried eating natto?",
                "chinese": "你吃过纳豆吗？",
                "audioKey": "納豆を食べたことがありますか？"
            }
        ],
        "quiz": {
            "question": "富士山に___ことがあります。",
            "questionFurigana": "ふじさんに___ことがあります。",
            "options": ["登った", "登る", "登り", "登って"],
            "correctIndex": 0,
            "explanationZh": "表达过去经历必须接动词た形『登った』。",
            "explanationEn": "Past experience requires verb past form (た-form): '登ったことがある'."
        }
    },
    {
        "id": "g_n5_004",
        "title": "〜たい / 〜たくない",
        "level": "N5",
        "romaji": "~tai / ~takunai",
        "meaningZh": "想…… / 不想……",
        "meaningEn": "Want to do / Do not want to do (1st person desire)",
        "connectionRule": "V[ます-stem] + たい / たくない",
        "nuanceExplanation": "Used directly for the speaker's own desires ('I want to...'). To express a 3rd person's desire, use '〜たがっている'.",
        "scenarioTag": "dining",
        "examTip": "The object particle can be either 'を' or 'が' (e.g. 水を飲みたい / 水が飲みたい).",
        "sentences": [
            {
                "id": "s_g_n5_004_1",
                "japanese": "温かいラーメンを食べたいです。",
                "furigana": "あたたかい らーめんを たべたいです。",
                "english": "I want to eat hot ramen.",
                "chinese": "我想吃热拉面。",
                "audioKey": "温かいラーメンを食べたいです。"
            }
        ],
        "quiz": {
            "question": "日本へ旅行に___です。",
            "questionFurigana": "にほんへ りょこうに___です。",
            "options": ["行きたい", "行くたい", "行きた", "行きて"],
            "correctIndex": 0,
            "explanationZh": "动词ます形词干『行き』 + たい。",
            "explanationEn": "Desire takes verb stem + tai: '行きたいです'."
        }
    },

    # --- N4 Grammar Points ---
    {
        "id": "g_n4_001",
        "title": "〜たら / 〜なら / 〜ば / 〜と (Four Conditionals)",
        "level": "N4",
        "romaji": "~tara / ~nara / ~ba / ~to",
        "meaningZh": "如果……就……（四大条件假定）",
        "meaningEn": "If / When / Upon (Conditionals and hypotheticals)",
        "connectionRule": "V[たら] / N[なら] / V[ば] / V[辞書形] + と",
        "nuanceExplanation": "'〜たら' is conversational and sequential; '〜と' represents natural laws or machine triggers; '〜なら' gives tailored advice on a topic.",
        "scenarioTag": "transit",
        "examTip": "Crucial distinction: '〜と' cannot be followed by invitations, commands, or requests ('〜てください').",
        "sentences": [
            {
                "id": "s_g_n4_001_1",
                "japanese": "駅に着いたら、電話してください。",
                "furigana": "えきに ついたら、でんわ してください。",
                "english": "When you arrive at the station, please give me a call.",
                "chinese": "到了车站后，请给我打电话。",
                "audioKey": "駅に着いたら、電話してください。"
            },
            {
                "id": "s_g_n4_001_2",
                "japanese": "ボタンを押すと、切符が出ます。",
                "furigana": "ぼたんを おすと、きっぷが でます。",
                "english": "Press the button and the ticket will dispense.",
                "chinese": "按一下按钮，车票就会出来。",
                "audioKey": "ボタンを押すと、切符が出ます。"
            }
        ],
        "quiz": {
            "question": "時間があったら、一緒にカフェに___。",
            "questionFurigana": "じかんが あったら、いっしょに かふぇに___。",
            "options": ["行きませんか", "行くと", "行けば", "行きますと"],
            "correctIndex": 0,
            "explanationZh": "『〜たら』后项可以接邀请句『行きませんか』。",
            "explanationEn": "'〜たら' allows invitations and proposals in the main clause: '行きませんか'."
        }
    },
    {
        "id": "g_n4_002",
        "title": "〜てあげる / 〜てもらう / 〜てくれる (Giving & Receiving)",
        "level": "N4",
        "romaji": "~te ageru / ~te morau / ~te kureru",
        "meaningZh": "为某人做 / 得到某人的恩惠 / 某人为我做",
        "meaningEn": "Do a favor for / Receive a favor from / Someone does a favor for me",
        "connectionRule": "V[て-form] + あげる / もらう / くれる",
        "nuanceExplanation": "Core Japanese social psychology: '〜てくれる' highlights gratitude when someone voluntarily helps you or your in-group.",
        "scenarioTag": "social",
        "examTip": "Watch the subject particles carefully: [Giver] が [Receiver] に ~てあげる; [Receiver] は [Giver] に ~てもらう; [Giver] が [Me] に ~てくれる.",
        "sentences": [
            {
                "id": "s_g_n4_002_1",
                "japanese": "店員さんが道を教えてくれました。",
                "furigana": "てんいんさんが みちを おしえて くれました。",
                "english": "The store clerk kindly gave me directions.",
                "chinese": "店员好心地给我指了路。",
                "audioKey": "店員さんが道を教えてくれました。"
            }
        ],
        "quiz": {
            "question": "友達が引っ越しを___。",
            "questionFurigana": "ともだちが ひっこしを___。",
            "options": ["手伝ってくれました", "手伝ってもらいました", "手伝ってあげました", "手伝いました"],
            "correctIndex": 0,
            "explanationZh": "朋友（主语）为我提供帮助，用『〜てくれました』。",
            "explanationEn": "When a friend does a favor for you (friend is subject with が), use '手伝ってくれました'."
        }
    },
    {
        "id": "g_n4_003",
        "title": "〜ようにする / 〜ことになる",
        "level": "N4",
        "romaji": "~you ni suru / ~koto ni naru",
        "meaningZh": "努力做到…… / 决定/变成了……",
        "meaningEn": "Make an effort to do / It has been decided that (external rule or outcome)",
        "connectionRule": "V[辞書形/ない形] + ようにする / ことになる",
        "nuanceExplanation": "'〜ようにする' expresses continuous conscious effort (e.g. healthy habits). '〜ことになる' expresses corporate decisions or external circumstances.",
        "scenarioTag": "daily",
        "examTip": "Contrast with '〜ことにする' (personal decision) vs '〜ことになる' (external decision).",
        "sentences": [
            {
                "id": "s_g_n4_003_1",
                "japanese": "毎日日本語のニュースを聞くようにしています。",
                "furigana": "まいにち にほんごの にゅーすを きくように しています。",
                "english": "I make a conscious effort to listen to Japanese news every day.",
                "chinese": "我每天都努力坚持听日语新闻。",
                "audioKey": "毎日日本語のニュースを聞くようにしています。"
            }
        ],
        "quiz": {
            "question": "健康のために、野菜をたくさん___ようにしています。",
            "questionFurigana": "けんこうのために、やさいを たくさん___ようにしています。",
            "options": ["食べる", "食べた", "食べ", "食べよう"],
            "correctIndex": 0,
            "explanationZh": "表达日常努力用动词辞书形 + ようにする。",
            "explanationEn": "Conscious habit requires dictionary form + you ni suru: '食べるようにしています'."
        }
    },

    # --- N3 Grammar Points ---
    {
        "id": "g_n3_001",
        "title": "〜わけにはいかない / 〜わけがない",
        "level": "N3",
        "romaji": "~wake ni wa ikanai / ~wake ga nai",
        "meaningZh": "不能……（情理不容） / 绝不可能……",
        "meaningEn": "Cannot afford to do (due to social/moral obligations) / Absolutely impossible that",
        "connectionRule": "V[辞書形/ない形] + わけにはいかない",
        "nuanceExplanation": "'〜わけにはいかない' expresses that internal ethics, duty, or social decorum prevent you from doing something, even if physically capable.",
        "scenarioTag": "business",
        "examTip": "Double negative: '〜ないわけにはいかない' means 'have no choice but to do' (must do).",
        "sentences": [
            {
                "id": "s_g_n3_001_1",
                "japanese": "大事な会議があるので、休むわけにはいきません。",
                "furigana": "だいじな かいぎが あるので、やすむ わけには いきません。",
                "english": "I have an important meeting, so I cannot afford to take the day off.",
                "chinese": "因为有重要会议，我绝不能请假。",
                "audioKey": "大事な会議があるので、休むわけにはいきません。"
            }
        ],
        "quiz": {
            "question": "明日は試験だから、勉強___わけにはいかない。",
            "questionFurigana": "あしたは しけんだから、べんきょう___わけにはいかない。",
            "options": ["しない", "する", "した", "しよう"],
            "correctIndex": 0,
            "explanationZh": "『不能不学习（必须学）』使用双重否定『勉強しないわけにはいかない』。",
            "explanationEn": "Double negative obligation: '勉強しないわけにはいかない' (cannot afford not to study)."
        }
    },
    {
        "id": "g_n3_002",
        "title": "〜かねない / 〜かねる",
        "level": "N3",
        "romaji": "~kanenai / ~kaneru",
        "meaningZh": "很有可能造成不良后果 / 难以……（委婉拒绝）",
        "meaningEn": "Could easily lead to a bad result / Cannot easily do (polite refusal)",
        "connectionRule": "V[ます-stem] + かねない / かねる",
        "nuanceExplanation": "'〜かねない' ALWAYS predicts an undesirable, dangerous, or negative outcome. '〜かねる' is formal business Japanese to politely decline.",
        "scenarioTag": "business",
        "examTip": "High frequency JLPT N3/N2 exam point: Note that '〜かねない' has negative morphology but affirmative meaning ('might happen').",
        "sentences": [
            {
                "id": "s_g_n3_002_1",
                "japanese": "スピードの出しすぎは、大事故を起こしかねない。",
                "furigana": "すぴーどの だしすぎは、だいじこを おこしかねない。",
                "english": "Excessive speeding could easily cause a major accident.",
                "chinese": "超速行驶极有可能引发重大事故。",
                "audioKey": "スピードの出しすぎは、大事故を起こしかねない。"
            }
        ],
        "quiz": {
            "question": "個人情報に関するご質問には、お答え___。",
            "questionFurigana": "こじんじょうほうに かんする ごしつもんには、おこたえ___。",
            "options": ["しかねます", "しかねません", "し得ます", "しそうです"],
            "correctIndex": 0,
            "explanationZh": "商务委婉拒绝用『お答えしかねます（难以回答）』。",
            "explanationEn": "Polite business refusal takes stem + kanemasu: 'お答えしかねます' (We are unable to answer)."
        }
    },
    {
        "id": "g_n3_003",
        "title": "〜を中心に / 〜をはじめ",
        "level": "N3",
        "romaji": "~o chuushin ni / ~o hajime",
        "meaningZh": "以……为中心 / 以……为代表",
        "meaningEn": "Centering around... / Starting with / Led by...",
        "connectionRule": "N + を中心に / をはじめ（として）",
        "nuanceExplanation": "Used in news broadcasts and essays to indicate the representative core of a broader trend, demographic, or region.",
        "scenarioTag": "transit",
        "examTip": "Essential for reading comprehension (Dokkai) sections in JLPT N3.",
        "sentences": [
            {
                "id": "s_g_n3_003_1",
                "japanese": "東京駅を中心に、再開発が進んでいます。",
                "furigana": "とうきょうえきを ちゅうしんに、さいかいはつが すすんでいます。",
                "english": "Urban redevelopment is progressing centering around Tokyo Station.",
                "chinese": "以东京站为中心，城市再开发正在推进。",
                "audioKey": "東京駅を中心に、再開発が進んでいます。"
            }
        ],
        "quiz": {
            "question": "若者___、幅広い世代に人気がある。",
            "questionFurigana": "わかもの___、はばひろい せだいに にんきが ある。",
            "options": ["をはじめ", "を中心で", "を皮切り", "をとって"],
            "correctIndex": 0,
            "explanationZh": "以年轻人为代表/首要群体，用『〜をはじめ』。",
            "explanationEn": "Representative primary group takes N + o hajime: '若者をはじめ'."
        }
    },

    # --- N2 Grammar Points ---
    {
        "id": "g_n2_001",
        "title": "〜ざるを得ない / 〜ずにはいられない",
        "level": "N2",
        "romaji": "~zaru o enai / ~zu ni wa irarenai",
        "meaningZh": "不得不……（无可奈何） / 忍不住……（情绪不可控）",
        "meaningEn": "Cannot help but do / Have no choice but to / Cannot resist doing",
        "connectionRule": "V[ない-stem] + ざるを得ない (する -> せざるを得ない)",
        "nuanceExplanation": "'〜ざるを得ない' implies reluctance in the face of inevitable reality. 'する' becomes the irregular 'せざるを得ない'.",
        "scenarioTag": "business",
        "examTip": "Watch for the irregular form: 'する -> せざるを得ない', never 'しざるを得ない'.",
        "sentences": [
            {
                "id": "s_g_n2_001_1",
                "japanese": "台風の影響で、イベントは中止せざるを得ない。",
                "furigana": "たいふうの えいきょうで、いべんとは ちゅうし せざるを えない。",
                "english": "Due to the typhoon, we have no choice but to cancel the event.",
                "chinese": "受台风影响，不得不取消活动。",
                "audioKey": "台風の影響で、イベントは中止せざるを得ない。"
            }
        ],
        "quiz": {
            "question": "証拠が揃っている以上、事実を___を得ない。",
            "questionFurigana": "しょうこが そろっている いじょう、じじつを___を えない。",
            "options": ["認めざる", "認める", "認めない", "認めず"],
            "correctIndex": 0,
            "explanationZh": "动词ない形词干『認め』 + ざるを得ない。",
            "explanationEn": "Unavoidable recognition requires nai-stem + zaru o enai: '認めざるを得ない'."
        }
    },
    {
        "id": "g_n2_002",
        "title": "〜に違いない / 〜に相違ない",
        "level": "N2",
        "romaji": "~ni chigainai / ~ni souinai",
        "meaningZh": "必定…… / 毫无疑问……",
        "meaningEn": "Must be / There is no doubt that (Strong logical certainty)",
        "connectionRule": "Plain Form + に違いない / に相違ない",
        "nuanceExplanation": "Speaker has strong logical evidence or high subjective conviction that something is true.",
        "scenarioTag": "daily",
        "examTip": "'〜に相違ない' is more formal and written compared to conversational '〜に違いない'.",
        "sentences": [
            {
                "id": "s_g_n2_002_1",
                "japanese": "彼が犯人に違いない。",
                "furigana": "かれが はんにんに ちがいない。",
                "english": "He must be the culprit without a doubt.",
                "chinese": "凶手一定是他。",
                "audioKey": "彼が犯人に違いない。"
            }
        ],
        "quiz": {
            "question": "これだけ練習したのだから、合格する___。",
            "questionFurigana": "これだけ れんしゅうしたのだから、ごうかくする___。",
            "options": ["に違いない", "にすぎない", "にほかならない", "に限らない"],
            "correctIndex": 0,
            "explanationZh": "基于充分练习推断必定合格，用『〜に違いない』。",
            "explanationEn": "Strong positive certainty based on evidence takes 'に違いない'."
        }
    },
    {
        "id": "g_n2_003",
        "title": "〜を契機に / 〜を皮切りに",
        "level": "N2",
        "romaji": "~o keiki ni / ~o kawakiri ni",
        "meaningZh": "以……为契机 / 以……为开端",
        "meaningEn": "Taking the opportunity of / Starting with (and spreading sequentially)",
        "connectionRule": "N + を契機に / を皮切りに（して）",
        "nuanceExplanation": "'〜を契機に' denotes a turning point that brings about a major change. '〜を皮切りに' denotes an event that kicks off a series of similar actions.",
        "scenarioTag": "business",
        "examTip": "Very frequent in news reporting and business history questions.",
        "sentences": [
            {
                "id": "s_g_n2_003_1",
                "japanese": "東京公演を皮切りに、全国ツアーがスタートした。",
                "furigana": "とうきょうこうえんを かわきりに、ぜんこくつあーが すたーとした。",
                "english": "Starting with the Tokyo concert, the nationwide tour kicked off.",
                "chinese": "以东京演出为开端，全国巡演正式启动。",
                "audioKey": "東京公演を皮切りに、全国ツアーがスタートした。"
            }
        ],
        "quiz": {
            "question": "留学___、国際問題に関心を持つようになった。",
            "questionFurigana": "りゅうがく___、こくさいもんだいに かんしんを もつようになった。",
            "options": ["を契機に", "を皮切りに", "を限りに", "を抜きに"],
            "correctIndex": 0,
            "explanationZh": "以留学为人生契机转变兴趣，用『〜を契機に』。",
            "explanationEn": "Personal turning point takes N + o keiki ni: '留学を契機に'."
        }
    },

    # --- N1 Grammar Points ---
    {
        "id": "g_n1_001",
        "title": "〜を余儀なくされる / 〜を余儀なくさせる",
        "level": "N1",
        "romaji": "~o yogi naku sareru / ~o yogi naku saseru",
        "meaningZh": "被迫…… / 迫使……（极为无奈）",
        "meaningEn": "Be forced / compelled to do something (against one's will due to unavoidable circumstances)",
        "connectionRule": "N + を余儀なくされる（被动） / を余儀なくさせる（使役）",
        "nuanceExplanation": "High-level written formal expression. Passive '~される' means human subjects are forced into a situation; Causative '~させる' means an external factor forces people.",
        "scenarioTag": "emergency",
        "examTip": "Top JLPT N1 trap: Pay close attention to Passive (される) vs Causative (させる) subject alignment.",
        "sentences": [
            {
                "id": "s_g_n1_001_1",
                "japanese": "資金難により、プロジェクトの凍結を余儀なくされた。",
                "furigana": "しきんなんにより、ぷろじぇくとの とうけつを よぎなく された。",
                "english": "Due to financial difficulties, we were forced to freeze the project.",
                "chinese": "由于资金困难，不得不冻结该项目。",
                "audioKey": "資金難により、プロジェクトの凍結を余儀なくされた。"
            }
        ],
        "quiz": {
            "question": "大雪のため、飛行機の欠航を___。",
            "questionFurigana": "おおゆきのため、ひこうきの けっこうを___。",
            "options": ["余儀なくされた", "余儀なくさせた", "余儀なくした", "余儀なくあられた"],
            "correctIndex": 0,
            "explanationZh": "航班（我们）被迫取消，使用被动态『余儀なくされた』。",
            "explanationEn": "Being forced into cancellation uses passive form: '余儀なくされた'."
        }
    },
    {
        "id": "g_n1_002",
        "title": "〜極まりない / 〜の極み",
        "level": "N1",
        "romaji": "~kiwamarinai / ~no kiwami",
        "meaningZh": "极其…… / 达到顶点的……",
        "meaningEn": "Extremely / Boundlessly / The pinnacle of...",
        "connectionRule": "Na-adj[stem] + 極まりない / N + の極み",
        "nuanceExplanation": "Literary exaggeration indicating an extreme emotional state (e.g. 失礼極まりない = extremely insolent; 痛恨の極み = deepest regret).",
        "scenarioTag": "business",
        "examTip": "Notice that '極まりない' attaches directly to na-adjective stem (失礼極まりない) or with な (失礼なこと極まりない).",
        "sentences": [
            {
                "id": "s_g_n1_002_1",
                "japanese": "無断で遅刻するとは、無責任極まりない態度だ。",
                "furigana": "むだんで ちこくするとは、むせきにん きわまりない たいどだ。",
                "english": "Showing up late without notice is an attitude of utmost irresponsibility.",
                "chinese": "擅自迟到是极其不负责任的态度。",
                "audioKey": "無断で遅刻するとは、無責任極まりない態度だ。"
            }
        ],
        "quiz": {
            "question": "このような名誉ある賞をいただき、感激の___です。",
            "questionFurigana": "このような めいよある しょうを いただき、かんげきの___です。",
            "options": ["極み", "極まりない", "限り", "始末"],
            "correctIndex": 0,
            "explanationZh": "名词接『の極み』表达极其感激。",
            "explanationEn": "Noun takes 'の極み': '感激の極み' (the height of gratitude)."
        }
    },
    {
        "id": "g_n1_003",
        "title": "〜ならでは / 〜ならではの",
        "level": "N1",
        "romaji": "~naredewa / ~naredewa no",
        "meaningZh": "独有的…… / 只有……才具备的",
        "meaningEn": "Distinctive to / Unique to / Only possible because of...",
        "connectionRule": "N + ならでは（の N）",
        "nuanceExplanation": "Expresses high praise for a unique quality or charm that only that specific person, place, or tradition can offer.",
        "scenarioTag": "dining",
        "examTip": "Very frequent in tourism features, essays, and JLPT N1 reading comprehension.",
        "sentences": [
            {
                "id": "s_g_n1_003_1",
                "japanese": "下町ならではの温かい人情に触れた。",
                "furigana": "したまち ならではの あたたかい にんじょうに ふれた。",
                "english": "I experienced the warm hospitality unique to traditional Tokyo downtown.",
                "chinese": "体会到了老街独有的温厚人情。",
                "audioKey": "下町ならではの温かい人情に触れた。"
            }
        ],
        "quiz": {
            "question": "手作り___の素朴な味わいがある。",
            "questionFurigana": "てづくり___の そぼくな あじわいが ある。",
            "options": ["ならでは", "にあって", "を限りに", "ならではで"],
            "correctIndex": 0,
            "explanationZh": "表达纯手工制作独有的风味，用『〜ならではの』。",
            "explanationEn": "Unique charm takes N + naredewa no: '手作りならではの素朴な味わい'."
        }
    }
]

with open("TokyoFlow/Resources/jlpt_grammar.json", "w", encoding="utf-8") as f:
    json.dump(grammars, f, ensure_ascii=False, indent=2)

print(f"✅ Generated {len(grammars)} comprehensive JLPT Grammar points with 100% English explanations.")
