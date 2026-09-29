#!/usr/bin/env python3
# Assemble le dossier chiens-paris en un seul markdown avec sommaire et ancres.
import re, unicodedata, datetime, os

SRC = "/root/chiens-paris"
OUT = os.path.join(SRC, "DOSSIER-CHIEN-CITOYEN-PARIS.md")

# (fichier, label court du sommaire)
PARTIES = [
    ("I — Le pitch général", [
        ("PITCH-ET-RESUME.md", "Le pitch général"),
    ]),
    ("II — Les pitchs spécifiques", [
        ("PITCH-CITOYEN.md", "Pitch grand public"),
        ("PITCH-ELU.md", "Note pour un élu"),
        ("PITCH-CABINET-TECHNIQUE.md", "Note technique — collaborateur de cabinet"),
        ("PITCH-COLLAB-TECHNIQUE-IT.md", "Pitch pour un collègue technique"),
    ]),
    ("III — Les annexes vérifiées et triées", [
        ("AUDIT-SOURCES.md", "Audit anti-hallucination des sources"),
        ("NOTE-JURIDIQUE-ARRETE-ADN.md", "Note juridique — l'arrêté ADN canin"),
        ("ADN-COUTS-FAISABILITE.md", "Tests ADN canins : coûts et faisabilité"),
        ("STATUT-CHIEN-CITOYEN.md", "Statut du chien citoyen — note de conception"),
        ("PROJET-ARRETE-STATUT-CHIEN-CITOYEN.md", "Projet d'arrêté et règlement du statut"),
        ("PROJET-CHIENS-PARIS.md", "Projet « chiens de Paris » — creusage"),
        ("RAPPORT-COMPLET-CHIENS-PARIS.md", "Rapport complet et chiffrage"),
    ]),
]

FILES = [f for _, docs in PARTIES for f, _ in docs]
SLUG_ID = {}
AUTO_ID = {}

def gh_slug(text):
    """Slug des ancres telles que GitHub les génère depuis un titre."""
    t = unicodedata.normalize("NFC", text).strip().lower()
    out = []
    for ch in t:
        if ch.isalnum() or ch in "-_":
            out.append(ch)
        elif ch.isspace():
            out.append("-")
    return "".join(out)

def demote(text, first_is_section=True):
    """Décale d'un niveau tous les titres, le premier devenant le titre de section."""
    lines = text.split("\n")
    out, title_used = [], False
    counts = {}
    for ln in lines:
        m = re.match(r"^(#{1,6})(\s+)(.*)$", ln)
        if not m:
            out.append(ln)
            continue
        hashes, _, txt = m.groups()
        if not title_used:
            title_used = True
            out.append(("__SECTION__", txt))
        else:
            out.append("#" * min(len(hashes) + 1, 6) + " " + txt)
    return out

def relink(text):
    """Transforme les mentions de fichiers du dossier en liens vers les sections."""
    def repl(m):
        name = m.group(0)
        if name in SLUG_ID:
            return "[%s](#%s)" % (name, AUTO_ID[name])
        return name
    text = text.replace("/root/chiens-paris/", "")
    text = text.replace("Tout est dans  :", "Tout est dans ce document :")
    text = text.replace("sont dans le dossier :", "sont dans ce document :")
    return re.sub(r"(?<![\w/-])(" + "|".join(re.escape(f) for f in FILES) + r")", repl, text)

docs = {}
for f in FILES:
    with open(os.path.join(SRC, f), encoding="utf-8") as fh:
        docs[f] = fh.read()

# slugs GitHub calculés sur les titres de section définitifs (numéro + titre d'origine)
section_titles = {}
for i, f in enumerate(FILES, 1):
    raw_title = docs[f].split("\n", 1)[0].lstrip("# ").strip()
    section_titles[f] = "%d. %s" % (i, raw_title)

# dédoublonnage des slugs auto (GitHub suffixe -1, -2...)
seen = {}
for f in FILES:
    s = gh_slug(section_titles[f])
    n = seen.get(s, 0)
    seen[s] = n + 1
    AUTO_ID[f] = s if n == 0 else "%s-%d" % (s, n)
    SLUG_ID[f] = "s%d" % FILES.index(f)

