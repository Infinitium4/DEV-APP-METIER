# Vérification du 13 novembre 2026

La partie clients et le contrôle JWT fonctionnent après les corrections ci-dessous. L'application complète n'est pas encore terminée : la connexion utilisateur et les permissions manquent, et plusieurs routes métier échouent.

## Corrections effectuées

- Imports adaptés à la réorganisation dans `API/` : `API.main`, `API.routes.auth` et `API.securite`.
- Serveur relancé depuis la racine avec `python -m uvicorn API.main:app --host 127.0.0.1 --port 8000 --reload --env-file .env`.
- API clients alignée sur la colonne actuelle `telephone`. La colonne `num_tel` a disparu de la BDD pendant les contrôles. Les réponses acceptent un téléphone nul pour les lignes existantes, conformément au schéma réel.
- Paramètre de `DELETE /clients/{client_id}` corrigé pour utiliser l'identifiant du chemin.
- `mot_de_passe_hash` exclu des trois lectures publiques du personnel par sélection explicite des colonnes autorisées.

## Vérifications réussies

| Partie | Vérification réellement effectuée |
| --- | --- |
| Démarrage | Import de `API.main` et démarrage Uvicorn réussis. |
| BDD | `/api` répond 200 ; lecture des structures et des données publiques réussie. |
| Documentation | `/docs`, `/redoc` et `/openapi.json` répondent 200. |
| Interface | Page `/` et modules JavaScript servis en 200 ; Chrome sans interface affiche les trois clients attendus. |
| CSS | Ressource Bootstrap répond 200. |
| Création client | POST réel : 201 ; hash Argon2 persisté, bon mot de passe accepté et mauvais refusé. |
| Lecture client | GET du client temporaire : 200, uniquement `id`, `nom`, `prenom`, `telephone`. |
| Modification client | PUT réel : 200 ; prénom modifié en BDD et hash de mot de passe conservé. |
| Suppression client | DELETE réel du client temporaire : 204. |
| Validation | Création sans mot de passe refusée en 422. |
| JWT | Token absent, mal signé ou expiré : 401 ; token valide : 200 sur `/auth/test`. |
| Personnel | Liste, détail et lecture par rôle : 200, sans champ de mot de passe ni hash. |
| Syntaxe | 25 fichiers Python analysés et deux modules JavaScript vérifiés sans erreur de syntaxe. |

Le contrôle ciblé final comporte **15 vérifications réussies**. Le client temporaire d'identifiant 5 a été supprimé ; le nombre de clients est de 3 avant et après. Nos écritures n'ont concerné que cette ligne de test. Le compteur des identifiants n'a pas été réinitialisé. Les profils Chrome temporaires ont également été supprimés.

## Échecs HTTP constatés

| Routes | Résultat observé | Cause constatée dans le code |
| --- | --- | --- |
| GET `/chambres/sales`, `/chambres/reserves`, `/chambres/reservable` | 422 | La route `/{chambre_id}` est déclarée avant ces chemins et intercepte leurs noms. |
| GET `/chambres/{chambre_id}`, `/chambres/propre/{chambre_id}` | 500 | Les requêtes utilisent `id`, alors que la clé de `chambre` est `numero`. |
| GET `/reservations/dates/{reservation_id}` | 500 | La requête lit `date_debut` et `date_fin` au lieu de `date_debut_resa` et `date_fin_resa`. |

Autres défauts constatés dans les modules métier :

- Deux routes chambres portent le même chemin `/propre/{chambre_id}` ; un avertissement d'identifiant OpenAPI dupliqué apparaît.
- Les chemins PUT de propreté et réservation sont assemblés en `/chambresproprete/...` et `/chambresreserve/...`, faute de `/` initial.
- Les requêtes chambres utilisent aussi `reserve` alors que la BDD contient `reserver`.
- Hors clients, plusieurs routes DELETE attendent encore un identifiant en paramètre de requête au lieu de celui du chemin. Elles n'ont pas été exécutées sur les données existantes.

## Échecs reproduits sans écrire dans la BDD

- Appel de la route de création chambre avec un `ChambreCreate` valide : `AttributeError` sur `nom`, car ce modèle déclare uniquement `nb_lit`.
- Appel de la route de modification nettoyage : `AttributeError` sur `date_debut`, absent de `NettoyageUpdate`.
- Modifications du personnel et des rôles avec connexion simulée : HTTP 500 ; `updated.commit()` est appelé sur le nombre de lignes modifiées et la connexion ne reçoit pas de `commit()`.

Les écritures réelles de ces modules métier n'ont pas été testées et ne sont pas présentées comme validées.

## Authentification encore à terminer

- L'interface actuelle affiche une liste de clients ; elle ne contient pas de formulaire de connexion.
- `/auth/test` existe, mais aucune route `/auth/connexion` n'émet encore un JWT après vérification d'un compte et de son mot de passe.
- Les listes métier répondent sans token ; les contrôles de rôle et d'accès aux données ne sont pas encore appliqués.
- Le modèle et le service de création du personnel ne prennent pas encore en charge son mot de passe.
- `ajouterClients` dans le JavaScript n'est relié à aucun formulaire présent et son contenu ne correspond pas au contrat de création actuel : il manque notamment le mot de passe.

## Limites de cette vérification

- Docker n'a pas été exécuté.
- Les scripts `BDD/create_bdd.sql` et `BDD/insert_donnees.sql` conservent l'ancien schéma, notamment `num_tel`. Ils restent à aligner avec l'API et la base actuelle avant de recréer une base.
- Les réponses 500 génériques des services masquent la différence entre une connexion impossible et une requête SQL incorrecte.
- Les tests JWT établissent la validité du token de test ; l'existence et les droits du compte en BDD ne sont pas encore vérifiés par cette dépendance.

Aucun mot de passe, token, hash réel ou clé secrète n'est conservé dans ce rapport.
