import { AxiosError } from "axios";

export const getErrorMessage = (error: any): string => {
  if (error instanceof AxiosError) {
    if (error.response) {
      return error.response?.data.detail as string;
    } else {
      return error.message;
    }
  } else {
    return error.message;
  }
};
