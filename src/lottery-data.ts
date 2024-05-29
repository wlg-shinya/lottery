export interface LotteryUserInputData {
  text: string;
  title: string;
}

export const defaultLotteryUserInputData: LotteryUserInputData = {
  text: "",
  title: "",
};

export interface LotteryResultData {
  result: string;
  histories: string[];
  historyShowCount: number;
}

export const defaultLotteryResultData: LotteryResultData = {
  result: "",
  histories: [],
  historyShowCount: 10,
};

export interface LotteryData {
  input: LotteryUserInputData;
  result: LotteryResultData;
}

export const defaultLotteryData: LotteryData = {
  input: defaultLotteryUserInputData,
  result: defaultLotteryResultData,
};

export interface LotteryListData {
  list: LotteryData[];
  selectedIndex: number;
}

export const defaultLotteryListData: LotteryListData = {
  list: [defaultLotteryData],
  selectedIndex: 0,
};
