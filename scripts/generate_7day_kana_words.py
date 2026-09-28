import json

# 7 distinct daily words for all Seion, Dakuon, and Yoon Kana (Day 1..7 -> Monday..Sunday)
# Carefully selected for high frequency in Tokyo daily life (food, transit, shopping, convenience store, manga, everyday phrases)

kana_7day_dict = {
    # --- あ行 ---
    "a": [
        ("ありがとう", "arigatou", "Thank you (谢谢/感谢)"),
        ("あさ (朝)", "asa", "Morning (早晨/清晨)"),
        ("あめ (雨)", "ame", "Rain / Candy (下雨/雨水)"),
        ("あき (秋)", "aki", "Autumn (秋天/秋季)"),
        ("あたま (頭)", "atama", "Head (头部/脑筋)"),
        ("あか (赤)", "aka", "Red color (红色)"),
        ("あんない (案内)", "annai", "Guidance / Info (指引/向导)")
    ],
    "i": [
        ("いぬ (犬)", "inu", "Dog (小狗)"),
        ("いいえ", "iie", "No / You're welcome (不/不客气)"),
        ("いくら", "ikura", "How much (多少钱/鲑鱼子)"),
        ("いざかや (居酒屋)", "izakaya", "Izakaya Pub (居酒屋)"),
        ("いっしょに (一緒に)", "isshoni", "Together (一起)"),
        ("いま (今)", "ima", "Now / Right now (现在)"),
        ("いちばん (一番)", "ichiban", "Number one / Best (最/第一)")
    ],
    "u": [
        ("うどん", "udon", "Udon noodles (乌冬面)"),
        ("うみ (海)", "umi", "Sea / Ocean (大海)"),
        ("うしろ (後ろ)", "ushiro", "Behind / Back (后面)"),
        ("うえ (上)", "ue", "Above / Up (上面)"),
        ("うれしい (嬉しい)", "ureshii", "Happy / Glad (高兴/开心)"),
        ("うまい (旨い)", "umai", "Delicious / Good (美味/厉害)"),
        ("うけつけ (受付)", "uketsuke", "Reception desk (前台/接待处)")
    ],
    "e": [
        ("えき (駅)", "eki", "Train Station (车站/电车站)"),
        ("えいが (映画)", "eiga", "Movie (电影)"),
        ("えのぐ (絵の具)", "enogu", "Paints / Color (颜料/水彩)"),
        ("えんぴつ (鉛筆)", "enpitsu", "Pencil (铅笔)"),
        ("えび (海老)", "ebi", "Shrimp / Prawn (虾)"),
        ("えがお (笑顔)", "egao", "Smiling face (笑脸/笑容)"),
        ("えきいん (駅員)", "ekiin", "Station attendant (车站工作人员)")
    ],
    "o": [
        ("おにぎり", "onigiri", "Rice ball (饭团)"),
        ("おちゃ (お茶)", "ocha", "Green tea (绿茶/茶)"),
        ("おいしい (美味しい)", "oishii", "Delicious (好吃/美味)"),
        ("おねがい (お願い)", "onegai", "Please (拜托/请)"),
        ("おかいけい (お会計)", "okaikei", "Bill / Check (结账/买单)"),
        ("おと (音)", "oto", "Sound / Noise (声音)"),
        ("おみやげ (お土産)", "omiyage", "Souvenir / Gift (土特产/伴手礼)")
    ],

    # --- か行 ---
    "ka": [
        ("かわいい", "kawaii", "Cute / Adorable (可爱)"),
        ("かさ (傘)", "kasa", "Umbrella (雨伞)"),
        ("かいさつ (改札)", "kaisatsu", "Ticket barrier (闸机/检票口)"),
        ("かばん (鞄)", "kaban", "Bag / Backpack (包/提包)"),
        ("からあげ (唐揚げ)", "karaage", "Fried chicken (日式炸鸡)"),
        ("カフェ", "kafe", "Cafe (咖啡馆)"),
        ("かんぱい (乾杯)", "kanpai", "Cheers! (干杯)")
    ],
    "ki": [
        ("きっぷ (切符)", "kippu", "Train Ticket (车票)"),
        ("きっさてん (喫茶店)", "kissaten", "Classic Coffee shop (咖啡茶座)"),
        ("きょう (今日)", "kyou", "Today (今天)"),
        ("きのう (昨日)", "kinou", "Yesterday (昨天)"),
        ("きゅうこう (急行)", "kyuukou", "Express train (急行列车)"),
        ("きいろ (黄色)", "kiiro", "Yellow color (黄色)"),
        ("きもち (気持ち)", "kimochi", "Feeling / Mood (心情/感觉)")
    ],
    "ku": [
        ("くるま (車)", "kuruma", "Car / Vehicle (汽车)"),
        ("くすり (薬)", "kusuri", "Medicine (药物/药品)"),
        ("くうこう (空港)", "kuukou", "Airport (机场)"),
        ("くだもの (果物)", "kudamono", "Fruit (水果)"),
        ("くつ (靴)", "kutsu", "Shoes (鞋子)"),
        ("くも (雲)", "kumo", "Cloud (云彩)"),
        ("クレジットカード", "kurejitto kaado", "Credit card (信用卡)")
    ],
    "ke": [
        ("けいたい (携帯)", "keitai", "Mobile phone (手机)"),
        ("けしき (景色)", "keshiki", "Scenery / View (风景/景色)"),
        ("ケーキ", "keeki", "Cake (蛋糕)"),
        ("けっこん (結婚)", "kekkon", "Marriage (结婚)"),
        ("けっこう (結構)", "kekkou", "Fine / No thanks (挺好/不用了)"),
        ("けいさつ (警察)", "keisatsu", "Police (警察/交番)"),
        ("けむり (煙)", "kemuri", "Smoke (烟雾)")
    ],
    "ko": [
        ("コンビニ", "konbini", "Convenience store (便利店)"),
        ("こうえん (公園)", "kouen", "Park (公园)"),
        ("コーヒー", "koohii", "Coffee (咖啡)"),
        ("こんばん (今晩)", "konban", "Tonight / This evening (今晚)"),
        ("ここ", "koko", "Here / This place (这里)"),
        ("こども (子供)", "kodomo", "Child / Kids (孩子)"),
        ("こころ (心)", "kokoro", "Heart / Mind (心灵/心情)")
    ],

    # --- さ行 ---
    "sa": [
        ("さくら (桜)", "sakura", "Cherry blossom (樱花)"),
        ("さかな (魚)", "sakana", "Fish (鱼/生鱼片)"),
        ("さいふ (財布)", "saifu", "Wallet (钱包)"),
        ("さようなら", "sayounara", "Goodbye (再见)"),
        ("さとう (砂糖)", "satou", "Sugar (白糖/砂糖)"),
        ("さんぽ (散歩)", "sanpo", "Stroll / Walk (散步)"),
        ("サービス", "saabisu", "Service / Free perk (服务/附赠)")
    ],
    "shi": [
        ("しんじゅく (新宿)", "shinjuku", "Shinjuku (新宿)"),
        ("しんかんせん (新幹線)", "shinkansen", "Bullet train (新干线)"),
        ("しぶや (渋谷)", "shibuya", "Shibuya (涩谷)"),
        ("しゃしん (写真)", "shashin", "Photo / Picture (照片)"),
        ("しゅうでん (終電)", "shuuden", "Last train of the night (末班车)"),
        ("しお (塩)", "shio", "Salt (食盐)"),
        ("しつれいします (失礼します)", "shitsurei shimasu", "Excuse me (打扰了/失礼了)")
    ],
    "su": [
        ("すいか (Suica)", "suika", "Suica Card / Watermelon (西瓜卡/西瓜)"),
        ("すし (寿司)", "sushi", "Sushi (寿司)"),
        ("すみません", "sumimasen", "Excuse me / Sorry (不好意思/抱歉)"),
        ("スーパー", "suupaa", "Supermarket (超市)"),
        ("すき (好き)", "suki", "Like / Fond of (喜欢)"),
        ("すずしい (涼しい)", "suzushii", "Cool weather (凉爽)"),
        ("すこし (少し)", "sukoshi", "A little bit (稍微/一点)")
    ],
    "se": [
        ("せんせい (先生)", "sensei", "Teacher / Doctor (老师/前辈)"),
        ("せき (席)", "seki", "Seat / Table (座位)"),
        ("せんたく (洗濯)", "sentaku", "Laundry / Washing (洗衣服)"),
        ("せまい (狭い)", "semai", "Narrow / Cozy space (狭窄/小巧)"),
        ("せかい (世界)", "sekai", "World (世界)"),
        ("せつめい (説明)", "setsumei", "Explanation (说明/解释)"),
        ("セット (セット)", "setto", "Combo set / Meal set (套餐)")
    ],
    "so": [
        ("そば", "soba", "Soba noodles (荞麦面)"),
        ("そら (空)", "sora", "Sky (天空)"),
        ("そこ", "soko", "There / That place (那里)"),
        ("ソフトクリーム", "sofutokuriimu", "Soft serve ice cream (冰淇淋)"),
        ("そうですね", "sou desu ne", "I see / That's right (确实如此)"),
        ("そうじ (掃除)", "souji", "Cleaning (打扫/清洁)"),
        ("そと (外)", "soto", "Outside (外面/室外)")
    ],

    # --- た行 ---
    "ta": [
        ("たこやき", "takoyaki", "Takoyaki (章鱼小丸子)"),
        ("たべもの (食べ物)", "tabemono", "Food (食物)"),
        ("たいへん (大変)", "taihen", "Tough / Hard (辛苦/不容易)"),
        ("タクシー", "takushii", "Taxi (出租车)"),
        ("たのしい (楽しい)", "tanoshii", "Fun / Enjoyable (愉快/开心)"),
        ("たまご (卵)", "tamago", "Egg (鸡蛋)"),
        ("たかい (高い)", "takai", "High / Expensive (高/贵)")
    ],
    "chi": [
        ("ちかてつ (地下鉄)", "chikatetsu", "Subway / Metro (地下铁)"),
        ("ちかい (近い)", "chikai", "Near / Close by (很近)"),
        ("チケット", "chiketto", "Ticket (入场券/票)"),
        ("ちず (地図)", "chizu", "Map (地图)"),
        ("ちゅうもん (注文)", "chuumon", "Order food (点单/点菜)"),
        ("ちょっと", "chotto", "A moment / A bit (稍等/稍微)"),
        ("ちから (力)", "chikara", "Strength / Power (力量)")
    ],
    "tsu": [
        ("つき (月)", "tsuki", "Moon / Month (月亮/月份)"),
        ("つくえ (机)", "tsukue", "Desk / Table (书桌)"),
        ("つぎ (次)", "tsugi", "Next (下一个/下一站)"),
        ("つめたい (冷たい)", "tsumetai", "Cold / Chilled drink (冰凉/冷)"),
        ("つかう (使う)", "tsukau", "To use (使用)"),
        ("つよい (強い)", "tsuyoi", "Strong (强劲/强烈)"),
        ("つうきん (通勤)", "tsuukin", "Commuting to work (通勤)")
    ],
    "te": [
        ("てんぷら", "tenpura", "Tempura (天妇罗)"),
        ("てんき (天気)", "tenki", "Weather (天气)"),
        ("てがみ (手紙)", "tegami", "Letter (信件)"),
        ("テーブル", "teeburu", "Table (餐桌)"),
        ("てんいん (店員)", "ten'in", "Clerk / Store staff (店员)"),
        ("ていしょく (定食)", "teishoku", "Set meal (定食套餐)"),
        ("テレビ", "terebi", "Television (电视)")
    ],
    "to": [
        ("とうきょう (東京)", "toukyou", "Tokyo (东京)"),
        ("ともだち (友達)", "tomodachi", "Friend (朋友)"),
        ("とりあえずにく", "toriaezu nama", "Beer for starters! (先来杯生啤！)"),
        ("トイレ", "toire", "Restroom (洗手间/厕所)"),
        ("となり (隣)", "tonari", "Next door / Beside (旁边/隔壁)"),
        ("とおり (通り)", "toori", "Street / Avenue (街道/马路)"),
        ("とけい (時計)", "tokei", "Clock / Watch (时钟/手表)")
    ],

    # --- な行 ---
    "na": [
        ("なつ (夏)", "natsu", "Summer (夏天)"),
        ("なまえ (名前)", "namae", "Name (名字/姓名)"),
        ("なっとう (納豆)", "nattou", "Natto fermented beans (纳豆)"),
        ("なに (何)", "nani", "What? (什么)"),
        ("なか (中)", "naka", "Inside / Middle (里面/内部)"),
        ("ならぶ (並ぶ)", "narabu", "To line up / Queue (排队)"),
        ("なつかしい (懐かしい)", "natsukashii", "Nostalgic (令人怀念)")
    ],
    "ni": [
        ("にほん (日本)", "nihon", "Japan (日本)"),
        ("にく (肉)", "niku", "Meat (肉类)"),
        ("にちようび (日曜日)", "nichiyoubi", "Sunday (周日)"),
        ("にもつ (荷物)", "nimotsu", "Luggage / Package (行李/包裹)"),
        ("にぎやか (賑やか)", "nigiyaka", "Lively / Bustling (热闹/繁华)"),
        ("にんじん", "ninjin", "Carrot (胡萝卜)"),
        ("ニュース", "nyuusu", "News (新闻)")
    ],
    "nu": [
        ("ぬいぐるみ", "nuigurumi", "Plush doll (玩偶/毛绒玩具)"),
        ("ぬるい (温い)", "nurui", "Lukewarm (温温的/不够烫)"),
        ("ぬぐ (脱ぐ)", "nugu", "To take off shoes/coat (脱鞋/脱衣服)"),
        ("ぬりえ (塗り絵)", "nurie", "Coloring book (涂色画)"),
        ("ぬま (沼)", "numa", "Pond / Obsession (沼泽/深陷爱好)"),
        ("ぬけみち (抜け道)", "nukemichi", "Shortcut alley (捷径/小道)"),
        ("ぬれたおる (濡れタオル)", "nure taoru", "Wet hand towel (湿毛巾)")
    ],
    "ne": [
        ("ねこ (猫)", "neko", "Cat (猫咪)"),
        ("ねつ (熱)", "netsu", "Fever / Heat (发烧/热情)"),
        ("ねだん (値段)", "nedan", "Price (价格/售价)"),
        ("ネット", "netto", "Internet (网络)"),
        ("ねる (寝る)", "neru", "To sleep / Go to bed (睡觉)"),
        ("ネギ", "negi", "Green onion (大葱)"),
        ("ねんまつ (年末)", "nenmatsu", "Year-end (年末/岁末)")
    ],
    "no": [
        ("のみもの (飲み物)", "nomimono", "Beverage / Drink (饮料)"),
        ("のりかえ (乗り換え)", "norikae", "Train transfer (换乘/转车)"),
        ("のど (喉)", "nodo", "Throat (嗓子/喉咙)"),
        ("ノート", "nooto", "Notebook (笔记本)"),
        ("のる (乗る)", "noru", "To ride / Board train (乘坐/乘车)"),
        ("のり (海苔)", "nori", "Seaweed sheet (海苔)"),
        ("のんびり", "nonbiri", "Relaxed / Chill (悠闲/放松)")
    ],

    # --- は行 ---
    "ha": [
        ("はなび (花火)", "hanabi", "Fireworks (烟花/花火)"),
        ("はる (春)", "haru", "Spring (春天)"),
        ("はし (箸)", "hashi", "Chopsticks (筷子)"),
        ("はい", "hai", "Yes (是的/明白)"),
        ("はこ (箱)", "hako", "Box (盒子/箱子)"),
        ("はな (花)", "hana", "Flower (鲜花)"),
        ("はんぶん (半分)", "hanbun", "Half portion (一半)")
    ],
    "hi": [
        ("ひかり (光)", "hikari", "Light / Shinkansen Hikari (光芒/光速)"),
        ("ひと (人)", "hito", "Person / People (人)"),
        ("ひるごはん (昼ご飯)", "hirugohan", "Lunch (午餐)"),
        ("ひだり (左)", "hidari", "Left side (左边)"),
        ("ひがし (東)", "higashi", "East (东面/东口)"),
        ("ひろい (広い)", "hiroi", "Spacious (宽敞)"),
        ("ひとつ (一つ)", "hitotsu", "One item (一个)")
    ],
    "fu": [
        ("ふじさん (富士山)", "fujisan", "Mt. Fuji (富士山)"),
        ("ふくろ (袋)", "fukuro", "Plastic / Paper bag (袋子/购物袋)"),
        ("ふゆ (冬)", "fuyu", "Winter (冬天)"),
        ("ふね (船)", "fune", "Boat / Ship (轮船)"),
        ("ふたつ (二つ)", "futatsu", "Two items (两个)"),
        ("ふざいひょう (不在票)", "fuzaihyou", "Missed delivery slip (不在通知单)"),
        ("ふつう (普通)", "futsuu", "Local train / Normal (普通列车/平常)")
    ],
    "he": [
        ("へや (部屋)", "heya", "Room / Apartment (房间/宿舍)"),
        ("へんじ (返事)", "henji", "Reply / Answer (回复)"),
        ("へん (変)", "hen", "Strange / Unusual (奇怪)"),
        ("へいわ (平和)", "heiwa", "Peace (和平)"),
        ("へいき (平気)", "heiki", "All fine / No problem (没事/不在乎)"),
        ("へた (下手)", "heta", "Unskilled (不擅长)"),
        ("へる (減る)", "heru", "To decrease (减少)")
    ],
    "ho": [
        ("ほん (本)", "hon", "Book (书本)"),
        ("ホテル", "hoteru", "Hotel (酒店)"),
        ("ホーム", "hoomu", "Train platform (月台/站台)"),
        ("ほっかいどう (北海道)", "hokkaidou", "Hokkaido (北海道)"),
        ("ほし (星)", "hoshi", "Star (星星)"),
        ("ほしい (欲しい)", "hoshii", "Want / Desire (想要)"),
        ("ほんとう (本当)", "hontou", "Really / Truly (真的吗/真实)")
    ],

    # --- ま行 ---
    "ma": [
        ("まんが (漫画)", "manga", "Manga (漫画)"),
        ("まち (町)", "machi", "Town / City street (街道/城市)"),
        ("まつり (祭り)", "matsuri", "Festival (祭典/庙会)"),
        ("まど (窓)", "mado", "Window (窗户)"),
        ("まえ (前)", "mae", "Front / Before (前面)"),
        ("まぐろ (鮪)", "maguro", "Tuna fish (金枪鱼)"),
        ("まっすぐ", "massugu", "Straight ahead (一直走/笔直)")
    ],
    "mi": [
        ("みず (水)", "mizu", "Water / Chilled water (凉水/清水)"),
        ("みせ (店)", "mise", "Shop / Restaurant (店铺)"),
        ("みち (道)", "michi", "Road / Path (道路)"),
        ("みぎ (右)", "migi", "Right side (右边)"),
        ("みなみ (南)", "minami", "South (南面/南口)"),
        ("みんな", "minna", "Everyone (大家)"),
        ("みどり (緑)", "midori", "Green color (绿色)")
    ],
    "mu": [
        ("むりょう (無料)", "muryou", "Free of charge (免费)"),
        ("むずかしい (難しい)", "muzukashii", "Difficult (困难/复杂)"),
        ("むすめ (娘)", "musume", "Daughter (女儿)"),
        ("むかし (昔)", "mukashi", "Old times / Long ago (很久以前)"),
        ("むらさき (紫)", "murasaki", "Purple color (紫色)"),
        ("むし (虫)", "mushi", "Bug / Insect (昆虫)"),
        ("むかい (向かい)", "mukai", "Opposite side (正对面)")
    ],
    "me": [
        ("めがね (眼鏡)", "megane", "Glasses (眼镜)"),
        ("メニュー", "menyuu", "Menu (菜单)"),
        ("め (目)", "me", "Eye (眼睛)"),
        ("めいし (名刺)", "meishi", "Business card (名片)"),
        ("メール", "meeru", "Email (电子邮件)"),
        ("めずらしい (珍しい)", "mezurashii", "Rare / Unique (罕见/稀奇)"),
        ("めん (麺)", "men", "Noodles (面条)")
    ],
    "mo": [
        ("もういちど", "mou ichido", "Once more (请再说一次)"),
        ("もの (物)", "mono", "Thing / Object (物品)"),
        ("もちろん", "mochiron", "Of course (当然/自然)"),
        ("もり (森)", "mori", "Forest (森林)"),
        ("もん (門)", "mon", "Gate (大门)"),
        ("もんだい (問題)", "mondai", "Problem / Question (问题)"),
        ("もつ (持つ)", "motsu", "To carry / Hold (拿/持有)")
    ],

    # --- や行 ---
    "ya": [
        ("やま (山)", "yama", "Mountain (大山)"),
        ("やさい (野菜)", "yasai", "Vegetables (蔬菜)"),
        ("やすみ (休み)", "yasumi", "Holiday / Day off (休息/放假)"),
        ("やすい (安い)", "yasui", "Cheap / Inexpensive (便宜)"),
        ("やくそく (約束)", "yakusoku", "Promise / Appointment (约定)"),
        ("やきとり (焼き鳥)", "yakitori", "Grilled chicken skewer (烤鸡肉串)"),
        ("やさしい (優しい)", "yasashii", "Kind / Gentle / Easy (亲切/温柔)")
    ],
    "yu": [
        ("ゆめ (夢)", "yume", "Dream (梦想/梦境)"),
        ("ゆうがた (夕方)", "yuugata", "Early evening (傍晚)"),
        ("ゆうびんきょく (郵便局)", "yuubinkyoku", "Post office (邮局)"),
        ("ゆき (雪)", "yuki", "Snow (雪花)"),
        ("ゆかた (浴衣)", "yukata", "Summer kimono (浴衣)"),
        ("ゆび (指)", "yubi", "Finger (手指)"),
        ("ゆっくり", "yukkuri", "Slowly / Take your time (慢慢来/从容)")
    ],
    "yo": [
        ("よる (夜)", "yoru", "Night (夜晚)"),
        ("よやく (予約)", "yoyaku", "Reservation / Booking (预订/预约)"),
        ("ようこそ", "youkoso", "Welcome! (欢迎光临)"),
        ("よっつ (四つ)", "yottsu", "Four items (四个)"),
        ("よこ (横)", "yoko", "Beside / Horizontal (旁边/横向)"),
        ("よい (良い)", "yoi", "Good / Nice (好的)"),
        ("よむ (読む)", "yomu", "To read (阅读)")
    ],

    # --- ら行 ---
    "ra": [
        ("ラーメン", "raamen", "Ramen noodles (拉面)"),
        ("らいしゅう (来週)", "raishuu", "Next week (下周)"),
        ("ラジオ", "rajio", "Radio (收音机/广播)"),
        ("らいねん (来年)", "rainen", "Next year (明年)"),
        ("らく (楽)", "raku", "Easy / Comfortable (轻松/舒适)"),
        ("ライター", "raitaa", "Lighter (打火机)"),
        ("ランチ", "ranchi", "Lunch set (午市套餐)")
    ],
    "ri": [
        ("りんご (林檎)", "ringo", "Apple (苹果)"),
        ("りょうしゅうしょ (領収書)", "ryoushuusho", "Official Receipt (发票/收据)"),
        ("りょこう (旅行)", "ryokou", "Travel / Trip (旅游)"),
        ("りゆう (理由)", "riyuu", "Reason (理由/原因)"),
        ("りょうり (料理)", "ryouri", "Cuisine / Cooking (料理/菜肴)"),
        ("りゅうがくせい (留学生)", "ryuugakusei", "International student (留学生)"),
        ("リアル", "riaru", "Real / Authentic (真实/逼真)")
    ],
    "ru": [
        ("るすばん (留守番)", "rusuban", "House-sitting (看家)"),
        ("ルート", "ruuto", "Route / Navigation path (路线)"),
        ("ルール", "ruuru", "Rule / Etiquette (规则/规矩)"),
        ("ルーム", "ruumu", "Room (客房/房间)"),
        ("ルーズ", "ruuzu", "Loose / Relaxed (宽松)"),
        ("ルーレット", "ruuretto", "Roulette wheel (轮盘)"),
        ("ルーペ", "ruupe", "Magnifying glass (放大镜)")
    ],
    "re": [
        ("れっしゃ (列車)", "ressha", "Train (列车)"),
        ("レジ", "reji", "Cash register (收银台)"),
        ("レシート", "reshiito", "Store receipt (小票/收据)"),
        ("れんしゅう (練習)", "renshuu", "Practice (练习)"),
        ("レストラン", "resutoran", "Restaurant (西餐厅)"),
        ("れんらく (連絡)", "renraku", "Contact / Message (联络)"),
        ("れいぞうこ (冷蔵庫)", "reizouko", "Refrigerator (冰箱)")
    ],
    "ro": [
        ("ろうそく", "rousoku", "Candle (蜡烛)"),
        ("ろく (六)", "roku", "Number 6 (数字六)"),
        ("ロッカー", "rokkaa", "Coin locker (储物柜)"),
        ("ロビー", "robii", "Lobby (酒店大堂)"),
        ("ローカル", "rookaru", "Local (当地/本地)"),
        ("ロールケーキ", "roorukeeki", "Swiss roll cake (蛋糕卷)"),
        ("ろじうら (路地裏)", "rojiura", "Back alley (后巷/胡同)")
    ],

    # --- わ行・ん ---
    "wa": [
        ("わさび", "wasabi", "Wasabi (山葵/芥末)"),
        ("わたし (私)", "watashi", "I / Me (我)"),
        ("わかる (分かる)", "wakaru", "To understand (明白/理解)"),
        ("わすれもの (忘れ物)", "wasuremono", "Lost and found item (遗落物品)"),
        ("わりばし (割り箸)", "waribashi", "Disposable chopsticks (一次性筷子)"),
        ("わふう (和風)", "wafu", "Japanese style (日式风情)"),
        ("わらう (笑う)", "warau", "To laugh / Smile (笑/微笑)")
    ],
    "wo": [
        ("〜をください", "o kudasai", "Please give me... (请给我...)"),
        ("みずをのむ (水を飲む)", "mizu o nomu", "Drink water (喝水)"),
        ("きっぷをかう (切符を買う)", "kippu o kau", "Buy ticket (买车票)"),
        ("ドアをあける (ドアを開ける)", "doa o akeru", "Open door (开门)"),
        ("ほんをよむ (本を読む)", "hon o yomu", "Read book (看书)"),
        ("ごはんをたべる (ご飯を食べる)", "gohan o taberu", "Eat meal (吃饭)"),
        ("しゃしんをとる (写真を撮る)", "shashin o toru", "Take photo (拍照)")
    ],
    "n": [
        ("にほん (日本)", "nihon", "Japan (日本)"),
        ("しんかんせん (新幹線)", "shinkansen", "Bullet train (新干线)"),
        ("かんぱい (乾杯)", "kanpai", "Cheers! (干杯)"),
        ("ぜんぶ (全部)", "zenbu", "All of it (全部)"),
        ("ほん (本)", "hon", "Book (书本)"),
        ("でんしゃ (電車)", "densha", "Train (电车)"),
        ("ラーメン", "raamen", "Ramen (拉面)")
    ],

    # --- 浊音 / 半浊音 ---
    "ga": [
        ("がっこう (学校)", "gakkou", "School (学校)"),
        ("外国 (がいこく)", "gaikoku", "Foreign country (外国)"),
        ("がんばって (頑張って)", "ganbatte", "Do your best! (加油)"),
        ("がいこくご (外国語)", "gaikokugo", "Foreign language (外语)"),
        ("がくせい (学生)", "gakusei", "Student (学生)"),
        ("がめん (画面)", "gamen", "Screen / Display (屏幕)"),
        ("がっか (学科)", "gakka", "Department / Subject (学科)")
    ],
    "gi": [
        ("ぎゅうどん (牛丼)", "gyuudon", "Beef bowl (牛肉饭)"),
        ("ぎんざ (銀座)", "ginza", "Ginza district (银座)"),
        ("ぎんこう (銀行)", "ginkou", "Bank (银行)"),
        ("ぎゅうにゅう (牛乳)", "gyuunyuu", "Milk (牛奶)"),
        ("ぎょうざ (餃子)", "gyouza", "Gyoza dumplings (煎饺/饺子)"),
        ("ぎじゅつ (技術)", "gijutsu", "Technology / Technique (技术)"),
        ("ギター", "gitaa", "Guitar (吉他)")
    ],
    "gu": [
        ("ぐんま (群馬)", "gunma", "Gunma (群马)"),
        ("グラス", "gurasu", "Drinking glass (玻璃杯)"),
        ("ぐあい (具合)", "guai", "Physical condition (健康状态)"),
        ("グループ", "guruupu", "Group (小组/团队)"),
        ("軍手 (ぐんて)", "gunte", "Cotton work gloves (劳保手套)"),
        ("グルメ", "gurume", "Gourmet food (美食)"),
        ("ぐんかん (軍艦巻き)", "gunkan", "Battleship sushi (军舰卷寿司)")
    ],
    "ge": [
        ("げんき (元気)", "genki", "Energetic / Well (有精神/健康)"),
        ("げんかん (玄関)", "genkan", "Entryway / Foyer (玄关)"),
        ("ゲーム", "geemu", "Game / Video game (游戏)"),
        ("げきじょう (劇場)", "gekijou", "Theater (剧场)"),
        ("げつようび (月曜日)", "getsuyoubi", "Monday (周一)"),
        ("げんざい (現在)", "genzai", "Present / Current time (现在)"),
        ("げんきん (現金)", "genkin", "Cash payment (现金)")
    ],
    "go": [
        ("ごはん (ご飯)", "gohan", "Rice / Meal (米饭/饭)"),
        ("ごご (午後)", "gogo", "Afternoon (下午)"),
        ("ごぜん (午前)", "gozen", "Morning (上午)"),
        ("ごみ (ゴミ)", "gomi", "Trash / Garbage (垃圾)"),
        ("ごちそうさま", "gochisousama", "Thank you for the meal (多谢款待)"),
        ("ごうけい (合計)", "goukei", "Total sum (合计)"),
        ("ごめんなさい", "gomennasai", "I'm sorry (对不起)")
    ],
    "za": [
        ("ざっし (雑誌)", "zasshi", "Magazine (杂志)"),
        ("ざぶとん (座布団)", "zabuton", "Floor cushion (坐垫)"),
        ("ざんねん (残念)", "zannen", "Regrettable / What a pity (可惜/遗憾)"),
        ("ざるそば", "zarusoba", "Chilled soba on bamboo (竹笼荞麦面)"),
        ("ざいりょう (材料)", "zairyou", "Ingredients / Material (材料/食材)"),
        ("ざっか (雑貨)", "zakka", "Sundries / Daily goods (杂货/文创)"),
        ("ざんぎょう (残業)", "zangyou", "Overtime work (加班)")
    ],
    "ji": [
        ("じかん (時間)", "jikan", "Time / Hour (时间)"),
        ("じどうはんばいき (自動販売機)", "jidouhanbaiki", "Vending machine (自动售货机)"),
        ("じゆう (自由)", "jiyuu", "Freedom / Free choice (自由)"),
        ("じこ (事故)", "jiko", "Accident (事故)"),
        ("じしょ (辞書)", "jisho", "Dictionary (字典)"),
        ("じゅうしょ (住所)", "juusho", "Address (住址)"),
        ("じゅんび (準備)", "junbi", "Preparation (准备)")
    ],
    "zu": [
        ("ずっと", "zutto", "All the time / By far (一直/非常)"),
        ("ずかん (図鑑)", "zukan", "Illustrated encyclopedia (图鉴/图册)"),
        ("ずぼん (ズボン)", "zubon", "Trousers / Pants (裤子)"),
        ("ずけい (図形)", "zukei", "Graphic figure (图形)"),
        ("ずじょう (頭上)", "zujou", "Overhead (头顶上方)"),
        ("ずるい", "zurui", "Sly / Unfair (狡猾/狡黠)"),
        ("ずし (逗子)", "zushi", "Zushi Beach (逗子海滩)")
    ],
    "ze": [
        ("ぜんぶ (全部)", "zenbu", "Everything / All (全部)"),
        ("ぜいこみ (税込)", "zeikomi", "Tax included (含税价)"),
        ("ぜったい (絶対)", "zettai", "Absolutely / Definitely (绝对)"),
        ("ぜんぜん (全然)", "zenzen", "Not at all (完全不)"),
        ("ぜひ (是非)", "zehi", "By all means / Please do (务必/一定)"),
        ("ゼロ", "zero", "Zero (零)"),
        ("ぜんこく (全国)", "zenkoku", "Nationwide (全国)")
    ],
    "zo": [
        ("ぞう (象)", "zou", "Elephant (大象)"),
        ("ぞくぞく", "zokuzoku", "Thrilled / Shivering (阵阵发抖/兴奋)"),
        ("ぞうきん (雑巾)", "zoukin", "Cleaning rag (抹布)"),
        ("ぞくへん (続編)", "zokuhen", "Sequel chapter (续集)"),
        ("ゾーン", "zoon", "Zone / Area (区域)"),
        ("ぞうしき (雑色)", "zoushiki", "Mixed colors (杂色)"),
        ("ぞうぜい (増税)", "zouzei", "Tax hike (增税)")
    ],
    "da": [
        ("だいじょうぶ (大丈夫)", "daijoubu", "All right / OK (没问题)"),
        ("だいがく (大学)", "daigaku", "University (大学)"),
        ("だんせい (男性)", "dansei", "Male / Gentlemen (男士)"),
        ("だれ (誰)", "dare", "Who? (谁)"),
        ("だんだん", "dandan", "Gradually (渐渐/逐步)"),
        ("だいどころ (台所)", "daidokoro", "Kitchen (厨房)"),
        ("ダイヤ", "daiya", "Train timetable (列车运行图)")
    ],
    "de": [
        ("でんしゃ (電車)", "densha", "Train (电车)"),
        ("でぐち (出口)", "deguchi", "Exit (出口)"),
        ("でんわ (電話)", "denwa", "Telephone (电话)"),
        ("デザート", "dezaato", "Dessert (甜点)"),
        ("デパート", "depaato", "Department store (百货商场)"),
        ("できる (出来る)", "dekiru", "Can do / Possible (能够/可以)"),
        ("デート", "deeto", "Date / Romance (约会)")
    ],
    "do": [
        ("どこ (何処)", "doko", "Where? (哪里)"),
        ("どうも", "doumo", "Thanks / Hello (多谢/你好)"),
        ("どようび (土曜日)", "doyoubi", "Saturday (周六)"),
        ("ドア", "doa", "Door (车门/房间门)"),
        ("どうぶつ (動物)", "doubutsu", "Animal (动物)"),
        ("どれ", "dore", "Which one? (哪一个)"),
        ("どうして", "doushite", "Why? (为什么)")
    ],
    "ba": [
        ("ばしょ (場所)", "basho", "Place / Location (场所/地点)"),
        ("バス", "basu", "Bus (公交车/巴士)"),
        ("ばあい (場合)", "baai", "Case / Situation (情况)"),
        ("ばんごはん (晩ご飯)", "bangohan", "Dinner (晚餐)"),
        ("ばっぐ (バッグ)", "baggu", "Bag (包)"),
        ("ばくだん (爆弾)", "bakudan", "Bomb / Special onigiri (炸弹饭团)"),
        ("ばいきん (バイキン)", "baikin", "Germs (细菌)")
    ],
    "bi": [
        ("ビール", "biiru", "Beer (啤酒)"),
        ("ビル", "biru", "Building / High-rise (大楼/大厦)"),
        ("びじゅつかん (美術館)", "bijutsukan", "Art Museum (美术馆)"),
        ("びょういん (病院)", "byouin", "Hospital (医院)"),
        ("びっくり", "bikkuri", "Surprised (吃惊/吓一跳)"),
        ("びよういん (美容院)", "biyouin", "Hair salon (美发店)"),
        ("ビニールぶくろ (ビニール袋)", "biniirubukuro", "Plastic shopping bag (塑料袋)")
    ],
    "bu": [
        ("ぶんか (文化)", "bunka", "Culture (文化)"),
        ("ぶたにく (豚肉)", "butaniku", "Pork (猪肉)"),
        ("ぶどう (葡萄)", "budou", "Grape (葡萄)"),
        ("ぶちょう (部長)", "buchou", "Department Manager (部长/主管)"),
        ("ぶらぶら", "burabura", "Strolling around (闲逛/溜达)"),
        ("ぶぶん (部分)", "bubun", "Part / Section (部分)"),
        ("ぶっか (物価)", "bukka", "Cost of living (物价)")
    ],
    "be": [
        ("べんり (便利)", "benri", "Convenient (方便/便利)"),
        ("べんとう (弁当)", "bentou", "Bento boxed lunch (便当)"),
        ("ベッド", "beddo", "Bed (床)"),
        ("べつ (別)", "betsu", "Separate / Different (分开/另外)"),
        ("べんきょう (勉強)", "benkyou", "Studying (学习)"),
        ("ベル", "beru", "Bell / Chime (门铃/铃声)"),
        ("べろ (舌)", "bero", "Tongue (舌头)")
    ],
    "bo": [
        ("ぼく (僕)", "boku", "I / Me (我)"),
        ("ぼうし (帽子)", "boushi", "Hat / Cap (帽子)"),
        ("ボタン", "botan", "Button (按钮/纽扣)"),
        ("ボールペン", "boorupen", "Ballpoint pen (圆珠笔)"),
        ("ぼうけん (冒険)", "bouken", "Adventure (冒险)"),
        ("ボトル", "botoru", "Bottle (瓶子)"),
        ("ぼんさい (盆栽)", "bonsai", "Bonsai miniature tree (盆栽)")
    ],
    "pa": [
        ("パン", "pan", "Bread / Pastry (面包)"),
        ("パスポート", "pasupooto", "Passport (护照)"),
        ("パトカー", "patokaa", "Police patrol car (警车)"),
        ("パスタ", "pasuta", "Pasta (意面)"),
        ("パーティー", "paatii", "Party (派对/聚会)"),
        ("パソコン", "pasokon", "Personal Computer (电脑/笔记本)"),
        ("パーク", "paaku", "Park / Theme park (公园/乐园)")
    ],
    "pi": [
        ("ピンク", "pinku", "Pink color (粉色)"),
        ("ピアノ", "piano", "Piano (钢琴)"),
        ("ピザ", "piza", "Pizza (披萨)"),
        ("ビル (ピル)", "piru", "Pill (药片)"),
        ("ピクニック", "pikunikku", "Picnic (野餐)"),
        ("ピンポン", "pinpon", "Door chime / Table tennis (门铃/乒乓)"),
        ("ピース", "piisu", "Peace sign (和平手势/一块)")
    ],
    "pu": [
        ("プリン", "purin", "Caramel pudding (焦糖布丁)"),
        ("プレゼント", "purezento", "Present / Gift (礼物)"),
        ("プール", "puuru", "Swimming pool (游泳池)"),
        ("プロ", "puro", "Professional (专业人士)"),
        ("プラスチック", "purasuchikku", "Plastic (塑料制品)"),
        ("プラン", "puran", "Plan / Strategy (计划)"),
        ("プレート", "pureeto", "Plate / Platter (餐盘/招牌)")
    ],
    "pe": [
        ("ペン", "pen", "Pen / Marker (笔/钢笔)"),
        ("ペットボトル", "pettobotoru", "PET plastic bottle (塑料饮料瓶)"),
        ("ページ", "peeji", "Page (页面/页码)"),
        ("ペア", "pea", "Pair / Couple (一对/双人)"),
        ("ペーパー", "peepaa", "Paper / Napkin (纸张/纸巾)"),
        ("ペコペコ", "pekopeko", "Starving hungry (肚子饿得咕咕叫)"),
        ("ペイント", "peinto", "Paint (油漆/绘画)")
    ],
    "po": [
        ("ポスト", "posuto", "Postbox / Mailbox (邮筒/邮箱)"),
        ("ポテト", "poteto", "French fries / Potato (薯条/土豆)"),
        ("ポケット", "poketto", "Pocket (口袋)"),
        ("ポイント", "pointo", "Points / Reward points (积分/要点)"),
        ("ポスター", "posutaa", "Poster (海报)"),
        ("ポップコーン", "poppukoon", "Popcorn (爆米花)"),
        ("ポリス", "porisu", "Police (警察)")
    ],

    # --- 拗音 Yoon ---
    "kya": [
        ("きゃく (客)", "kyaku", "Customer / Guest (客人)"),
        ("キャベツ", "kyabetsu", "Cabbage (卷心菜)"),
        ("キャンプ", "kyanpu", "Camping (露营)"),
        ("キャンディー", "kyandii", "Candy (糖果)"),
        ("キャッシャー", "kyasshaa", "Cashier counter (收银台)"),
        ("キャラ", "kyara", "Character / Anime figure (角色)"),
        ("キャンセル", "kyanseru", "Cancellation (取消/退订)")
    ],
    "kyu": [
        ("きゅうこう (急行)", "kyuukou", "Express train (急行列车)"),
        ("きゅうり (胡瓜)", "kyuuri", "Cucumber (黄瓜)"),
        ("きゅうけい (休憩)", "kyuukei", "Break / Rest (休息)"),
        ("きゅうじつ (休日)", "kyuujitsu", "Day off / Holiday (休假日)"),
        ("きゅうしゅう (九州)", "kyuushuu", "Kyushu (九州)"),
        ("きゅうきゅうしゃ (救急車)", "kyuukyuusha", "Ambulance (救护车)"),
        ("きゅうりょう (給料)", "kyuuryou", "Salary / Paycheck (薪水/工资)")
    ],
    "kyo": [
        ("きょう (今日)", "kyou", "Today (今天)"),
        ("きょうと (京都)", "kyouto", "Kyoto (京都)"),
        ("きょうしつ (教室)", "kyoushitsu", "Classroom (教室)"),
        ("きょうみ (興味)", "kyoumi", "Interest / Curiosity (兴趣)"),
        ("きょり (距離)", "kyori", "Distance (距离)"),
        ("きょねん (去年)", "kyonen", "Last year (去年)"),
        ("きょうりょく (協力)", "kyouryoku", "Cooperation (协助/合作)")
    ],
    "sha": [
        ("しゃしん (写真)", "shashin", "Photo (照片)"),
        ("しゃちょう (社長)", "shachou", "Company President (社长/总经理)"),
        ("しゃかい (社会)", "shakai", "Society (社会)"),
        ("シャワー", "shawaa", "Shower (淋浴)"),
        ("しゃせん (車線)", "shasen", "Traffic lane (车道)"),
        ("シャツ", "shatsu", "Shirt (衬衫)"),
        ("しゃりん (車輪)", "sharin", "Wheel (车轮)")
    ],
    "shu": [
        ("しゅうでん (終電)", "shuuden", "Last train (末班车)"),
        ("しゅくだい (宿題)", "shukudai", "Homework (作业)"),
        ("しゅみ (趣味)", "shumi", "Hobby (爱好)"),
        ("しゅうかん (週間)", "shuukan", "Week / Weekly (周/星期)"),
        ("しゅうまつ (週末)", "shuumatsu", "Weekend (周末)"),
        ("しゅっぱつ (出発)", "shuppatsu", "Departure (出发)"),
        ("しゅるい (種類)", "shurui", "Type / Variety (种类)")
    ],
    "sho": [
        ("しょうひん (商品)", "shouhin", "Merchandise / Goods (商品)"),
        ("しょうゆ (醤油)", "shouyu", "Soy sauce (酱油)"),
        ("しょうしょう (少々)", "shoushou", "A moment please (请稍候)"),
        ("しょくどう (食堂)", "shokudou", "Dining hall / Canteen (食堂)"),
        ("しょくじ (食事)", "shokuji", "Meal (用餐)"),
        ("ショップ", "shoppu", "Shop / Store (商店)"),
        ("しょうてんがい (商店街)", "shoutengai", "Shopping street (商业街)")
    ],
    "cha": [
        ("おちゃ (お茶)", "ocha", "Green tea (绿茶/茶水)"),
        ("ちゃわん (茶碗)", "chawan", "Rice bowl / Teacup (饭碗/茶碗)"),
        ("チャンス", "chansu", "Opportunity / Chance (机会)"),
        ("ちゃいろ (茶色)", "chairo", "Brown color (茶色/棕色)"),
        ("チャージ (チャージ)", "chaaji", "Recharge IC card (充值)"),
        ("チャーハン", "chaahan", "Fried rice (炒饭)"),
        ("チャーシュー", "chaashuu", "Chashu pork (叉烧肉)")
    ],
    "chu": [
        ("ちゅうもん (注文)", "chuumon", "Food order (点单/订购)"),
        ("ちゅうしゃじょう (駐車場)", "chuushajou", "Parking lot (停车场)"),
        ("ちゅうごく (中国)", "chuugoku", "China (中国)"),
        ("ちゅうい (注意)", "chuui", "Caution / Attention (注意)"),
        ("ちゅうか (中華)", "chuuka", "Chinese cuisine (中华料理)"),
        ("ちゅうし (中止)", "chuushi", "Suspension / Cancelled (停运/中止)"),
        ("ちゅうしゃ (注射)", "chuusha", "Injection (打针)")
    ],
    "cho": [
        ("ちょっと", "chotto", "A moment / A little (稍等/稍微)"),
        ("ちょうど (丁度)", "choudo", "Exactly / Just right (正好/恰好)"),
        ("ちょうしょく (朝食)", "choushoku", "Breakfast (早餐)"),
        ("チョコ", "choko", "Chocolate (巧克力)"),
        ("ちょうさ (調査)", "chousa", "Survey / Investigation (调查)"),
        ("ちょうみりょう (調味料)", "choumiryou", "Seasoning / Condiment (调味料)"),
        ("ちょうじょう (頂上)", "choujou", "Summit / Mountaintop (山顶)")
    ],
    "nya": [
        ("にゃんこ", "nyanko", "Kitty cat (猫咪)"),
        ("ニャーニャー", "nyaanyaa", "Meow meow sound (喵喵叫)"),
        ("にゃんダフル", "nyandaful", "Meow-nderful (妙极了)"),
        ("こねこ (子猫)", "koneko", "Kitten (小猫)"),
        ("にゃんこカフェ", "nyanko kafe", "Cat cafe (猫咪咖啡馆)"),
        ("にゃんこせんせい", "nyanko sensei", "Master Nyanko (猫咪老师)"),
        ("にゃんの手", "nyan no te", "Cat's helping paw (猫咪借力/帮忙)")
    ],
    "ryo": [
        ("りょうしゅうしょ (領収書)", "ryoushuusho", "Official receipt (发票/收据)"),
        ("りょこう (旅行)", "ryokou", "Travel / Journey (旅游/旅行)"),
        ("りょうり (料理)", "ryouri", "Cooking / Cuisine (料理/菜肴)"),
        ("りょうきん (料金)", "ryoukin", "Fee / Fare (车费/费用)"),
        ("りょうがえ (両替)", "ryougae", "Currency exchange (兑换外币)"),
        ("りょう (量)", "ryou", "Quantity / Portion (份量)"),
        ("りょかん (旅館)", "ryokan", "Traditional Ryokan inn (日式旅馆)")
    ]
}

print(f"Loaded {len(kana_7day_dict)} Kana word sets with 7 days of non-repeating words.")
