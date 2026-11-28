#!/usr/bin/env python3
"""Genera le pagine articolo (SEO + anteprime social) e la sitemap.

Uso: python3 scripts/share.py [file_edizione.json] [sottocartella]
  python3 scripts/share.py                       -> edition.json, radice
  python3 scripts/share.py ufo/edition.json ufo  -> giornale UFO (pagine noindex)

Per ogni notizia crea <sottocartella>/n/AAAA-MM-GG/<id>.html: pagina completa e indicizzabile
(titolo e descrizione SEO, dati strutturati NewsArticle, testo integrale del riassunto, tesi 1vs1,
approfondimento, fonti) e, se Pillow è disponibile, <id>.png 1200x630 per le anteprime social.
Poi rigenera sitemap.xml (solo giornale principale).
"""
import glob, html, json, os, re, sys

SITE = "https://news.raimondo.it"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COL = {"ind": "#d97706", "inc": "#ca8a04", "ads": "#753cef", "ia": "#e0306a", "geo": "#0284c7",
       "sci": "#0f766e", "uap": "#16a34a", "lavoro": "#059669", "regole": "#2563eb"}
MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto",
        "settembre", "ottobre", "novembre", "dicembre"]

e = lambda x: html.escape(str(x or ""), quote=True)


def cut(s, n):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    if len(s) <= n:
        return s
    s = s[: n - 1].rsplit(" ", 1)[0].rstrip(",;:.-–—")
    return s + "…"


def seo_title(s):
    t = s.get("seo_title") or s.get("title", "")
    return cut(t, 62)


def seo_desc(s):
    d = s.get("seo_desc") or s.get("sum", "")
    return cut(d, 158)


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
    f = ImageFont.truetype(fm, 30); lab = cat.upper()
    tw = d.textlength(lab, font=f)
    d.rounded_rectangle((70, 64, 70 + tw + 36, 64 + 52), 10, fill=color)
    d.text((88, 72), lab, font=f, fill="#ffffff")
    if vs:
        d.rounded_rectangle((70 + tw + 56, 64, 70 + tw + 56 + 112, 116), 10, fill="#e0306a")
        d.text((70 + tw + 74, 72), "1vs1", font=ImageFont.truetype(fx, 30), fill="#ffffff")
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


CSS = """:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#14121c;color:#e7e4ee;font:18px/1.65 Inter,system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
a{color:#b592ff}main{max-width:760px;margin:0 auto;padding:22px 18px 60px}
.top{display:flex;align-items:center;gap:10px;font-weight:800;font-size:20px;text-decoration:none;color:#fff;margin-bottom:26px}.top b{color:#9b6bff}
.kick{display:inline-block;background:var(--c);color:#fff;font:700 13px/1 Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;padding:6px 10px;border-radius:7px}
.vsb{display:inline-block;margin-left:8px;background:linear-gradient(90deg,#753cef,#e0306a);color:#fff;font:800 13px/1 Inter,sans-serif;padding:6px 10px;border-radius:7px}
h1{font-size:clamp(28px,6vw,44px);line-height:1.1;letter-spacing:-.02em;color:#fff;margin:16px 0 10px;text-wrap:balance}
.meta{color:#c9c4d6;font-size:15px;margin-bottom:22px}.pd{display:inline-block;margin-left:8px;background:#fff;color:#14121c;font:800 13px/1 Inter,sans-serif;padding:6px 10px;border-radius:7px;vertical-align:top}.sum{font-size:20px;color:#f2f0f7}.dl{color:#fff;font-weight:800}
h2{font-size:22px;color:#fff;margin:32px 0 10px}ul{padding-left:20px}li{margin:6px 0}
.sides{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));margin-top:18px}
.side{border-radius:14px;padding:16px 18px;background:#1d1a28}.side.a{border-top:4px solid #753cef}.side.b{border-top:4px solid #e0306a}
.side h3{margin:0 0 4px;font-size:19px;color:#fff;line-height:1.25}.side p{margin:0 0 8px;color:#a29db0;font-size:15px}
.why{border-left:4px solid var(--c);padding:6px 0 6px 16px;margin:28px 0}.why b{display:block;color:var(--c);font-size:13px;letter-spacing:.08em;text-transform:uppercase}
.src a{word-break:break-word}.lang{font-size:12px;color:#a29db0;border:1px solid #3a3548;border-radius:5px;padding:1px 5px;margin-left:6px}
.cta{display:inline-block;margin-top:30px;background:linear-gradient(90deg,#753cef,#e0306a);color:#fff;text-decoration:none;font-weight:800;padding:14px 20px;border-radius:12px}
footer{margin-top:40px;color:#8f8a9c;font-size:14px;border-top:1px solid #2c2838;padding-top:16px}"""


