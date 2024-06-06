export interface LotteryUserInputData {
  text: string;
  title: string;
  id: number;
}

export const defaultLotteryUserInputData: LotteryUserInputData = {
  text: "",
  title: "",
  id: -1,
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
  inputData: LotteryUserInputData;
  resultData: LotteryResultData;
}

export const defaultLotteryData: LotteryData = {
  inputData: defaultLotteryUserInputData,
  resultData: defaultLotteryResultData,
};

export interface LotteryListData {
  list: LotteryData[];
  selectedIndex: number;
}

export const defaultLotteryListData: LotteryListData = {
  list: [defaultLotteryData],
  selectedIndex: 0,
};

export interface LotteryTopData {
  accessToken: string;
  listData: LotteryListData;
}

export const defaultLotteryTopData: LotteryTopData = {
  accessToken: "",
  listData: defaultLotteryListData,
};
