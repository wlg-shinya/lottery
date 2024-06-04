import axios from "axios";

// export type TableQueryResult = QueryResult<any>;
// export const DefaultTableQueryResult: TableQueryResult = {
//   command: "",
//   rowCount: null,
//   oid: 0,
//   fields: [],
//   rows: [],
// };

function notNull(arg: any) {
  if (!arg) {
    throw new Error(`Invalid ${{ arg }}`);
  }
}

export async function dbUserCreate(accountName: string, identification: string): Promise<any> {
  notNull(accountName);
  notNull(identification);
  return await axios
    .post("/api/create_user", {
      account_name: accountName,
      identification: identification,
    })
    .then((response) => response)
    .catch((error) => {
      throw error;
    });
}

// export async function dbTableGet(name: string): Promise<TableQueryResult> {
//   if (!name) {
//     throw new Error(`Invalid name=${name}`);
//   }
//   return await axios
//     .get("/api/db_table", {
//       params: {
//         name: name,
//       },
//     })
//     .then((response) => {
//       const data: QueryResult<any> = JSON.parse(JSON.stringify(response.data));
//       // timestamptz型データはISO8601タイムゾーンUTCな文字列です(例 2023-12-22T02:16:43.000Z)
//       return data;
//     })
//     .catch((error) => {
//       throw error;
//     });
// }

// export async function dbTableDelete(id: number): Promise<any> {
//   if (id <= 0) {
//     throw new Error(`Invalid id=${id}`);
//   }
//   return await axios
//     .delete("/api/db_table", {
//       data: {
//         id: id,
//       },
//     })
//     .then((response) => response)
//     .catch((error) => {
//       throw error;
//     });
// }
