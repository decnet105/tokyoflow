#!/usr/bin/env python3
"""
TokyoFlow Japanese • Multi-Language (i18n) Framework & Locale Registry
======================================================================
Defines localized pedagogical voices, UI strings, visual badge labels,
and CTA templates to enable seamless multi-native-language video generation.
"""

LOCALES = {
    "en": {
        "code": "en",
        "name": "English",
        "explainer_voice": "en-US-AndrewNeural",
        "explainer_name": "Andrew",
        "explainer_rate": "+2%",
        "explainer_pitch": "+0Hz",
        "font_family": "Helvetica.ttc",
        
        # UI Strings for Slide Layouts
        "brand_title": "TokyoFlow Japanese",
        "brand_subtitle": "Real-Life Tokyo Japanese Academy",
        "chapter_prefix": "Chapter",
        "meaning_label": "Meaning: ",
        "pro_tip_label": "[ PRO-TIP ] ",
        "breakdown_category": "[ BREAKDOWN ]  Sentence Structure & Nuance",
        "sentence_label": "Sentence: ",
        "spotlight_label": "[ GRAMMAR SPOTLIGHT ] ",
        "rule_prefix": "• Rule",
        
        # Explainer / Drill Banners
        "explainer_banner_title": "[ ENGLISH EXPLANATION ACTIVE ]  Andrew explaining English meaning & nuance",
        "explainer_banner_sub": "Next: Shadowing Drill • Repeat aloud in Japanese with native timing",
        "shadowing_banner_title": "[ SHADOWING DRILL ]  Repeat aloud with native timing & pitch accent",
        "shadowing_banner_sub": "Native Audio: Nanami (Tokyo Standard) • Millisecond Follow-Along Highlighting",
        "academy_cta": "[ TOKYOFLOW ACADEMY ]  Practice interactive word drills & pitch accent scoring in the TokyoFlow iOS App!",
        
        # Outro Ending Card
        "outro_hero": "Subscribe to TokyoFlow Japanese on YouTube",
        "outro_sub": "Learn Natural Tokyo Japanese Through Real-Life Scenarios",
        "outro_bullets": [
            "• Real Tokyo Life Scenarios (Transit, Kombini, Izakaya, Akiba...)",
            "• 14,000+ Native VoiceBank Audio & Pitch Accent Intonation Guides",
            "• 10,000+ JLPT N5-N1 Vocabulary & Interactive Drills"
        ],
        "outro_app_cta": "[ iOS APP STORE ]  Download 'TokyoFlow - Japanese Speaking' Free on App Store",
        "outro_app_sub": "Pair with iOS App for Speech Shadowing Scoring, Kana Mastery & SRS Flashcards",
        "outro_passcode_badge": "[ STUDY PASSCODE ]",
        "outro_passcode_title": "OFFICIAL STUDY WORKBOOK UNLOCK CODE:",
        "outro_passcode_subtitle": "Download full JLPT N5-N3 Study Workbook PDF in description with this code",
        "outro_passcode_spoken_template": "Great job today! Download this episode's complete JLPT study workbook in the description below using unlock passcode {passcode}. Remember to subscribe to TokyoFlow for daily Tokyo immersion masterclasses!",
        
        # Thumbnail & Cover Labels
        "thumb_brand": "TokyoFlow Japanese",
        "thumb_default_sub_hook": "REAL JAPANESE BREAKDOWN",
        "thumb_tag_prefix": "Native Transit Audio • Shadowing"
    },
    
    "zh": {
        "code": "zh",
        "name": "Chinese",
        "explainer_voice": "zh-CN-YunxiNeural",
        "explainer_name": "云希",
        "explainer_rate": "+2%",
        "explainer_pitch": "+0Hz",
        "font_family": "Hiragino Sans GB.ttc",
        
        # UI Strings for Slide Layouts
        "brand_title": "TokyoFlow 日语",
        "brand_subtitle": "东京实景沉浸式日语学院",
        "chapter_prefix": "章节",
        "meaning_label": "中文释义：",
        "pro_tip_label": "【 重点提示 】 ",
        "breakdown_category": "【 句型拆解 】  词汇精讲与语法文化剖析",
        "sentence_label": "原句：",
        "spotlight_label": "【 核心语法与文化深度精讲 】 ",
        "rule_prefix": "• 规则",
        
        # Explainer / Drill Banners
        "explainer_banner_title": "【 教师精讲中 】  云希正在拆解词汇含义与语境用法",
        "explainer_banner_sub": "下一步：跟读练习 • 配合地道东京语调大声朗读",
        "shadowing_banner_title": "【 跟读训练 • 影子跟读 】  配合地道语调与音高曲线大声朗读",
        "shadowing_banner_sub": "日语音频：七海 (Nanami • 东京标准音) • 毫秒级发光卡拉OK同步",
        "academy_cta": "【 TOKYOFLOW 日语学院 】  搭配 iOS App 体验：AI 实时发音评测打分与全场景互动练习！",
        
        # Outro Ending Card
        "outro_hero": "关注 TokyoFlow 日语 • 开启沉浸式口语进阶",
        "outro_sub": "在东京真实生活场景中，轻松掌握地道口语与核心语法",
        "outro_bullets": [
            "• 20+ 东京实景真实对话（山手线、便利店、居酒屋、秋叶原等）",
            "• 14,000+ 原声母语语音库 & 东京标准音调声调图谱",
            "• 10,000+ JLPT N5-N1 核心词汇与全场景交互练习"
        ],
        "outro_app_cta": "【 iOS App Store 】  免费下载「TokyoFlow - 沉浸式日语口语」",
        "outro_app_sub": "搭配 iOS App 体验：AI 实时发音评测打分、五十音图速记与 SRS 遗忘曲线闪卡",
        "outro_passcode_badge": "【 讲义解锁密码 】",
        "outro_passcode_title": "本期 JLPT 配套研习讲义官方解锁口令：",
        "outro_passcode_subtitle": "在置顶评论区获取网盘链接，输入本密码免费下载完整 A4 复习手册",
        "outro_passcode_spoken_template": "今天的实景跟读训练完成！欢迎在视频简介栏和置顶评论区获取本期 JLPT 配套研习讲义，输入解锁密码 {passcode} 即可免费下载。记得点击订阅开启每日跟读！",
        
        # Thumbnail & Cover Labels
        "thumb_brand": "TokyoFlow 日语",
        "thumb_default_sub_hook": "东京实景地道精讲",
        "thumb_tag_prefix": "东京原声广播 • 影子跟读"
    }
}

def get_locale_config(locale_code: str = "en") -> dict:
    return LOCALES.get(locale_code, LOCALES["en"])
