# Interfaces et protection des routes

## Ce qui est implémenté

Toutes les modifications de cette intervention sont dans `FRONTEND`.

- `index.html` : point d'entrée commun, connexion centrée sans session, inscription client et espaces par rôle.
- `style.css` : présentation commune et responsive.
- `js/app.js` : connexion, inscription client, réservations, chambres, nettoyages et création de comptes par l'accueil.
- `js/session.js` : lecture de l'expiration et du sujet JWT, récupération du profil et du rôle via les routes existantes.
- `js/api.js` : envoi du Bearer token, remontée des erreurs et retour à la connexion sur un 401 métier.
- `connexion.html` et `js/connexion.js` : ancienne adresse redirigée vers l'accueil commun. `connexion.css` et `js/clients.js` sont conservés mais ne sont plus chargés par ces pages.

Le client n'a aucun champ permettant de choisir un autre client. L'identifiant envoyé à la réservation vient de sa session. L'accueil choisit le client et peut créer des clients ou des personnels avec n'importe quel rôle existant renvoyé par `/roles/`. Aucun rôle n'est créé automatiquement.

Le personnel d'entretien voit les chambres sales sans nettoyage actif et, séparément, les nettoyages en cours de tous les agents. Il peut agir sur ses propres nettoyages. Annuler utilise le DELETE existant : la ligne est supprimée, pas conservée avec un statut « annulé ».

## Limites actuelles du backend

Ces restrictions sont des règles d'interface, pas des autorisations serveur. Les routes métier actuelles ne vérifient pas le JWT : quelqu'un peut encore appeler directement une API avec un autre identifiant. Le décodage du JWT dans le navigateur ne vérifie pas sa signature.

Le JWT existant contient `sub` (`client:ID` ou `personnel:ID`) et `exp`. Le frontend récupère ensuite `/clients/{id}` ou `/personnels/{id}`, puis `/roles/{id_role}`. Il n'existe pas de route `/auth/me` : aucune n'est appelée ni inventée.

Les noms `Accueil`, `Receptionniste`, `Réceptionniste` et `personnel d'accueil` donnent l'espace accueil ; `Entretien` et `personnel d'entretien` donnent l'espace entretien, sans sensibilité à la casse. Un autre rôle ne reçoit aucun espace. Attention : le service nettoyage actuel n'accepte que le nom `entretien` après passage en minuscules ; son nom réel en base doit donc être `Entretien` pour pouvoir démarrer et terminer un nettoyage.

La fin d'un nettoyage utilise deux appels : chambre propre, puis date de fin. Une panne entre les deux laisse un état partiel, signalé à l'écran ; on peut réessayer « Terminer ». Le backend devrait effectuer les deux écritures dans une transaction. L'annulation rétablit d'abord l'état sale, puis supprime la ligne.

Les chambres proposées à la réservation sont propres et non réservées selon leurs booléens actuels. Les chevauchements sont vérifiés avant l'envoi avec `/reservations/chambre/{id}`. Ce contrôle ne remplace pas une transaction serveur face aux réservations simultanées. Le champ `nb_lit` est affiché ; aucune équivalence non définie entre lits et capacité en personnes n'est inventée. La création actuelle ne met pas automatiquement `reserve` à jour : l'affichage du statut actuel dépend donc de l'état existant en base et ne constitue pas un calendrier.

`PersonnelCreate` demande un prénom, mais le service actuel ne le stocke pas. Le formulaire l'envoie pour respecter le modèle existant. Les comptes de démonstration SQL n'ont pas de mots de passe hachés ; ils ne peuvent pas servir de preuve de connexion réussie. Il faut un compte créé par l'API et une `JWT_SECRET_KEY` configurée.

## Guide : mettre en place une vraie protection

Les extraits backend ci-dessous sont des propositions à appliquer séparément. Aucun fichier API n'a été modifié dans cette intervention. Lire `docs/checklist-technique.md` avant de les appliquer et mettre à jour le suivi après les tests.

### 1. Vérifier l'authentification

Déjà côté frontend : `js/session.js` refuse un JWT mal formé ou expiré ; `js/app.js` supprime la session à son expiration et affiche la connexion. `js/api.js` joint `Authorization: Bearer ...` à chaque appel et supprime la session lorsqu'une route métier renvoie 401.

Côté serveur, réutiliser `exiger_token_valide` de `API/securite.py`. Cette dépendance existante vérifie la signature HS256 et l'expiration avec `JWT_SECRET_KEY`. Une erreur doit interrompre le traitement avant toute lecture métier ou écriture.

### 2. Retrouver le rôle depuis la base

Créer par exemple `API/dependances.py` avec cette dépendance. Ne jamais prendre le rôle ou l'identifiant personnel dans le formulaire comme preuve d'identité.

```python
from fastapi import Depends, HTTPException
from API.securite import exiger_token_valide
from API.services.client import show_client
from API.services.personnel import show_personnel
from API.services.role import show_role


