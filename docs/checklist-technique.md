# Checklist technique API et BDD

Suivi établi le 14 novembre 2026. À consulter avant une modification importante et à mettre à jour après vérification. Les points ouverts proviennent de la revue du projet ; vérifier leur état actuel avant intervention. Cette liste n'autorise pas à élargir une demande de l'utilisateur.

## Validations à prévoir

- [ ] Utiliser `date` pour les réservations et `datetime` pour les nettoyages, puis adapter leur passage aux services et au SQL.
- [ ] Vérifier que la fin est postérieure au début.
- [ ] Imposer des quantités strictement positives : lits, personnes, identifiants si pertinent.
- [ ] Limiter les longueurs des champs selon les colonnes SQL.
- [ ] Refuser les noms vides ou composés uniquement d'espaces et les mots de passe vides ; ne pas modifier silencieusement le mot de passe.
- [ ] Ajouter des contraintes SQL pour les quantités et les dates essentielles.

## Authentification et réponses

- [ ] Créer une route de connexion qui vérifie le mot de passe et délivre un token.
- [ ] Protéger les routes métier et appliquer les permissions selon l'identité authentifiée et le rôle en BDD.
- [ ] Ne pas utiliser un `id_personnel` envoyé par le client comme preuve d'identité.
- [ ] Choisir un identifiant de connexion unique et garantir son unicité en BDD.
- [ ] Transmettre `JWT_SECRET_KEY` au conteneur API lorsque l'authentification sera branchée.
- [x] `PersonnelPublic` aligné sur les champs publics du service et du script SQL : `id`, `nom`, `telephone` nullable et `id_role`, sans `prenom`. Les GET de collection et de recherche par rôle utilisent `list[PersonnelPublic]` ; le détail utilise `PersonnelPublic` (vérifié le 17 novembre 2026, sans accès à la BDD réelle).
- [ ] Conserver les messages métier des erreurs 404 au lieu de les remplacer systématiquement par « route inexistante ».
- [ ] Distinguer erreurs de connexion, erreurs SQL et violations de clés étrangères ; envisager 409 pour une suppression empêchée.
- [ ] Harmoniser les suppressions : 204 sans corps, ou 200 avec un message.
- [ ] Déployer avec HTTPS pour protéger les mots de passe pendant leur transport.

## Cohérence métier

- [ ] Refuser explicitement un rôle non autorisé dans les nettoyages avec HTTP 403, au lieu de retourner `None`.
- [ ] Vérifier les chevauchements de réservations à la création et à la modification, y compris les demandes concurrentes.
- [ ] Calculer la disponibilité pour une période à partir des réservations. Le booléen `reserve` ne représente pas un calendrier.
- [ ] Définir la capacité d'une chambre et vérifier `nb_personnes` par rapport à celle-ci.
- [ ] Décider si terminer un nettoyage rend automatiquement la chambre propre ; si oui, effectuer les deux mises à jour dans une seule transaction.

## BDD et déploiement

- [ ] Comparer le schéma réel de la VM aux scripts avant migration. `CREATE TABLE IF NOT EXISTS` ne modifie pas les tables existantes.
- [ ] Préparer les migrations nécessaires, notamment le retrait de l'ancienne colonne `numero` et de l'ancienne table `tour_de_garde` si elles existent encore. Leur état sur la VM n'a pas été vérifié.
- [ ] Prévoir l'initialisation explicite des tables : Compose n'exécutait pas les scripts BDD. Un montage dans `/docker-entrypoint-initdb.d` ne s'exécute qu'à l'initialisation d'un volume vide.
- [ ] Utiliser les mêmes variables pour le nom de base et l'utilisateur dans les services Compose API et MariaDB, au lieu de valeurs codées en dur côté MariaDB.
- [ ] Ajouter un contrôle de disponibilité MariaDB avant le démarrage de l'API.
- [ ] Prévoir des mots de passe hachés pour les comptes de démonstration si leur connexion doit être testée.
- [ ] Retirer `email` du SQL si ce champ est définitivement abandonné.
- [ ] Choisir explicitement l'accès réseau BDD : `127.0.0.1` sur la VM permet les accès locaux mais pas l'accès direct depuis le PC ; l'API dans Compose utilise `db:3306`.

