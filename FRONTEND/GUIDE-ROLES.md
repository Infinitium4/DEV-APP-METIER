# Interfaces et protection des routes

## Ce qui est implémenté

La protection est désormais appliquée dans l'API et l'interface. La matrice actuelle des routes est décrite dans [docs/acces-par-role.md](../docs/acces-par-role.md).

- `index.html` : point d'entrée commun, connexion centrée sans session, inscription client et espaces par rôle.
- `style.css` : présentation commune et responsive.
- `js/app.js` : connexion, inscription client, réservations, chambres, nettoyages et création de comptes par l'accueil.
- `js/session.js` : lecture de l'expiration et du sujet JWT, récupération du profil et du rôle via les routes existantes.
- `js/api.js` : envoi du Bearer token, remontée des erreurs et retour à la connexion sur un 401 métier.
- `connexion.html` et `js/connexion.js` : ancienne adresse redirigée vers l'accueil commun. `connexion.css` et `js/clients.js` sont conservés mais ne sont plus chargés par ces pages.

Le client n'a aucun champ permettant de choisir un autre client. L'identifiant envoyé à la réservation vient de sa session. L'accueil choisit le client, peut ajouter une chambre en indiquant son nombre de lits et créer des clients. Seuls les managers hôtel/général peuvent créer ou modifier du personnel et attribuer les rôles existants. Les rôles réceptionniste sont affichés dans l'espace accueil. Aucun rôle n'est créé automatiquement.

Le personnel d'entretien voit les chambres sales sans nettoyage actif et, séparément, les nettoyages en cours de tous les agents. Il peut agir sur ses propres nettoyages. Annuler utilise le DELETE existant : la ligne est supprimée, pas conservée avec un statut « annulé ».

## Limites actuelles du backend

Les routes métier vérifient maintenant le JWT, le compte, le rôle et les droits de propriétaire concernés. La connexion et l'inscription client restent publiques. Le décodage du JWT dans le navigateur sert seulement à l'affichage ; l'autorisation est contrôlée par le serveur.

Le JWT existant contient `sub` (`client:ID` ou `personnel:ID`) et `exp`. Le frontend récupère ensuite `/clients/{id}` ou `/personnels/{id}`, puis `/roles/{id_role}`. Il n'existe pas de route `/auth/me` : aucune n'est appelée ni inventée.

Les libellés réceptionniste/accueil, entretien et leurs variantes sont normalisés, y compris les accents et apostrophes. Les managers hôtel/général disposent des espaces accueil et entretien ; ils seuls peuvent gérer les comptes du personnel. Sécurité et manager de garde ont un espace sans opérations disponibles, puisque les gardes ont été abandonnées.

La fin d'un nettoyage utilise deux appels : chambre propre, puis date de fin. Une panne entre les deux laisse un état partiel, signalé à l'écran ; on peut réessayer « Terminer ». Le backend devrait effectuer les deux écritures dans une transaction. L'annulation rétablit d'abord l'état sale, puis supprime la ligne.

Les chambres proposées à la réservation sont propres et non réservées selon leurs booléens actuels. Les chevauchements sont vérifiés avant l'envoi avec `/reservations/chambre/{id}`. Ce contrôle ne remplace pas une transaction serveur face aux réservations simultanées. Le champ `nb_lit` est affiché ; aucune équivalence non définie entre lits et capacité en personnes n'est inventée. La création actuelle ne met pas automatiquement `reserve` à jour : l'affichage du statut actuel dépend donc de l'état existant en base et ne constitue pas un calendrier.

`PersonnelCreate` demande un prénom, mais le service actuel ne le stocke pas. Le formulaire l'envoie pour respecter le modèle existant. Les comptes de démonstration SQL n'ont pas de mots de passe hachés ; ils ne peuvent pas servir de preuve de connexion réussie. Il faut un compte créé par l'API et une `JWT_SECRET_KEY` configurée.

## Guide : mettre en place une vraie protection

Les contrôles ci-dessous sont intégrés dans les fichiers API. Lire `docs/checklist-technique.md` avant de modifier leurs règles ; la matrice active dans `docs/acces-par-role.md` précise les droits de chaque opération.

### 1. Vérifier l'authentification

Déjà côté frontend : `js/session.js` refuse un JWT mal formé ou expiré ; `js/app.js` supprime la session à son expiration et affiche la connexion. `js/api.js` joint `Authorization: Bearer ...` à chaque appel et supprime la session lorsqu'une route métier renvoie 401.

Côté serveur, réutiliser `exiger_token_valide` de `API/securite.py`. Cette dépendance existante vérifie la signature HS256 et l'expiration avec `JWT_SECRET_KEY`. Une erreur doit interrompre le traitement avant toute lecture métier ou écriture.

### 2. Retrouver le rôle depuis la base

Les fonctions sont dans `API/dependances.py` :

- `utilisateur_courant` utilise le `sub` du JWT vérifié, vérifie l'existence du compte et relit le rôle en BDD.
- `normaliser_role` accepte les variantes de noms présentes dans les scripts et le tableau de `notes.md`.
- `exiger_roles` renvoie 403 si le compte n'a pas un rôle autorisé. Les groupes `ACCUEIL`, `MANAGERS`, `RESERVATIONS`, `NETTOYAGES` et `CHAMBRES_SALES` évitent de répéter les libellés dans chaque route.

Les erreurs BDD restent des erreurs serveur ; elles ne sont pas transformées en « mauvais mot de passe ». Le rôle est relu à chaque requête pour prendre en compte ses modifications.

### 3. Empêcher l'accès aux vues sans session

