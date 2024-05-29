export interface LotteryData {
  text: string;
  result: string;
  title: string;
  histories: string[];
}

export const defaultLotteryData: LotteryData = {
  text: "",
  result: "",
  title: "",
  histories: [],
};

export interface LotteryListData {
  list: LotteryData[];
  selectedIndex: number;
}

export const defaultLotteryListData: LotteryListData = {
  list: [defaultLotteryData],
  selectedIndex: 0,
};