def page(s, ed, base, sec_name, img, url, target, noindex):
    date = ed["date"]; y, m, d = date.split("-")
    nice = f"{int(d)} {MESI[int(m) - 1]} {y}"
    color = COL.get(s["sec"], "#753cef")
    ttl = seo_title(s); desc = seo_desc(s)
    ld = {"@context": "https://schema.org", "@type": "NewsArticle", "headline": cut(s.get("title"), 110),
          "description": desc, "datePublished": f"{date}T07:00:00+01:00", "dateModified": f"{date}T07:00:00+01:00",
          "inLanguage": "it-IT", "image": [img], "mainEntityOfPage": url, "articleSection": sec_name,
          "author": {"@type": "Person", "name": "Federico Raimondo", "url": "https://raimondo.it"},
          "publisher": {"@type": "Organization", "name": "News.Raimondo.it", "url": SITE + "/",
                        "logo": {"@type": "ImageObject", "url": SITE + "/thumb.png"}},
          "isBasedOn": [x[1] for x in s.get("src", []) if isinstance(x, list) and len(x) > 1]}
    body = []
    body.append(f'<span class="kick">{e(sec_name)}</span>' + ('<span class="vsb">1vs1</span>' if s.get("vs") else "")
                + f'<time class="pd" datetime="{date}">{nice}</time>')
    body.append(f"<h1>{e(s.get('title'))}</h1>")
    body.append(f'<p class="meta">Pubblicato il <time datetime="{date}">{nice}</time> nell\'edizione di <a href="{e(target)}">News.Raimondo.it</a></p>')
    ev = s.get("ev") if isinstance(s.get("ev"), dict) else None
    line = ", ".join(x for x in [ev.get("place"), ev.get("date", "") + (", ore " + ev["time"] if ev.get("time") else "")] if x) if ev and ev.get("date") else s.get("date", "")
    dline = f'<b class="dl">{e(line)} —</b> ' if line else ""
    body.append(f'<p class="sum">{dline}{e(s.get("sum"))}</p>')
    if s.get("facts"):
        body.append("<h2>I fatti</h2><ul>" + "".join(f"<li>{e(x)}</li>" for x in s["facts"]) + "</ul>")
    if s.get("vs") and s.get("a") and s.get("b"):
        body.append("<h2>Le due tesi a confronto</h2><div class=\"sides\">")
        for k in ("a", "b"):
            x = s[k]
            body.append(f'<div class="side {k}"><h3>{e(x.get("h"))}</h3><p>{e(x.get("who"))}</p><ul>'
                        + "".join(f"<li>{e(p)}</li>" for p in x.get("pts", [])) + "</ul></div>")
        body.append("</div>")
    if s.get("why"):
        body.append(f'<div class="why"><b>Perché conta</b>{e(s["why"])}</div>')
    if s.get("deep"):
        body.append("<h2>Approfondimento</h2>" + "".join(f"<p>{e(p)}</p>" for p in s["deep"]))
    srcs = [x for x in s.get("src", []) if isinstance(x, list) and len(x) > 1 and str(x[1]).startswith("https://")]
    if srcs:
        body.append('<h2>Fonti</h2><ul class="src">' + "".join(
            f'<li><a href="{e(x[1])}" rel="noopener">{e(x[0])}</a>'
            + (f'<span class="lang">{e(x[2])}</span>' if len(x) > 2 and x[2] else "") + "</li>" for x in srcs) + "</ul>")
    for v in s.get("yt", []) or []:
        if isinstance(v, list) and len(v) > 1 and str(v[1]).startswith("https://"):
            body.append(f'<p>Video: <a href="{e(v[1])}" rel="noopener">{e(v[0])}</a></p>')
    body.append(f'<a class="cta" href="{e(target)}">Leggi l\'edizione completa del {nice}</a>')
    robots = '<meta name="robots" content="noindex,nofollow,noarchive">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    return f"""<!DOCTYPE html>
