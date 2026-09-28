import os
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1440
HEIGHT = 2560
img = Image.new("RGBA", (WIDTH, HEIGHT), "#0D1117")
draw = ImageDraw.Draw(img)

# Background subtle subway grid
for x in range(0, WIDTH, 80):
    draw.line([(x, 0), (x, HEIGHT)], fill=(255, 255, 255, 12), width=1)
for y in range(0, HEIGHT, 80):
    draw.line([(0, y), (WIDTH, y)], fill=(255, 255, 255, 12), width=1)

# Header Title Box
draw.rectangle([(60, 100), (WIDTH - 60, 260)], fill=(22, 27, 34, 230), outline=(56, 139, 253, 200), width=2)
# Text Header
try:
    font_title = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 52)
    font_sub = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 26)
    font_station = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 28)
    font_station_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
    font_legend = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 22)
except:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_station = ImageFont.load_default()
    font_station_sub = ImageFont.load_default()
    font_legend = ImageFont.load_default()

draw.text((90, 125), "東京地下鉄路線図 • TOKYO SUBWAY NETWORK", fill="#FFFFFF", font=font_title)
draw.text((90, 195), "Tokyo Metro & Toei Subway Official Navigation Route Map (実写本物スタイル)", fill="#8B949E", font=font_sub)

# Tokyo Metro Official Line Colors
LINES = {
    "G_Ginza": ("#FF9500", "G 銀座線 (Ginza Line)"),
    "M_Marunouchi": ("#F62E36", "M 丸ノ内線 (Marunouchi Line)"),
    "H_Hibiya": ("#B5B5AC", "H 日比谷線 (Hibiya Line)"),
    "T_Tozai": ("#009BBF", "T 東西線 (Tozai Line)"),
    "C_Chiyoda": ("#00BB85", "C 千代田線 (Chiyoda Line)"),
    "Y_Yurakucho": ("#C1A470", "Y 有楽町線 (Yurakucho Line)"),
    "Z_Hanzomon": ("#8F76D6", "Z 半蔵門線 (Hanzomon Line)"),
    "N_Namboku": ("#00AC9B", "N 南北線 (Namboku Line)"),
    "F_Fukutoshin": ("#9C5E31", "F 副都心線 (Fukutoshin Line)"),
    "JY_Yamanote": ("#99CC00", "JY 山手線 (JR Yamanote Loop)")
}

# 1. Draw Yamanote Loop Line (Green)
yamanote_coords = [
    (360, 600),   # Ikebukuro
    (720, 480),   # Ueno
    (1080, 720),  # Akihabara
    (1140, 1100), # Tokyo Station
    (1020, 1600), # Shinagawa
    (480, 1720),  # Meguro
    (300, 1400),  # Shibuya
    (280, 1000),  # Shinjuku
    (360, 600)    # Ikebukuro
]
draw.line(yamanote_coords, fill="#99CC00", width=14)

# 2. Draw Ginza Line (Orange)
ginza_coords = [
    (300, 1400), # Shibuya
    (520, 1320), # Omotesando
    (680, 1260), # Aoyama-itchome
    (780, 1200), # Akasaka-mitsuke
    (920, 1160), # Ginza
    (1060, 1060),# Nihombashi
    (1100, 850), # Kanda
    (1120, 600), # Ueno
    (1240, 520)  # Asakusa
]
draw.line(ginza_coords, fill="#FF9500", width=10)

# 3. Draw Marunouchi Line (Red)
marunouchi_coords = [
    (180, 1080), # Ogikubo
    (280, 1000), # Shinjuku
    (480, 940),  # Yotsuya
    (780, 1200), # Akasaka-mitsuke
    (920, 1160), # Ginza
    (1140, 1100),# Tokyo Station
    (1080, 900), # Otemachi
    (800, 700),  # Korakuen
    (360, 600)   # Ikebukuro
]
draw.line(marunouchi_coords, fill="#F62E36", width=10)

# 4. Draw Tozai Line (Sky Blue)
tozai_coords = [
    (220, 920),  # Nakano
    (280, 1000), # Takadanobaba
    (600, 920),  # Iidabashi
    (1080, 900), # Otemachi
    (1060, 1060),# Nihombashi
    (1260, 1200),# Monzen-nakacho
    (1380, 1300) # Nishi-funabashi
]
draw.line(tozai_coords, fill="#009BBF", width=10)

