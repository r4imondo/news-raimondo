#!/usr/bin/env python3
"""Genera le pagine di condivisione (anteprime per Facebook, LinkedIn, WhatsApp, X).

Uso: python3 scripts/share.py [file_edizione.json]   (default: edition.json)
Per ogni notizia crea a/AAAA-MM-GG/<id>.html (tag Open Graph + rinvio alla notizia)
e, se Pillow è disponibile, a/AAAA-MM-GG/<id>.png (immagine 1200x630 con il titolo).
"""
import html, json, os, re, sys, textwrap

SITE = "https://news.raimondo.it"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COL = {"ind": "#d97706", "inc": "#ca8a04", "ads": "#753cef", "ia": "#e0306a", "geo": "#0284c7",
       "sci": "#0f766e", "lavoro": "#059669", "regole": "#2563eb"}

def card(path, title, cat, color, vs):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        return False
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), "#14121c")
    d = ImageDraw.Draw(im)
    d.ellipse((820, -260, 1420, 340), fill="#2a1c55")
    d.rectangle((0, 0, 14, H), fill=color)
    fx = os.path.join(ROOT, "fonts", "Inter-ExtraBold.otf"); fm = os.path.join(ROOT, "fonts", "Inter-Medium.otf")
    big = lambda s: ImageFont.truetype(fx, s)
    # categoria
    f = ImageFont.truetype(fm, 30); lab = cat.upper()
    tw = d.textlength(lab, font=f)
    d.rounded_rectangle((70, 64, 70 + tw + 36, 64 + 52), 10, fill=color)
    d.text((88, 72), lab, font=f, fill="#ffffff")
    if vs:
        d.rounded_rectangle((70 + tw + 56, 64, 70 + tw + 56 + 112, 116), 10, fill="#e0306a")
        d.text((70 + tw + 74, 72), "1vs1", font=ImageFont.truetype(fx, 30), fill="#ffffff")
    # titolo: scegli il corpo più grande che sta in 5 righe
    for size in (76, 68, 60, 54, 48, 42):
        fo = big(size); lines = []; cur = ""
        for w in title.split():
            t = (cur + " " + w).strip()
            if d.textlength(t, font=fo) <= W - 160: cur = t
            else: lines.append(cur); cur = w
        lines.append(cur)
        if len(lines) * size * 1.12 <= 360 and len(lines) <= 5: break
    y = 150 + (360 - len(lines) * size * 1.12) / 2
    for ln in lines:
        d.text((70, y), ln, font=fo, fill="#ffffff"); y += size * 1.12
    d.rectangle((70, 548, 330, 554), fill="#753cef"); d.rectangle((330, 548, 420, 554), fill="#e0306a")
    d.text((70, 568), "[R]", font=ImageFont.truetype(fx, 34), fill="#9b6bff")
    d.text((140, 568), "News.Raimondo.it", font=ImageFont.truetype(fx, 34), fill="#ffffff")
    im.save(path, "PNG", optimize=True)
    return True

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "edition.json")
    ed = json.load(open(src, encoding="utf-8"))
    date = ed["date"]; assert re.match(r"^\d{4}-\d{2}-\d{2}$", date)
    names = {k: v for k, v in ed.get("secs", [])}
    out = os.path.join(ROOT, "a", date); os.makedirs(out, exist_ok=True)
    n = 0
    for s in ed["stories"]:
        sid = s["id"]
        if not re.match(r"^[a-z0-9-]{1,80}$", sid): continue
        cat = names.get(s["sec"], s.get("kick", ""))
        img = f"{SITE}/thumb.png"
        if card(os.path.join(out, sid + ".png"), s["title"], cat, COL.get(s["sec"], "#753cef"), bool(s.get("vs"))):
            img = f"{SITE}/a/{date}/{sid}.png"
        target = f"{SITE}/?d={date}#{sid}"
        desc = s.get("sum", "")
        if len(desc) > 220: desc = desc[:217].rsplit(" ", 1)[0] + "…"
        e = lambda x: html.escape(x, quote=True)
        title = ("1vs1 · " if s.get("vs") else "") + s["title"]
        page = f"""<!DOCTYPE html>
<html lang="it"><head><meta charset="utf-8">
<title>{e(title)} · News.Raimondo.it</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(target)}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="News.Raimondo.it">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{e(img)}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:url" content="{SITE}/a/{date}/{sid}.html">
<meta property="og:locale" content="it_IT">
<meta name="twitter:card" content="summary_large_image">
<meta http-equiv="refresh" content="0;url={e(target)}">
<script>location.replace({json.dumps(target)})</script>
</head><body style="font-family:sans-serif;background:#14121c;color:#fff;padding:24px">
<p><a style="color:#b592ff" href="{e(target)}">{e(s['title'])}</a> · News.Raimondo.it</p>
</body></html>
"""
        open(os.path.join(out, sid + ".html"), "w", encoding="utf-8").write(page); n += 1
    print(f"{n} pagine di condivisione in a/{date}/")

if __name__ == "__main__":
    main()
