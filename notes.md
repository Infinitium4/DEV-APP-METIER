# Hôtel-casino

Hôtel d'un casino

rôles :
- clients
- Receptionistes
- Personnel d'entretien
- Personnel de sécurité
- Manager hôtel
- Manager général


Règles de gestion :
- Que la chambre soit disponible avant réservation
- Que la chambre soit nétoyée avant l'arrivée des clients
- Avoir minimum 1 receptionniste 24h/24
- Avoir minimum 1 vigile 24h/24
- Le personnel d'entretient ne renettoie pas une chambre déjà nettoyée

Risques/enjeux
-
-


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
