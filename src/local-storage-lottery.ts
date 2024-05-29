import { LocalStorage } from "./storage";

export interface LocalStorageLotteryData {
  text: string;
  result: string;
}

const defaultData: LocalStorageLotteryData = {
  text: "",
  result: "",
};

class LocalStorageLottery extends LocalStorage<LocalStorageLotteryData> {
  constructor() {
    super(LocalStorageLottery.name, defaultData);
  }
}

export default new LocalStorageLottery();
