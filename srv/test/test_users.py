import pytest

@pytest.mark.asyncio
async def test_read_users(async_client):
    response = await (await async_client.__anext__()).get("/api/read_users")
    assert response.status_code == 200
