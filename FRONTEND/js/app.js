import { appelerApi } from './api.js';
import { chargerUtilisateur } from './session.js';

const application = document.querySelector('#application');
const message = document.querySelector('#message');
let utilisateur = null;
let expiration;
let generation = 0;
const envoyer = (url, method, donnees) => appelerApi(url, {
  method, headers: { 'Content-Type': 'application/json' },
  ...(donnees === undefined ? {} : { body: JSON.stringify(donnees) }),
});
const valeur = (form, nom) => form.elements.namedItem(nom).value;
const nombre = (form, nom) => Number(valeur(form, nom));
const normaliserBool = valeur => valeur === true || valeur === 1 || valeur === '1';
const maintenant = () => {
  const date = new Date();
  return new Date(date.getTime() - date.getTimezoneOffset() * 60000).toISOString().slice(0, 19).replace('T', ' ');
};
function afficherErreur(erreur) { message.textContent = erreur.message || 'Une erreur est survenue.'; }
function option(select, id, texte) { select.add(new Option(texte, String(id))); }
function ligne(liste, texte) {
  const li = document.createElement('li');
  const contenu = document.createElement('div');
  contenu.textContent = texte;
  li.append(contenu); liste.append(li); return li;
}
function action(parent, texte, traitement) {
  const bouton = document.createElement('button');
  bouton.type = 'button'; bouton.textContent = texte;
  bouton.addEventListener('click', () => executer(bouton, traitement));
  parent.append(bouton);
}
async function executer(bouton, traitement) {
  bouton.disabled = true; message.textContent = '';
  try {
    if (utilisateur && utilisateur.expiration <= Date.now()) {
      deconnecter(); throw new Error('Session expirée. Reconnectez-vous.');
    }
    await traitement();
  } catch (erreur) { afficherErreur(erreur); }
  finally { bouton.disabled = false; }
}
function formulaire(id, traitement) {
  const form = document.getElementById(id);
  form.addEventListener('submit', event => {
    event.preventDefault();
    executer(form.querySelector('button[type="submit"]'), () => traitement(form));
  });
  return form;
}
function deconnecter() {
  generation++; clearTimeout(expiration);
  sessionStorage.removeItem('access_token'); utilisateur = null;
  document.querySelector('#entete').hidden = true;
  message.textContent = ''; afficherPublic();
}
document.querySelector('#deconnexion').addEventListener('click', deconnecter);
window.addEventListener('session-expiree', () => {
  deconnecter(); message.textContent = 'Session expirée. Reconnectez-vous.';
});

const champsCompte = `
  <label>Nom<input name="nom" autocomplete="family-name" required></label>
  <label>Prénom<input name="prenom" autocomplete="given-name" required></label>
  <label>Téléphone<input name="telephone" type="tel" autocomplete="tel" required></label>
  <label>Mot de passe<input name="mot_de_passe" type="password" autocomplete="new-password" required></label>`;
function donneesCompte(form) {
  const donnees = Object.fromEntries(['nom', 'prenom', 'telephone', 'mot_de_passe'].map(nom => [nom, valeur(form, nom)]));
  for (const nom of ['nom', 'prenom', 'telephone']) {
    donnees[nom] = donnees[nom].trim();
    if (!donnees[nom]) throw new Error('Complétez tous les champs.');
  }
  return donnees;
}
function afficherPublic(inscription = false) {
  application.className = 'public'; application.setAttribute('aria-busy', 'false');
  application.innerHTML = inscription ? `
    <div class="carte"><h1>Créer un compte client</h1>
    <form id="inscription">${champsCompte}<button type="submit">Créer mon compte</button></form>
    <p class="note">L'inscription publique crée uniquement un compte client.</p>
    <button type="button" id="retour">Revenir à la connexion</button></div>` : `
    <div class="carte"><h1>Connexion</h1><form id="connexion">
    <label>Type de compte<select name="type_utilisateur"><option value="client">Client</option><option value="personnel">Personnel</option></select></label>
    <label>Téléphone<input name="telephone" type="tel" autocomplete="username" required></label>
    <label>Mot de passe<input name="mot_de_passe" type="password" autocomplete="current-password" required></label>
    <button type="submit">Se connecter</button></form>
    <p>Vous n'avez pas de compte ?</p><button type="button" id="inscrire">Créer un compte client</button></div>`;
  if (inscription) {
    document.querySelector('#retour').onclick = () => { message.textContent = ''; afficherPublic(); };
    formulaire('inscription', async form => {
      await envoyer('/clients/', 'POST', donneesCompte(form));
      afficherPublic(); message.textContent = 'Compte client créé. Vous pouvez vous connecter.';
    });
  } else {
    document.querySelector('#inscrire').onclick = () => { message.textContent = ''; afficherPublic(true); };
    formulaire('connexion', async form => {
      try {
        const resultat = await envoyer('/auth/connexion', 'POST', {
          telephone: valeur(form, 'telephone').trim(), mot_de_passe: valeur(form, 'mot_de_passe'),
          type_utilisateur: valeur(form, 'type_utilisateur'),
        });
        if (typeof resultat?.access_token !== 'string') throw new Error('Token absent de la réponse API.');
        sessionStorage.setItem('access_token', resultat.access_token);
        await demarrer();
      } finally { form.elements.mot_de_passe.value = ''; }
    });
  }
}

