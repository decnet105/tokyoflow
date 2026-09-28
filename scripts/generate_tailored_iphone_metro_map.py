from PIL import Image, ImageDraw, ImageFont
import os
import math

# Target resolution: 1290 x 2796 (Perfect 9:19.5 for iPhone 14 Pro / 15 / 16 / 17 Pro)
WIDTH = 1290
HEIGHT = 2796

img = Image.new("RGBA", (WIDTH, HEIGHT), (248, 249, 252, 255))
draw = ImageDraw.Draw(img)

# Background subway grid texture (soft engineering lines)
for x in range(0, WIDTH, 80):
    draw.line([(x, 0), (x, HEIGHT)], fill=(235, 238, 244, 180), width=1)
for y in range(0, HEIGHT, 80):
    draw.line([(0, y), (WIDTH, y)], fill=(235, 238, 244, 180), width=1)

# Metro Line Colors (Official Tokyo Metro & Toei Subway hex)
COLORS = {
    "YAMANOTE": (154, 205, 50, 255),    # #9ACD32 Olive Green
    "MARUNOUCHI": (230, 0, 18, 255),    # #E60012 Red
    "GINZA": (255, 149, 0, 255),        # #FF9500 Orange
    "HIBIYA": (156, 163, 175, 255),     # #9CA3AF Silver Gray
    "TOZAI": (0, 167, 219, 255),        # #00A7DB Sky Blue
    "CHIYODA": (0, 153, 68, 255),       # #009944 Dark Green
    "HANZOMON": (143, 65, 157, 255),    # #8F419D Purple
    "NAMBOKU": (0, 172, 155, 255),      # #00AC9B Emerald Teal
    "FUKUTOSHIN": (156, 62, 24, 255),   # #9C3E18 Brown
    "OEDO": (182, 0, 100, 255),         # #B60064 Magenta
    "ASAKUSA": (232, 82, 70, 255),      # #E85246 Rose Red
    "CHUO": (255, 102, 0, 255),         # #FF6600 Bright Orange
    "MITA": (0, 114, 188, 255)          # #0072BC Royal Blue
}

