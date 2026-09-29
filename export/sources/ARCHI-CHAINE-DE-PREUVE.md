# Architecture — une chaîne de preuve outillée (photo en contexte, QR, registre horodaté)

29 septembre 2026. Question posée : peut-on faire quelque chose de solide et d'ouvert — photo en
contexte, QR code, données et chiffres — en respectant la chaîne de preuve (la « chaîne du froid »
du prélèvement) ? Réponse : oui, et c'est même la bonne façon de faire, à condition de comprendre ce
que l'outil peut apporter et ce qu'aucun outil ne peut produire. Note de conception. Rien n'a été
voté.

## 1. Le partage à ne pas se tromper

**Ce que le logiciel peut faire, et qu'aucun humain ne fait proprement :** l'intégrité, la datation,
la traçabilité des transferts, et la publication vérifiable. C'est le pilier « daté et intègre » de
la note juridique du comptage, et c'est exactement là qu'un serveur quelconque ne vaut rien.

**Ce qu'aucun logiciel ne peut produire :**

- **L'autorité de constater.** Un procès-verbal n'a de force que par un agent habilité (art. 537 du
  code de procédure pénale). Aucune application ne verbalise.
- **Le contradictoire.** Il tient à une invitation écrite, datée, envoyée avant le premier passage, et
  à deux observateurs dont un non partie prenante. Un logiciel peut *enregistrer* cette invitation et
  *rendre visible* qui a compté ; il ne peut pas la remplacer.
- **La représentativité.** Si les rues sont choisies parce qu'elles sont sales, aucun outil ne sauvera
  le chiffre. D'où la zone témoin et le pré-enregistrement du protocole : c'est de la gouvernance,
  pas du code.

Corollaire de conception, et c'est la règle qui structure tout le reste : **l'outil ne doit jamais
devenir la preuve.** Si le chiffre ne tient que parce que notre application l'affirme, l'adversaire
n'a qu'un mot à dire — « votre serveur, vos chiffres » — et le dossier est mort. La vérification ne
doit exiger de faire confiance à personne, nous compris.

## 2. Le principe : un identifiant, deux chaînes

Tout se tient sur une idée simple : **un identifiant unique lie l'objet physique et l'enregistrement
numérique**, et chaque transfert de cet objet est un événement daté et signé.

**Chaîne matérielle** (le prélèvement, la « chaîne du froid ») :

1. L'agent ou l'observateur prélève la déjection, la place dans un tube et **appose un scellé
   numéroté**, issu d'un carnet à séquence continue — comme un carnet d'exhibits. Un scellé manquant
   dans la séquence est visible, donc un prélèvement fabriqué après coup laisse une trace.