## Corrections déjà constatées

Ces constats ne garantissent pas l'état de la VM et doivent être revérifiés après des modifications importantes.

- [x] Lors de la revue précédente : imports, démarrage Python et génération OpenAPI fonctionnels.
- [x] Ordre des routes chambres corrigé et paramètres des chemins de suppression alignés.
- [x] Création client cohérente entre modèle, route et service, avec hachage testé et vérification du mot de passe.
- [x] Hachage personnel présent dans la route et champ `mot_de_passe` dans le modèle, constatés le 14 novembre ; pas de test d'intégration BDD effectué.
- [x] Création de rôle : un seul `%s` pour `nom`, constaté le 14 novembre.
- [x] Comparaison du rôle nettoyage via `role["nom"].lower()`.
- [x] `date_fin` retiré du modèle de création de nettoyage, constaté le 14 novembre.
- [x] Anciens `updated.commit()` remplacés par `connection.commit()`.
- [x] Chambre limitée à `id`, `nb_lit`, `propre`, `reserve` dans les scripts ; références à `numero` retirées de l'API et des SQL.
- [x] Tours de garde retirés de l'API et des scripts SQL.
- [x] Démarrage Docker sur `API.main:app`, frontend dans `FRONTEND` et montage statique après les routes.

## Vérification du 17 novembre 2026 : résolution du conflit personnel

- Conflit de réapplication du stash résolu dans `API/routes/personnel.py` : conservation du chemin `/roles/{id_role}` et des modèles publics de réponse.
- Le service `show_role_personnel` utilise désormais `fetchall()` : la route renvoie une liste de `PersonnelPublic`, vide si aucun personnel ne correspond au rôle.
- Six requêtes ASGI en mémoire vérifiées : liste, détail avec téléphone nul, rôle avec plusieurs personnes, rôle sans résultat (`[]`), détail absent (404) et rôle invalide (422). Connexions BDD simulées ; filtrage des champs privés et paramètres SQL vérifiés.
- Import de l'application, modèles OpenAPI des trois GET et syntaxe des 21 fichiers Python de l'API vérifiés. Aucun changement de schéma, aucune migration ni connexion à MariaDB réelle pour cette intervention.

## Méthode de vérification

Pour chaque évolution, vérifier les modèles, les paramètres de routes, les signatures des services, les colonnes SQL, les transactions et les réponses HTTP. Distinguer les vérifications statiques et avec connexions simulées des tests réellement exécutés sur MariaDB. Ne pas annoncer une migration ou un déploiement comme réalisé sans l'avoir effectué.

## Vérification connexion du 17 novembre 2026

- Route `POST /auth/connexion` ajoutée : téléphone, mot de passe et type client/personnel ; vérification du hash existant et émission du JWT existant (30 minutes).
- Téléphones en doublon dans une même table refusés ; aucune contrainte SQL ni migration ajoutée.
- `JWT_SECRET_KEY` transmise par Compose ; sa valeur doit être définie dans l'environnement ou le fichier `.env`. Aucune valeur secrète créée ou modifiée.
- Page autonome `FRONTEND/connexion.html` : token dans `sessionStorage` pour l'onglet, suppression locale à la déconnexion. Les autres pages ne consomment pas encore ce token et les routes métier restent inchangées.
- Vérifications réussies : import et OpenAPI ; connexions client/personnel, JWT, compte absent, mauvais mot de passe, doublons et clé absente avec BDD simulée.
- Limites : aucun test MariaDB réel, navigateur, déploiement ou migration VM effectué. Les points historiques ci-dessus restent le suivi de la revue initiale.
- Réorganisation : modèle dans `API/models/auth.py`, logique et SQL dans `API/services/auth.py`, route limitée à un appel du service. Contrat HTTP inchangé ; import/OpenAPI et authentification client/personnel revérifiés avec BDD simulée, sans test MariaDB réel.
