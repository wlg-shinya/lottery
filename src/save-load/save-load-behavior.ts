import { type SaveLoadInterface } from "./save-load-interface";

// 保存・読込に関するふるまいが実装されたクラス
export class SaveLoadBehavior<T extends object> {
  constructor(private saveLoad: SaveLoadInterface<T>, private defaultData: T) {}

  // 保存
  async save(data: T): Promise<void> {
    return await this.saveLoad.save(data);
  }

  // 読込
  async load(): Promise<T> {
    return await this.saveLoad.load();
  }

  // リセット
  async reset(): Promise<void> {
    return await this.save(this.getDefaultData());
  }

  // セットアップ。具体的には以下のことが行われます。
  // - デフォルトデータに新しくプロパティが追加された場合、保存されているデータにプロパティをデフォルトデータの値で追加して保存
  // - 保存されているデータにデフォルトデータからもう削除された古いプロパティがある場合はプロパティを削除して保存
  // - データ自体がなければデフォルトデータで保存
  async setup(): Promise<void> {
    const data = await this.saveLoad
      .load()
      .then(async (data: T) => {
        const defaultData = this.getDefaultData();
        const dataKeys = Object.keys(data);
        const defaultDataKeys = Object.keys(defaultData);
        // TS正攻法が思いつかないので抑制。文脈上 x は data にも defaultData にも存在するプロパティなので問題なし
        // @ts-ignore
        const entries = defaultDataKeys.map((x) => [[x], dataKeys.some((y) => y === x) ? data[x] : defaultData[x]]);
        return Object.fromEntries(entries) as T;
      })
      .catch(() => this.defaultData);
    return await this.saveLoad.save(data);
  }

  // デフォルトデータ取得
  // 継承先でオーバーライドできるようにメソッドとして用意
  getDefaultData(): T {
    return this.defaultData;
  }
}
