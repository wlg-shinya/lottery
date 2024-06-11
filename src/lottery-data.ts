export interface LotteryContentsData {
  text: string;
  title: string;
  description: string;
  id: number;
  mine: boolean;
  used_count: number;
}

export const defaultLotteryContentsData: LotteryContentsData = {
  text: "",
  title: "",
  description: "",
  id: -1,
  mine: true,
  used_count: 0,
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
  contentsData: LotteryContentsData;
  resultData: LotteryResultData;
}

export const defaultLotteryData: LotteryData = {
  contentsData: structuredClone(defaultLotteryContentsData),
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

export interface LotteryPublicData extends LotteryContentsData {
  user_name: string;
  pulled_count: number;
}
