import pytest

# Creating a dict to test off of
def user_payload(uid=1, name="Paul", email="pl@atu.ie", age=25, sid="S1234567"):
    return {"user_id": uid, "name": name, "email": email, "age": age, "student_id": sid}

# test user creation and user_id == 1 and name == Paul
def test_create_user_ok(client):
    r = client.post("/api/users", json=user_payload())
    assert r.status_code == 201
    data = r.json()
    assert data["user_id"] == 1
    assert data["name"] == "Paul"

# create user with uid=2, check if 'exists' then assert 409
def test_duplicate_user_id_conflict(client):
    client.post("/api/users", json=user_payload(uid=2))
    r = client.post("/api/users", json=user_payload(uid=2))
    assert r.status_code == 409 # duplicate id -> conflict
    assert "exists" in r.json()["detail"].lower()

# check if 'bad' student id's fail correctly
@pytest.mark.parametrize("bad_sid", ["BAD123", "s1234567", "S123", "S12345678"]) # one test can try multiple invalid inputs
def test_bad_student_id_422(client, bad_sid):
    r = client.post("/api/users", json=user_payload(uid=3, sid=bad_sid))
    assert r.status_code == 422 # pydantic validation error

# if user doesn't exist, get 404
def test_get_user_404(client):
    r = client.get("/api/users/999")
    assert r.status_code == 404

# create user with uid 10, if deleted successfully, return 204, if use not found, return 404
def test_delete_then_404(client):
    client.post("/api/users", json=user_payload(uid=10))
    r1 = client.delete("/api/users/10")
    assert r1.status_code == 204
    r2 = client.delete("/api/users/10")
    assert r2.status_code == 404

