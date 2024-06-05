export class AlreadyExistsError implements Error {
  name = "AlreadyExistsError";
  message = "すでに存在しています";

  constructor(target?: string) {
    if (target) {
      this.message = `${target} は${this.message}`;
    }
  }
}

export class NoSignupError implements Error {
  name = "NoSignupError";
  message = "登録されていません";

  constructor(target?: string) {
    if (target) {
      this.message = `${target} は${this.message}`;
    }
  }
}

export class InvalidPasswordError implements Error {
  name = "InvalidPasswordError";
  message = "パスワードが違います";

  constructor() {}
}