Déjà dans `FRONTEND/js/app.js` : `demarrer()` charge la session avant de construire les espaces. Sans utilisateur, seule `afficherPublic()` s'exécute. Les interfaces protégées ne sont pas présentes dans le HTML initial. L'expiration ramène au formulaire.

Pour une future page HTML séparée, charger un module avant de rendre ses données :

```javascript
import { chargerUtilisateur } from './session.js';

let utilisateur;
try { utilisateur = await chargerUtilisateur(); }
catch { utilisateur = null; }
if (!utilisateur) {
  window.location.replace('./index.html');
} else {
  // Construire la vue et charger uniquement ses données autorisées.
}
```

### 4. Restreindre les routes selon les rôles et le propriétaire

Chaque route métier utilise les dépendances de `API/dependances.py`. Un groupe entier partageant les mêmes rôles peut les déclarer dans son `APIRouter`, comme les nettoyages. Les chambres utilisent des contrôles par opération car leurs droits diffèrent.

- Clients : profil et réservations personnels ; les disponibilités d'une chambre ne divulguent pas les identités des autres clients.
- Réception : gestion des réservations, des chambres et des comptes clients.
- Les réservations ne se modifient plus : supprimer puis recréer une réservation pour la remplacer. La nouvelle création vérifie à nouveau la disponibilité.
- Entretien : signalement et suivi des chambres à nettoyer ; modification/annulation de ses nettoyages actifs uniquement.
- Managers hôtel/général : droits opérationnels étendus, gestion du personnel et des rôles.
- Connexion et inscription client : publiques. La création publique utilise uniquement `ClientCreate` et ne peut pas créer de personnel.

L'identité de l'agent vient du JWT, pas du corps HTTP. Les services vérifient l'affectation et l'état actif sous verrou SQL avant de terminer ou supprimer un nettoyage. Le démarrage refuse une chambre propre ou déjà affectée. L'affectation initiale est celle de l'agent connecté.

La fin du nettoyage et la mise à jour de la propreté restent deux opérations distinctes. Aucun schéma SQL ni migration n'est modifié pour ces contrôles.

### 5. Diriger vers la bonne interface

Déjà dans `FRONTEND/js/app.js` : après connexion et au rechargement, `demarrer()` choisit `afficherEntretien()` pour entretien, sinon `afficherReservations()` pour client/accueil. Le rôle inconnu est refusé dans `session.js`. La redirection de `connexion.html` vers `index.html` conserve une seule entrée, sans route dynamique supplémentaire.

### 6. Résister à la saisie directe d'une URL

Dans le frontend actuel, il n'existe qu'une page d'espace commun ; ajouter un fragment à l'URL ne change pas les droits. Pour une future page réservée à l'accueil :

```javascript
const utilisateur = await chargerUtilisateur().catch(() => null);
if (!utilisateur || utilisateur.role !== 'accueil') {
  window.location.replace('./index.html');
} else {
  // Afficher l'espace accueil.
}
```

Cela masque la vue, mais le fichier HTML/JS reste public avec le montage `StaticFiles` actuel de `API/main.py`. Ne pas mettre de données sensibles dans des fichiers statiques. Une URL directe `/reservations/`, un script externe ou un JWT modifié doivent être bloqués par les dépendances API ci-dessus ; une redirection JavaScript ne peut pas assurer cette protection.

### 7. Compléter et vérifier côté serveur

- Dans les services réservation : dates et quantités valides, client existant, disponibilité contrôlée sous transaction/verrou afin de refuser deux créations concurrentes pour la même chambre et période. Ne pas se fier aux validations HTML.
- Dans les services nettoyage : chambre sale, absence d'autre opération active, propriété du nettoyage, fin et propreté mises à jour ensemble. L'annulation doit avoir une sémantique serveur définie.
- Dans les modèles personnel/client : ne pas accepter un rôle personnel sur l'inscription publique ; limiter les champs et garantir l'unicité de l'identifiant de connexion en BDD après audit des doublons.
- Dans les services personnel : aligner le prénom entre modèle, service et SQL, ou le retirer du contrat si ce champ est abandonné. Préparer une migration si le schéma change.
- Utiliser HTTPS en déploiement. Garder la clé de signature côté serveur. Une déconnexion `sessionStorage` ne révoque pas un JWT déjà copié : il reste valable jusqu'à son expiration, sauf ajout d'une révocation serveur.
- Tester 401 sans token/avec token expiré ou altéré ; 403 avec rôle incorrect ; impossibilité pour client A de lire/réserver au nom de B ; impossibilité de créer du personnel sans accueil ; refus des actions sur le nettoyage d'un autre agent. Tester également les succès de chaque rôle et les appels directs sans navigateur.

La mécanique `Depends` utilisée dans ces propositions correspond aux [dépendances d'utilisateur courant de FastAPI](https://fastapi.tiangolo.com/tutorial/security/get-current-user/). Les extraits sont adaptés au dépôt et ne sont pas encore intégrés ni validés sur MariaDB.

## Vérifications de cette intervention

Syntaxe JavaScript vérifiée avec Node. Tests exécutés avec réponses API simulées : résolution client/entretien/accueil/réceptionniste, refus d'un rôle inconnu, JWT mal formé ou expiré, en-tête Bearer, suppression de session après 401 et réponse DELETE 204 sans JSON. Aucun test dans un navigateur ni avec MariaDB réelle effectué.

Pour la recette réelle, ouvrir l'application depuis le serveur API et tester successivement : inscription client publique, connexion puis rechargement, réservation du client sans sélecteur de propriétaire, sélection d'un client et création d'un personnel à l'accueil, démarrage/fin/annulation d'un nettoyage avec un compte Entretien, expiration et déconnexion. Vérifier en base les écritures et simuler une panne entre les deux appels de fin de nettoyage.
