# Consignes pour les agents

Avant toute modification importante de l'API, de la BDD, de l'authentification ou du déploiement, lire [la checklist technique](docs/checklist-technique.md).

- Vérifier l'état réel des fichiers : la checklist est un suivi, pas une preuve que chaque problème existe encore.
- Respecter le périmètre demandé ; ne pas corriger automatiquement toute la checklist.
- Préserver les modifications en cours de l'utilisateur.
- Contrôler la cohérence modèles → routes → services → SQL et les conséquences sur la base existante.
- Ne pas confondre modification des scripts d'initialisation et migration de la BDD de la VM.
- Après un changement concerné, mettre à jour la checklist avec les vérifications effectuées et leurs limites.
- Les chambres ont uniquement les champs `id`, `nb_lit`, `propre`, `reserve`. Ne pas réintroduire `numero`.
- La fonctionnalité tours de garde a été abandonnée. Ne pas la réintroduire.
