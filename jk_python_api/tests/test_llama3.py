# Test cases for llama3

import pytest
from app.services import llama3

@pytest.mark.asyncio
async def test_generate_summary(monkeypatch):
    async def mock_post(*args, **kwargs):
        class MockResponse:
            def raise_for_status(self):
                pass
            def json(self):
                return {"response": "This is a summary."}
        return MockResponse()
    monkeypatch.setattr("httpx.AsyncClient.post", mock_post)
    summary = await llama3.generate_summary("Test content")
    assert summary == "This is a summary."
