import asyncio
from datetime import datetime, timedelta
import importlib
import json
from unittest.mock import MagicMock
from zoneinfo import ZoneInfo

import pytest
from API.main import app
from API.securite import creer_token


@pytest.fixture(autouse=True)
def isolation(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "unit-test-secret-at-least-32-bytes-long")

    def forbidden(*args, **kwargs):
        raise AssertionError("A unit test must never access the real database")

    for name in ("auth", "chambre", "client", "nettoyage", "personnel", "reservation", "role"):
        monkeypatch.setattr(importlib.import_module(f"API.services.{name}"), "get_connection", forbidden)
    monkeypatch.setattr("API.dependances.show_client", lambda identifiant: {"id": identifiant})
    monkeypatch.setattr("API.dependances.show_personnel", lambda identifiant: {"id": identifiant, "id_role": identifiant})
    monkeypatch.setattr("API.dependances.show_role", lambda identifiant: {
        "nom": {4: "Receptionniste", 5: "Entretien", 9: "Manager hotel"}[identifiant]
    })


def request(method, path, payload=None, compte=None):
    async def execute():
        headers = [(b"content-type", b"application/json")]
        if compte:
            token = creer_token(compte[1], compte[0], "unit-test-secret-at-least-32-bytes-long")
            headers.append((b"authorization", f"Bearer {token}".encode()))
        scope = {
            "type": "http", "asgi": {"version": "3.0"}, "http_version": "1.1",
            "method": method, "scheme": "http", "path": path, "raw_path": path.encode(),
            "query_string": b"", "root_path": "", "headers": headers,
            "client": ("127.0.0.1", 1), "server": ("test", 80),
        }
        events = []

        async def receive():
            return {"type": "http.request", "body": json.dumps(payload).encode(), "more_body": False}

        async def send(event):
            events.append(event)

        await app(scope, receive, send)
        status = next(e["status"] for e in events if e["type"] == "http.response.start")
        body = b"".join(e.get("body", b"") for e in events if e["type"] == "http.response.body")
        return status, json.loads(body) if body else None

    return asyncio.run(execute())


def reservation():
    today = datetime.now(ZoneInfo("Europe/Paris")).date()
    return {
        "date_debut": str(today + timedelta(days=10)),
        "date_fin": str(today + timedelta(days=12)),
        "nb_personnes": 1, "id_chambre": 101, "id_client": 6,
    }


def test_inscription_publique_et_lectures_protegees(monkeypatch):
    monkeypatch.setattr("API.routes.client.hacher_mot_de_passe", lambda password: "mock-hash")
    insertion = MagicMock(return_value={"id": 99})
    monkeypatch.setattr("API.routes.client.insert_client", insertion)
    assert request("POST", "/clients/", {
        "nom": "Test", "prenom": "Test", "telephone": "0699999999", "mot_de_passe": "test",
    })[0] == 201
    assert request("GET", "/clients/")[0] == 401
    assert request("GET", "/clients/", compte=("client", 6))[0] == 403
    insertion.assert_called_once()


@pytest.mark.parametrize("compte", [("client", 6), ("personnel", 4), ("personnel", 5)])
def test_creation_personnel_interdite_aux_non_managers(compte):
    assert request("POST", "/personnels/", {
        "nom": "Test", "prenom": "Test", "telephone": "0699999999", "mot_de_passe": "test", "id_role": 1,
    }, compte)[0] == 403


@pytest.mark.parametrize("champ,valeur", [
    ("date_debut", "2000-01-01"), ("date_fin", "2000-01-01"),
    ("date_debut", "2030-02-30"), ("id_chambre", 0), ("id_client", -1), ("nb_personnes", 0),
])
def test_validation_reservation(champ, valeur):
    assert request("POST", "/reservations/", {**reservation(), champ: valeur}, ("client", 6))[0] == 422


def test_reservation_pour_autrui_interdite():
    assert request("POST", "/reservations/", {**reservation(), "id_client": 7}, ("client", 6))[0] == 403


@pytest.mark.parametrize("rows,status,detail", [
    ([None], 404, "Chambre introuvable"),
    ([{"id": 101}, None, None], 404, "Client introuvable"),
    ([{"id": 101}, {"id": 88}], 409, None),
    ([{"id": 101}, None, {"id": 6}], 201, None),
])
def test_creation_et_conflits_reservation(monkeypatch, rows, status, detail):
    db = MagicMock()
    cursor = db.cursor.return_value.__enter__.return_value
    cursor.fetchone.side_effect = rows
    cursor.lastrowid = 99
    monkeypatch.setattr("API.services.reservation.get_connection", lambda: db)
    resultat, body = request("POST", "/reservations/", reservation(), ("client", 6))
    assert resultat == status
    if detail:
        assert body["detail"] == detail
    db.begin.assert_called_once()
    db.close.assert_called_once()
    if status == 201:
        db.commit.assert_called_once()
    else:
        db.rollback.assert_called_once()
        db.commit.assert_not_called()


def test_reservation_modification_supprimee():
    assert "put" not in app.openapi()["paths"]["/reservations/{reservation_id}"]
    assert request("PUT", "/reservations/99", reservation(), ("client", 6))[0] == 405


def test_suppression_reservation_proprietaire(monkeypatch):
    monkeypatch.setattr("API.routes.reservation.show_reservation", lambda identifiant: {"id_client": 6})
    suppression = MagicMock(return_value=None)
    monkeypatch.setattr("API.routes.reservation.supprimer_reservation", suppression)
    assert request("DELETE", "/reservations/99", compte=("client", 7))[0] == 403
    suppression.assert_not_called()
    assert request("DELETE", "/reservations/99", compte=("client", 6))[0] == 204


def test_identite_nettoyage_issue_du_token(monkeypatch):
    insertion = MagicMock(return_value={"id": 99})
    monkeypatch.setattr("API.routes.nettoyage.insert_nettoyage", insertion)
    payload = {"date_debut": "2099-01-01 10:00:00", "id_chambre": 101, "id_personnel": 999}
    assert request("POST", "/nettoyages/", payload, ("client", 6))[0] == 403
    insertion.assert_not_called()
    assert request("POST", "/nettoyages/", payload, ("personnel", 5))[0] == 201
    assert insertion.call_args.args[2] == 5


@pytest.mark.parametrize("rows,status", [
    ([None], 404), ([{"id": 101, "propre": 1}], 409),
    ([{"id": 101, "propre": 0}, {"id": 88}], 409),
    ([{"id": 101, "propre": 0}, None], 201),
])
def test_demarrage_nettoyage(monkeypatch, rows, status):
    db = MagicMock()
    cursor = db.cursor.return_value.__enter__.return_value
    cursor.fetchone.side_effect = rows
    cursor.lastrowid = 99
    monkeypatch.setattr("API.services.nettoyage.get_connection", lambda: db)
    payload = {"date_debut": "2099-01-01 10:00:00", "id_chambre": 101}
    assert request("POST", "/nettoyages/", payload, ("personnel", 5))[0] == status
    db.begin.assert_called_once()
    db.close.assert_called_once()
    if status == 201:
        db.commit.assert_called_once()
    else:
        db.rollback.assert_called_once()
        db.commit.assert_not_called()


def test_nettoyage_indisponibilite_bdd(monkeypatch):
    def fail():
        raise RuntimeError("Connection unavailable")

    monkeypatch.setattr("API.services.nettoyage.get_connection", fail)
    assert request("POST", "/nettoyages/", {
        "date_debut": "2099-01-01 10:00:00", "id_chambre": 101,
    }, ("personnel", 5))[0] == 500
