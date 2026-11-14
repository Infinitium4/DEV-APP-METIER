-- Initialisation uniquement : CREATE TABLE IF NOT EXISTS ne migre pas les tables existantes.
-- Creation de la base et des tables pour MariaDB.
CREATE DATABASE IF NOT EXISTS ma_database;

USE ma_database;

CREATE TABLE IF NOT EXISTS client (
    id INT AUTO_INCREMENT PRIMARY KEY,
    telephone VARCHAR(20) NOT NULL,
    email VARCHAR(255) NULL,
    mot_de_passe_hash VARCHAR(255) NULL,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS chambre (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nb_lit INT NOT NULL,
    reserve BOOLEAN NOT NULL DEFAULT FALSE,
    propre BOOLEAN NOT NULL DEFAULT TRUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `role` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS personnel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    telephone VARCHAR(20) NULL,
    mot_de_passe_hash VARCHAR(255) NULL,
    id_role INT NOT NULL,

    FOREIGN KEY (id_role) REFERENCES `role`(id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS reservation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_debut DATE NOT NULL,
    date_fin DATE NOT NULL,
    nb_personnes INT NOT NULL,
    id_client INT NOT NULL,
    id_chambre INT NOT NULL,

    FOREIGN KEY (id_client) REFERENCES client(id),
    FOREIGN KEY (id_chambre) REFERENCES chambre(id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS nettoyage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_debut DATETIME NOT NULL,
    date_fin DATETIME NULL,
    id_personnel INT NOT NULL,
    id_chambre INT NOT NULL,

    FOREIGN KEY (id_personnel) REFERENCES personnel(id),
    FOREIGN KEY (id_chambre) REFERENCES chambre(id)
) ENGINE=InnoDB;
