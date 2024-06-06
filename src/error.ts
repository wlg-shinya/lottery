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

export class CanNotCreateLotteryError implements Error {
  name = "CanNotCreateLotteryError";
  message = "くじ引きデータを新規追加できませんでした";

  constructor(target?: object) {
    if (target) {
      this.message = `${this.message}\n${target}`;
    }
  }
}

export class CanNotUpdateLotteryError implements Error {
  name = "CanNotUpdateLotteryError";
  message = "くじ引きデータを更新できませんでした";

  constructor(target?: object) {
    if (target) {
      this.message = `${this.message}\n${target}`;
    }
  }
}
