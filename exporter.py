#!/usr/bin/env python3
"""Exporte le dossier chiens-paris en HTML autonome, PDF et DOCX.

Deux paquets :
  - dossier-complet   : le document assemblé (sommaire, pitchs, annexes)
  - version-grand-public : pour quelqu'un qui n'a jamais entendu parler du sujet

Usage : python3 exporter.py [dossier-complet|version-grand-public|tout]
"""
import os, re, sys, unicodedata, html, subprocess, datetime, shutil, zipfile

SRC = "/root/chiens-paris"
EXPORT = os.path.join(SRC, "export")
DATE = "29 septembre 2026"

# ---------------------------------------------------------------- markdown -> blocs

def gh_slug(text):
    t = unicodedata.normalize("NFC", text).strip().lower()
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"[*`~]", "", t)
    return "".join(ch if (ch.isalnum() or ch in "-_") else ("-" if ch.isspace() else "")
                   for ch in t)


def inline_runs(text):
    """Découpe une ligne en runs (texte, gras, italique, code, lien)."""
    runs, i = [], 0
    pattern = re.compile(r"\*\*(.+?)\*\*|(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)|`([^`]+)`|"
                         r"\[([^\]]+)\]\(([^)]+)\)")
    for m in pattern.finditer(text):
        if m.start() > i:
            runs.append(("text", text[i:m.start()]))
        if m.group(1) is not None:
            runs.append(("bold", m.group(1)))
        elif m.group(2) is not None:
            runs.append(("italic", m.group(2)))
        elif m.group(3) is not None:
            runs.append(("code", m.group(3)))
        else:
            runs.append(("link", (m.group(4), m.group(5))))
        i = m.end()
    if i < len(text):
        runs.append(("text", text[i:]))
    return runs or [("text", text)]