2. Relevé obligatoire au moment du prélèvement : horodatage, tronçon, position, **photo en
   contexte**, conditions (météo, heure, température si la chaîne du froid s'applique au transport).
3. Chaque remise (observateur → transporteur → laboratoire) est un **transfert à deux signatures** :
   qui remet, qui reçoit, quand, dans quel état. Le laboratoire renvoie un accusé de réception.
4. Conservation et délai : la date limite d'analyse et les conditions de transport sont inscrites
   dans le protocole, pas improvisées. C'est aussi le point technique numéro un du dossier — la
   robustesse de l'ADN environnemental sur un trottoir n'est documentée nulle part publiquement.

**Chaîne numérique** (le même identifiant, côté données) :

1. Chaque fiche de relevé produit un enregistrement immuable : identifiant, tronçon, créneau,
   comptage, observateurs, empreinte de la photo, version du protocole.
2. **Empreinte SHA-256** de chaque fiche et de chaque photo.
3. **Arbre de Merkle par session**, dont la racine est horodatée par un service de confiance
   qualifié (eIDAS, RFC 3161). Résultat : n'importe qui peut vérifier, des années plus tard, qu'une
   photo donnée existait à cette date et n'a pas bougé — sans nous croire et sans accéder à nos
   serveurs. Une variante gratuite et indépendamment vérifiable (ancrage en chaîne de blocs) est
   utile en complément, mais reste appréciée librement par le juge : ce n'est pas un service qualifié.
4. **Registre en ajout seul** : aucun enregistrement n'est modifiable. Une correction est un nouvel
   enregistrement qui référence l'ancien, et les deux restent visibles. C'est ce qui rend un chiffre
   inattaquable sur le terrain où toutes les administrations se font prendre : « vous avez ajusté
   après coup ».
5. **Divergence publiée, jamais lissée** : quand les deux observateurs d'un même passage ne comptent
   pas la même chose, l'écart est publié avec sa raison. Un écart affiché crédibilise ; un écart
   effacé se retrouve un jour en commentaire.

## 3. La photo en contexte, et à quoi sert vraiment le QR

Une photo seule ne dit pas où, quand, ni par qui — et ses métadonnées se réécrivent. Trois usages du
QR, dans cet ordre d'utilité :

1. **L'étiquette de passage, imprimée à l'avance et numérotée.** Elle porte un QR contenant :
   identifiant du tronçon, numéro de session, date prévue, version du protocole, identifiant de
   l'observateur. La règle photographique est : **l'étiquette et la déjection dans le même cadre**.
   L'image porte alors son contexte, lisible par un humain sur la photo et par une machine dans le
   QR. Les étiquettes sont émises en séquence continue : un manque dans la séquence est un signal.
2. **Le lien de vérification** : le QR renvoie à la page publique de l'enregistrement — empreinte,
   horodatage, statut. C'est ce qui permet à un journaliste, à un élu ou à un contradicteur de
   vérifier sans rien nous demander.
3. **La même étiquette pour le prélèvement** : le QR porte aussi le numéro de scellé du tube, ce qui
   fait qu'un seul identifiant suit l'objet du trottoir jusqu'au résultat du laboratoire.

## 4. Contradictoire outillé, sans le remplacer

Ce que le logiciel ajoute au contradictoire, sans jamais s'y substituer :

- **l'invitation est un enregistrement du registre** : courrier à la mairie, à la mairie
  d'arrondissement, au préfet, daté et horodaté, avec le protocole et les dates ;
- **la clé publique des observateurs** est publiée : chacun peut voir qui a compté, et un opposant
  peut demander une clé de lecture, voire une clé d'écriture pour son propre observateur ;
- **une reconstitution publique** : n'importe qui peut refaire le comptage sur les mêmes tronçons et
  les mêmes créneaux, et déposer ses propres enregistrements.

## 5. Les chiffres, et comment ils résistent

- **Unité** : déjections pour 100 m de voie et par passage — jamais un total brut, qui ne veut rien
  dire et se retourne contre celui qui le présente.
- **Comparaison** : tronçons traités contre zone témoin, sur plusieurs périodes. C'est le motif exact
  du jugement de Béziers : le juge compare des années, pas deux semaines.
- **Conditions en covariables** : météo, jour de collecte, marché, vacances, travaux. Une baisse après
  un passage de balayeuse n'est pas un effet du dispositif.
- **Méthode d'agrégation écrite avant** : médiane par tronçon, intervalle par rééchantillonnage, seuil
  de significativité. Écrite avant, elle n'est pas choisie pour le résultat.
- **Données brutes publiées** : JSON, CSV et GeoJSON, plus les empreintes. Une preuve reproductible
  est une preuve qu'on ne peut pas écarter.

## 6. Ouvert : ce que « ouvert » doit vouloir dire

Ouvrir le code ne suffit pas. Les quatre pièces qui rendent l'ensemble vérifiable par un tiers :

1. **protocole versionné** (les versions successives restent consultables, on ne réécrit pas le
   passé) ;
2. **schéma de données publié** avec le format des enregistrements ;
3. **code source ouvert**, exécutable par un tiers, sans dépendance à notre hébergement ;
4. **jeu de données ouvert** sous licence claire, avec les empreintes et les jetons d'horodatage.

## 7. La séquence, et pourquoi il ne faut pas commencer par l'application

Le risque de ce genre de projet est connu : deux mois d'application, zéro comptage.

1. **Semaine 1-2, à la main.** Fiche papier standardisée, téléphone, étiquettes imprimées, un
   tronçon, une zone témoin. Export des photos et des fiches, une empreinte globale par semaine,
   horodatée. Coût : du temps, quelques euros d'horodatage.
2. **Semaine 3-6.** On teste ce qui casse : deux observateurs en désaccord, une pluie, un marché, un
   tronçon où personne ne passe. C'est là qu'on apprend ce que doit gérer l'outil.
3. **Après, seulement si l'échelle le justifie** (plus de dix compteurs, ou une mairie qui veut
   reprendre l'instrument) : l'application hors ligne d'abord, clé par observateur, QR des étiquettes,
   registre en ajout seul, publication automatique des agrégats.

## 8. Ce que ça peut devenir

Le même instrument sert à tout ce qu'une administration ne mesure pas : déjections, dépôts sauvages,
bruit, chaleur de rue, bus qui ne passent pas, trottoirs impraticables. Une chaîne de preuve
citoyenne réutilisable — protocole, outil, données ouvertes — est un actif qui se prête ou se vend à
une association, une mairie, un journal, sans jamais vendre le dossier lui-même. Mais l'ordre compte :
c'est le pilote qui donne le droit d'en faire un produit, pas l'inverse.

Ce que cette architecture ne règle pas, et qu'il faut répéter : elle ne remplace ni l'invitation
écrite à l'adversaire, ni la zone témoin, ni la démonstration que l'identification classique est
insuffisante. Elle rend seulement les preuves que nous produisons impossibles à écarter pour de
mauvaises raisons.

Suite : écrire la fiche de relevé en une page, la règle photographique en une ligne (« l'étiquette et
la déjection dans le même cadre »), et le protocole de transfert à deux signatures. Tout le reste est
du logiciel, et le logiciel vient après.
