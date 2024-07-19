import pytest
import api.schemas.users as usersSchema
from httpx import Headers

@pytest.mark.asyncio
async def test_signup_step1(client_generator):
    client = await client_generator.__anext__()

    headers = Headers(headers={"accept": "application/json"}, encoding=None)
    body_signup_step1 = usersSchema.UserSignupStep1(email="test@welovegamesinc.com", account_name="TEST", identification="test")

    res_signup_step1 = await client.post(
        "/api/signup_step1",
        headers=headers,
        content=body_signup_step1.model_dump_json()
        )

    assert res_signup_step1.status_code == 200
