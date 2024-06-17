import pytest
import api.schemas.users as schema

@pytest.mark.asyncio
async def test_integration(client_generator):
    client = await client_generator.__anext__()

    body_signin = schema.UserSignin(email="test@dummy.com", identification="test")
    body_signup_step1 = schema.UserSignupStep1(email=body_signin.email, identification=body_signin.identification, account_name="test")

    # サインアップステップ1(Eメール非送信版)
    res_signup_step1 = await client.post(
        "/api/admin/signup_step1",
        headers={"accept": "application/json"},
        content=body_signup_step1.model_dump_json()
        )
    assert res_signup_step1.status_code == 200
    res_signup_step1_obj = schema.UserSignupStep2(**res_signup_step1.json())
    assert res_signup_step1_obj.signup_token != ""

    # サインアップステップ2
    res_signup_step2 = await client.post(
        "/api/signup_step2",
        headers={"accept": "application/json"},
        content=res_signup_step1.content
        )
    assert res_signup_step2.status_code == 200

    # サインイン
    res_signin = await client.post(
        "/api/signin",
        headers={"accept": "application/json"},
        content=body_signin.model_dump_json()
        )
    assert res_signin.status_code == 200    
    res_signin_obj = schema.UserSigninResponse(**res_signin.json())
    assert res_signin_obj.access_token != ""

    # 
    access_token = res_signin_obj.access_token
