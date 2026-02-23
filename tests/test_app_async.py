import pytest


@pytest.mark.asyncio
async def test_get_activities(client):
    r = await client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert len(data) >= 1
    name = next(iter(data))
    assert isinstance(name, str)


@pytest.mark.asyncio
async def test_signup_success_and_cleanup(client, unique_email):
    email = unique_email()
    r = await client.get("/activities")
    data = r.json()
    name = next(iter(data))
    try:
        resp = await client.post(f"/activities/{name}/signup", params={"email": email})
        assert resp.status_code == 200
        r2 = await client.get("/activities")
        assert email in r2.json()[name]["participants"]
    finally:
        await client.delete(f"/activities/{name}/participants", params={"email": email})


@pytest.mark.asyncio
async def test_signup_duplicate(client, unique_email):
    email = unique_email()
    r = await client.get("/activities")
    name = next(iter(r.json()))
    r1 = await client.post(f"/activities/{name}/signup", params={"email": email})
    assert r1.status_code == 200
    r2 = await client.post(f"/activities/{name}/signup", params={"email": email})
    assert r2.status_code == 400
    await client.delete(f"/activities/{name}/participants", params={"email": email})


@pytest.mark.asyncio
async def test_signup_not_found(client, unique_email):
    email = unique_email()
    r = await client.post(f"/activities/non-existent-activity/signup", params={"email": email})
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_remove_participant_not_found(client):
    r = await client.get("/activities")
    name = next(iter(r.json()))
    resp = await client.delete(f"/activities/{name}/participants", params={"email": "noone@example.com"})
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_static_index(client):
    r = await client.get("/static/index.html")
    assert r.status_code == 200
    assert "<!DOCTYPE html>" in r.text or "<html" in r.text
