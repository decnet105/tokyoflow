#!/usr/bin/env python3
"""
scripts/enrich_scenarios_chinese.py
Adds complete, authentic Chinese fields (contextZh, culturalTipZh, jfCanDoDescriptionZh, 
keyVocabulary[].meaningZh, interactiveChallenge.promptZh, interactiveOption[].explanationZh, titleZh)
to all 11 scenarios in TokyoFlow/Resources/scenarios.json.
"""

import json

SCENARIOS_PATH = "TokyoFlow/Resources/scenarios.json"

CHINESE_SCENARIO_DATA = {
    "scenario_01_morning_train": {
        "titleZh": "早高峰山手线：车票与Suica西瓜卡通勤",
        "jfCanDoDescriptionZh": "能够购买电车车票、为IC交通卡充值，并向车站站务员询问站台方向。",
        "contextZh": "你在早高峰时段抵达新宿站。你需要为Suica卡充值，并找到前往涩谷方向的山手线站台。",
        "culturalTipZh": "在东京检票闸机，请将Suica/Pasmo轻触右侧感应区。若闸机发出蜂鸣并关闸，请移步至人工窗口（精算所 / 改札窓口）说明「タッチできませんでした」（刚才没刷上）。",
        "promptZh": "你在自动售票机前，想用10,000日元纸币充值2,000日元，并需要打印收据。",
        "optionExplanationsZh": [
            "自然且礼貌：明确充值金额并请求开具收据（領収書 ryōshūsho）。",
            "过于随意且表达模糊，不适用于对客服人员或正式场合。",
            "这是在要求购买单程实体车票，而非为Suica充值。"
        ],
        "vocabMeaningZh": [
            "几号站台",
            "上（楼梯/台阶）",
            "充值（给IC交通卡充钱）",
            "自动售票机",
            "按下（按钮）"
        ]
    },
    "scenario_02_kombini_morning": {
        "titleZh": "便利店清晨：便当加热、购物袋与支付全流程",
        "jfCanDoDescriptionZh": "能够应对日本便利店结账时的连环提问（便当加热、袋子、积分卡），并完成无现金或现金支付。",
        "contextZh": "早上在涉谷的7-Eleven购买便当、饮料和咖啡。店员语速极快地提出一系列结账问题。",
        "culturalTipZh": "日本便利店塑料袋收费。如不需要袋子，微笑并点头说「大丈夫です」或「このままでいいです」即可；若需要袋子则说「袋（ふくろ）お願いします」。",
        "promptZh": "店员询问你便当是否需要加热，以及是否需要塑料袋，你希望加热便当但不需要袋子。",
        "optionExplanationsZh": [
            "完美回答：简洁明确地请求加热并礼貌拒绝塑料袋。",
            "语法生硬且意思不明确，店员可能无法确认是否要加热。",
            "表达过于粗鲁，不符合便利店对话礼仪。"
        ],
        "vocabMeaningZh": [
            "加热（微波炉加热）",
            "购物塑料袋",
            "没关系 / 不需要",
            "收银台 / 结账",
            "积分卡"
        ]
    },
    "scenario_03_ramen_ticket_machine": {
        "titleZh": "拉面店食券机与“面条硬度/汤头浓度”定制",
        "jfCanDoDescriptionZh": "能够使用拉面店自动食券机选餐，并向店员准确表达面条硬度、汤头浓度和配料需求。",
        "contextZh": "来到新宿歌舞伎町附近的人气拉面店。进门先在食券机购买食券，入座后店员询问你的口味偏好（お好み）。",
        "culturalTipZh": "吃拉面时发出吸溜声在日本被视作是对厨师厨艺的赞赏与享受；在吧台就座后，将食券放在抬高的台面上（カウンター上）即可。",
        "promptZh": "店员询问你的面条喜好，你希望面条偏硬（硬め）、味道偏浓（濃いめ）。",
        "optionExplanationsZh": [
            "地道且专业：精准使用拉面定制术语「麺硬め、味濃いめ」。",
            "表达不符合拉面店惯用术语，容易引起误解。",
            "没有表达出定制要求，只是泛泛要求做拉面。"
        ],
        "vocabMeaningZh": [
            "食券机",
            "硬度（面条）",
            "浓郁（汤头）",
            "大份（加量）",
            "替玉（加面）"
        ]
    },
    "scenario_04_izakaya_table_booking": {
        "titleZh": "居酒屋之夜：入座点餐、先来杯生啤与AA制结账",
        "jfCanDoDescriptionZh": "能够在居酒屋完成点单（「先来杯生啤！」）、理解前菜（お通し）文化并要求分开结账。",
        "contextZh": "周五晚与朋友前往新宿回忆横丁的居酒屋。你需要入座、先点饮品、随后加点烤串，并在最后结账。",
        "culturalTipZh": "在日本居酒屋，入座第一件事通常是先点酒水饮料（通常是「とりあえず生」先来杯生啤酒）；随后端上来的小菜叫「お通し」（收取座位费）。",
        "promptZh": "入座后你想先为两个人各点一杯生啤酒，并询问推荐烤串。",
        "optionExplanationsZh": [
            "地道居酒屋开场句：先点两杯生啤并咨询招牌推荐。",
            "用词不自然，居酒屋一般不这么点单。",
            "缺少对推荐菜品的询问，且表达不够自然。"
        ],
        "vocabMeaningZh": [
            "先来…（居酒屋惯用语）",
            "生啤酒",
            "小菜 / 座位费前菜",
            "结账 / 买单",
            "AA制 / 各自平摊"
        ]
    },
    "scenario_05_docomo_bike_rental": {
        "titleZh": "东京城市出行：Docomo小红车与LUUP滑板车租赁",
        "jfCanDoDescriptionZh": "能够理解共享单车/滑板车解锁说明、按键操作并向客服或附近路人询问还车点。",
        "contextZh": "在六本木准备骑乘Docomo红色共享单车前往表参道，需要确认密码锁解锁流程与还车桩位置。",
        "culturalTipZh": "东京自行车不能随意随地停放，必须停在指定的Port（驻轮场），违规停放会被拖走并面临罚款。",
        "promptZh": "你想询问路人附近哪里有可还车的Docomo共享单车站桩。",
        "optionExplanationsZh": [
            "地道礼貌：使用「ポート（Port）」询问最近的还车站桩位置。",
            "「自転車の家」不是地道日语表达，容易让人困惑。",
            "问法过于生硬直接，缺乏日常礼貌用语。"
        ],
        "vocabMeaningZh": [
            "共享单车",
            "驻轮场 / 还车站桩",
            "解锁 / 密码输入",
            "电量剩余",
            "返还 / 还车"
        ]
    },
    "scenario_06_department_store_taxfree": {
        "titleZh": "银座百货：试穿、尺寸确认与退税柜台办理",
        "jfCanDoDescriptionZh": "能够在商场专柜提出试穿需求、询问其他尺码与颜色，并前往退税柜台办理免税。",
        "contextZh": "在银座百货商店挑选衣服，需要试穿并向店员询问大一号的尺码，最后办理Tax-Free免税。",
        "culturalTipZh": "在日本服装店进入试衣间前必须脱鞋；女士试穿套头衣物时，店员会提供面罩（Face Cover）以防粉底沾染衣物。",
        "promptZh": "你试穿后觉得稍微有点小，想询问店员有没有大一号的尺码。",
        "optionExplanationsZh": [
            "标准且地道的专柜表达：「ワンサイズ上（大一号）はありますか？」。",
            "表达生硬，非地道服装店习惯用语。",
            "只说太小，但没有明确提出需要大一号尺码。"
        ],
        "vocabMeaningZh": [
            "试穿（可以试穿吗）",
            "大一号尺寸",
            "试衣间",
            "免税（Tax-Free）",
            "退税柜台"
        ]
    },
    "scenario_07_post_office_delivery": {
        "titleZh": "东京生活实务：不在票再配送申请与邮局窗口取件",
        "jfCanDoDescriptionZh": "能够看懂日本邮便/宅急便的不在联络票（不在票），完成网上/电话再配送预约或去窗口自取。",
        "contextZh": "回到家在信箱发现了日本邮便的「ご不在連絡票」。你需要看懂追踪号码并安排明天晚上重新配送。",
        "culturalTipZh": "日本快递如果家中无人会留下「不在票」，上面有QR码和电话，当天一定时间前预约可享受当晚二次免费送达。",
        "promptZh": "你在电话自动语音或窗口中指定希望在明天晚上19点到21点之间重新配送。",
        "optionExplanationsZh": [
            "清晰标准的指定送达时间段表达：「明日の19時から21時の間」。",
            "时间表达不精准，容易导致快递员无法确认具体送货区间。",
            "只说了明天，未包含晚间时间段要求。"
        ],
        "vocabMeaningZh": [
            "不在联络票（快递未妥投通知）",
            "再配送（重新送货）",
            "包裹追踪单号",
            "指定送达时间段",
            "本人确认证件（窗口取件用）"
        ]
    },
    "scenario_08_gyudon_fastfood": {
        "titleZh": "牛丼屋点餐暗号：多汁(つゆだく)、多葱与生生鸡蛋套餐",
        "jfCanDoDescriptionZh": "能够在吉野家、松屋、Sukiya自如使用经典点餐术语（汁多、葱多、肉大碗）并搭配套餐。",
        "contextZh": "深夜在吉野家吧台就座，准备快速享用一顿地道牛丼套餐。你需要用行话准确提出自己的定制需求。",
        "culturalTipZh": "牛丼店常见术语：つゆだく（多汤汁）、ねぎだく（多洋葱）、あたまの大盛り（只要肉加量米饭普通）。生鸡蛋通常会打在小碗里加少许酱油搅拌后再淋在牛肉上。",
        "promptZh": "你想点一份中碗牛丼，要求多放汤汁（汁多），并加一份生鸡蛋和味噌汤套餐。",
        "optionExplanationsZh": [
            "完美行话搭配：「牛丼並盛り、つゆだくで、卵セットをお願いします」。",
            "没有使用「つゆだく」标准术语，店员可能无法精确掌握汤汁量。",
            "表达模糊，缺少中碗（並盛り）和套餐具体名称。"
        ],
        "vocabMeaningZh": [
            "中碗（普通分量）",
            "多加汤汁（牛丼术语）",
            "生鸡蛋",
            "味噌汤",
            "肉加量（饭量正常）"
        ]
    },
    "scenario_09_supermarket_halfprice": {
        "titleZh": "东京超市之夜：晚上8点半价（半額）抢购与熟食结算",
        "jfCanDoDescriptionZh": "能够看懂超市熟食区降价打折标签（20% OFF、半额），并在收银台正确结算。",
        "contextZh": "晚上8点走进住处附近的Life或AEON超市。熟食区店员正在给便当、刺身贴半价（半額）贴纸。",
        "culturalTipZh": "日本超市通常在闭店前2-3小时开始贴打折贴纸（割引シール），从「20円引」、「2割引(20% off)」直到最受欢迎的「半額(50% off)」。贴纸刚贴上即可拿取。",
        "promptZh": "你在熟食区看到店员正在贴标签，想确认手里的刺身拼盘是否也可以贴半价标签。",
        "optionExplanationsZh": [
            "礼貌且得体地向店员确认是否能贴半价标签：「こちらも半額シール貼っていただけますか？」。",
            "态度过于强硬，容易显得不够礼貌。",
            "问法含糊不清，未指明商品。"
        ],
        "vocabMeaningZh": [
            "半价（5折）",
            "打折 / 折扣（如2割引=8折）",
            "贴纸（降价贴纸）",
            "熟食（便当炸物等）",
            "保质期限 / 赏味期限"
        ]
    },
    "scenario_10_drugstore_medicine": {
        "titleZh": "药妆店买药：购买止痛药(EVE)与向药剂师描述症状",
        "jfCanDoDescriptionZh": "能够在Matsukiyo或Sundrug向药剂师或店员说明头痛、发热、胃痛症状，并选购对应常备药。",
        "contextZh": "因感冒头痛前往药妆店购买EVE止痛药或感冒颗粒（Pabron）。需要向店员描述具体症状并确认服用方法。",
        "culturalTipZh": "日本药妆店药品分为第1类、第2类、第3类。第1类（如强效止痛药洛索洛芬Loxonin）必须由执业药剂师（薬剤師）在场说明后方可购买。",
        "promptZh": "你向店员说明自己从昨晚开始头痛并且有点低烧，想买不瞌睡的止痛感冒药。",
        "optionExplanationsZh": [
            "详尽地道：准确描述头痛发热症状，并明确提出「眠くならない（不嗜睡）」的要求。",
            "缺少对不嗜睡药性的说明，店员可能会推荐容易犯困的强效感冒药。",
            "表达过于笼统，只说了身体不舒服。"
        ],
        "vocabMeaningZh": [
            "头痛",
            "发烧 / 发热",
            "止痛药",
            "不瞌睡 / 不嗜睡",
            "饭后服用"
        ]
    },
    "scenario_11_onsen_sento_etiquette": {
        "titleZh": "钱汤与温泉极意：淋浴冲洗礼仪、毛巾严禁入池与入浴规矩",
        "jfCanDoDescriptionZh": "能够看懂温泉/钱汤的入浴守则，并在前台购买入浴券、租借毛巾，严格遵守日本公共澡堂礼仪。",
        "contextZh": "体验东京下町的传统钱汤。在前台（番台）购买入浴券、租借小毛巾，并进入更衣室与浴室。",
        "culturalTipZh": "三大温泉铁律：1. 入池前必须在冲洗区（洗い場）彻底洗净身体；2. 毛巾严禁泡入浴池（可顶在头上或放池边）；3. 擦干身体后再返回更衣室。",
        "promptZh": "在前台你想购买成人入浴券，并租一条小毛巾和洗发水小样。",
        "optionExplanationsZh": [
            "地道钱汤点单：入浴券、毛巾与洗发水一并完整表达。",
            "用词不专业，钱汤一般不说「お風呂の切符」。",
            "遗漏了毛巾和洗发水的租借需求。"
        ],
        "vocabMeaningZh": [
            "入浴券",
            "冲洗水（入池前冲洗）",
            "冲洗区（坐着洗澡的地方）",
            "更衣室（脱衣所）",
            "温泉浴池"
        ]
    }
}

