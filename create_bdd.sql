CREATE DATABASE IF NOT EXISTS HotelBDD;

USE HotelBDD;

CREATE TABLE IF NOT EXISTS client (
    id INT AUTO_INCREMENT PRIMARY KEY,
    num_tel VARCHAR(20) NOT NULL,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL
) 

CREATE TABLE IF NOT EXISTS chambre (
    numero INT AUTO_INCREMENT PRIMARY KEY,
    nb_lit INT NOT NULL,
    reserver BIT NOT NULL,
    propre BIT NOT NULL
) 

CREATE TABLE IF NOT EXISTS `role` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL
) 

CREATE TABLE IF NOT EXISTS personnel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    id_role INT NOT NULL,

    FOREIGN KEY (id_role) REFERENCES `role`(id)
) 

CREATE TABLE IF NOT EXISTS reservation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_debut_resa DATE NOT NULL,
    date_fin_resa DATE NOT NULL,
    id_client INT NOT NULL,
    id_chambre INT NOT NULL,

    FOREIGN KEY (id_client) REFERENCES client(id),
    FOREIGN KEY (id_chambre) REFERENCES chambre(numero)
) 

CREATE TABLE IF NOT EXISTS nettoyage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_debut DATETIME NOT NULL,
    date_fin DATETIME NOT NULL,
    id_personnel INT NOT NULL,
    id_chambre INT NOT NULL,

    FOREIGN KEY (id_personnel) REFERENCES personnel(id),
    FOREIGN KEY (id_chambre) REFERENCES chambre(numero)
) 
CREATE TABLE IF NOT EXISTS tour_de_garde (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_debut DATETIME NOT NULL,
    date_fin DATETIME NOT NULL,
    id_personnel INT NOT NULL,

    FOREIGN KEY (id_personnel) REFERENCES personnel(id)
);