async function demarrer() {
  const version = ++generation;
  clearTimeout(expiration);
  application.setAttribute('aria-busy', 'true');
  try {
    const compte = await chargerUtilisateur();
    if (version !== generation) return;
    utilisateur = compte;
    if (!compte) { afficherPublic(); return; }
    application.className = '';
    document.querySelector('#entete').hidden = false;
    document.querySelector('#identite').textContent = `${compte.profil.nom} · ${compte.role}`;
    expiration = setTimeout(() => { deconnecter(); message.textContent = 'Session expirée. Reconnectez-vous.'; }, Math.max(0, compte.expiration - Date.now()));
    application.innerHTML = '<p>Chargement de votre espace…</p>';
    if (compte.role === 'entretien') await afficherEntretien();
    else await afficherReservations();
  } catch (erreur) {
    if (version !== generation) return;
    utilisateur = null; sessionStorage.removeItem('access_token');
    document.querySelector('#entete').hidden = true;
    afficherPublic(); afficherErreur(erreur);
  } finally { if (version === generation) application.setAttribute('aria-busy', 'false'); }
}

async function afficherReservations() {
  const compte = utilisateur;
  const accueil = compte.role === 'accueil';
  const [chambres, reservations, clients, roles] = await Promise.all([
    appelerApi('/chambres/'),
    appelerApi(accueil ? '/reservations/' : `/reservations/client/${compte.id}`),
    accueil ? appelerApi('/clients/') : Promise.resolve([]),
    accueil ? appelerApi('/roles/') : Promise.resolve([]),
  ]);
  if (utilisateur !== compte) return;
  application.innerHTML = `<h1>${accueil ? "Espace accueil" : "Mes réservations"}</h1>
    ${accueil ? `<section><h2>Chambres</h2><label>Statut<select id="filtre"><option value="toutes">Toutes</option><option value="libres">Disponibles</option><option value="reservees">Réservées</option></select></label><ul id="chambres"></ul></section>` : ''}
    <section><h2>${accueil ? 'Réservations' : 'Mes séjours'}</h2><ul id="reservations"></ul></section>
    <section><h2>Effectuer une réservation</h2>
    <p class="note">Les chambres proposées sont propres et libres selon leur statut actuel. La disponibilité pour les dates choisies est vérifiée à partir des réservations existantes, sans garantie contre deux demandes simultanées.</p>
    <form id="reservation"><div class="grille">
    ${accueil ? '<label>Client<select name="id_client" required></select></label>' : ''}
    <label>Chambre<select name="id_chambre" required></select></label>
    <label>Arrivée<input name="date_debut" type="date" required></label>
    <label>Départ<input name="date_fin" type="date" required></label>
    <label>Nombre de Personnes<input name="nb_personnes" type="number" min="1" step="1" required></label>
    </div><button type="submit">Réserver</button></form></section>
    ${accueil ? `<section><h2>Ajouter une chambre</h2><form id="chambre"><label>Nombre de lits<input name="nb_lit" type="number" min="1" step="1" required></label><button type="submit">Ajouter la chambre</button></form></section>
    <section><h2>Créer un compte</h2><form id="compte"><label>Type de compte<select name="type_compte"><option value="client">Client</option><option value="personnel">Personnel</option></select></label><label id="label-role" hidden>Rôle<select name="id_role"></select></label>${champsCompte}<button type="submit">Créer le compte</button></form></section>` : ''}`;
  const liste = document.querySelector('#reservations');
  const visibles = accueil ? reservations : reservations.filter(r => Number(r.id_client) === compte.id);
  if (!visibles.length) ligne(liste, 'Aucune réservation.');
  for (const r of visibles) {
    const client = clients.find(c => Number(c.id) === Number(r.id_client));
    ligne(liste, `Chambre ${r.id_chambre} · ${r.date_debut} · ${r.date_fin} · ${r.nb_personnes} personne(s)${accueil ? ` · ${client ? client.nom + ' ' + client.prenom : 'Client ' + r.id_client}` : ''}`);
  }
  const form = formulaire('reservation', async form => {
    const debut = valeur(form, 'date_debut'), fin = valeur(form, 'date_fin');
    const idChambre = nombre(form, 'id_chambre');
    if (fin <= debut) throw new Error("Le départ doit être après l'arrivée.");
    const existantes = await appelerApi(`/reservations/chambre/${idChambre}`);
    if (existantes.some(r => String(r.date_debut).slice(0, 10) < fin && String(r.date_fin).slice(0, 10) > debut)) {
      throw new Error('Cette chambre est déjà réservée sur cette période.');
    }
    await envoyer('/reservations/', 'POST', {
      date_debut: debut, date_fin: fin, nb_personnes: nombre(form, 'nb_personnes'),
      id_chambre: idChambre, id_client: accueil ? nombre(form, 'id_client') : compte.id,
    });
    await afficherReservations(); message.textContent = 'Réservation créée.';
  });
  const libres = chambres.filter(c => !normaliserBool(c.reserve) && normaliserBool(c.propre));
  option(form.elements.id_chambre, '', 'Choisir une chambre');
  for (const c of libres) option(form.elements.id_chambre, c.id, `Chambre ${c.id} · ${c.nb_lit} lit(s)`);
  if (!libres.length) form.querySelector('button').disabled = true;
  if (accueil) {
    formulaire('chambre', async form => {
      await envoyer('/chambres/', 'POST', { nb_lit: nombre(form, 'nb_lit') });
      await afficherReservations(); message.textContent = 'Chambre ajoutée.';
    });
    option(form.elements.id_client, '', 'Choisir un client');
    for (const c of clients) option(form.elements.id_client, c.id, `${c.nom} ${c.prenom} · ${c.telephone}`);
    afficherChambres(chambres);
    document.querySelector('#filtre').onchange = () => afficherChambres(chambres);
    const creation = formulaire('compte', async form => {
      const donnees = donneesCompte(form);
      const personnel = valeur(form, 'type_compte') === 'personnel';
      if (personnel) {
        donnees.id_role = nombre(form, 'id_role');
        if (!donnees.id_role) throw new Error('Sélectionnez un rôle existant.');
      }
      await envoyer(personnel ? '/personnels/' : '/clients/', 'POST', donnees);
      await afficherReservations(); message.textContent = 'Compte créé.';
    });
    option(creation.elements.id_role, '', 'Choisir un rôle');
    for (const r of roles) option(creation.elements.id_role, r.id, r.nom);
    creation.elements.type_compte.onchange = () => {
      const personnel = valeur(creation, 'type_compte') === 'personnel';
      document.querySelector('#label-role').hidden = !personnel;
      creation.elements.id_role.required = personnel;
    };
  }
}
function afficherChambres(chambres) {
  const filtre = document.querySelector('#filtre').value;
  const liste = document.querySelector('#chambres'); liste.replaceChildren();
  for (const c of chambres.filter(c => filtre === 'toutes' || (filtre === 'reservees' ? normaliserBool(c.reserve) : !normaliserBool(c.reserve)))) {
    const li = ligne(liste, `Chambre ${c.id} · ${c.nb_lit} lit(s) · ${normaliserBool(c.reserve) ? 'Réservée' : 'Disponible'} · ${normaliserBool(c.propre) ? 'Propre' : 'Sale'}`);
    if (normaliserBool(c.propre)) action(li, 'Signaler sale', async () => {
      await envoyer(`/chambres/proprete/${c.id}`, 'PUT', { propre: false });
      await afficherReservations(); message.textContent = 'Chambre signalée sale.';
    });
  }
  if (!liste.children.length) ligne(liste, 'Aucune chambre pour ce filtre.');
}

