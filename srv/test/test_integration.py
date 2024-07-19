import pytest
import json
import api.schemas.users as usersSchema
import api.schemas.lotteries as lotteriesSchema
from httpx import Headers

@pytest.mark.asyncio
async def test_integration(client_generator):
    client = await client_generator.__anext__()

    headers = Headers(headers={"accept": "application/json"}, encoding=None)
    body_signin = usersSchema.UserSignin(email="test@dummy.com", identification="test")
    body_signup_step1 = usersSchema.UserSignupStep1(email=body_signin.email, identification=body_signin.identification, account_name="TEST")

    # ユーザーは未登録なはず
    res_read_users = await client.get("/api/read_users", headers=headers)
    assert res_read_users.status_code == 200
    assert len(res_read_users.json()) == 0

    # くじ引きも未登録なはず
    res_read_lotteries = await client.get("/api/read_lotteries", headers=headers)
    assert res_read_lotteries.status_code == 200
    assert len(res_read_lotteries.json()) == 0

    # サインアップステップ1(Eメール非送信版)
    res_signup_step1 = await client.post(
        "/api/test/signup_step1",
        headers=headers,
        content=body_signup_step1.model_dump_json()
        )
    assert res_signup_step1.status_code == 200
    res_signup_step1_obj = usersSchema.UserSignupStep2(**res_signup_step1.json())
    assert res_signup_step1_obj.signup_token != ""

    # サインアップステップ2
    res_signup_step2 = await client.post(
        "/api/signup_step2",
        headers=headers,
        content=res_signup_step1.content
        )
    assert res_signup_step2.status_code == 200

    # ユーザー登録数は1名になったはず
    res_read_users = await client.get("/api/read_users", headers=headers)
    assert res_read_users.status_code == 200
    assert len(res_read_users.json()) == 1

    # サインイン
    res_signin = await client.post(
        "/api/signin",
        headers=headers,
        content=body_signin.model_dump_json()
        )
    assert res_signin.status_code == 200
    res_signin_obj = usersSchema.UserSigninResponse(**res_signin.json())
    assert res_signin_obj.access_token != ""

    # アクセストークン確保
    access_token = res_signin_obj.access_token

    # アクセストークンでユーザー情報を得る
    res_read_user_by_access_token = await client.get(
        f"/api/read_user_by_access_token?access_token={access_token}", 
        headers=headers)
    assert res_read_user_by_access_token.status_code == 200
    res_read_user_by_access_token_obj = usersSchema.Users(**res_read_user_by_access_token.json())
    assert res_read_user_by_access_token_obj.email == body_signin.email
    assert res_read_user_by_access_token_obj.identification == access_token
    assert res_read_user_by_access_token_obj.account_name == body_signup_step1.account_name

    # IDでユーザー情報を得る
    res_read_user = await client.get(
        f"/api/read_user?id={res_read_user_by_access_token_obj.id}", 
        headers=headers)
    assert res_read_user.status_code == 200
    res_read_user_obj = usersSchema.Users(**res_read_user.json())
    assert res_read_user_obj.email == res_read_user_by_access_token_obj.email
    assert res_read_user_obj.identification == res_read_user_by_access_token_obj.identification
    assert res_read_user_obj.account_name == res_read_user_by_access_token_obj.account_name

    # ユーザ情報更新
    body_update = usersSchema.UserUpdate(
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
    res_update_user_account_name_obj = usersSchema.UserUpdateResponse(**res_update_user.json())
    assert res_update_user_account_name_obj.access_token != access_token

    # アクセストークン更新
    access_token = res_update_user_account_name_obj.access_token

    # ユーザー情報が正しく更新されたか確認
    res_read_user_by_access_token = await client.get(f"/api/read_user_by_access_token?access_token={access_token}", headers=headers)
    assert res_read_user_by_access_token.status_code == 200
    res_read_user_by_access_token_obj = usersSchema.Users(**res_read_user_by_access_token.json())
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
    res_update_user_account_name_obj = usersSchema.UserUpdateResponse(**res_update_user_account_name.json())
    assert res_update_user_account_name_obj.access_token == access_token # このAPIではアクセストークンは変わらないはず
    # ほかの人のくじ引きID登録情報の更新
    user_pull_lottery_ids3 = [1, 2]
    res_update_user_pull_lottery_ids = await client.put(
        f"/api/update_user_pull_lottery_ids?access_token={access_token}",
        headers=headers,
        content=json.dumps(user_pull_lottery_ids3)
        )
    assert res_update_user_pull_lottery_ids.status_code == 200
    res_update_user_pull_lottery_ids_obj = usersSchema.UserUpdateResponse(**res_update_user_pull_lottery_ids.json())
    assert res_update_user_pull_lottery_ids_obj.access_token == access_token # このAPIではアクセストークンは変わらないはず

    # ユーザー情報が正しく更新されたか確認
    res_read_user_by_access_token = await client.get(f"/api/read_user_by_access_token?access_token={access_token}", headers=headers)
    assert res_read_user_by_access_token.status_code == 200
    res_read_user_by_access_token_obj = usersSchema.Users(**res_read_user_by_access_token.json())
    assert res_read_user_by_access_token_obj.account_name == account_name3
    assert res_read_user_by_access_token_obj.pull_lottery_ids == user_pull_lottery_ids3

    # パスワード変更
    body_change_password = usersSchema.UserChangePassword(
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
    res_change_password_obj = usersSchema.UserUpdateResponse(**res_change_password.json())
    assert res_change_password_obj.access_token != access_token

    # アクセストークン更新
    access_token = res_change_password_obj.access_token

    # くじ引き作成
    body_create_lottery = lotteriesSchema.LotteryCreate(
        access_token=access_token,
        text="1",
        title="test",
        description="TEST"
        )
    res_create_lottery = await client.post(
        "/api/create_lottery",
        headers=headers,
        content=body_create_lottery.model_dump_json()
        )
    assert res_create_lottery.status_code == 200
    res_create_lottery_obj = lotteriesSchema.LotteryCreateResponse(**res_create_lottery.json())
    assert res_create_lottery_obj.user_id == res_read_user_obj.id

    # くじ引き登録数は1件になったはず
    res_read_lotteries = await client.get("/api/read_lotteries", headers=headers)
    assert res_read_lotteries.status_code == 200
    assert len(res_read_lotteries.json()) == 1
    read_lotteries_top_obj = lotteriesSchema.Lotteries(**res_read_lotteries.json()[0])

    # 自分のくじ引き登録数の1件なはず
    res_read_my_lotteries = await client.get(f"/api/read_my_lotteries?access_token={access_token}", headers=headers)
    assert res_read_my_lotteries.status_code == 200
    assert len(res_read_my_lotteries.json()) == 1

    # IDでくじ引きを得る
    res_read_lottery = await client.get(f"/api/read_lottery?id={read_lotteries_top_obj.id}", headers=headers)
    assert res_read_lottery.status_code == 200
    res_read_lottery_obj = lotteriesSchema.Lotteries(**res_read_lottery.json())
    assert res_read_lottery_obj.text == body_create_lottery.text
    assert res_read_lottery_obj.title == body_create_lottery.title
    assert res_read_lottery_obj.description == body_create_lottery.description

    # くじ引き更新
    body_update_lottery = lotteriesSchema.LotteryCreate(
        access_token=access_token,
        text="1\n2",
        title="test2",
        description="TEST2"
        )
    res_update_lottery = await client.put(
        f"/api/update_lottery?id={res_read_lottery_obj.id}",
        headers=headers,
        content=body_update_lottery.model_dump_json()
        )
    assert res_update_lottery.status_code == 200
    res_update_lottery_obj = lotteriesSchema.LotteryCreateResponse(**res_update_lottery.json())
    assert res_update_lottery_obj.id == res_read_lottery_obj.id
    assert res_update_lottery_obj.user_id == res_read_lottery_obj.user_id

    # くじ引きは更新されているはず
    res_read_lottery = await client.get(f"/api/read_lottery?id={res_read_lottery_obj.id}", headers=headers)
    assert res_read_lottery.status_code == 200
    res_read_lottery_obj = lotteriesSchema.Lotteries(**res_read_lottery.json())
    assert res_read_lottery_obj.text == body_update_lottery.text
    assert res_read_lottery_obj.title == body_update_lottery.title
    assert res_read_lottery_obj.description == body_update_lottery.description
    assert res_read_lottery_obj.used_count == 0

    # これまでに得たIDなら自分のくじ引きデータなはず
    res_is_lottery_id_mine = await client.get(f"/api/is_lottery_id_mine?id={res_read_lottery_obj.id}&access_token={access_token}", headers=headers)
    assert res_is_lottery_id_mine.status_code == 200
    assert bool(res_is_lottery_id_mine.json()) == True

    # 適当なIDなら自分のくじ引きデータではない
    res_is_lottery_id_mine = await client.get(f"/api/is_lottery_id_mine?id=999&access_token={access_token}", headers=headers)
    assert res_is_lottery_id_mine.status_code == 200
    assert bool(res_is_lottery_id_mine.json()) == False

    # くじ引き抽選回数を増加
    res_increment_lottery_used_count = await client.post(f"/api/increment_lottery_used_count?id={res_read_lottery_obj.id}&access_token={access_token}", headers=headers)
    assert res_increment_lottery_used_count.status_code == 200
    res_increment_lottery_used_count_obj = lotteriesSchema.LotteryCreateResponse(**res_increment_lottery_used_count.json())
    assert res_increment_lottery_used_count_obj.id == res_read_lottery_obj.id
    assert res_increment_lottery_used_count_obj.user_id == res_read_lottery_obj.user_id

    # くじ引き抽選回数は更新されているはず
    res_read_lottery = await client.get(f"/api/read_lottery?id={res_read_lottery_obj.id}", headers=headers)
    assert res_read_lottery.status_code == 200
    res_read_lottery_obj = lotteriesSchema.Lotteries(**res_read_lottery.json())
    assert res_read_lottery_obj.used_count == 1

    # くじ引きをもう1回抽選
    res_increment_lottery_used_count = await client.post(f"/api/increment_lottery_used_count?id={res_read_lottery_obj.id}&access_token={access_token}", headers=headers)
    assert res_increment_lottery_used_count.status_code == 200

    # くじ引き抽選回数は更新されているはず
    res_read_lottery = await client.get(f"/api/read_lottery?id={res_read_lottery_obj.id}", headers=headers)
    assert res_read_lottery.status_code == 200
    res_read_lottery_obj = lotteriesSchema.Lotteries(**res_read_lottery.json())
    assert res_read_lottery_obj.used_count == 2

    # くじ引き削除
    res_delete_lottery = await client.delete(f"/api/delete_lottery?id={res_read_lottery_obj.id}&access_token={access_token}", headers=headers)
    assert res_delete_lottery.status_code == 200

    # 作成したくじ引きを消したので0なはず
    res_read_lotteries = await client.get("/api/read_lotteries", headers=headers)
    assert res_read_lotteries.status_code == 200
    assert len(res_read_lotteries.json()) == 0

    # ユーザー削除
    res_delete_user_by_access_token = await client.delete(f"/api/delete_user_by_access_token?access_token={access_token}", headers=headers)
    assert res_delete_user_by_access_token.status_code == 200

    # 作成したユーザーを消したので0なはず
    res_read_users = await client.get("/api/read_users", headers=headers)
    assert res_read_users.status_code == 200
    assert len(res_read_users.json()) == 0
