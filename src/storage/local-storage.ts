import { SaveLoadBehavior, type SaveLoadInterface } from "../save-load";
import AsyncLock from "async-lock";

export class LocalStorage<T extends object> extends SaveLoadBehavior<T> {
  constructor(key: string, defaultData: T) {
    super(new LocalStorageSaveLoad<T>(key), defaultData);
  }
}

class LocalStorageSaveLoad<T> implements SaveLoadInterface<T> {
  constructor(private key: string) {}

  async load(): Promise<T> {
    return await this.lock
      .acquire(this.key, () => localStorage.getItem(this.key))
      .then((value: string | null) => {
        if (value) {
          return JSON.parse(value) as T;
        } else {
          throw new Error(`LocalStorage not found data (key = ${this.key}`);
        }
      })
      .catch((error) => {
        throw error;
      });
  }

  async save(data: T): Promise<void> {
    return await this.lock
      .acquire(this.key, () => localStorage.setItem(this.key, JSON.stringify(data)))
      .catch((error) => {
        throw error;
      });
  }

  private readonly lock = new AsyncLock();
}