def load_font(size, bold=False):
    font_paths = [
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc"
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()

font_title = load_font(60, bold=True)
font_subtitle = load_font(32, bold=True)
font_station = load_font(36, bold=True)
font_station_en = load_font(24, bold=False)
font_code = load_font(22, bold=True)

# 1. Header & Title Banner
draw.text((WIDTH//2, 180), "TOKYO METRO ROUTE MAP", fill=(20, 30, 45, 240), font=font_title, anchor="mm")
draw.text((WIDTH//2, 240), "東京地下鉄・JR山手線 路線図 (Tokyo Transit Network)", fill=(100, 116, 139, 220), font=font_subtitle, anchor="mm")

# Center Coordinates of major Tokyo Hubs on 1290x2796 screen
STATIONS = {
    "IKEBUKURO": (380, 750, "池袋", "Ikebukuro", "JY13 / M25"),
    "SHINJUKU": (340, 1200, "新宿", "Shinjuku", "JY17 / M08 / E27"),
    "SHIBUYA": (360, 1680, "渋谷", "Shibuya", "JY20 / G01 / Z01"),
    "ROPPONGI": (560, 1740, "六本木", "Roppongi", "H04 / E23"),
    "SHINAGAWA": (480, 2250, "品川", "Shinagawa", "JY25 / A07"),
    "SHIMBASHI": (760, 1920, "新橋", "Shimbashi", "JY29 / G08 / A10"),
    "GINZA": (820, 1650, "銀座", "Ginza", "G09 / M16 / H08"),
    "TOKYO": (840, 1380, "東京", "Tokyo", "JY01 / M17"),
    "AKIHABARA": (850, 1020, "秋葉原", "Akihabara", "JY03 / H15"),
    "UENO": (840, 780, "上野", "Ueno", "JY05 / G16 / H17"),
    "ASAKUSA": (1020, 780, "浅草", "Asakusa", "G19 / A18"),
    "OMOTESANDO": (460, 1560, "表参道", "Omotesando", "G02 / Z02 / C04"),
    "OTEMACHI": (740, 1350, "大手町", "Otemachi", "M18 / T09 / C11 / Z08"),
    "IIDABASHI": (560, 1050, "飯田橋", "Iidabashi", "T06 / Y13 / N10 / E06"),
    "KUDANSHITA": (620, 1200, "九段下", "Kudanshita", "T07 / Hanzomon"),
    "KASUMIGASEKI": (660, 1620, "霞ケ関", "Kasumigaseki", "M15 / H06 / C08"),
    "TSUKIJI": (940, 1780, "築地", "Tsukiji", "H10 / E18")
}

# Draw Lines
LINE_WIDTH = 18

def draw_smooth_route(points, color, width=LINE_WIDTH):
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=color, width=width)

# 1. Yamanote Loop Line (JR JY)
yamanote_pts = [
    STATIONS["IKEBUKURO"][:2],
    (600, 720),
    STATIONS["UENO"][:2],
    STATIONS["AKIHABARA"][:2],
    STATIONS["TOKYO"][:2],
    STATIONS["SHIMBASHI"][:2],
    (680, 2150),
    STATIONS["SHINAGAWA"][:2],
    (380, 2050),
    STATIONS["SHIBUYA"][:2],
    STATIONS["SHINJUKU"][:2],
    STATIONS["IKEBUKURO"][:2]
]
draw_smooth_route(yamanote_pts, COLORS["YAMANOTE"], LINE_WIDTH + 4)

# 2. Marunouchi Line (M)
maru_pts = [
    (240, 680),
    STATIONS["IKEBUKURO"][:2],
    (500, 920),
    (600, 1100),
    STATIONS["OTEMACHI"][:2],
    STATIONS["TOKYO"][:2],
    STATIONS["GINZA"][:2],
    STATIONS["KASUMIGASEKI"][:2],
    (480, 1420),
    STATIONS["SHINJUKU"][:2],
    (200, 1280)
]
draw_smooth_route(maru_pts, COLORS["MARUNOUCHI"])

# 3. Ginza Line (G)
ginza_pts = [
    STATIONS["SHIBUYA"][:2],
    STATIONS["OMOTESANDO"][:2],
    (580, 1560),
    STATIONS["SHIMBASHI"][:2],
    STATIONS["GINZA"][:2],
    (900, 1450),
    STATIONS["UENO"][:2],
    STATIONS["ASAKUSA"][:2]
]
draw_smooth_route(ginza_pts, COLORS["GINZA"])

# 4. Chuo Line Rapid (JC)
chuo_pts = [
    (180, 1200),
    STATIONS["SHINJUKU"][:2],
    (460, 1120),
    STATIONS["IIDABASHI"][:2],
    STATIONS["AKIHABARA"][:2],
    STATIONS["TOKYO"][:2]
]
draw_smooth_route(chuo_pts, COLORS["CHUO"], LINE_WIDTH + 2)

# 5. Hibiya Line (H)
hibiya_pts = [
    (460, 1920),
    STATIONS["ROPPONGI"][:2],
    STATIONS["KASUMIGASEKI"][:2],
    STATIONS["GINZA"][:2],
    STATIONS["TSUKIJI"][:2],
    (920, 1320),
    STATIONS["AKIHABARA"][:2],
    STATIONS["UENO"][:2],
    (960, 650)
]
draw_smooth_route(hibiya_pts, COLORS["HIBIYA"])

# 6. Tozai Line (T)
tozai_pts = [
    (200, 1050),
    STATIONS["IIDABASHI"][:2],
    STATIONS["KUDANSHITA"][:2],
    STATIONS["OTEMACHI"][:2],
    (950, 1350),
    (1150, 1350)
]
draw_smooth_route(tozai_pts, COLORS["TOZAI"])

# 7. Toei Oedo Line Loop (E)
oedo_pts = [
    (220, 1120),
    STATIONS["SHINJUKU"][:2],
    STATIONS["ROPPONGI"][:2],
    (680, 1980),
    (880, 1980),
    STATIONS["TSUKIJI"][:2],
    (1020, 1450),
    (1020, 1050),
    (880, 920),
    STATIONS["IIDABASHI"][:2]
]
draw_smooth_route(oedo_pts, COLORS["OEDO"], 14)

# Draw Stations Nodes & Labels
for key, (x, y, name_ja, name_en, code) in STATIONS.items():
    # Outer Station Ring
    draw.ellipse([x - 22, y - 22, x + 22, y + 22], fill=(255, 255, 255, 255), outline=(30, 41, 59, 255), width=5)
    draw.ellipse([x - 12, y - 12, x + 12, y + 12], fill=(15, 23, 42, 255))
    
    # Station Badge Background
    offset_x = 36
    offset_y = -28
    if x > 750:
        offset_x = -220
    
    box_w = 210
    box_h = 74
    draw.rounded_rectangle([x + offset_x, y + offset_y, x + offset_x + box_w, y + offset_y + box_h], radius=12, fill=(255, 255, 255, 235), outline=(203, 213, 225, 200), width=2)
    
    # Text
    draw.text((x + offset_x + 12, y + offset_y + 8), name_ja, fill=(15, 23, 42, 255), font=font_station)
    draw.text((x + offset_x + 12, y + offset_y + 44), name_en, fill=(100, 116, 139, 255), font=font_station_en)

# Bottom Legend Box
legend_y = 2500
draw.rounded_rectangle([80, legend_y, WIDTH - 80, legend_y + 180], radius=20, fill=(255, 255, 255, 240), outline=(226, 232, 240, 255), width=2)
draw.text((WIDTH//2, legend_y + 30), "TOKYO TRANSIT COLOR GUIDE", fill=(15, 23, 42, 240), font=load_font(28, bold=True), anchor="mm")

legend_items = [
    ("JY 山手線", COLORS["YAMANOTE"]),
    ("M 丸ノ内線", COLORS["MARUNOUCHI"]),
    ("G 銀座線", COLORS["GINZA"]),
    ("H 日比谷線", COLORS["HIBIYA"]),
    ("T 東西線", COLORS["TOZAI"]),
    ("E 大江戸線", COLORS["OEDO"])
]

for idx, (label, col) in enumerate(legend_items):
    lx = 140 + (idx % 3) * 360
    ly = legend_y + 70 + (idx // 3) * 48
    draw.rounded_rectangle([lx, ly, lx + 36, ly + 24], radius=6, fill=col)
    draw.text((lx + 48, ly + 2), label, fill=(51, 65, 85, 255), font=load_font(24, bold=True))

# Save Wallpaper Image
out_path_jpg = "TokyoFlow/Resources/Wallpapers/tokyo_subway.jpg"
out_path_asset = "TokyoFlow/Resources/Assets.xcassets/wallpaper_tokyo_subway.imageset/tokyo_subway.jpg"

img_rgb = img.convert("RGB")
img_rgb.save(out_path_jpg, "JPEG", quality=95)
img_rgb.save(out_path_asset, "JPEG", quality=95)

print("Generated tailored iPhone 14 Pro / 15 / 16 full-screen Tokyo Metro Route Map at 1290x2796!")
