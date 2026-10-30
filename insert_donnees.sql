-- Donnees d'exemple pour MariaDB : executer create_bdd.sql auparavant.
-- Chaque WHERE NOT EXISTS evite de reinserer une donnee deja presente.
USE HotelBDD;

START TRANSACTION;

-- Roles.
INSERT INTO `role` (nom)
SELECT 'Receptionniste'
WHERE NOT EXISTS (
    SELECT 1 FROM `role` WHERE nom = 'Receptionniste'
);

INSERT INTO `role` (nom)
SELECT 'Entretien'
WHERE NOT EXISTS (
    SELECT 1 FROM `role` WHERE nom = 'Entretien'
);

INSERT INTO `role` (nom)
SELECT 'Securite'
WHERE NOT EXISTS (
    SELECT 1 FROM `role` WHERE nom = 'Securite'
);

SET @role_reception = (SELECT MIN(id) FROM `role` WHERE nom = 'Receptionniste');
SET @role_entretien = (SELECT MIN(id) FROM `role` WHERE nom = 'Entretien');
SET @role_securite = (SELECT MIN(id) FROM `role` WHERE nom = 'Securite');

-- Client.
INSERT INTO client (num_tel, nom, prenom)
SELECT '0600000001', 'Dupont', 'Marie'
WHERE NOT EXISTS (
    SELECT 1 FROM client
    WHERE num_tel = '0600000001' AND nom = 'Dupont' AND prenom = 'Marie'
);

SET @client_marie = (
    SELECT MIN(id) FROM client
    WHERE num_tel = '0600000001' AND nom = 'Dupont' AND prenom = 'Marie'
);

-- Chambres : le numero identifie chaque chambre.
INSERT INTO chambre (numero, nb_lit, reserver, propre)
SELECT 101, 2, 0, 1
WHERE NOT EXISTS (
    SELECT 1 FROM chambre WHERE numero = 101
);

INSERT INTO chambre (numero, nb_lit, reserver, propre)
SELECT 102, 1, 0, 0
WHERE NOT EXISTS (
    SELECT 1 FROM chambre WHERE numero = 102
);

-- Personnel.
INSERT INTO personnel (nom, id_role)
SELECT 'Claire Martin', @role_reception
WHERE NOT EXISTS (
    SELECT 1 FROM personnel
    WHERE nom = 'Claire Martin' AND id_role = @role_reception
);

INSERT INTO personnel (nom, id_role)
SELECT 'Sophie Bernard', @role_entretien
WHERE NOT EXISTS (
    SELECT 1 FROM personnel
    WHERE nom = 'Sophie Bernard' AND id_role = @role_entretien
);

INSERT INTO personnel (nom, id_role)
SELECT 'Karim Petit', @role_securite
WHERE NOT EXISTS (
    SELECT 1 FROM personnel
    WHERE nom = 'Karim Petit' AND id_role = @role_securite
);

SET @personnel_reception = (
    SELECT MIN(id) FROM personnel
    WHERE nom = 'Claire Martin' AND id_role = @role_reception
);
SET @personnel_entretien = (
    SELECT MIN(id) FROM personnel
    WHERE nom = 'Sophie Bernard' AND id_role = @role_entretien
);
SET @personnel_securite = (
    SELECT MIN(id) FROM personnel
    WHERE nom = 'Karim Petit' AND id_role = @role_securite
);

-- Reservation : ne pas ajouter de sejour qui chevauche une reservation existante.
INSERT INTO reservation (date_debut_resa, date_fin_resa, id_client, id_chambre)
SELECT '2026-11-01', '2026-11-03', @client_marie, 101
WHERE NOT EXISTS (
    SELECT 1 FROM reservation
    WHERE id_chambre = 101
      AND date_debut_resa < '2026-11-03'
      AND date_fin_resa > '2026-11-01'
);

-- Nettoyage termine avant le sejour de Marie.
INSERT INTO nettoyage (date_debut, date_fin, id_personnel, id_chambre)
SELECT '2026-10-31 10:00:00', '2026-10-31 10:30:00', @personnel_entretien, 101
WHERE NOT EXISTS (
    SELECT 1 FROM nettoyage
    WHERE id_chambre = 101
      AND id_personnel = @personnel_entretien
      AND date_debut = '2026-10-31 10:00:00'
      AND date_fin = '2026-10-31 10:30:00'
);

-- Exemples de creneaux de reception et de securite.
INSERT INTO tour_de_garde (date_debut, date_fin, id_personnel)
SELECT '2026-11-01 06:00:00', '2026-11-01 14:00:00', @personnel_reception
WHERE NOT EXISTS (
    SELECT 1 FROM tour_de_garde
    WHERE id_personnel = @personnel_reception
      AND date_debut < '2026-11-01 14:00:00'
      AND date_fin > '2026-11-01 06:00:00'
);

INSERT INTO tour_de_garde (date_debut, date_fin, id_personnel)
SELECT '2026-11-01 22:00:00', '2026-11-02 06:00:00', @personnel_securite
WHERE NOT EXISTS (
    SELECT 1 FROM tour_de_garde
    WHERE id_personnel = @personnel_securite
      AND date_debut < '2026-11-02 06:00:00'
      AND date_fin > '2026-11-01 22:00:00'
);

COMMIT;