today = datetime.date.today().isoformat()
out = []
out.append("# Dossier « chien citoyen de Paris » — version assemblée")
out.append("")
out.append("Document unique rassemblant le dossier complet : le pitch général, les pitchs ciblés "
           "(grand public, élu, cabinet technique, collègue technique) puis les annexes vérifiées et "
           "triées (audit des sources, note juridique, coûts et faisabilité, arrêté et règlement, "
           "rapport complet).")
out.append("")
out.append("Version du %s. Les sources de chaque affirmation chiffrée sont dans l'annexe 6 "
           "(audit anti-hallucination), qui indique aussi ce qui a été corrigé et ce qui reste "
           "incertain. Ce qui est marqué [E] dans le texte est une estimation, pas un chiffre sourcé. "
           "Rien n'a été voté : le dossier décrit un projet, pas un dispositif en vigueur." % today)
out.append("")
out.append("## Sommaire")
out.append("")
for ptitle, plist in PARTIES:
    out.append("**Partie %s**" % ptitle)
    out.append("")
    for f, label in plist:
        n = FILES.index(f) + 1
        out.append("- [%d. %s](#%s) — `%s`" % (n, label, AUTO_ID[f], f))
    out.append("")
out.append("- [Fichiers du dossier](#fichiers-du-dossier)")
out.append("")
out.append("---")
out.append("")

i = 0
for ptitle, plist in PARTIES:
    out.append("# Partie %s" % ptitle)
    out.append("")
    for f, label in plist:
        i += 1
        body = demote(docs[f])
        out.append('<a id="s%d"></a>' % i)
        out.append("")
        started = False
        for ln in body:
            if isinstance(ln, tuple):
                out.append("## " + section_titles[f])
                out.append("")
                out.append("*Source : `%s`.*" % f)
                out.append("")
                started = True
            else:
                out.append(relink(ln) if started else ln)
        out.append("")
        out.append("---")
        out.append("")

# index des fichiers
out.append('<a id="fichiers-du-dossier"></a>')
out.append("")
out.append("## Fichiers du dossier")
out.append("")
out.append("| Fichier | Rôle | Lignes |")
out.append("| --- | --- | --- |")
roles = {
    "PITCH-ET-RESUME.md": "Pitch général (version longue)",
    "PITCH-CITOYEN.md": "Pitch grand public",
    "PITCH-ELU.md": "Note pour un élu",
    "PITCH-CABINET-TECHNIQUE.md": "Note technique pour un cabinet",
    "PITCH-COLLAB-TECHNIQUE-IT.md": "Pitch pour un profil technique",
    "AUDIT-SOURCES.md": "Audit anti-hallucination, corrections, sources vérifiées",
    "NOTE-JURIDIQUE-ARRETE-ADN.md": "Ce qui a fait annuler Béziers, recette juridique",
    "ADN-COUTS-FAISABILITE.md": "Coûts réels des tests ADN, faisabilité, chiffrage",
    "STATUT-CHIEN-CITOYEN.md": "Note de conception du statut",
    "PROJET-ARRETE-STATUT-CHIEN-CITOYEN.md": "Projet d'arrêté, règlement, parcours, maquette de données",
    "PROJET-CHIENS-PARIS.md": "Première note d'exploration politique",
    "RAPPORT-COMPLET-CHIENS-PARIS.md": "Rapport complet et chiffrage détaillé",
}
for f in FILES:
    n = len(docs[f].split("\n"))
    out.append("| [%s](#%s) | %s | %d |" % (f, AUTO_ID[f], roles.get(f, ""), n))
out.append("")
out.append("Le brouillon antérieur à la passe de réécriture est conservé hors dossier sous "
           "`PITCH-ET-RESUME.avant-humanizer.md`.")
out.append("")

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(out))

print("écrit :", OUT)
print("lignes :", len(out))
print("section auto-ids :", AUTO_ID)