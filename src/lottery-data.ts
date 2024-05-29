export interface LotteryData {
  text: string;
  result: string;
  title: string;
  history: string[];
}

export const defaultLotteryData: LotteryData = {
  text: "",
  result: "",
  title: "",
  history: [],
};

export interface LotteryListData {
  list: LotteryData[];
  selectedIndex: number;
}

export const defaultLotteryListData: LotteryListData = {
  list: [defaultLotteryData],
  selectedIndex: 0,
};
