import { DefaultApi } from "./generated/api";
import { Configuration } from "./generated/configuration";

export * from "./generated";

export const DefaultApiClient = new DefaultApi(
  new Configuration({
    baseOptions: { withCredentials: false },
  })
);
