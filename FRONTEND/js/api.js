export async function appelerApi(url, options = {}) {
  const reponse = await fetch(url, options);

  if (!reponse.ok) {
    throw new Error(`Erreur HTTP ${reponse.status}`);
  }

  return reponse.status === 204 ? null : reponse.json();
}