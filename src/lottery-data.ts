export interface LotteryContentsData {
  text: string;
  title: string;
  description: string;
  id: number;
  mine: boolean;
  usedCount: number;
}

export const defaultLotteryContentsData: LotteryContentsData = {
  text: "",
  title: "",
  description: "",
  id: -1,
  mine: true,
  usedCount: 0,
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
  username: string;
  pulledCount: number;
  filteredString: string; // 検索フィルター対象文字列
}
