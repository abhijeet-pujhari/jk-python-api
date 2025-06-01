# Test cases for auth

import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_user_registration_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register user
        resp = await ac.post("/auth/register", json={"username": "testuser", "password": "testpass"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["username"] == "testuser"
        # Login
        resp = await ac.post("/auth/token", data={"username": "testuser", "password": "testpass"})
        assert resp.status_code == 200
        token = resp.json()["access_token"]
        assert token

@pytest.mark.asyncio
async def test_duplicate_user_registration():
    from httpx import AsyncClient
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/register", json={"username": "dupe", "password": "pass"})
        resp = await ac.post("/auth/register", json={"username": "dupe", "password": "pass"})
        assert resp.status_code == 400
        assert "already registered" in resp.text
