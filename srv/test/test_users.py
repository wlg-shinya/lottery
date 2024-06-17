import pytest
import api.schemas.users as schema
from httpx import Headers
 
@pytest.mark.asyncio
async def test_integration(client_generator):
    client = await client_generator.__anext__()

    headers = Headers(headers={"accept": "application/json"}, encoding=None)
    body_signin = schema.UserSignin(email="test@dummy.com", identification="test")
    body_signup_step1 = schema.UserSignupStep1(email=body_signin.email, identification=body_signin.identification, account_name="test")

    # ユーザーは未登録なはず
    read_users = await client.get("/api/read_users", headers=headers)
    assert read_users.status_code == 200
    assert len(read_users.json()) == 0

    # サインアップステップ1(Eメール非送信版)
    res_signup_step1 = await client.post(
        "/api/admin/signup_step1",
        headers=headers,
        content=body_signup_step1.model_dump_json()
        )
    assert res_signup_step1.status_code == 200
    res_signup_step1_obj = schema.UserSignupStep2(**res_signup_step1.json())
    assert res_signup_step1_obj.signup_token != ""

    # サインアップステップ2
    res_signup_step2 = await client.post(
        "/api/signup_step2",
        headers=headers,
        content=res_signup_step1.content
        )
    assert res_signup_step2.status_code == 200

    # ユーザー登録数は1名になったはず
    read_users = await client.get("/api/read_users", headers=headers)
    assert read_users.status_code == 200
    assert len(read_users.json()) == 1

    # サインイン
    res_signin = await client.post(
        "/api/signin",
        headers=headers,
        content=body_signin.model_dump_json()
        )
    assert res_signin.status_code == 200
    res_signin_obj = schema.UserSigninResponse(**res_signin.json())
    assert res_signin_obj.access_token != ""

    # 
    access_token = res_signin_obj.access_token

    # アクセストークンでユーザー情報を得る
    res_read_user_by_access_token = await client.get(
        f"/api/read_user_by_access_token?access_token={access_token}", 
        headers=headers)
    assert res_read_user_by_access_token.status_code == 200
    res_read_user_by_access_token_obj = schema.Users(**res_read_user_by_access_token.json())
    assert res_read_user_by_access_token_obj.email == body_signin.email
    assert res_read_user_by_access_token_obj.identification == access_token
    assert res_read_user_by_access_token_obj.account_name == body_signup_step1.account_name

    # IDでユーザー情報を得る
    res_read_user = await client.get(
        f"/api/read_user?id={res_read_user_by_access_token_obj.id}", 
        headers=headers)
    assert res_read_user.status_code == 200
    res_read_user = schema.Users(**res_read_user.json())
    assert res_read_user.email == res_read_user_by_access_token_obj.email
    assert res_read_user.identification == res_read_user_by_access_token_obj.identification
    assert res_read_user.account_name == res_read_user_by_access_token_obj.account_name
