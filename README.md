# DEV-APP-METIER

- [Schéma UML Hôtel-casino en Markdown](docs/uml-hotel-casino.md)

Pour initialiser MariaDB, exécuter dans cet ordre :

1. [create_bdd.sql](create_bdd.sql) pour créer la base et les tables.
2. [insert_donnees.sql](insert_donnees.sql) pour ajouter les données d'exemple.

Le script d'insertion utilise `WHERE NOT EXISTS` pour pouvoir être relancé sans ajouter de doublons. Il contient un client, deux chambres, trois rôles, trois membres du personnel, une réservation, un nettoyage et deux créneaux de garde.
