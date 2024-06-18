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
  users_email: 80,
  users_account_name: 24,
  users_identification: 64,
  users_access_token: 64,
};

// HTTPException(detail="*")の*部 (AxiosError.response.data.detail と比較可能)
export const DUPLICATED_EXCEPTION = "DuplicatedException";
export const EXPIRED_ACCESS_TOKEN_EXCEPTION = "ExpiredAccessTokenException";
export const EXPIRED_SIGNUP_TOKEN_EXCEPTION = "ExpiredSignupTokenException";
export const NOT_FOUND_EXCEPTION = "NotFoundException";
export const UNAUTHORIZED_EXCEPTION = "UnauthorizedException";