<html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(ttl)} | News.Raimondo.it</title>
<meta name="description" content="{e(desc)}">
{robots}
<link rel="canonical" href="{e(url)}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="News.Raimondo.it">
<meta property="og:title" content="{e(('1vs1 · ' if s.get('vs') else '') + s.get('title', ''))}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{e(img)}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:url" content="{e(url)}">
<meta property="og:locale" content="it_IT">
<meta property="article:published_time" content="{date}T07:00:00+01:00">
<meta property="article:section" content="{e(sec_name)}">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")}</script>
<style>{CSS}</style>
</head><body style="--c:{color}"><main>
<a class="top" href="{SITE}/{base}"><b>[R]</b> News.Raimondo.it</a>
<article>
{chr(10).join(body)}
</article>
<footer>Rassegna automatica realizzata con l'intelligenza artificiale a partire dalle fonti citate, senza redazione né direttore responsabile: per i dettagli fa fede la fonte originale. Un'idea di <a href="https://raimondo.it">Federico Raimondo</a>.</footer>
</main></body></html>
"""


def sitemap():
    urls = [(SITE + "/", None)]
    for f in sorted(glob.glob(os.path.join(ROOT, "n", "*", "*.html"))):
        rel = os.path.relpath(f, ROOT).replace(os.sep, "/")
        urls.append((f"{SITE}/{rel}", rel.split("/")[1]))
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, d in urls:
        out.append(f"  <url><loc>{html.escape(u)}</loc>" + (f"<lastmod>{d}</lastmod>" if d else "") + "</url>")
    out.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(
        f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    return len(urls)


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "edition.json")
    base = (sys.argv[2].strip("/") + "/") if len(sys.argv) > 2 and sys.argv[2].strip("/") else ""
    assert re.match(r"^([a-z0-9-]+/)?$", base)
    ed = json.load(open(src, encoding="utf-8"))
    date = ed["date"]; assert re.match(r"^\d{4}-\d{2}-\d{2}$", date)
    names = {k: v for k, v in ed.get("secs", [])}
    out = os.path.join(ROOT, base, "n", date); os.makedirs(out, exist_ok=True)
    n = 0
    for s in ed["stories"]:
        sid = s.get("id", "")
        if not re.match(r"^[a-z0-9-]{1,80}$", sid): continue
        cat = names.get(s["sec"], s.get("kick", ""))
        img = f"{SITE}/{base}thumb.png"
        if card(os.path.join(out, sid + ".png"), s["title"], cat, COL.get(s["sec"], "#753cef"), bool(s.get("vs"))):
            img = f"{SITE}/{base}n/{date}/{sid}.png"
        url = f"{SITE}/{base}n/{date}/{sid}.html"
        target = f"{SITE}/{base}?d={date}#{sid}"
        open(os.path.join(out, sid + ".html"), "w", encoding="utf-8").write(
            page(s, ed, base, cat, img, url, target, noindex=bool(base)))
        n += 1
    keep = {s.get("id") for s in ed["stories"]}
    for f in glob.glob(os.path.join(out, "*")):
        if os.path.splitext(os.path.basename(f))[0] not in keep:
            os.remove(f)
    print(f"{n} pagine articolo in {base}n/{date}/")
    if not base:
        print(f"sitemap.xml: {sitemap()} indirizzi")


if __name__ == "__main__":
    main()