async function afficherEntretien() {
  const compte = utilisateur;
  const [sales, nettoyages] = await Promise.all([appelerApi('/chambres/sales'), appelerApi('/nettoyages/')]);
  if (utilisateur !== compte) return;
  const actifs = nettoyages.filter(n => !n.date_fin);
  application.innerHTML = `<h1>Espace entretien</h1><section><h2>Chambres sales à nettoyer</h2><ul id="sales"></ul></section><section><h2>Nettoyages en cours</h2><ul id="nettoyages"></ul><p class="note">Seul l'agent ayant démarré un nettoyage peut le terminer ou l'annuler depuis cette interface. Une annulation supprime le nettoyage.</p></section>`;
  const liste = document.querySelector('#sales');
  for (const chambre of sales.filter(c => !actifs.some(n => Number(n.id_chambre) === Number(c.id)))) {
    const li = ligne(liste, `Chambre ${chambre.id} · ${chambre.nb_lit} lit(s) · Sale`);
    action(li, 'Démarrer le nettoyage', async () => {
      const recents = await appelerApi(`/nettoyages/chambre/${chambre.id}`);
      if (recents.some(n => !n.date_fin)) throw new Error('Un nettoyage est déjà en cours pour cette chambre.');
      const resultat = await envoyer('/nettoyages/', 'POST', { date_debut: maintenant(), id_chambre: chambre.id, id_personnel: compte.id });
      if (!resultat?.id) throw new Error("Le serveur n'a pas confirmé le démarrage. Vérifiez que le rôle en base est nommé entretien.");
      await afficherEntretien(); message.textContent = 'Nettoyage démarré.';
    });
  }
  if (!liste.children.length) ligne(liste, 'Aucune chambre sale en attente.');
  const cours = document.querySelector('#nettoyages');
  for (const n of actifs) {
    const mien = Number(n.id_personnel) === compte.id;
    const li = ligne(cours, `Chambre ${n.id_chambre} · En cours depuis ${n.date_debut} · ${mien ? 'Votre nettoyage' : 'Autre agent'}`);
    if (!mien) continue;
    action(li, 'Terminer', async () => {
      // Deux opérations distinctes : le backend ne les regroupe pas en transaction.
      await envoyer(`/chambres/proprete/${n.id_chambre}`, 'PUT', { propre: true });
      try {
        const resultat = await envoyer(`/nettoyages/${n.id}`, 'PUT', { date_fin: maintenant(), id_personnel: compte.id });
        if (!resultat) throw new Error('Fin de nettoyage non confirmée par le serveur.');
      } catch (erreur) {
        throw new Error(`La chambre a été marquée propre, mais la fin du nettoyage n'est pas confirmée. Réessayez Terminer. ${erreur.message}`);
      }
      await afficherEntretien(); message.textContent = 'Nettoyage terminé et chambre marquée propre.';
    });
    action(li, 'Annuler', async () => {
      if (!window.confirm(`Annuler le nettoyage de la chambre ${n.id_chambre} ?`)) return;
      // Rétablir sale, notamment après une fin partiellement échouée.
      await envoyer(`/chambres/proprete/${n.id_chambre}`, 'PUT', { propre: false });
      await envoyer(`/nettoyages/${n.id}`, 'DELETE');
      await afficherEntretien(); message.textContent = 'Nettoyage annulé. La chambre reste sale.';
    });
  }
  if (!cours.children.length) ligne(cours, 'Aucun nettoyage en cours.');
}

demarrer();
