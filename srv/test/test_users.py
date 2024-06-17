import pytest
import json
import api.schemas.users as schema
from httpx import Headers
 
@pytest.mark.asyncio
async def test_integration(client_generator):
    client = await client_generator.__anext__()

    headers = Headers(headers={"accept": "application/json"}, encoding=None)
    body_signin = schema.UserSignin(email="test@dummy.com", identification="test")
    body_signup_step1 = schema.UserSignupStep1(email=body_signin.email, identification=body_signin.identification, account_name="TEST")

    # ユーザーは未登録なはず
    read_users = await client.get("/api/read_users", headers=headers)
    assert read_users.status_code == 200
    assert len(read_users.json()) == 0

    # サインアップステップ1(Eメール非送信版)
    res_signup_step1 = await client.post(
        "/api/test/signup_step1",
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

    # ユーザ情報更新
    body_update = schema.UserUpdate(
        access_token=access_token,
        email="test2@dummy.com", 
        identification="test2",
        account_name="TEST2",
        pull_lottery_ids=[1]
        )
    res_update_user = await client.post(
        "/api/update_user",
        headers=headers,
        content=body_update.model_dump_json()
        )
    assert res_update_user.status_code == 200
    res_update_user_account_name_obj = schema.UserUpdateResponse(**res_update_user.json())
    assert res_update_user_account_name_obj.access_token != access_token

    # アクセストークン更新
    access_token = res_update_user_account_name_obj.access_token

    # ユーザー情報が正しく更新されたか確認
    res_read_user_by_access_token = await client.get(f"/api/read_user_by_access_token?access_token={access_token}", headers=headers)
    assert res_read_user_by_access_token.status_code == 200
    res_read_user_by_access_token_obj = schema.Users(**res_read_user_by_access_token.json())
    assert res_read_user_by_access_token_obj.email == body_update.email
    assert res_read_user_by_access_token_obj.account_name == body_update.account_name
    assert res_read_user_by_access_token_obj.pull_lottery_ids == body_update.pull_lottery_ids

    # アカウント名更新
    account_name3 = "TEST3"
    res_update_user_account_name = await client.put(
        f"/api/update_user_account_name?access_token={access_token}&account_name={account_name3}",
        headers=headers
        )
    assert res_update_user_account_name.status_code == 200
    res_update_user_account_name_obj = schema.UserUpdateResponse(**res_update_user_account_name.json())
    assert res_update_user_account_name_obj.access_token == access_token # このAPIではアクセストークンは変わらないはず
    # ほかの人のくじ引きID登録情報の更新
    user_pull_lottery_ids3 = [1, 2]
    res_update_user_pull_lottery_ids = await client.put(
        f"/api/update_user_pull_lottery_ids?access_token={access_token}",
        headers=headers,
        content=json.dumps(user_pull_lottery_ids3)
        )
    assert res_update_user_pull_lottery_ids.status_code == 200
    res_update_user_pull_lottery_ids_obj = schema.UserUpdateResponse(**res_update_user_pull_lottery_ids.json())
    assert res_update_user_pull_lottery_ids_obj.access_token == access_token # このAPIではアクセストークンは変わらないはず

    # ユーザー情報が正しく更新されたか確認
    res_read_user_by_access_token = await client.get(f"/api/read_user_by_access_token?access_token={access_token}", headers=headers)
    assert res_read_user_by_access_token.status_code == 200
    res_read_user_by_access_token_obj = schema.Users(**res_read_user_by_access_token.json())
    assert res_read_user_by_access_token_obj.account_name == account_name3
    assert res_read_user_by_access_token_obj.pull_lottery_ids == user_pull_lottery_ids3

    # パスワード変更
    body_change_password = schema.UserChangePassword(
        access_token=access_token,
        old_password=body_update.identification,
        new_password="test3"
        )
    res_change_password = await client.post(
        "/api/change_password",
        headers=headers,
        content=body_change_password.model_dump_json()
        )
    assert res_change_password.status_code == 200
    res_change_password_obj = schema.UserUpdateResponse(**res_change_password.json())
    assert res_change_password_obj.access_token != access_token

    # アクセストークン更新
    access_token = res_change_password_obj.access_token

    # ユーザー削除
    res_delete = await client.delete(f"/api/delete_user_by_access_token?access_token={access_token}", headers=headers)
    assert res_delete.status_code == 200

    # 作成したユーザー消したので0なはず
    read_users = await client.get("/api/read_users", headers=headers)
    assert read_users.status_code == 200
    assert len(read_users.json()) == 0