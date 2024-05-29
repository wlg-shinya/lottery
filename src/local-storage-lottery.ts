import { LocalStorage } from "./storage";

export interface LocalStorageLotteryData {
  input: string;
  result: string;
}

const defaultData: LocalStorageLotteryData = {
  input: "",
  result: "",
};

class LocalStorageLottery extends LocalStorage<LocalStorageLotteryData> {
  constructor() {
    super(LocalStorageLottery.name, defaultData);
  }
}

export default new LocalStorageLottery();
