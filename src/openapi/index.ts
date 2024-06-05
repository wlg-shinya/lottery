import { DefaultApi } from "./generated/api";
import { Configuration } from "./generated/configuration";

export const ApiClient = new DefaultApi(
  new Configuration({
    baseOptions: { withCredentials: false },
  })
);
