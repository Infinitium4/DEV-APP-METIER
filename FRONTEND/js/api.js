export async function appelerApi(url, options = {}) {
  const headers = new Headers(options.headers);
  const token = sessionStorage.getItem('access_token');
  if (token) headers.set('Authorization', `Bearer ${token}`);
  const reponse = await fetch(url, { ...options, headers });
  if (!reponse.ok) {
    const donnees = await reponse.json().catch(() => null);
    const detail = typeof donnees?.detail === 'string' ? donnees.detail : `Erreur HTTP ${reponse.status}`;
    if (reponse.status === 401 && token && url !== '/auth/connexion') {
      sessionStorage.removeItem('access_token');
      window.dispatchEvent(new Event('session-expiree'));
    }
    throw new Error(detail);
  }
  return reponse.status === 204 ? null : reponse.json();
}
