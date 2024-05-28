// このインターフェースを継承して物理的な保存・読込を実装する
export interface SaveLoadInterface<T> {
  save(data: T): Promise<void>;
  load(): Promise<T>;
}
