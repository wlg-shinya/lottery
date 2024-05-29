import { LocalStorage } from "./storage";

export interface LocalStorageLotteryData {
  input: string;
}

const defaultData: LocalStorageLotteryData = {
  input: "",
};

class LocalStorageLottery extends LocalStorage<LocalStorageLotteryData> {
  constructor() {
    super(LocalStorageLottery.name, defaultData);
  }
}

export default new LocalStorageLottery();
