import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from src.app import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac


@pytest.fixture
def unique_email():
    def _gen():
        return f"test-{uuid.uuid4().hex}@example.com"
    return _gen
