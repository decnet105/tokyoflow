#!/usr/bin/env python3
"""
TokyoFlow Japanese • Targeted Re-renderer for EP.15 (OpenAI Rogue Agents)
Uses authentic Tokyo AI Tech Summit scene photograph (news_bg.jpg) for 100% video and cover immersion.
"""

import os
import sys
import json
import asyncio
import shutil
import subprocess
from pathlib import Path
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VIDEOGEN_DIR = PROJECT_ROOT / "scripts" / "videogen"
TREND_DIR = PROJECT_ROOT / "scripts" / "trend_radar"

sys.path.insert(0, str(VIDEOGEN_DIR))
sys.path.insert(0, str(TREND_DIR))

from slide_designer import (
    prepare_16_9_background_canvas,
    render_follow_along_video_clip,
    render_breakdown_video_clip,
    render_static_video_clip,
    render_outro_frame,
    render_news_broadcast_video_clip
)
from generate_thumbnails import generate_serialized_thumbnail
from generate_shorts_thumbnails import create_shorts_cover
from timing_engine import extract_tokens_from_text, align_sentence_tokens_with_audio

from daily_trend_producer import (
    concat_videos_seamless,
    generate_trend_short_video,
    synth_audio,
    get_audio_duration,
    generate_silence,
    build_teamwork_breakdown_audio,
    VOICE_NEWS_ANCHOR_JA,
    VOICE_FEMALE_JA,
    VOICE_MALE_EN
)

