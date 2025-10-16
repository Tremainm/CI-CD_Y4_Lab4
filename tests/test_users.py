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

# if deleted successfully, return 204, if user not found, return 404
def test_delete_then_404(client):
    r1 = client.delete("/api/users/1")
    assert r1.status_code == 204
    r2 = client.delete("/api/users/1")
    assert r2.status_code == 404

# test for invalid email formats
@pytest.mark.parametrize("bad_email", ["tremain.com", "tremain@mail", "john.mail.ie", "email@.com"]) # one test can try multiple invalid inputs
def test_bad_email_422(client, bad_email):
    r = client.post("/api/users", json=user_payload(uid=3, email=bad_email))
    assert r.status_code == 422 # pydantic validation error

# test to check if user update is successful
def test_update_user_ok(client):
    client.post("/api/users", json=user_payload(uid=4))
    r = client.put("/api/users/4", json=user_payload(uid=4, name="Tremain")) # update name to 'Tremain'
    assert r.status_code == 202
    data = r.json() # 'Tremain' parsed as json & stored in 'data'
    assert data["name"] == "Tremain" # check if name was updated
