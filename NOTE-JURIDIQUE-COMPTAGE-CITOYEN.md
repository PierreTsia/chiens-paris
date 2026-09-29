# Note juridique — ce qui donne une valeur juridique au comptage citoyen

29 septembre 2026. Question posée : suffit-il d'une photo géodatée stockée sur un serveur, ou faut-il
un protocole ? Réponse courte : non, une photo sur un serveur ne prouve rien — ce qui prouve, c'est
la manière dont le relevé est préconstitué, contradictoire et daté. Détail ci-dessous. Rien n'a été
voté.

## 1. Ce que le juge a réellement reproché à Béziers

C'est le point de départ, et il fixe tout le reste. Le tribunal administratif de Montpellier annule
l'arrêté du 12 mai 2023 par jugement du 6 mai 2025, sur trois motifs, dans cet ordre :

1. **L'atteinte n'est pas démontrée.** « Aucune pièce du dossier ne permet de corroborer les éléments
   indiqués dans l'exposé des motifs de l'arrêté, notamment l'atteinte qui serait portée à la
   sécurité et à la salubrité publique par le nombre de déjections canines ramassées au cours des
   années 2020, 2021, 2022. »
2. **L'inefficacité des mesures déjà prises n'est pas démontrée** — la mairie n'a pas non plus
   établi que ce qu'elle faisait déjà ne suffisait pas.
3. **La mesure n'est « ni nécessaire, ni adaptée, ni proportionnée »**, et l'identification
   classique (tatouage ou marquage, obligatoire au titre de l'article L. 212-10 du code rural)
   n'est pas démontrée insuffisante.

Conséquence pour un comptage : **ce n'est pas un relevé, c'est un dossier de preuve**, et il doit
répondre à ces trois points. Le premier exige un **volume daté sur plusieurs périodes** — le juge
compare 2020, 2021, 2022, il ne compare pas une semaine à une autre. Un comptage unique ne ferme
aucun de ces trous.

## 2. Les trois piliers d'un relevé qui tient

Un comptage citoyen est une preuve par témoins et par écrits : le juge administratif apprécie
librement les moyens de preuve, mais il apprécie la crédibilité de leur fabrication. Trois mots
comptent plus que la photo.

**a. Préconstitué.** Le protocole — tronçons, créneaux, règle de comptage, dates de début et de fin —
est publié avant le premier passage, et ne bouge plus. Un protocole connu après coup est réputé
arrangé ; un protocole publié d'avance est opposable. C'est la même logique que le préenregistrement
d'un essai clinique, et c'est ce qui distingue un relevé d'un argument.

**b. Contradictoire.** Deux observateurs distincts par passage, dont un qui n'est pas partie prenante.
Et surtout : la partie adverse est **informée par écrit et invitée** — courrier à la mairie, à la
mairie d'arrondissement et au préfet, avec le protocole, les dates et l'invitation à désigner un
observateur. Si elle ne vient pas, la preuve de l'invitation reste au dossier : c'est exactement ce
qui prive l'autre partie du droit de contester la méthode. Sans cette pièce, tout relevé est
« unilatéral ».

**c. Daté et intègre.** C'est ici que le serveur lambda ne suffit pas. Un fichier photo, une date
EXIF et un stockage quelconque ne prouvent ni la date ni la non-modification : les métadonnées se
réécrivent en deux clics, et personne ne peut affirmer que le fichier conservé est celui qui a été
pris. Ce qu'il faut, et ce qui est vérifiable par un tiers :

- une **fiche de relevé** identique à chaque passage : tronçon, heure, nombre, position, conditions
  (météo, balayeuse, marché, vacances, travaux), nom des deux observateurs, photo ;
- une **empreinte SHA-256 de chaque fiche et de chaque photo**, imprimée dans le tableau publié ;
- un **horodatage électronique** de ces empreintes, chaque semaine. Un horodatage **qualifié**
  (règlement eIDAS n° 910/2014, art. 41 § 2 et 42, prestataire de services de confiance qualifié,
  protocole RFC 3161) bénéficie d'une **présomption d'exactitude de la date et d'intégrité des
  données** : c'est à celui qui conteste de démontrer la fausseté. Un horodatage simple reste
  recevable mais n'emporte aucune présomption, et l'ancrage en chaîne de blocs, pratique et gratuit,
  reste apprécié librement par le juge — utile parce que n'importe qui peut le vérifier, mais ce
  n'est pas un service de confiance qualifié.
- la **publication des données brutes** (fiches, photos, tableaux) : une preuve que l'adversaire peut
  refaire est une preuve qu'il ne peut pas écarter.

## 3. Le piège à ne pas recréer : les données personnelles

Le dispositif est attaqué sur le fichage des propriétaires ; un comptage citoyen qui photographie la
rue en grand angle et conserve des plaques d'immatriculation reconstitue l'argument de l'adversaire.
Donc : cadrage serré sur la déjection, pas de visage ni de plaque, aucun fichier de personnes, aucune
géolocalisation d'individus, une finalité écrite et une durée de conservation annoncée. Le registre
du comptage enregistre des tronçons et des nombres, pas des gens.

## 4. Ce qu'un comptage citoyen ne peut pas faire

Il ne permet pas de verbaliser. La contravention est prouvée par procès-verbal ou rapport d'un agent
habilité, et, pour les contraventions, l'article 537 du code de procédure pénale prévoit que ces
rapports « font foi jusqu'à preuve contraire » et que la preuve contraire ne peut être rapportée que
par écrit ou par témoins. Le comptage citoyen sert à **justifier la mesure devant le juge
administratif**, pas à constater l'infraction. Les deux chaînes sont distinctes et ne doivent pas
être mélangées dans le discours public — c'est le mélange qui fait dire « ils veulent nous ficher ».

## 5. Les trois niveaux d'escalade

1. **Comptage citoyen avec protocole publié et horodaté** (coût : du temps). Suffisant pour un
   conseil d'arrondissement, un budget participatif et un premier article de presse.
2. **Convention avec la mairie ou la mairie d'arrondissement**, les agents relayant le comptage :
   le relevé change de nature et devient un document administratif.
3. **Constat de commissaire de justice**, contradictoire, sur un échantillon de passages seulement :
   c'est l'acte le plus difficile à contester, et il coûte cher — d'où l'intérêt de le réserver à la
   démonstration finale, une fois le protocole rodé et les chiffres stabilisés.

À faire en parallèle, et gratuitement : **demander les pièces de l'administration** (extractions
DansMaRue sur le secteur, statistiques de propreté, marché de nettoiement, bilan des campagnes
précédentes). Ce sont des documents administratifs communicables ; ils donnent la base officielle que
le juge réclamait à Béziers, et ils obligent la Ville à prendre position par écrit.

