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
  if (typeof arg === "undefined" || arg === null) {
    throw new Error(`Invalid ${{ arg }}`);
  }
}

export async function dbCreateUser(accountName: string, identification: string): Promise<any> {
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

export async function dbReadUsers(): Promise<any> {
  return await axios
    .get("/api/read_users")
    .then((response) => {
      return JSON.parse(JSON.stringify(response.data));
    })
    .catch((error) => {
      throw error;
    });
}

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
