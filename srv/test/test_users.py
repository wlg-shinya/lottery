import pytest

@pytest.mark.asyncio
async def test_read_users(client_generator):
    client = await client_generator.__anext__()

    response = await client.get("/api/read_users")
    assert response.status_code == 200
