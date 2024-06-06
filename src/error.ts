import { LotteryCreate } from "./openapi";

export class AlreadyExistsError implements Error {
  name = "AlreadyExistsError";
  message = "すでに存在しています";

  constructor(target?: string) {
    if (target) {
      this.message = `${target} は${this.message}`;
    }
  }
}

export class InvalidAccountOrPasswordError implements Error {
  name = "InvalidAccountOrPasswordError";
  message = "アカウントかパスワードが間違っています";

  constructor() {}
}

export class CanNotSaveLotteryError implements Error {
  name = "CanNotUpdateLotteryError";
  message = "くじ引きデータを保存できませんでした";

  constructor(target?: LotteryCreate) {
    if (target) {
      this.message = `${this.message}\nuser_id: ${target.user_id},\ntext: ${target.text},\ntitle: ${target.title}`;
    }
  }
}
