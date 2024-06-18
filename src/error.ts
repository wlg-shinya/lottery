import { AxiosError } from "axios";
import {
  DUPLICATED_EXCEPTION,
  EXPIRED_ACCESS_TOKEN_EXCEPTION,
  EXPIRED_SIGNUP_TOKEN_EXCEPTION,
  INVALID_PASSWORD_EXCEPTION,
  NOT_FOUND_EXCEPTION,
  UNAUTHORIZED_EXCEPTION,
} from "./openapi";

export const getErrorMessage = (error: any): string => {
  if (error instanceof AxiosError) {
    if (error.response) {
      const exception = error.response?.data.detail as string;
      switch (exception) {
        case DUPLICATED_EXCEPTION:
          return "すでに登録済みです。別の内容で登録してください";
        case EXPIRED_ACCESS_TOKEN_EXCEPTION:
          return "アクセスの有効期限が切れました。再度サインインしてください";
        case EXPIRED_SIGNUP_TOKEN_EXCEPTION:
          return "サインアップの有効期限が切れました。再度サインアップを試みてください";
        case INVALID_PASSWORD_EXCEPTION:
          return "パスワードが正しくありません";
        case NOT_FOUND_EXCEPTION:
          return "データが見つかりませんでした";
        case UNAUTHORIZED_EXCEPTION:
          return "認証に失敗しました";
        default:
          return exception;
      }
    } else {
      return error.message;
    }
  } else if (error instanceof Error) {
    return error.message;
  } else {
    return error;
  }
};