def parse(md):
    lines = md.split("\n")
    blocks, i = [], 0
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if not s:
            i += 1
            continue
        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", s):
            blocks.append({"type": "hr"}); i += 1; continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            blocks.append({"type": "h", "level": len(m.group(1)), "text": m.group(2).strip()})
            i += 1; continue
        if s.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
            head = [c.strip() for c in s.strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            blocks.append({"type": "table", "head": head, "rows": rows}); continue
        if s.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip()); i += 1
            blocks.append({"type": "quote", "text": " ".join(quote)}); continue
        ml = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", ln)
        if ml:
            ordered = ml.group(2)[0].isdigit()
            items = []
            while i < len(lines):
                cur = lines[i]
                m2 = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", cur)
                if m2:
                    items.append([len(m2.group(1)) // 2, m2.group(3).strip()])
                    i += 1
                    continue
                if not cur.strip():
                    break
                if items and re.match(r"^\s{2,}\S", cur):
                    items[-1][1] += " " + cur.strip()
                    i += 1
                    continue
                break
            blocks.append({"type": "ol" if ordered else "ul", "items": items}); continue
        para = [s]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(
                r"^\s*(#{1,6}\s|[-*+]\s|\d+[.)]\s|>|\|)", lines[i]) and not re.match(
                r"^(-{3,}|\*{3,})$", lines[i].strip()):
            para.append(lines[i].strip()); i += 1
        blocks.append({"type": "p", "text": " ".join(para)})
    return blocks


# ---------------------------------------------------------------- rendu HTML

def esc(t):
    return html.escape(t, quote=False)

def runs_html(runs):
    out = []
    for kind, val in runs:
        if kind == "text":
            out.append(esc(val))
        elif kind == "bold":
            out.append("<strong>%s</strong>" % esc(val))
        elif kind == "italic":
            out.append("<em>%s</em>" % esc(val))
        elif kind == "code":
            out.append("<code>%s</code>" % esc(val))
        else:
            text, url = val
            out.append('<a href="%s">%s</a>' % (esc(url), esc(text)))
    return "".join(out)

def blocks_html(blocks, cover_after=None):
    out, slug_count = [], {}
    for b in blocks:
        if b["type"] == "h":
            txt = b["text"]
            s = gh_slug(txt)
            n = slug_count.get(s, 0)
            slug_count[s] = n + 1
            anchor = s if n == 0 else "%s-%d" % (s, n)
            cls = ' class="partie"' if txt.startswith("Partie ") else (
                ' class="section"' if re.match(r"^\d+\.\s", txt) else "")
            out.append("<h%d%s id=\"%s\">%s</h%d>" % (b["level"], cls, anchor,
                                                      runs_html(inline_runs(txt)), b["level"]))
        elif b["type"] == "p":
            out.append("<p>%s</p>" % runs_html(inline_runs(b["text"])))
        elif b["type"] in ("ul", "ol"):
            t = b["type"]
            stack, out = [], out
            out.append("<%s>" % t)
            cur = None
            for lvl, txt in b["items"]:
                if cur is None:
                    stack = [lvl]; cur = lvl
                elif lvl > cur:
                    for _ in range(lvl - cur):
                        out.append("<%s>" % t); stack.append(cur + 1); cur += 1
                elif lvl < cur:
                    while stack and lvl < cur:
                        out.append("</li></%s>" % t); stack.pop(); cur -= 1
                else:
                    out.append("</li>")
                out.append("<li>%s" % runs_html(inline_runs(txt)))
            out.append("</li>")
            while stack:
                out.append("</%s>" % t); stack.pop()
        elif b["type"] == "table":
            out.append('<div class="tw"><table>')
            out.append("<thead><tr>%s</tr></thead>" % "".join(
                "<th>%s</th>" % runs_html(inline_runs(c)) for c in b["head"]))
            out.append("<tbody>")
            for row in b["rows"]:
                out.append("<tr>%s</tr>" % "".join(
                    "<td>%s</td>" % runs_html(inline_runs(c)) for c in row))
            out.append("</tbody></table></div>")
        elif b["type"] == "quote":
            out.append("<blockquote>%s</blockquote>" % runs_html(inline_runs(b["text"])))
        elif b["type"] == "hr":
            out.append("<hr>")
    return "\n".join(out)


CSS = """
:root { --txt:#1b1b1b; --muted:#5b5b5b; --line:#dcdcdc; --accent:#1f4e79; --accent2:#8a5a00; }
* { box-sizing: border-box; }
body { margin:0; color:var(--txt); background:#fff;
  font-family: Georgia, "Times New Roman", serif; font-size:16px; line-height:1.62; }
main { max-width: 46rem; margin: 0 auto; padding: 2.5rem 1.4rem 4rem; }
h1,h2,h3,h4 { font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height:1.25; color:var(--accent); }
h1 { font-size:1.9rem; margin:2.4rem 0 .8rem; padding-bottom:.4rem; border-bottom:2px solid var(--line); }
h1:first-of-type { margin-top:0; }
h2 { font-size:1.45rem; margin:2rem 0 .7rem; }
h3 { font-size:1.15rem; margin:1.6rem 0 .5rem; color:#2c2c2c; }
h4 { font-size:1rem; margin:1.3rem 0 .4rem; color:var(--muted); text-transform:none; }
p { margin:.65rem 0; }
ul, ol { margin:.6rem 0 .9rem; padding-left:1.4rem; }
li { margin:.25rem 0; }
strong { color:#111; }
code { font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace; font-size:.86em;
  background:#f4f4f4; padding:.08em .3em; border-radius:3px; }
a { color:var(--accent); text-decoration:none; border-bottom:1px solid #c9d6e4; }
table { border-collapse: collapse; width:100%; margin:1rem 0; font-size:.93rem;
  font-family:-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }
th, td { border:1px solid var(--line); padding:.45rem .6rem; text-align:left; vertical-align:top; }
th { background:#f2f5f8; }
blockquote { margin:1rem 0; padding:.6rem 1rem; border-left:4px solid var(--accent2);
  background:#fbf8f1; font-style:normal; }
hr { border:0; border-top:1px solid var(--line); margin:2.2rem 0; }
.cover { max-width:46rem; margin:0 auto; padding:5rem 1.4rem 0; text-align:left; }
.cover .kicker { font-family:-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  text-transform:uppercase; letter-spacing:.14em; font-size:.75rem; color:var(--muted); }
.cover h1 { font-size:2.5rem; border:0; margin:.5rem 0 0; }
.cover .sub { font-size:1.1rem; color:var(--muted); margin-top:.8rem; }
.cover .meta { margin-top:2.5rem; font-size:.9rem; color:var(--muted); }
.cover .warn { margin-top:1.2rem; padding:.8rem 1rem; border:1px solid var(--line);
  background:#fafafa; font-size:.9rem; }
.tw { overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 1rem 0; }
.cover.small { padding: 2.5rem 1.4rem 0; }
.cover.small h1 { font-size: 1.7rem; }
@media (max-width: 600px) {
  body { font-size: 17px; }
  main { padding: 1.2rem .9rem 3rem; }
  .cover, .cover.small { padding: 1.6rem .9rem 0; }
  .cover h1 { font-size: 1.8rem; }
  h1 { font-size: 1.5rem; }
  h2 { font-size: 1.25rem; }
  h3 { font-size: 1.08rem; }
  table { font-size: .88rem; }
  th, td { padding: .35rem .45rem; }
  ul, ol { padding-left: 1.1rem; }
}
@media print {
  @page { size:A4; margin:20mm 18mm; }
  html, body { font-size:10.8pt; }
  main { max-width:none; padding:0; }
  h1.partie { page-break-before: always; }
  h2.section { page-break-before: always; }
  table, blockquote, ul, ol { page-break-inside: avoid; }
  h1, h2, h3 { page-break-after: avoid; }
  a { color:#1b1b1b; border:0; }
  .cover { padding:0; page-break-after: always; }
}
"""


def html_doc(title, blocks, kicker, subtitle, note, cover=True):
    head = ""
    if cover:
        head = f"""<section class="cover">
<div class="kicker">{esc(kicker)}</div>
<h1>{esc(title)}</h1>
<div class="sub">{esc(subtitle)}</div>
<div class="meta">Paris, {DATE}. Version assemblée le {datetime.date.today().isoformat()}.</div>
<div class="warn">{esc(note)}</div>
</section>"""
    else:
        head = f"""<header class="cover small">
<div class="kicker">{esc(kicker)} · dossier « chien citoyen de Paris »</div>
<h1>{esc(title)}</h1>
<div class="meta">{esc(note)}</div>
</header>"""
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} — chien citoyen de Paris</title>
<style>{CSS}</style></head>
<body>
{head}
<main>
{blocks_html(blocks)}
</main>
</body></html>"""


# ---------------------------------------------------------------- rendu DOCX

def docx_doc(title, blocks, subtitle, note, path):
    from docx import Document
    from docx.shared import Pt, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Georgia"; st.font.size = Pt(11)
    d.add_heading(title, level=0)
    p = d.add_paragraph(subtitle); p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    d.add_paragraph("Paris, %s." % DATE)
    d.add_paragraph(note)

    def add_runs(par, text):
        for kind, val in inline_runs(text):
            if kind == "code":
                r = par.add_run(val); r.font.name = "Consolas"; r.font.size = Pt(10)
            elif kind == "link":
                r = par.add_run(val[0]); r.bold = False
            else:
                r = par.add_run(val)
                if kind == "bold":
                    r.bold = True
                elif kind == "italic":
                    r.italic = True

    for b in blocks:
        if b["type"] == "h":
            t = b["text"]
            if t.startswith("Partie "):
                d.add_page_break()
            d.add_heading(re.sub(r"[*`]", "", t), level=min(b["level"], 4))
        elif b["type"] == "p":
            add_runs(d.add_paragraph(), b["text"])
        elif b["type"] in ("ul", "ol"):
            base = None
            for lvl, txt in b["items"]:
                if base is None:
                    base = lvl
                style = "List Bullet" if b["type"] == "ul" else "List Number"
                if lvl > base:
                    style += " %d" % min(lvl - base + 1, 3)
                add_runs(d.add_paragraph(style=style), txt)
        elif b["type"] == "table":
            tbl = d.add_table(rows=1, cols=len(b["head"]))
            tbl.style = "Light Grid Accent 1"
            for c, txt in zip(tbl.rows[0].cells, b["head"]):
                c.text = re.sub(r"[*`]", "", txt)
            for row in b["rows"]:
                cells = tbl.add_row().cells
                for c, txt in zip(cells, row):
                    c.text = re.sub(r"[*`]", "", txt)
        elif b["type"] == "quote":
            add_runs(d.add_paragraph(style="Intense Quote"), b["text"])
        elif b["type"] == "hr":
            d.add_paragraph("")
    d.save(path)


# ---------------------------------------------------------------- PDF (chromium)

def pdf(html_path, pdf_path):
    subprocess.run(["chromium", "--headless=new", "--no-sandbox", "--disable-gpu",
                    "--no-pdf-header-footer", "--virtual-time-budget=10000",
                    "--print-to-pdf=%s" % pdf_path, "file://" + html_path],
                   check=True, capture_output=True, timeout=180)
    return os.path.getsize(pdf_path)


# ---------------------------------------------------------------- paquets

def md_of(pieces):
    return "\n\n".join(open(os.path.join(SRC, f), encoding="utf-8").read().rstrip()
                       for f, _ in pieces)


def page_count(pdf_path):
    return len(re.findall(rb"/Type\s*/Page[^s]", open(pdf_path, "rb").read()))


def build(name, pieces, title, kicker, subtitle, note, cover=True, site=True):
    """Produit html + docx + pdf pour un paquet, et éventuellement une page du site."""
    blocks = parse(md_of(pieces))
    os.makedirs(EXPORT, exist_ok=True)
    page = html_doc(title, blocks, kicker, subtitle, note, cover=cover)
    hp = os.path.join(EXPORT, "%s.html" % name)
    open(hp, "w", encoding="utf-8").write(page)
    dp = os.path.join(EXPORT, "%s.docx" % name)
    docx_doc(title, blocks, subtitle, note, dp)
    pp = os.path.join(EXPORT, "%s.pdf" % name)
    size = pdf(hp, pp)
    print("  %-46s html %4.0f Ko | docx %4.0f Ko | pdf %4.0f Ko, %3d pages" % (
        name, os.path.getsize(hp) / 1024, os.path.getsize(dp) / 1024,
        size / 1024, page_count(pp)))
    return {"name": name, "html": hp, "docx": dp, "pdf": pp, "title": title,
            "kicker": kicker, "pages": page_count(pp)}


PIECES = [
    ("PITCH-CITOYEN.md", "Le chien citoyen de Paris, version grand public", "Grand public"),
    ("PITCH-ET-RESUME.md", "Le statut du chien citoyen de Paris, pitch général", "Vue d'ensemble"),
    ("PITCH-ELU.md", "Note pour un élu", "Ciblé"),
    ("PITCH-CABINET-TECHNIQUE.md", "Note technique pour un collaborateur de cabinet", "Ciblé"),
    ("PITCH-COLLAB-TECHNIQUE-IT.md", "Pitch pour un collègue technique", "Ciblé"),
    ("AUDIT-SOURCES.md", "Audit anti-hallucination des sources", "Annexe"),
    ("NOTE-JURIDIQUE-ARRETE-ADN.md", "L'arrêté ADN canin : ce qui a fait annuler Béziers", "Annexe"),
    ("ADN-COUTS-FAISABILITE.md", "Tests ADN canins : coûts et faisabilité", "Annexe"),
    ("STATUT-CHIEN-CITOYEN.md", "Statut du chien citoyen : note de conception", "Annexe"),
    ("PROJET-ARRETE-STATUT-CHIEN-CITOYEN.md", "Projet d'arrêté et règlement du statut", "Annexe"),
    ("PROJET-CHIENS-PARIS.md", "Projet « chiens de Paris » : creusage", "Annexe"),
    ("RAPPORT-COMPLET-CHIENS-PARIS.md", "Rapport complet et chiffrage", "Annexe"),
]

INDEX_CSS = """
body { font-family:-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }
.card { border:1px solid var(--line); border-radius:8px; padding:1rem 1.1rem; margin:.8rem 0; }
.card h3 { margin:0 0 .3rem; color:var(--accent); }
.card p { margin:.2rem 0 .6rem; color:var(--muted); font-size:.94rem; }
.dl { font-size:.9rem; }
.dl a { margin-right:1rem; white-space:nowrap; }
ul.plain { list-style:none; padding:0; }
ul.plain li { padding:.35rem 0; border-bottom:1px solid var(--line); }
.tag { font-size:.75rem; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); }
"""


def build_site(landing_pages, piece_paths):
    """index.html : point d'entrée lisible au téléphone comme sur ordinateur."""
    cards = []
    for p in landing_pages:
        cards.append(f"""<div class="card">
<h3><a href="{os.path.basename(p['html'])}">{esc(p['title'])}</a></h3>
<p>{esc(p['kicker'])} — {p['pages']} pages en PDF, lisible en ligne sur téléphone comme sur ordinateur.</p>
<p class="dl">Ouvrir : <a href="{os.path.basename(p['html'])}">version web</a>
<a href="{os.path.basename(p['pdf'])}">PDF</a>
<a href="{os.path.basename(p['docx'])}">Word (modifiable)</a></p></div>""")
    rows = []
    for path, title, tag in piece_paths:
        rows.append('<li><span class="tag">%s</span><br><a href="%s">%s</a></li>'
                    % (esc(tag), os.path.basename(path), esc(title)))
    html_out = f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Le chien citoyen de Paris — dossier</title>
