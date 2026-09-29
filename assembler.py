#!/usr/bin/env python3
# Assemble le dossier chiens-paris en un seul markdown : sommaire imbriqué avec ancres
# vérifiées contre le moteur de GitHub, navigation retour-sommaire, index des fichiers.
import re, unicodedata, datetime, os

SRC = "/root/chiens-paris"
OUT = os.path.join(SRC, "DOSSIER-CHIEN-CITOYEN-PARIS.md")

PARTIES = [
    ("I — Le pitch général", [
        ("PITCH-ET-RESUME.md", "Le pitch général"),
    ]),
    ("II — Les pitchs spécifiques", [
        ("PITCH-CITOYEN.md", "Pitch grand public"),
        ("PITCH-ELU.md", "Note pour un élu"),
        ("PITCH-CABINET-TECHNIQUE.md", "Note technique — collaborateur de cabinet"),
        ("PITCH-COM-PRESSE-RESEAUX.md", "Volet communication, presse et réseaux"),
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

EN_BREF = [
    ("Le problème", "100 000 chiens à Paris pour 45 espaces canins, les bus et tramways fermés aux "
                    "chiens, et 800 M€ de propreté par an qui ne règlent pas la crotte sur le trottoir."),
    ("L'idée", "Un statut de « chien·ne citoyen·ne » : le maître identifie son chien, ramasse, le "
               "tient en laisse, le fait éduquer et assurer ; en échange le chien obtient des droits "
               "qui n'existent aujourd'hui pour personne."),
    ("Ce que ça coûte", "Identification et enregistrement gratuits, cotisation possible autour de "
                        "20 € par an et par chien, exonération pour les propriétaires modestes. "
                        "Décision encore ouverte."),
    ("Le point juridique", "L'arrêté ADN de Béziers a été annulé faute de preuves de son utilité, non "
                           "pour illégalité : avant de sanctionner, il faut compter, mesurer et publier."),
    ("Ce qui n'est pas réglé", "Le nombre réel de chiens à Paris (100 000 à 300 000 selon les "
                               "sources), l'accord d'Île-de-France Mobilités pour les transports, et "
                               "le régime des données génétiques."),
    ("Statut", "Rien n'a été voté. Dossier de travail du 29 septembre 2026."),
]


def gh_slug(text):
    """Slug des ancres telles que GitHub les génère depuis un titre."""
    t = unicodedata.normalize("NFC", text).strip().lower()
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)     # [texte](lien) -> texte
    t = re.sub(r"[*`~]", "", t)                        # gras, italique, code
    return "".join(ch if (ch.isalnum() or ch in "-_") else ("-" if ch.isspace() else "")
                   for ch in t)


def demote(text):
    """Le premier titre devient le titre de section, les suivants descendent d'un niveau."""
    out, title_used = [], False
    for ln in text.split("\n"):
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


docs = {f: open(os.path.join(SRC, f), encoding="utf-8").read() for f in FILES}

section_titles = {}
for i, f in enumerate(FILES, 1):
    section_titles[f] = "%d. %s" % (i, docs[f].split("\n", 1)[0].lstrip("# ").strip())

# les titres de section portent un numéro, donc leur ancre est stable et sans collision
SLUG = {f: gh_slug(section_titles[f]) for f in FILES}


def relink(text):
    """Mentions de fichiers du dossier -> liens vers les sections ; nettoyage des chemins."""
    text = text.replace("/root/chiens-paris/", "")
    text = text.replace("Tout est dans  :", "Tout est dans ce document :")
    text = text.replace("sont dans le dossier :", "sont dans ce document :")
    text = re.sub(r"(?<![\w/-])(" + "|".join(re.escape(f) for f in FILES) + r")",
                  lambda m: "[%s](#%s)" % (m.group(0), SLUG[m.group(0)]), text)
    return text


# ---------- corps du document (hors sommaire) ----------
body = []
toc_entries = []          # (niveau 0/1/2, libellé du sommaire, titre cible, fichier)
for ptitle, plist in PARTIES:
    body += ["# Partie %s" % ptitle, ""]
    toc_entries.append((0, "Partie %s" % ptitle, None, None))
    for f, label in plist:
        n = FILES.index(f) + 1
        body += ["", "## " + section_titles[f], "", "*Source : `%s`.*" % f, ""]
        toc_entries.append((1, "%d. %s" % (n, label), section_titles[f], f))
        started = False
        for ln in demote(docs[f]):
            if isinstance(ln, tuple):
                started = True
                continue
            if started and re.match(r"^###\s", ln):
                toc_entries.append((2, ln.lstrip("# ").strip(), ln.lstrip("# ").strip(), f))
            body.append(relink(ln) if started else ln)
        body += ["", "[↑ Sommaire](#sommaire)", "", "---", ""]

body += ["", "## Fichiers du dossier", ""]
body += ["| Fichier | Rôle | Lignes |", "| --- | --- | --- |"]
roles = {
    "PITCH-ET-RESUME.md": "Pitch général (version longue)",
    "PITCH-CITOYEN.md": "Pitch grand public",
    "PITCH-ELU.md": "Note pour un élu",
    "PITCH-CABINET-TECHNIQUE.md": "Note technique pour un cabinet",
    "PITCH-COM-PRESSE-RESEAUX.md": "Volet communication, presse et réseaux", 
    "AUDIT-SOURCES.md": "Audit anti-hallucination, corrections, sources vérifiées",
    "NOTE-JURIDIQUE-ARRETE-ADN.md": "Ce qui a fait annuler Béziers, recette juridique",
    "ADN-COUTS-FAISABILITE.md": "Coûts réels des tests ADN, faisabilité, chiffrage",
    "STATUT-CHIEN-CITOYEN.md": "Note de conception du statut",
    "PROJET-ARRETE-STATUT-CHIEN-CITOYEN.md": "Projet d'arrêté, règlement, parcours, maquette de données",
    "PROJET-CHIENS-PARIS.md": "Première note d'exploration politique",
    "RAPPORT-COMPLET-CHIENS-PARIS.md": "Rapport complet et chiffrage détaillé",
}
for f in FILES:
    body.append("| `%s` | %s | %d |" % (f, roles.get(f, ""), len(docs[f].split("\n"))))
body += ["", "Le brouillon antérieur à la passe de réécriture est conservé hors dossier sous "
             "`PITCH-ET-RESUME.avant-humanizer.md`.", ""]

# ---------- slugs : ordre réel des titres dans le document, dédoublonnage global ----------
seen = {}
heading_slug = {}
for idx, ln in enumerate(body):
    m = re.match(r"^(#{1,6})\s+(.*)$", ln)
    if m:
        s = gh_slug(m.group(2))
        n = seen.get(s, 0)
        seen[s] = n + 1
        heading_slug[idx] = s if n == 0 else "%s-%d" % (s, n)

# titre -> slug de sa première occurrence (les sous-titres peuvent se répéter d'une pièce à l'autre)
first_of = {}
for idx, ln in enumerate(body):
    m = re.match(r"^(#{1,6})\s+(.*)$", ln)
    if m:
        first_of.setdefault(m.group(2).strip(), heading_slug[idx])

SLUG = {f: first_of.get(section_titles[f], gh_slug(section_titles[f])) for f in FILES}

# ---------- sommaire ----------
toc = ["## Sommaire", ""]
for level, label, target, f in toc_entries:
    if level == 0:
        toc += ["", "**%s**" % label, ""]
    elif level == 1:
        toc.append("- [%s](#%s) — `%s`" % (label, SLUG[f], f))
    else:
        s = first_of.get(target)
        if s:
            toc.append("  - [%s](#%s)" % (label, s))
toc += ["", "- [Fichiers du dossier](#fichiers-du-dossier)", ""]

# ---------- document final ----------
today = datetime.date.today().isoformat()
head = [
    "# Dossier « chien citoyen de Paris » — version assemblée",
    "",
    "Document unique rassemblant le dossier complet : le pitch général, les notes ciblées "
    "(grand public, élu, cabinet technique, communication et presse) puis les annexes vérifiées et "
    "triées (audit des sources, note juridique, coûts et faisabilité, arrêté et règlement, "
    "rapport complet).",
    "",
    "## En bref",
    "",
]
head += ["- **%s** — %s" % (label, txt) for label, txt in EN_BREF]
head += [
    "",
    "Version du %s. Les sources de chaque affirmation chiffrée sont dans l'annexe 6 "
    "(audit anti-hallucination), qui indique aussi ce qui a été corrigé et ce qui reste incertain. "
    "Ce qui est marqué [E] dans le texte est une estimation, pas un chiffre sourcé. Rien n'a été "
    "voté : le dossier décrit un projet, pas un dispositif en vigueur." % today,
    "",
    "## Sommaire",
    "",
]

out = head + [l for l in toc[2:]] + ["", "---", ""] + body
text = "\n".join(out)
text = re.sub(r"\n{3,}", "\n\n", text)
text = re.sub(r"[ \t]+\n", "\n", text)
with open(OUT, "w", encoding="utf-8") as fh:
    fh.write(text.rstrip("\n") + "\n")

print("écrit :", OUT)
print("lignes :", text.count("\n") + 1)
print("sections :", len([e for e in toc_entries if e[0] == 1]),
      "| sous-entrées :", len([e for e in toc_entries if e[0] == 2]))
print("ancres de section :", SLUG)