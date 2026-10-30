# DEV-APP-METIER

- [Schéma UML Hôtel-casino en Markdown](docs/uml-hotel-casino.md)

Pour initialiser MariaDB, exécuter dans cet ordre :

1. [create_bdd.sql](create_bdd.sql) pour créer la base et les tables.
2. [insert_donnees.sql](insert_donnees.sql) pour ajouter les données d'exemple.

Le script d'insertion regroupe les données par table avec `INSERT IGNORE`. Les identifiants fixes permettent de relancer le script : une ligne dont la clé primaire existe déjà est ignorée. Il contient un client, deux chambres, trois rôles, trois membres du personnel, une réservation, un nettoyage et deux créneaux de garde.

Ce jeu de données est destiné à une base de démonstration initialement vide. Une même valeur avec un autre identifiant n'est pas considérée comme un doublon ; les contrôles de chevauchement des réservations et des gardes doivent être assurés par l'application.
