# Test cases for recommendations

import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_recommendations_with_cache(monkeypatch):
    # Mock redis get/set
    class DummyRedis:
        def __init__(self):
            self.store = {}
        async def get(self, key):
            return self.store.get(key)
        async def set(self, key, value, ex=None):
            self.store[key] = value
    monkeypatch.setattr("app.main.redis", DummyRedis())
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Should work even if no books exist
        resp = await ac.get("/recommendations?genre=Fiction&min_rating=0")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)