## 6. Ce que le comptage ne suffira pas à fermer

Le motif n° 3 de Béziers — l'identification classique est-elle suffisante ? — ne se règle pas en
comptant. Il se règle par un raisonnement : un tatouage ou un fichier I-CAD identifie un chien, mais
ne relie pas une déjection à son propriétaire, faute de quoi aucune attribution n'est possible. C'est
un argument juridique autonome, à écrire séparément, et la proportionnalité (périmètre réduit, durée
bornée, gratuité de l'identification, alternatives) reste à démontrer — le juge administratif contrôle
les trois, pas seulement l'utilité.

## Sources

- LDH, « Béziers : l'identification génétique des chiens » (citations du jugement du 6 mai 2025,
  TA Montpellier) : https://www.ldh-france.org/beziers-lidentification-genetique-des-chiens/
- Article 537 du code de procédure pénale (force probante des procès-verbaux et rapports en matière
  contraventionnelle ; texte à lire dans le code, partie législative, livre II, titre III) :
  https://www.legifrance.gouv.fr/codes/texte_lc/LEGITEXT000006071154/
- Sénat, question écrite rappelant le régime de l'article 537 (rapports faisant foi jusqu'à preuve
  contraire, preuve contraire par écrit ou témoins) :
  https://www.senat.fr/questions/base/2007/qSEQ070801568.html
- ANSSI, les services de confiance (horodatage électronique qualifié, eIDAS) :
  https://cyber.gouv.fr/reglementation/reglementation-identite-confiance-numerique/securite-echanges-voie-electronique/reglement-eidas/services-de-confiance/
- Règlement (UE) n° 910/2014 (eIDAS), art. 41 et 42 ; articles 1366 et 1367 du code civil.
- Le comptage national des oiseaux des jardins (LPO et Muséum national d'histoire naturelle) comme
  modèle de comptage citoyen : voir l'annexe C du rapport complet.