def main():
    print("Loading scenarios.json...")
    with open(SCENARIOS_PATH, "r", encoding="utf-8") as f:
        scenarios = json.load(f)

    print(f"Total scenarios: {len(scenarios)}")

    for s in scenarios:
        s_id = s.get("id", "")
        if s_id in CHINESE_SCENARIO_DATA:
            c_data = CHINESE_SCENARIO_DATA[s_id]
            s["titleZh"] = c_data["titleZh"]
            s["jfCanDoDescriptionZh"] = c_data["jfCanDoDescriptionZh"]
            s["contextZh"] = c_data["contextZh"]
            s["culturalTipZh"] = c_data["culturalTipZh"]

            if "interactiveChallenge" in s and s["interactiveChallenge"]:
                s["interactiveChallenge"]["promptZh"] = c_data["promptZh"]
                options = s["interactiveChallenge"].get("options", [])
                for idx, opt in enumerate(options):
                    if idx < len(c_data["optionExplanationsZh"]):
                        opt["explanationZh"] = c_data["optionExplanationsZh"][idx]

            vocab_list = s.get("keyVocabulary", [])
            for idx, v in enumerate(vocab_list):
                if idx < len(c_data["vocabMeaningZh"]):
                    v["meaningZh"] = c_data["vocabMeaningZh"][idx]

    with open(SCENARIOS_PATH, "w", encoding="utf-8") as f:
        json.dump(scenarios, f, ensure_ascii=False, indent=2)

    print("✅ Successfully enriched scenarios.json with 100% authentic Chinese content!")

if __name__ == "__main__":
    main()
