# Hôtel

Gestion d'un hôtel

rôles :
- clients
- Receptionistes
- Personnel d'entretien
- Personnel de sécurité
- Manager
- Manager hôtel
- Manager général


Règles de gestion :
- Que la chambre soit disponible avant réservation
- Que la chambre soit nétoyée avant l'arrivée des clients
- Avoir minimum 1 receptionniste 24h/24
- Avoir minimum 1 vigile 24h/24
- Le personnel d'entretient ne renettoie pas une chambre déjà nettoyée

Risques/enjeux








## User stories — Hôtel

- En tant que client, je peux consulter les chambres disponibles pour les dates de mon séjour afin de choisir une chambre adaptée.
- En tant que client, je peux réserver une chambre disponible afin de préparer mon séjour. Une chambre déjà réservée sur les mêmes dates ne peut pas être réservée une seconde fois.
- En tant que client, je peux consulter mes réservations afin de retrouver les informations de mon séjour.

-  En tant que réceptionniste, je peux consulter les réservations, les arrivées et les départs prévus afin d'organiser l'accueil des clients.
- En tant que réceptionniste, je peux créer une réservation pour un client afin de prendre en charge une demande à l'accueil, uniquement si la chambre est disponible aux dates demandées.
- En tant que réceptionniste, je peux enregistrer l'arrivée d'un client et lui attribuer une chambre disponible et nettoyée afin de l'accueillir dans de bonnes conditions.
-  En tant que réceptionniste, je peux enregistrer le départ d'un client afin de libérer sa chambre et de la signaler comme à nettoyer.

-  En tant que membre du personnel d'entretien, je peux consulter les chambres à nettoyer et les arrivées prévues afin de prioriser les chambres attendues par les clients.
-  En tant que membre du personnel d'entretien, je peux signaler qu'une chambre est en cours de nettoyage afin d'éviter qu'un collègue intervienne en même temps.
- En tant que membre du personnel d'entretien, je peux marquer une chambre comme nettoyée afin de permettre son attribution à un client. Une chambre déjà nettoyée ne peut pas faire l'objet d'un nouveau nettoyage tant que son état n'a pas changé.

- En tant que membre du personnel de sécurité, je peux consulter mon planning afin de connaître mes horaires et les zones à surveiller.
- En tant que membre du personnel de sécurité, je peux signaler un incident afin d'en informer le manager et d'en assurer le suivi.

- En tant que manager, je peux organiser le planning des réceptionnistes et du personnel de sécurité afin d'assurer la présence d'au moins un réceptionniste et un vigile 24 h/24. Le système me signale tout créneau non couvert.
- En tant que manager, je peux consulter l'occupation des chambres et leur état de nettoyage afin de suivre l'activité de l'hôtel et d'anticiper les arrivées.
| Roles | Voir les chambres dispo | Reserver une chambre | mettre une chambre à laver | consulter les chambres à laver | plannifier les cycles de garde | consulter les cycles de garde |
|---|---|---|---|---|---|---|
| clients | x |x |   |   | ||
| Receptionistes | x | x | x ||||
| Personnel d'entretien |x |||x|||
| Personnel de sécurité ||||||x|
| Manager garde |||||x|x|
| Manager hotel | x|x|x|

# Transport

Entreprise transport, Excel imprimer pour gestion des transport chaque jour. Faire une app pour gerer cette situation.
Les roles de l'app :
- Livreurs
- Clients
- Manager ( responsable de l'organisation )

Acces :
- Livreurs : acces au planning de ses livraisons et possibilité de finir une commande
- Clients : acces a ses commandes
- Manager : acces et modifications de tout les plannings

Règles de gestions :
- Verrifier que la commande, le camion et le livreurs sont tous disponnible sur le meme site de livraison
- Que le meme colis/camion/chauffeur n'est pas attribué 2 fois (ou plus)
- verifier que le volume annoncé des colis n'est pas superrieur au volume disponnible du vehicule
- verifier que les adresses des colis existe

Risques/enjeux
- Commande pendant la panne pas prise en compte
- Ne plus avoir de suivi sur les camions
- livreurs bloqués (sans adresses)

User story :
 En tant que ROLES je peux / peux pas faire :
- En tant que livreurs je peux lire les commandes qui me sont affilier
                    editer l'ordre de passage qui me sont affilier et qui sont a programmé a demain
- En tant que client je peux lire mes commandes et je peux editer le jour de passage
- En tant que manager je ne peux pas editer les ordres de passages
- En tant qu'admin je peux  tout faire

| Roles | Lire les livraison | Modifier les livraisons | ajouter les livraisons | finir(supprimer) une livraison | commander | programmer une commande |
|---|---|---|---|---|
| Admin | x | x | x
| Manager | x | x | x
| Livreur | o | o|
| Client | o | o |
