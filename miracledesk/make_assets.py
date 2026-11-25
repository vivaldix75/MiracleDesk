# MiracleDesk 아이콘/로고 생성 (GODF 코인 GF 로고 기반). 로컬에서 1회 실행, 결과물은 assets/에 커밋.
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageChops
SRC = r"C:\python\GODF_coin\logo\make_logo.py"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.environ["LOGO_TEXT"] = "GF"; os.environ["LOGO_SIZE"] = sys.argv[1] if len(sys.argv) > 1 else "900"
code = open(SRC, encoding="utf-8").read().split("out=img.resize")[0]
ns = {}; exec(code, ns); big = ns["img"]  # 2048x2048 RGBA

def sz(n): return big.resize((n, n), Image.LANCZOS)
sz(1024).save(f"{OUT}/icon.png")
for n, name in [(32, "32x32"), (64, "64x64"), (128, "128x128"), (256, "128x128@2x")]:
    sz(n).save(f"{OUT}/{name}.png")
sz(256).save(f"{OUT}/flutter_icon.png")
ico_sizes = [(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)]
sz(256).save(f"{OUT}/icon.ico", sizes=ico_sizes)
sz(256).save(f"{OUT}/tray-icon.ico", sizes=[(16,16),(24,24),(32,32),(48,48)])

# 로고 배너 (최대 300x60 표시) : 2배 해상도 600x120
W, H = 600, 120
logo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
logo.paste(sz(104), (8, 8), sz(104))
d = ImageDraw.Draw(logo)
f = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 62)
for name, col in [("logo_light.png", (20, 40, 110, 255)), ("logo_dark.png", (255, 255, 255, 255))]:
    im = logo.copy(); dd = ImageDraw.Draw(im)
    bb = dd.textbbox((0, 0), "MiracleDesk", font=f)
    dd.text((128 - bb[0], (H - (bb[3] - bb[1])) // 2 - bb[1]), "MiracleDesk", font=f, fill=col)
    im = im.crop(im.getbbox()); im.save(f"{OUT}/{name}")
print("ok", os.listdir(OUT))
