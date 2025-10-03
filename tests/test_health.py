def test_health(client):
    r = client.get("/health") # 'r' = endpoint to test
    assert r.status_code == 200 # expecting a '200' success response
    assert r.json() == {"status": "ok"} # expected result?