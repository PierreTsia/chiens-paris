# Pitch pour un collègue technique

Ce qu'on veut construire, ce qui est dur, et ce qu'on ne sait pas encore.

## Le produit en trois couches

1. Un registre des chiens parisiens. Une fiche par chien : identifiant I-CAD existant, empreinte
   génétique, propriétaire, adresse dans Paris, statut vaccinal, date d'enregistrement, statut
   (à jour / à renouveler / radié).
2. Une chaîne de prélèvement et d'analyse. Un agent ramasse une déjection non ramassée, la met dans
   un tube avec un numéro d'ordre, la chaîne part au laboratoire, le laboratoire renvoie un
   identifiant génétique, le système cherche la correspondance dans le registre et sort un nom. Le
   laboratoire détient la base génétique, la Ville ne détient que la correspondance prélèvement ->
   propriétaire, pour la durée de l'expérimentation. C'est la contrainte d'architecture principale,
   pas un détail de conformité : elle décide où vivent les données et qui peut interroger quoi.
3. Une application terrain. Pour l'agent : numéroter un prélèvement, géolocaliser, photographier,
   horodater, imprimer ou transmettre l'étiquette. Pour le propriétaire : s'enregistrer, prendre
   rendez-vous, télécharger l'attestation, voir ses droits (transports, espaces). Pour la mairie :
   compter, suivre les taux d'aboutissement, éditer les chiffres de l'évaluation.

## Volumes, pour dimensionner

- Pilote : 2 ou 3 arrondissements, environ 9 700 chiens identifiés, 5 000 enregistrés en année 1.
- Extension : 100 000 chiens, soit 100 000 prélèvements buccaux étalés sur deux à quatre ans.
- Débit vétérinaire : à 200 cabinets parisiens, 500 prélèvements par cabinet sur la durée totale.
  Ce n'est pas un problème de débit, c'est un problème de rendez-vous, de kit et de saisie.
- Analyses de déjections : de l'ordre de 500 par an au démarrage, 2 000 à 3 000 en régime établi.
- Coût unitaire vérifié : 34,10 € HT facturés par le laboratoire de Saint-Omer pour une analyse
  (source : FAQ de la Ville de Saint-Omer), 60,43 € HT tout compris au coût marginal dans notre
  modèle. À 500 analyses par an, le coût complet monte à 260 € l'unité ; à 2 000, il descend à 70 €.

## Ce qu'il faut attaquer en premier, par ordre de risque

1. La robustesse de l'ADN environnemental sur un trottoir. Une crotte ramassée reste-t-elle
   exploitable après une nuit de pluie, deux jours de soleil, un passage de balayeuse ? Personne ne
   le documente publiquement. C'est le risque numéro un du projet et il se teste en trois semaines,
   avec un laboratoire et vingt échantillons déposés dans des conditions contrôlées.
2. Le mélange et la contamination. Deux chiens sur le même trottoir, un prélèvement pris à la
   pince : quel taux de lecture, quel taux de fausse attribution ? La conséquence juridique d'une
   fausse attribution est un contentieux, pas une réclamation.
3. La chaîne de preuve. Un prélèvement qui n'est pas traçable ne vaut rien devant un juge. Il faut
   un numéro unique, un scellé, un horodatage, un accusé de réception du laboratoire et une durée de
   conservation décidée à l'avance.
4. Le délai de rendu. Un propriétaire doit savoir dans quel délai la contravention peut tomber. Si
   le laboratoire rend en six semaines, l'effet pédagogique disparaît.
5. La conformité. Analyse d'impact relative à la protection des données, registre des traitements,
   durée de conservation, information des personnes, et la question du fichier de personnes morales
   ou physiques qui n'existe pas encore. Béziers a perdu sur la preuve de nécessité, pas sur la
   technique, mais la LDH attaque aussi sur les données.

## Ce qu'on ne sait pas, et qu'il faut dire avant de coder

- Combien de chiens vivent réellement à Paris : 100 000 selon la Ville, 300 000 selon le chiffre qui
  circule. Tout le dimensionnement change d'un facteur trois.
- Quel taux d'aboutissement est atteignable. Notre seuil d'autofinancement est de 20 % des analyses
  abouties pour couvrir le coût marginal, 33 % pour le coût complet. Ce sont des calculs.
- Le temps agent par prélèvement (20 minutes dans notre modèle, 8 € au coût marginal) : à mesurer.
- Les capacités réelles des laboratoires sur ce volume, et leurs délais.

## Le test à trente jours, sans budget

1. Compter les déjections sur un périmètre de dix rues pendant deux semaines, matin et soir, avec un
   protocole écrit et deux compteurs. C'est ce que le tribunal a reproché à Béziers de ne pas avoir.
2. Demander des devis à trois laboratoires (Antagene, Genindexe, Animagene) sur 500, 2 000 et 5 000
   analyses, avec délai, taux de réussite annoncé et conditions de conservation.
3. Demander les pièces du marché de Saint-Omer et le bilan de Reims : documents administratifs
   communicables, réponse en un mois.
4. Déposer vingt échantillons témoins dans trois conditions (soleil, pluie simulée, deux jours
   d'attente) et faire analyser.

## Ce qu'il me faut de toi

Deux personnes et un cahier des charges de données : quelqu'un qui sait interroger un laboratoire de
génétique et lire un protocole de prélèvement, quelqu'un qui sait faire un registre avec des droits
d'accès et une analyse d'impact. Le reste, comptage, dossier, courriers administratifs, je m'en
occupe. Le budget d'entrée du test est de zéro euro ; le premier vrai poste de dépense est le
laboratoire, et il n'a lieu qu'après le comptage et les devis.

Détail des coûts : /root/chiens-paris/ADN-COUTS-FAISABILITE.md et section 7 du rapport complet.
Ce qui est prouvé, ville par ville : /root/chiens-paris/AUDIT-SOURCES.md.