# 5. Draw Hanzomon Line (Purple)
hanzomon_coords = [
    (300, 1400), # Shibuya
    (520, 1320), # Omotesando
    (680, 1260), # Aoyama-itchome
    (740, 1040), # Kudanshita
    (1080, 900), # Otemachi
    (1280, 750), # Kiyosumi-shirakawa
    (1360, 620)  # Oshiage (Skytree)
]
draw.line(hanzomon_coords, fill="#8F76D6", width=10)

# 6. Draw Hibiya Line (Silver Grey)
hibiya_coords = [
    (280, 1600), # Naka-meguro
    (420, 1500), # Ebisu
    (600, 1420), # Roppongi
    (920, 1160), # Ginza
    (1120, 920), # Akihabara
    (1120, 600), # Ueno
    (1200, 420)  # Kita-senju
]
draw.line(hibiya_coords, fill="#B5B5AC", width=10)

# Key Major Stations
STATIONS = [
    ((280, 1000), "新宿", "Shinjuku (M08/JY17)", "#F62E36"),
    ((300, 1400), "渋谷", "Shibuya (G01/Z01/JY20)", "#FF9500"),
    ((1140, 1100), "東京", "Tokyo (M17/JY01)", "#F62E36"),
    ((920, 1160), "銀座", "Ginza (G09/M16/H08)", "#FF9500"),
    ((1080, 720), "秋葉原", "Akihabara (H15/JY03)", "#99CC00"),
    ((720, 480), "上野", "Ueno (G16/H17/JY05)", "#FF9500"),
    ((1240, 520), "浅草", "Asakusa (G19/A18)", "#FF9500"),
    ((360, 600), "池袋", "Ikebukuro (M25/Y09/F09)", "#F62E36"),
    ((600, 1420), "六本木", "Roppongi (H04/E23)", "#B5B5AC"),
    ((1020, 1600), "品川", "Shinagawa (JY25)", "#99CC00"),
    ((520, 1320), "表参道", "Omotesando (G02/C04/Z02)", "#00BB85"),
    ((1080, 900), "大手町", "Otemachi (M18/T09/C11/Z08)", "#009BBF"),
    ((1360, 620), "押上 (スカイツリー)", "Oshiage Skytree (Z14)", "#8F76D6")
]

# Draw station nodes
for (sx, sy), name_ja, name_en, color in STATIONS:
    # Outer white ring
    draw.ellipse([(sx - 18, sy - 18), (sx + 18, sy + 18)], fill="#FFFFFF", outline="#000000", width=3)
    # Inner colored hub
    draw.ellipse([(sx - 11, sy - 11), (sx + 11, sy + 11)], fill=color)
    
    # Station Badge Background
    offset_x = 26
    offset_y = -18
    if sx > 900:
        offset_x = -240
    
    draw.rounded_rectangle([(sx + offset_x - 6, sy + offset_y - 4), (sx + offset_x + 230, sy + offset_y + 48)], radius=8, fill=(22, 27, 34, 220), outline=(255, 255, 255, 80), width=1)
    draw.text((sx + offset_x, sy + offset_y), name_ja, fill="#FFFFFF", font=font_station)
    draw.text((sx + offset_x, sy + offset_y + 26), name_en, fill="#58A6FF", font=font_station_sub)

# Bottom Route Legend Box
draw.rectangle([(60, 1920), (WIDTH - 60, 2460)], fill=(22, 27, 34, 240), outline=(56, 139, 253, 180), width=2)
draw.text((90, 1940), "路線凡例 • SUBWAY LINE LEGEND", fill="#58A6FF", font=font_sub)

leg_items = list(LINES.items())
for i, (k, (col, label)) in enumerate(leg_items):
    col_x = 90 if i < 5 else 740
    row_y = 1990 + (i % 5) * 85
    draw.rounded_rectangle([(col_x, row_y), (col_x + 40, row_y + 24)], radius=4, fill=col)
    draw.text((col_x + 55, row_y - 2), label, fill="#E6EDF3", font=font_legend)

# Save
out_path = "TokyoFlow/Resources/Wallpapers/tokyo_subway.jpg"
img.convert("RGB").save(out_path, quality=95)

# Also save into assets
asset_path = "TokyoFlow/Resources/Assets.xcassets/wallpaper_tokyo_subway.imageset/tokyo_subway.jpg"
img.convert("RGB").save(asset_path, quality=95)
print(f"✅ Generated Real Tokyo Subway Transit Route Map to {out_path} and {asset_path}")