def utilisateur_courant(claims: dict = Depends(exiger_token_valide)):
    try:
        type_compte, identifiant = claims["sub"].split(":")
        identifiant = int(identifiant)
        if type_compte not in ("client", "personnel") or identifiant <= 0:
            raise ValueError()
    except (KeyError, ValueError, TypeError, AttributeError):
        raise HTTPException(status_code=401, detail="Identité invalide")

    try:
        if type_compte == "client":
            profil = show_client(identifiant)
            role = "client"
        else:
            profil = show_personnel(identifiant)
            nom = show_role(profil["id_role"])["nom"].strip().lower()
            role = {
                "accueil": "accueil",
                "receptionniste": "accueil",
                "réceptionniste": "accueil",
                "personnel d'accueil": "accueil",
                "entretien": "entretien",
                "personnel d'entretien": "entretien",
            }.get(nom)
            if role is None:
                raise HTTPException(status_code=403, detail="Rôle non autorisé")
    except HTTPException as erreur:
        if erreur.status_code == 404:
            raise HTTPException(status_code=401, detail="Compte introuvable")
        raise
    return {"id": identifiant, "type": type_compte, "role": role}


def exiger_roles(*roles):
    def verifier(utilisateur: dict = Depends(utilisateur_courant)):
        if utilisateur["role"] not in roles:
            raise HTTPException(status_code=403, detail="Accès interdit")
        return utilisateur
    return verifier
```

Les erreurs BDD doivent rester des erreurs serveur ; ne pas les transformer en « mauvais mot de passe ». Le rôle est relu en base à chaque requête pour prendre en compte ses modifications.

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

Dans `API/routes/reservation.py`, protéger la liste globale pour l'accueil et contrôler le propriétaire pour la lecture par client :

```python
from fastapi import Depends, HTTPException
from API.dependances import exiger_roles


@router.get("/")
def get_reservations(u: dict = Depends(exiger_roles("accueil"))):
    return show_reservations()


@router.get("/client/{id_client}")
def get_reservation_client(
    id_client: int,
    u: dict = Depends(exiger_roles("client", "accueil")),
):
    if u["role"] == "client" and u["id"] != id_client:
        raise HTTPException(status_code=403, detail="Accès interdit")
    return show_reservation_client(id_client)


@router.post("/", status_code=201)
def create_reservation(
    reservation: ReservationCreate,
    u: dict = Depends(exiger_roles("client", "accueil")),
):
    id_client = u["id"] if u["role"] == "client" else reservation.id_client
    return insert_reservation(
        reservation.date_debut, reservation.date_fin,
        reservation.nb_personnes, reservation.id_chambre, id_client,
    )
```

Ces exemples remplacent les fonctions correspondantes ; ne pas ajouter des routes en doublon. Contrôler aussi les lectures par réservation et par dates, ainsi que PUT/DELETE : vérifier le propriétaire ou réserver ces actions à l'accueil. La route de lecture par chambre est actuellement utilisée pour les disponibilités : prévoir une réponse limitée aux dates occupées pour les clients, sans exposer les identités des autres clients, puis adapter le frontend à ce contrat.

Appliquer cette matrice à toutes les routes, y compris les variantes :

| Fichier | Autorisations à appliquer |
| --- | --- |
| `API/routes/auth.py` | Connexion publique, mot de passe vérifié, token signé. |
| `API/routes/client.py` | POST public avec `ClientCreate` uniquement ; liste globale pour accueil ; profil individuel pour soi ou accueil ; modification/suppression explicitement autorisées selon la politique choisie. |
| `API/routes/personnel.py` | POST pour accueil ; profil individuel pour soi ou accueil ; listes et gestion pour accueil. |
| `API/routes/role.py` | Lecture de son rôle ou lecture pour accueil ; interdire par défaut création/modification/suppression de rôles tant qu'une politique n'est pas définie. |
| `API/routes/chambre.py` | Lectures utiles pour les trois rôles ; signaler sale pour accueil ; marquer propre pour entretien ; autres créations/modifications/suppressions pour accueil selon la politique retenue. |
| `API/routes/reservation.py` | Client : ses réservations et création pour soi ; accueil : gestion pour tous ; entretien : refus. |
| `API/routes/nettoyage.py` | Entretien : lire les opérations utiles, créer avec son ID serveur, terminer/annuler uniquement ses opérations actives ; autres rôles : refus. |

Dans `API/routes/nettoyage.py`, obtenir `u` avec `Depends(exiger_roles("entretien"))`. À la création, passer `u["id"]` au service, jamais l'ID envoyé par le navigateur. Avant PUT/DELETE, charger `show_nettoyage(nettoyage_id)`, vérifier `id_personnel == u["id"]` et `date_fin is None`, sinon retourner 403 ou 409 selon le cas. Déplacer les vérifications et la transaction dans `API/services/nettoyage.py` pour éviter les opérations concurrentes incohérentes.

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
