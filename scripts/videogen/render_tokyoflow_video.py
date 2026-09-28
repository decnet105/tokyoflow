#!/usr/bin/env python3
"""
TokyoFlow Japanese • YouTube Scenario Video Production Engine
Inspired by Mystory's video factory architecture.
Generates 1080p full HD videos with native edge_tts narration, stylized typography cards,
and sample-accurate audio-video synchronization.
"""

import os
import sys
import json
import asyncio
import subprocess
from PIL import Image, ImageDraw, ImageFont
import edge_tts

FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"

def get_font(size: int):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

async def generate_speech_audio(text: str, voice: str, out_path: str, rate: str = "-5%", pitch: str = "+0Hz"):
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(out_path)

def get_audio_duration(audio_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(res.stdout.strip())

def create_slide_image(
    title_category: str,
    title_main: str,
    japanese_text: str,
    furigana_text: str,
    chinese_text: str,
    tip_text: str,
    chapter_label: str,
    out_img_path: str,
    is_outro: bool = False
):
    width, height = 1920, 1080
    
    # Background: Clean Japanese Ivory & Navy Modern Theme
    img = Image.new("RGB", (width, height), color=(248, 249, 252))
    draw = ImageDraw.Draw(img)

    # Top Brand Ribbon
    draw.rectangle([(0, 0), (width, 80)], fill=(22, 28, 45))
    
    font_brand = get_font(28)
    draw.text((60, 24), "TokyoFlow Japanese  |  东京实景沉浸式日语", fill=(255, 255, 255), font=font_brand)
    
    font_badge = get_font(22)
    draw.text((width - 320, 26), f"章节: {chapter_label}", fill=(244, 114, 182), font=font_badge)

    if is_outro:
        # Outro Ending Card
        draw.rectangle([(160, 160), (width - 160, height - 120)], fill=(255, 255, 255), outline=(226, 232, 240), width=4)
        
        font_hero = get_font(56)
        draw.text((220, 240), "关注 YouTube 官方频道: TokyoFlow Japanese", fill=(220, 38, 38), font=font_hero)
        
        font_sub = get_font(36)
        draw.text((220, 340), "订阅频道 • 获取最新东京实景教学更新", fill=(30, 41, 59), font=font_sub)
        
        font_bullets = get_font(30)
        draw.text((220, 440), "✓ 20+ 东京真实生活场景全覆盖 (电车/便利店/居酒屋/药妆店)", fill=(71, 85, 105), font=font_bullets)
        draw.text((220, 510), "✓ NHK 慢速原声跟读 • 毫秒级发音对齐", fill=(71, 85, 105), font=font_bullets)
        draw.text((220, 580), "✓ JLPT N5-N1 核心词汇与避坑礼仪全收录", fill=(71, 85, 105), font=font_bullets)
        
        # App CTA Box
        draw.rectangle([(220, 680), (width - 220, 840)], fill=(239, 246, 255), outline=(191, 219, 254), width=3)
        font_app = get_font(34)
        draw.text((260, 715), "📱 在 App Store 搜索「TokyoFlow」下载配套 App", fill=(37, 99, 235), font=font_app)
        font_app_sub = get_font(24)
        draw.text((260, 775), "配合 iOS App 一键跟读评分、假名记忆与词汇 SRS 记忆", fill=(100, 116, 139), font=font_app_sub)

    else:
        # Main Scenario Content Card
        # Left Category Badge
        font_cat = get_font(24)
        draw.rectangle([(120, 120), (450, 165)], fill=(238, 242, 255))
        draw.text((135, 128), title_category, fill=(79, 70, 229), font=font_cat)

        font_title = get_font(42)
        draw.text((120, 190), title_main, fill=(15, 23, 42), font=font_title)

        # Center Main Japanese Phrase Card
        draw.rectangle([(120, 270), (width - 120, 720)], fill=(255, 255, 255), outline=(226, 232, 240), width=4)

        # Furigana (Top)
        if furigana_text:
            font_furi = get_font(32)
            draw.text((180, 320), furigana_text, fill=(100, 116, 139), font=font_furi)

        # Japanese Kanji Main Text
        font_jp = get_font(52)
        draw.text((180, 385), japanese_text, fill=(15, 23, 42), font=font_jp)

        # Divider line
        draw.line([(180, 485), (width - 180, 485)], fill=(241, 245, 249), width=3)

        # Chinese Meaning
        font_zh = get_font(36)
        draw.text((180, 520), f"中文释义:  {chinese_text}", fill=(30, 41, 59), font=font_zh)

        # Bottom Tip & Tone
        font_tip = get_font(28)
        draw.text((180, 600), f"💡 实战精要:  {tip_text}", fill=(16, 185, 129), font=font_tip)

        # Bottom Call-to-action
        draw.rectangle([(120, 770), (width - 120, 920)], fill=(241, 245, 249), outline=(226, 232, 240), width=2)
        font_shadow = get_font(30)
        draw.text((160, 805), "🗣️  跟读指导 (Shadowing): 请随母语音频大声模仿声调起伏与停顿节奏", fill=(51, 65, 85), font=font_shadow)
        font_shadow_sub = get_font(22)
        draw.text((160, 860), "母语发音: Nanami (Tokyo Standard) • 敬语动词与车站/店员语境解密", fill=(100, 116, 139), font=font_shadow_sub)

    # Save slide image
    img.save(out_img_path, quality=95)

def render_scene_video(img_path: str, audio_path: str, duration: float, out_mp4_path: str):
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", img_path,
        "-i", audio_path,
        "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-t", str(duration + 0.5),
        "-shortest",
        out_mp4_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def concat_videos(video_list: list, final_output_path: str):
    concat_txt_path = "tmp/videogen/concat_list.txt"
    with open(concat_txt_path, "w") as f:
        for v in video_list:
            f.write(f"file '{os.path.abspath(v)}'\n")
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_txt_path,
        "-c", "copy",
        final_output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

async def build_video_package(spec: dict):
    video_id = spec["id"]
    print(f"🎬 Starting production for Video: {spec['title']} ({video_id})...")
    
    workdir = f"tmp/videogen/{video_id}"
    os.makedirs(workdir, exist_ok=True)
    
    segment_videos = []
    
    for idx, slide in enumerate(spec["slides"]):
        seg_prefix = f"{workdir}/seg_{idx:02d}"
        img_path = f"{seg_prefix}.jpg"
        audio_path = f"{seg_prefix}.mp3"
        video_path = f"{seg_prefix}.mp4"
        
        # 1. Generate Voiceover
        voice = slide.get("voice", "ja-JP-NanamiNeural")
        rate = slide.get("rate", "-6%")
        pitch = slide.get("pitch", "+3Hz")
        spoken_text = slide["spoken_text"]
        
        await generate_speech_audio(spoken_text, voice, audio_path, rate=rate, pitch=pitch)
        duration = get_audio_duration(audio_path)
        
        # 2. Render Graphic Slide
        create_slide_image(
            title_category=spec.get("category", "东京场景精讲"),
            title_main=spec["title"],
            japanese_text=slide.get("ja", ""),
            furigana_text=slide.get("furi", ""),
            chinese_text=slide.get("zh", ""),
            tip_text=slide.get("tip", ""),
            chapter_label=slide.get("chapter", f"Part {idx+1}"),
            out_img_path=img_path,
            is_outro=slide.get("is_outro", False)
        )
        
        # 3. Assemble Segment Video
        render_scene_video(img_path, audio_path, duration, video_path)
        segment_videos.append(video_path)
        print(f"  ✓ Segment {idx+1}/{len(spec['slides'])} rendered ({duration:.1f}s)")
        
    final_output = f"output/videos/{video_id}.mp4"
    concat_videos(segment_videos, final_output)
    total_duration = sum(get_audio_duration(f"{workdir}/seg_{i:02d}.mp3") for i in range(len(spec["slides"])))
    print(f"🎉 Successfully produced full HD video: {final_output} (Total Length: {total_duration:.1f}s)\n")

async def main():
    videos = [
        {
            "id": "tokyoflow_v01_yamanote_transit",
            "title": "【东京电车现场】山手线高峰换乘与站台广播彻底解密",
            "category": "东京交通 • Yamanote Line",
            "slides": [
                {
                    "chapter": "01. 现场实景还原",
                    "spoken_text": "まもなく、2番線に山手線内回りがまいります。黄色い点字ブロックの内側までお下がりください。",
                    "ja": "まもなく、2番線に山手線内回りがまいります。",
                    "furi": "まもなく、にばんせんに やまのてせん うちまわりが まいります。",
                    "zh": "2号站台内环山手线列车即将进站。",
                    "tip": "「まいります」为谦逊语，JR东京站台标准进站广播句式。"
                },
                {
                    "chapter": "02. 站台警示与安全",
                    "spoken_text": "黄色い点字ブロックの内側までお下がりください。危ないですから、ご注意ください。",
                    "ja": "黄色い点字ブロックの内側までお下がりください。",
                    "furi": "きいろい てんじぶろっくの うちがわまで おさがりください。",
                    "zh": "请退到黄色盲道点字砖内侧候车。",
                    "tip": "「お下がりください」为极其礼貌的劝告要求句型。"
                },
                {
                    "chapter": "03. 换乘求助金句",
                    "spoken_text": "すみません、中央線への乗り換えはどのホームですか？",
                    "ja": "中央線への乗り換えはどのホームですか？",
                    "furi": "ちゅうおうせんへの のりかえは どのほーむですか？",
                    "zh": "请问换乘中央线在哪个站台？",
                    "tip": "快速向站务员求助的高频口语句型，只需替换线路名称即可。"
                },
                {
                    "chapter": "04. 频道订阅与下载",
                    "spoken_text": "ご視聴ありがとうございました！チャンネル登録と高評価をお願いします。TokyoFlowアプリでさらに深く学びましょう！",
                    "is_outro": True
                }
            ]
        },
        {
            "id": "tokyoflow_v02_kombini_checkout",
            "title": "【便利店攻防战】日本7-11结账连环问与微波炉加热全攻略",
            "category": "东京便利店 • Kombini Checkout",
            "slides": [
                {
                    "chapter": "01. 便当加热连环问",
                    "spoken_text": "お弁当温めますか？少々お待ちください。",
                    "ja": "お弁当温めますか？",
                    "furi": "おべんとう あたためますか？",
                    "zh": "便当需要帮您微波炉加热吗？",
                    "tip": "回复「温めてください（请加热）」或「大丈夫です（不用了）」。"
                },
                {
                    "chapter": "02. 塑料袋与环保",
                    "spoken_text": "レジ袋はご利用ですか？レジ袋は大丈夫です。",
                    "ja": "レジ袋は大丈夫です。",
                    "furi": "れじぶくろは だいじょうぶです。",
                    "zh": "塑料袋不用了（我有自带）。",
                    "tip": "「大丈夫です」在口语中配合微摇头，表示委婉拒绝。"
                },
                {
                    "chapter": "03. 移动支付指定",
                    "spoken_text": "Suicaでお願いします。ポイントカードはお持ちですか？",
                    "ja": "Suicaでお願いします。",
                    "furi": "すいかで おねがいします。",
                    "zh": "请用 Suica 西瓜卡结账。",
                    "tip": "「〜でお願いします」是指定西瓜卡、PayPay或信用卡的万能句型。"
                },
                {
                    "chapter": "04. 频道订阅与下载",
                    "spoken_text": "TokyoFlow Japanese 公式チャンネルを登録して、毎日の生きた日本語をマスターしましょう！",
                    "is_outro": True
                }
            ]
        },
        {
            "id": "tokyoflow_v03_izakaya_night",
            "title": "【居酒屋江湖】日本昭和居酒屋点单、开胃菜与干杯礼仪",
            "category": "居酒屋文化 • Izakaya Protocol",
            "slides": [
                {
                    "chapter": "01. 入座第一杯酒",
                    "spoken_text": "いらっしゃい！とりあえず生ビール二つお願いします！",
                    "ja": "とりあえず生ビール二つお願いします！",
                    "furi": "とりあえず なまびーる ふたつ おねがいします！",
                    "zh": "先来两杯生啤！",
                    "tip": "日本居酒屋最地道的第一轮点酒黄金句型。"
                },
                {
                    "chapter": "02. 烤串盐与酱汁",
                    "spoken_text": "焼き鳥盛り合わせを塩でお願いします。お待たせいたしました！",
                    "ja": "焼き鳥盛り合わせを塩でお願いします。",
                    "furi": "やきとり もりあわせを しおで おねがいします。",
                    "zh": "烤鸡肉串拼盘，请帮我做盐烤口味。",
                    "tip": "店员常问「塩（しお）かタレか」，盐烤更能品尝鸡肉原汁原味。"
                },
                {
                    "chapter": "03. 结账与开收据",
                    "spoken_text": "お会計と領収書をお願いします。毎度ありがとうございました！",
                    "ja": "お会計と領収書をお願いします。",
                    "furi": "おかいけいと りょうしゅうしょを おねがいします。",
                    "zh": "请买单并开具报销发票。",
                    "tip": "「お会計」表示买单，「領収書（りょうしゅうしょ）」为报销发票。"
                },
                {
                    "chapter": "04. 频道订阅与下载",
                    "spoken_text": "TokyoFlow Japanese チャンネルを登録して、リアルな東京の日常会話を体験しましょう！",
                    "is_outro": True
                }
            ]
        }
    ]

    for v in videos:
        await build_video_package(v)

if __name__ == "__main__":
    asyncio.run(main())
