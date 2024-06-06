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
