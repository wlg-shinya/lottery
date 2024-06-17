import pytest
import api.schemas.users as schema

@pytest.mark.asyncio
async def test_integration(client_generator):
    client = await client_generator.__anext__()

    body_signin = schema.UserSignin(email="test@dummy.com", identification="test")
    body_signup_step1 = schema.UserSignupStep1(email=body_signin.email, identification=body_signin.identification, account_name="test")

    # サインアップステップ1(Eメール非送信版)
    res1 = await client.post(
        "/api/admin/signup_step1",
        headers={"accept": "application/json"},
        content=body_signup_step1.model_dump_json()
        )
    assert res1.status_code == 200
    res1Obj = schema.UserSignupStep2(**res1.json())
    assert res1Obj.signup_token != ""

    # サインアップステップ2
    res2 = await client.post(
        "/api/signup_step2",
        headers={"accept": "application/json"},
        content=res1.content
        )
    assert res2.status_code == 200

    # サインイン
    res3 = await client.post(
        "/api/signin",
        headers={"accept": "application/json"},
        content=body_signin.model_dump_json()
        )
    assert res3.status_code == 200    
    res3Obj = schema.UserSigninResponse(**res3.json())
    assert res3Obj.access_token != ""

    # 
    access_token = res3Obj.access_token
