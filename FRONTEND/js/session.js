import { appelerApi } from './api.js';

// Décodage pour l'affichage uniquement : seule l'API peut vérifier la signature JWT.
export function lireIdentite(token) {
  const charge = token.split('.')[1];
  const normalise = charge.replace(/-/g, '+').replace(/_/g, '/');
  const octets = Uint8Array.from(atob(normalise.padEnd(Math.ceil(normalise.length / 4) * 4, '=')), c => c.charCodeAt(0));
  const contenu = JSON.parse(new TextDecoder().decode(octets));
  const resultat = /^(client|personnel):([1-9][0-9]*)$/.exec(contenu.sub);
  if (!resultat || !Number.isFinite(contenu.exp) || contenu.exp * 1000 <= Date.now()) {
    throw new Error('Session invalide ou expirée. Reconnectez-vous.');
  }
  return { type: resultat[1], id: Number(resultat[2]), expiration: contenu.exp * 1000 };
}

export async function chargerUtilisateur() {
  const token = sessionStorage.getItem('access_token');
  if (!token) return null;
  let identite;
  try { identite = lireIdentite(token); }
  catch (erreur) { sessionStorage.removeItem('access_token'); throw erreur; }
  const profil = await appelerApi(`/${identite.type === 'client' ? 'clients' : 'personnels'}/${identite.id}`);
  let role = 'client';
  if (identite.type === 'personnel') {
    const donnees = await appelerApi(`/roles/${profil.id_role}`);
    const nom = donnees.nom.trim().toLowerCase().replace(/\u2019/g, "'");
    role = ({ accueil: 'accueil', receptionniste: 'accueil', 'r\u00e9ceptionniste': 'accueil', entretien: 'entretien', "personnel d'accueil": 'accueil', "personnel d'entretien": 'entretien' })[nom];
    if (!role) throw new Error(`Aucune interface prévue pour le rôle : ${donnees.nom}.`);
  }
  return { ...identite, profil, role };
}
