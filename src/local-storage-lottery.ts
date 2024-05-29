import { LocalStorage } from "./storage";
import { type LotteryListData, defaultLotteryListData } from "./lottery-data";

class LocalStorageLottery extends LocalStorage<LotteryListData> {
  constructor() {
    super(LocalStorageLottery.name, defaultLotteryListData);
  }
}

export default new LocalStorageLottery();
