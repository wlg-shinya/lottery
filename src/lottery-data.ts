export interface LotteryUserInputData {
  text: string;
  title: string;
  description: string;
  id: number;
  mine: boolean;
}

export const defaultLotteryUserInputData: LotteryUserInputData = {
  text: "",
  title: "",
  description: "",
  id: -1,
  mine: true,
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
  inputData: structuredClone(defaultLotteryUserInputData),
  resultData: structuredClone(defaultLotteryResultData),
};

export interface LotteryListData {
  list: LotteryData[];
}

export const defaultLotteryListData: LotteryListData = {
  list: [structuredClone(defaultLotteryData)],
};

export interface LotteryTopData {
  accessToken: string;
  listData: LotteryListData;
}

export const defaultLotteryTopData: LotteryTopData = {
  accessToken: "",
  listData: structuredClone(defaultLotteryListData),
};

export interface LotteryPublicData extends LotteryUserInputData {
  user_name: string;
  // TODO: お気に入り数
  // TODO: ほかのユーザーに抽選された回数
}