async def render_ep15_custom():
    release_dir = PROJECT_ROOT / "docs" / "youtube_releases" / "E15-openai_agent_buzz-v1.0"
    spec_file = release_dir / "production_spec.json"
    news_bg_file = release_dir / "news_bg.jpg"
    
    assert spec_file.exists(), f"Missing spec: {spec_file}"
    assert news_bg_file.exists(), f"Missing news_bg: {news_bg_file}"
    
    with open(spec_file, "r", encoding="utf-8") as f:
        spec = json.load(f)
        
    temp_dir = release_dir / "temp_render"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    print("==================================================")
    print("TokyoFlow • Targeted Re-render EP.15 with Authentic Tokyo AI Summit Photo")
    print(f"Base Scene Photo: {news_bg_file} ({news_bg_file.stat().st_size / (1024*1024):.2f} MB)")
    print("==================================================")
    
    base_canvas_16_9 = prepare_16_9_background_canvas(str(news_bg_file))
    rendered_clips = []
    
    # 1. News Intro Clip
    headline_jp = spec["news_broadcast"]["headline_ja"]
    news_speech = spec["news_broadcast"]["anchor_speech_ja"]
    raw_anchor = temp_dir / "00_anchor_raw.mp3"
    await synth_audio(news_speech, VOICE_NEWS_ANCHOR_JA, str(raw_anchor), rate="+0%", pitch="+1Hz")
    
    chime_path = PROJECT_ROOT / "TokyoFlow" / "Resources" / "Audio" / "news_chime.mp3"
    anchor_with_chime = temp_dir / "00_anchor_chime.mp3"
    if chime_path.exists():
        cmd = [
            "ffmpeg", "-y",
            "-i", str(chime_path),
            "-i", str(raw_anchor),
            "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[outa]",
            "-map", "[outa]",
            "-c:a", "libmp3lame",
            str(anchor_with_chime)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        intro_audio = anchor_with_chime
    else:
        intro_audio = raw_anchor
        
    dur_intro = get_audio_duration(str(intro_audio))
    clip_intro = temp_dir / "clip_00_news_broadcast.mp4"
    render_news_broadcast_video_clip(
        bg_image_path=str(news_bg_file),
        headline_ja=headline_jp,
        location_tag=spec.get("district", "TOKYO POP CULTURE"),
        audio_path=str(intro_audio),
        duration=dur_intro,
        out_mp4_path=str(clip_intro),
        ep_label=f"EP.{spec['ep_num']:02d}",
        fps=30
    )
    rendered_clips.append(str(clip_intro))
    print(f"  Live News Broadcast Clip Rendered: {dur_intro:.2f}s")
    
    # 2. Long Form Slides
    long_spec = spec["long_form"]
    ep_label = f"EP.{spec['ep_num']:02d} | [JLPT N5]"
    
    for idx, sl in enumerate(long_spec["slides"]):
        sl_type = sl.get("type", "follow_along")
        clip_mp4 = os.path.join(temp_dir, f"clip_{idx+1:02d}_{sl_type}.mp4")
        
        if sl_type == "follow_along":
            spoken_text = sl["spoken_text"]
            english_meaning = sl.get("en", "")
            fa_tmp = os.path.join(temp_dir, f"fa_{idx+1:02d}")
            audio_fa_path = os.path.join(temp_dir, f"slide_{idx+1:02d}_dual_track.mp3")
            
            os.makedirs(fa_tmp, exist_ok=True)
            fn_ja = os.path.join(fa_tmp, "nanami_ja.mp3")
            await synth_audio(spoken_text, VOICE_FEMALE_JA, fn_ja, rate="-12%", pitch="+2Hz")
            dur_ja = get_audio_duration(fn_ja)
            
            fn_sil = os.path.join(fa_tmp, "sil.mp3")
            generate_silence(0.3, fn_sil)
            
            fn_en = os.path.join(fa_tmp, "andrew_en.mp3")
            await synth_audio(english_meaning, VOICE_MALE_EN, fn_en, rate="+2%", pitch="+0Hz")
            dur_en = get_audio_duration(fn_en)
            
            concat_txt = os.path.join(fa_tmp, "concat.txt")
            with open(concat_txt, "w") as f:
                f.write(f"file '{os.path.abspath(fn_ja)}'\n")
                f.write(f"file '{os.path.abspath(fn_sil)}'\n")
                f.write(f"file '{os.path.abspath(fn_en)}'\n")
                
            cmd = [
                "ffmpeg", "-y",
                "-f", "concat", "-safe", "0",
                "-i", concat_txt,
                "-c:a", "libmp3lame",
                "-b:a", "192k",
                "-ar", "44100",
                "-ac", "2",
                audio_fa_path
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            total_dur = get_audio_duration(audio_fa_path)
            
            tokens = sl.get("tokens", [])
            if not tokens:
                tokens = extract_tokens_from_text(spoken_text)
            aligned_toks = align_sentence_tokens_with_audio(fn_ja, tokens, spoken_text)
            
            render_follow_along_video_clip(
                tokens=aligned_toks,
                category_label=f"[JLPT N5]  Pop Culture & Technology",
                title_label=f"{sl.get('chapter', '01. Follow Along')} • {spec['topic_title']}",
                english_meaning=english_meaning,
                pro_tip=sl.get("tip", ""),
                chapter_label=sl.get("chapter", "01. Follow Along"),
                ep_label=ep_label,
                audio_path=audio_fa_path,
                duration=total_dur,
                out_mp4_path=clip_mp4,
                fps=30,
                en_window=(dur_ja + 0.3, total_dur),
                base_canvas=base_canvas_16_9,
                bg_image_path=str(news_bg_file)
            )
            rendered_clips.append(clip_mp4)
            print(f"  Dual-Voice Follow-Along Clip {idx} Rendered: {total_dur:.2f}s")
            
        elif "breakdown" in sl_type:
            breakdown_tmp = os.path.join(temp_dir, f"bd_{idx+1:02d}")
            audio_bd_path = os.path.join(temp_dir, f"slide_{idx+1:02d}_bd_teamwork.mp3")
            
            cues = sl.get("teamwork_cues") or sl.get("audio_cues") or []
            if not cues:
                cues = [
                    {"speaker": "en", "text": "Let us break down today's key words and grammar."},
                    {"speaker": "ja", "text": sl.get("sentence_ja", spec["topic_title"])},
                    {"speaker": "en", "text": "Practice this sentence to speak natural Japanese in Tokyo."}
                ]
            bd_res = await build_teamwork_breakdown_audio(cues, audio_bd_path, breakdown_tmp)
            dur = bd_res["total_duration"]
            timings = bd_res["timings"]
            
            sentence_ja = sl.get("sentence_ja") or sl.get("spoken_text") or (long_spec["slides"][0]["spoken_text"] if long_spec.get("slides") else spec["topic_title"])
            vocab_list = sl.get("words") or sl.get("vocab") or []
            
            if isinstance(sl.get("grammar"), dict):
                grammar_title = sl["grammar"].get("title", "Grammar & Cultural Spotlight")
                grammar_bullets = sl["grammar"].get("bullets", [])
            else:
                grammar_title = sl.get("grammar_title", "Grammar & Cultural Spotlight")
                grammar_bullets = sl.get("grammar_bullets", [])
                
            render_breakdown_video_clip(
                sentence_ja=sentence_ja,
                vocab_list=vocab_list,
                grammar_title=grammar_title,
                grammar_bullets=grammar_bullets,
                category_label=f"[JLPT N5]  Sentence Structure & Nuance",
                chapter_label=sl.get("chapter", "02. Breakdown"),
                ep_label=ep_label,
                timings=timings,
                audio_path=audio_bd_path,
                duration=dur,
                out_mp4_path=clip_mp4,
                fps=30,
                base_canvas=base_canvas_16_9,
                bg_image_path=str(news_bg_file)
            )
            rendered_clips.append(clip_mp4)
            print(f"  Bilingual Breakdown Clip {idx} Rendered: {dur:.2f}s")
            
    # 3. Outro Clip
    outro_audio = str(temp_dir / "outro.mp3")
    await synth_audio("Subscribe to TokyoFlow Japanese, and practice interactive speaking drills in the TokyoFlow app!", VOICE_MALE_EN, outro_audio, rate="+2%")
    dur_out = get_audio_duration(outro_audio)
    outro_img = render_outro_frame(ep_label, base_canvas=base_canvas_16_9, bg_image_path=str(news_bg_file))
    clip_outro = str(temp_dir / "clip_outro.mp4")
    render_static_video_clip(outro_img, outro_audio, dur_out, clip_outro, fps=30)
    rendered_clips.append(clip_outro)
    
    # 4. Concat Long Video
    final_long_mp4 = str(release_dir / "video.mp4")
    concat_videos_seamless(rendered_clips, final_long_mp4, str(temp_dir))
    print(f"  Long-Form Video Rendered: {final_long_mp4}")
    
    # 5. 16:9 Thumbnail
    thumb_path = str(release_dir / "thumbnail.jpg")
    generate_serialized_thumbnail(
        ep_num=spec["ep_num"],
        english_hook=long_spec.get("english_hook", "AI AGENTS REBEL"),
        japanese_key_phrase=long_spec.get("japanese_key_phrase", "AIが自由になった"),
        bottom_tag="[JLPT N5]  Native Pop Culture • Shadowing",
        bg_image_path=str(news_bg_file),
        output_path=thumb_path,
        jlpt_level="JLPT N5"
    )
    print(f"  16:9 Thumbnail Rendered: {thumb_path}")
    
    # 6. 9:16 Shorts Cover
    shorts_spec = spec["shorts"]
    shorts_spec["ep_num"] = spec["ep_num"]
    shorts_spec["jlpt_level"] = "JLPT N5"
    shorts_spec["district"] = "Tokyo Pop Culture"
    
    short_thumb = str(release_dir / "short_thumbnail.jpg")
    shorts_cover_dict = {
        "ep_num": spec["ep_num"],
        "sh_code": f"SH.{spec['ep_num']:02d}",
        "folder": release_dir.name,
        "hook_main": "AI AGENTS REBEL",
        "hook_sub": "JAPAN TECH TREND",
        "jp_phrase": shorts_spec.get("jp_sentence", ""),
        "romaji": shorts_spec.get("romaji_sentence", ""),
        "en_meaning": shorts_spec.get("en_translation", ""),
        "accent_color": (236, 72, 153),
        "secondary_color": (250, 204, 21),
        "location": "TOKYO POP CULTURE • JLPT N5",
        "jlpt_level": "JLPT N5",
        "bg_image_path": str(news_bg_file)
    }
    cover_img = create_shorts_cover(shorts_cover_dict)
    cover_img.save(short_thumb, "JPEG", quality=95)
    print(f"  9:16 Shorts Cover Rendered: {short_thumb}")
    
    # 7. 9:16 Shorts Video with First-Frame Master Cover Burn-in
    short_mp4 = str(release_dir / "short.mp4")
    shorts_tmp = str(temp_dir / "shorts_render")
    await generate_trend_short_video(shorts_spec, short_mp4, short_thumb, shorts_tmp)
    print(f"  9:16 Shorts Video Rendered: {short_mp4}")
    
    print("\n[COMPLETE] Targeted EP.15 Re-render Finished Successfully!")

if __name__ == "__main__":
    asyncio.run(render_ep15_custom())
