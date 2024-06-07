import { LocalStorage } from "./storage";
import { type LotteryTopData, defaultLotteryTopData } from "./lottery-data";

class LocalStorageLottery extends LocalStorage<LotteryTopData> {
  constructor() {
    super(LocalStorageLottery.name, structuredClone(defaultLotteryTopData));
  }
}

export default new LocalStorageLottery();
