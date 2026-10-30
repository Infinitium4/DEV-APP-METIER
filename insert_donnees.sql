-- Donnees de demonstration pour MariaDB : executer create_bdd.sql auparavant.
-- Les identifiants fixes servent aux relations et a la detection des doublons.
-- Si une cle primaire existe deja, INSERT IGNORE conserve la ligne existante.
-- Ce jeu de donnees est prevu pour une base de demonstration initialement vide.
USE HotelBDD;

START TRANSACTION;

INSERT IGNORE INTO `role` (id, nom) VALUES
    (1, 'Receptionniste'),
    (2, 'Entretien'),
    (3, 'Securite');

INSERT IGNORE INTO client (id, num_tel, nom, prenom) VALUES
    (1, '0600000001', 'Dupont', 'Marie');

INSERT IGNORE INTO chambre (numero, nb_lit, reserver, propre) VALUES
    (101, 2, 0, 1),
    (102, 1, 0, 0);

INSERT IGNORE INTO personnel (id, nom, id_role) VALUES
    (1, 'Claire Martin', 1),
    (2, 'Sophie Bernard', 2),
    (3, 'Karim Petit', 3);

INSERT IGNORE INTO reservation
    (id, date_debut_resa, date_fin_resa, id_client, id_chambre) VALUES
    (1, '2026-11-01', '2026-11-03', 1, 101);

INSERT IGNORE INTO nettoyage
    (id, date_debut, date_fin, id_personnel, id_chambre) VALUES
    (1, '2026-10-31 10:00:00', '2026-10-31 10:30:00', 2, 101);

INSERT IGNORE INTO tour_de_garde
    (id, date_debut, date_fin, id_personnel) VALUES
    (1, '2026-11-01 06:00:00', '2026-11-01 14:00:00', 1),
    (2, '2026-11-01 22:00:00', '2026-11-02 06:00:00', 3);

COMMIT;
