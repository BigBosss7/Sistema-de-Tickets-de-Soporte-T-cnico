from fastapi.testclient import TestClient 

from app.main import app 

client = TestClient(app)



def test_create_ticket(auth_user):
    response = client.post(
        "/tickets",
        headers=auth_user["headers"],
        json={
            "title": "Test ticket",
            "description": "Ticket created from pytest",
            "priority": "MEDIUM",
            "created_by_id": auth_user["user"]["id"]
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Test ticket"


def test_user_cannot_assign_ticket(auth_user):
    create_response = client.post(
        "/tickets",
        headers=auth_user["headers"],
        json={
            "title": "RBAC test ticket",
            "description": "this ticket is used to test permisions",
            "priority": "MEDIUM",
            "created_by_id": auth_user["user"]["id"]
            }
    )        

    ticket_id = create_response.json()["id"]

    assign_response = client.patch(
        f"/tickets/{ticket_id}/assign",
        headers=auth_user["headers"],
        json={
            "assigned_to_id": 1
        }
    )
     

    assert assign_response.status_code == 403