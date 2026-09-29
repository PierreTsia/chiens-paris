# Dossier « chien citoyen de Paris »

Dossier de travail, 29 septembre 2026. Projet d'un statut de « chien·ne citoyen·ne » à Paris :
registre, identification ADN, droits d'accès (transports, espaces de liberté, jardins d'immeuble),
chiffrage, montage juridique et politique.

Rien n'a été voté, rien n'est en vigueur : c'est un dossier de projet, avec ses points ouverts et
les sources qui portent chaque chiffre.

## Lire le dossier

👉 **[DOSSIER-CHIEN-CITOYEN-PARIS.md](DOSSIER-CHIEN-CITOYEN-PARIS.md)** — le document assemblé :
sommaire, pitch général, pitchs ciblés, annexes vérifiées.

Ordre de lecture conseillé :

1. `PITCH-AMIS-BALADE.md` — la note courte pour un canal de copains promeneurs de chiens, à envoyer
   telle quelle (`export/Chien-citoyen-de-Paris-note-copains-balade.pdf`, 3 pages).
2. `PITCH-CITOYEN.md` — la version grand public, une page, sans jargon.
3. `PITCH-ET-RESUME.md` — le pitch général, la version longue et complète.
4. `PITCH-ELU.md` / `PITCH-CABINET-TECHNIQUE.md` / `PITCH-COLLAB-TECHNIQUE-IT.md` — selon
   l'interlocuteur.
5. `AUDIT-SOURCES.md` — ce qui est prouvé, ce qui a été corrigé, ce qui reste incertain.
6. `RAPPORT-COMPLET-CHIENS-PARIS.md` — le rapport détaillé et son chiffrage.

## Contenu

| Fichier | Rôle |
| --- | --- |
| `DOSSIER-CHIEN-CITOYEN-PARIS.md` | Dossier assemblé (sommaire + tout le reste) |
| `PITCH-AMIS-BALADE.md` | Note courte pour les copains de balade (canal WhatsApp) |
| `PITCH-ET-RESUME.md` | Pitch général, version longue |
| `PITCH-CITOYEN.md` | Pitch grand public |
| `PITCH-ELU.md` | Note pour un élu |
| `PITCH-CABINET-TECHNIQUE.md` | Note technique pour un collaborateur de cabinet |
| `PITCH-COLLAB-TECHNIQUE-IT.md` | Pitch pour un profil technique |
| `AUDIT-SOURCES.md` | Audit anti-hallucination : corrections et sources vérifiées (URL) |
| `NOTE-JURIDIQUE-ARRETE-ADN.md` | Ce qui a fait annuler Béziers, et la recette pour un arrêté qui tient |
| `ADN-COUTS-FAISABILITE.md` | Coûts réels des tests ADN, faisabilité, chiffrage |
| `STATUT-CHIEN-CITOYEN.md` | Note de conception du statut |
| `PROJET-ARRETE-STATUT-CHIEN-CITOYEN.md` | Projet d'arrêté, règlement, parcours, maquette de données |
| `PROJET-CHIENS-PARIS.md` | Première note d'exploration politique |
| `RAPPORT-COMPLET-CHIENS-PARIS.md` | Rapport complet et chiffrage |
| `assembler.py` | Script qui régénère le dossier assemblé |

Pour régénérer le document assemblé après une modification d'une pièce :

```
python3 assembler.py
```