<style>{CSS}{INDEX_CSS}</style></head>
<body>
<main>
<h1>Le chien citoyen de Paris</h1>
<p class="sub">Un statut pour les chiens de Paris : registre, identification génétique, droits
d'accès, chiffrage. Document de travail du {DATE} — rien n'a été voté.</p>
<h2>Commencer ici</h2>
{''.join(cards)}
<h2>Toutes les pièces du dossier</h2>
<ul class="plain">{''.join(rows)}</ul>
<p class="meta">Également dans ce dossier : <code>sources/</code> (les fichiers markdown d'origine).</p>
</main></body></html>"""
    ip = os.path.join(EXPORT, "index.html")
    open(ip, "w", encoding="utf-8").write(html_out)
    print("  index.html écrit")
    return ip


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "tout"
    os.makedirs(EXPORT, exist_ok=True)
    made = []
    if what in ("version-grand-public", "tout"):
        made.append(build(
            "Chien-citoyen-de-Paris-version-grand-public",
            [("PITCH-CITOYEN.md", None), ("PITCH-ET-RESUME.md", None)],
            "Le chien citoyen de Paris",
            "Dossier grand public",
            "Un statut pour les chiens de Paris : ce qu'on propose, ce que ça coûte, ce qui reste à décider.",
            "Document de travail, rien n'a été voté. Ce dossier décrit un projet, pas un "
            "dispositif en vigueur."))
    if what in ("dossier-complet", "tout"):
        made.append(build(
            "Chien-citoyen-de-Paris-dossier-complet",
            [(f, None) for f in [
                "PITCH-ET-RESUME.md", "PITCH-CITOYEN.md", "PITCH-ELU.md",
                "PITCH-CABINET-TECHNIQUE.md", "PITCH-COLLAB-TECHNIQUE-IT.md", "AUDIT-SOURCES.md",
                "NOTE-JURIDIQUE-ARRETE-ADN.md", "ADN-COUTS-FAISABILITE.md", "STATUT-CHIEN-CITOYEN.md",
                "PROJET-ARRETE-STATUT-CHIEN-CITOYEN.md", "PROJET-CHIENS-PARIS.md",
                "RAPPORT-COMPLET-CHIENS-PARIS.md"]],
            "Dossier « chien citoyen de Paris »",
            "Dossier complet",
            "Pitch, notes juridiques, chiffrage, sources vérifiées.",
            "Document de travail, rien n'a été voté. Chaque chiffre renvoie à l'annexe « audit "
            "anti-hallucination », qui dit ce qui est prouvé, corrigé, ou encore incertain."))
    if what in ("pieces", "tout"):
        os.makedirs(os.path.join(EXPORT, "pieces"), exist_ok=True)
        piece_paths = []
        for f, title, tag in PIECES:
            slug = gh_slug(os.path.basename(f).replace(".md", ""))
            p = build("pieces/%s" % slug, [(f, None)], title, tag,
                      "Pièce du dossier « chien citoyen de Paris ».",
                      "Document de travail du %s. Rien n'a été voté." % DATE)
            piece_paths.append((p["html"], title, tag))
        shutil.rmtree(os.path.join(EXPORT, "sources"), ignore_errors=True)
        os.makedirs(os.path.join(EXPORT, "sources"), exist_ok=True)
        for f in [f for f, _, _ in PIECES] + ["DOSSIER-CHIEN-CITOYEN-PARIS.md", "README.md"]:
            shutil.copy(os.path.join(SRC, f), os.path.join(EXPORT, "sources", f))
        build_site(made, piece_paths)

    # archive à envoyer par mail
    zpath = os.path.join(SRC, "Chien-citoyen-de-Paris-dossier.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, fnames in os.walk(EXPORT):
            for fn in fnames:
                full = os.path.join(root, fn)
                z.write(full, os.path.relpath(full, EXPORT))
    print("  archive %.0f Mo -> %s" % (os.path.getsize(zpath) / 1048576, zpath))