import { LocalStorage } from "./storage";
import { type LotteryTopData, defaultLotteryTopData } from "./lottery-data";

class LocalStorageLottery extends LocalStorage<LotteryTopData> {
  constructor() {
    super(LocalStorageLottery.name, defaultLotteryTopData);
  }
}

export default new LocalStorageLottery();
