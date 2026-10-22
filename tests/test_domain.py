import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from tests.conftest import login

EXPERIMENT = {
    "name": "Baseline",
    "model": "RandomForest",
    "dataset_version": "v1",
    "metric_name": "F1",
    "metric_value": 0.84,
    "notes": "Synthetic",
}


def create_project(client):
    response = client.post("/api/projects", json={"name": "Demanda", "description": "Demo"})
    assert response.status_code == 201, response.text
    return response.json()["id"]


def test_crud_filters_summary_and_deletion_rule(authenticated):
    client = authenticated
    project_id = create_project(client)
    assert (
        client.put(f"/api/projects/{project_id}", json={"name": "Nuevo"}).json()["name"] == "Nuevo"
    )
    assert client.get(f"/api/projects/{project_id}").status_code == 200
    response = client.post(f"/api/projects/{project_id}/experiments", json=EXPERIMENT)
    assert response.status_code == 201
    exp_id = response.json()["id"]
    assert client.get(f"/api/experiments/{exp_id}").json()["metric_value"] == 0.84
    assert client.get("/api/summary").json() == {"projects": 1, "experiments": 1}
    assert len(client.get(f"/api/projects/{project_id}/experiments?model=RandomForest").json()) == 1
    assert client.get(f"/api/projects/{project_id}/experiments?model=Other").json() == []
    assert client.delete(f"/api/projects/{project_id}").status_code == 409
    assert (
        client.put(f"/api/experiments/{exp_id}", json={**EXPERIMENT, "metric_value": 0.91}).json()[
            "metric_value"
        ]
        == 0.91
    )
    assert client.delete(f"/api/experiments/{exp_id}").status_code == 204
    assert client.delete(f"/api/projects/{project_id}").status_code == 204
    assert client.get("/api/summary").json() == {"projects": 0, "experiments": 0}


def test_tenant_isolation_all_operations(authenticated):
    client = authenticated
    project_id = create_project(client)
    exp_id = client.post(f"/api/projects/{project_id}/experiments", json=EXPERIMENT).json()["id"]
    login(client, "luis")
    assert client.get("/api/projects").json() == []
    assert client.get("/api/summary").json() == {"projects": 0, "experiments": 0}
    for method, path, payload in [
        ("GET", f"/api/projects/{project_id}", None),
        ("PUT", f"/api/projects/{project_id}", {"name": "Attack"}),
        ("DELETE", f"/api/projects/{project_id}", None),
        ("GET", f"/api/projects/{project_id}/experiments", None),
        ("POST", f"/api/projects/{project_id}/experiments", EXPERIMENT),
        ("GET", f"/api/experiments/{exp_id}", None),
        ("PUT", f"/api/experiments/{exp_id}", EXPERIMENT),
        ("DELETE", f"/api/experiments/{exp_id}", None),
    ]:
        assert client.request(method, path, json=payload).status_code == 404


@pytest.mark.parametrize(
    "payload", [{"name": " "}, {"name": "x" * 121}, {"name": "ok", "user_id": 1}]
)
def test_invalid_project(authenticated, payload):
    assert authenticated.post("/api/projects", json=payload).status_code == 422


@pytest.mark.parametrize(
    "change",
    [
        {"metric_value": "bad"},
        {"metric_value": "NaN"},
        {"metric_value": "Infinity"},
        {"metric_name": " "},
        {"project_id": 999},
        {"model": ""},
    ],
)
def test_invalid_experiment(authenticated, change):
    project_id = create_project(authenticated)
    response = authenticated.post(
        f"/api/projects/{project_id}/experiments", json={**EXPERIMENT, **change}
    )
    assert response.status_code == 422


def test_nonexistent_project(authenticated):
    assert (
        authenticated.post("/api/projects/999999/experiments", json=EXPERIMENT).status_code == 404
    )


def test_persistence_after_new_app(authenticated, database_url):
    project_id = create_project(authenticated)
    new_app = create_app(
        Settings(_env_file=None, database_url=database_url, allowed_origins=["http://testserver"])
    )
    with TestClient(new_app, headers={"Origin": "http://testserver"}) as second:
        login(second)
        assert second.get(f"/api/projects/{project_id}").json()["name"] == "Demanda"
