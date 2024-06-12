import { DefaultApi } from "./generated/api";
import { Configuration } from "./generated/configuration";

export * from "./generated";

export const DefaultApiClient = new DefaultApi(
  new Configuration({
    baseOptions: { withCredentials: false },
  })
);

// srv\api\models.py 以下の文字数条件の定数化
export const VarcharMax = {
  lotteries_text: 256,
  lotteries_title: 32,
  lotteries_description: 256,
  users_account_name: 24,
  users_identification: 64,
  users_access_token: 64,
};
