import { appelerApi } from "./api.js";

async function chargerClients() {
    const liste = document.querySelector("#liste-clients");
    const message = document.querySelector("#message");

    message.textContent = "Chargement…";
    liste.replaceChildren();

    try {
        const clients = await appelerApi("/clients/");

        for (const client of clients) {
            const element = document.createElement("li");
            element.className = "list-group-item";
            element.textContent = `${client.nom} ${client.prenom}`;
            

            liste.append(element);
        }

        message.textContent = clients.length === 0
            ? "Aucun client pour le moment."
            : "";
    } catch (erreur) {
        message.textContent = `Impossible de charger les clients`;
    }
}

// Lance le chargement à l’ouverture de la page.
chargerClients();


async function ajouterClients() {
    try {
        const resultat = await appelerApi("/clients/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                nom: document.querySelector("#nom").value,
                prenom: document.querySelector('#prenom').value,
                email: document.querySelector("#email").value,
                telephone: document.querySelector("#telephone").value,
            }),
        });

        console.log(resultat);
    } catch (erreur) {
        console.error(erreur.message);
    }
}