/* tslint:disable */
/* eslint-disable */
/**
 * FastAPI
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


import type { Configuration } from './configuration';
import type { AxiosPromise, AxiosInstance, RawAxiosRequestConfig } from 'axios';
import globalAxios from 'axios';
// Some imports not used depending on template conditions
// @ts-ignore
import { DUMMY_BASE_URL, assertParamExists, setApiKeyToObject, setBasicAuthToObject, setBearerAuthToObject, setOAuthToObject, setSearchParams, serializeDataIfNeeded, toPathString, createRequestFunction } from './common';
import type { RequestArgs } from './base';
// @ts-ignore
import { BASE_PATH, COLLECTION_FORMATS, BaseAPI, RequiredError, operationServerMap } from './base';

/**
 * 
 * @export
 * @interface HTTPValidationError
 */
export interface HTTPValidationError {
    /**
     * 
     * @type {Array<ValidationError>}
     * @memberof HTTPValidationError
     */
    'detail'?: Array<ValidationError>;
}
/**
 * 
 * @export
 * @interface Lotteries
 */
export interface Lotteries {
    /**
     * 
     * @type {number}
     * @memberof Lotteries
     */
    'user_id'?: number;
    /**
     * 
     * @type {string}
     * @memberof Lotteries
     */
    'text'?: string;
    /**
     * 
     * @type {string}
     * @memberof Lotteries
     */
    'title'?: string;
    /**
     * 
     * @type {number}
     * @memberof Lotteries
     */
    'id': number;
}
/**
 * 
 * @export
 * @interface LotteryCreate
 */
export interface LotteryCreate {
    /**
     * 
     * @type {number}
     * @memberof LotteryCreate
     */
    'user_id'?: number;
    /**
     * 
     * @type {string}
     * @memberof LotteryCreate
     */
    'text'?: string;
    /**
     * 
     * @type {string}
     * @memberof LotteryCreate
     */
    'title'?: string;
}
/**
 * 
 * @export
 * @interface LotteryCreateResponse
 */
export interface LotteryCreateResponse {
    /**
     * 
     * @type {number}
     * @memberof LotteryCreateResponse
     */
    'user_id'?: number;
    /**
     * 
     * @type {string}
     * @memberof LotteryCreateResponse
     */
    'text'?: string;
    /**
     * 
     * @type {string}
     * @memberof LotteryCreateResponse
     */
    'title'?: string;
    /**
     * 
     * @type {number}
     * @memberof LotteryCreateResponse
     */
    'id': number;
}
/**
 * 
 * @export
 * @interface UserCreate
 */
export interface UserCreate {
    /**
     * 
     * @type {string}
     * @memberof UserCreate
     */
    'account_name'?: string;
    /**
     * 
     * @type {string}
     * @memberof UserCreate
     */
    'identification'?: string;
}
/**
 * 
 * @export
 * @interface UserCreateResponse
 */
export interface UserCreateResponse {
    /**
     * 
     * @type {string}
     * @memberof UserCreateResponse
     */
    'account_name'?: string;
    /**
     * 
     * @type {string}
     * @memberof UserCreateResponse
     */
    'identification'?: string;
    /**
     * 
     * @type {number}
     * @memberof UserCreateResponse
     */
    'id': number;
}
/**
 * 
 * @export
 * @interface Users
 */
export interface Users {
    /**
     * 
     * @type {string}
     * @memberof Users
     */
    'account_name'?: string;
    /**
     * 
     * @type {string}
     * @memberof Users
     */
    'identification'?: string;
    /**
     * 
     * @type {number}
     * @memberof Users
     */
    'id': number;
}
/**
 * 
 * @export
 * @interface ValidationError
 */
export interface ValidationError {
    /**
     * 
     * @type {Array<ValidationErrorLocInner>}
     * @memberof ValidationError
     */
    'loc': Array<ValidationErrorLocInner>;
    /**
     * 
     * @type {string}
     * @memberof ValidationError
     */
    'msg': string;
    /**
     * 
     * @type {string}
     * @memberof ValidationError
     */
    'type': string;
}
/**
 * 
 * @export
 * @interface ValidationErrorLocInner
 */
export interface ValidationErrorLocInner {
}

/**
 * DefaultApi - axios parameter creator
 * @export
 */
export const DefaultApiAxiosParamCreator = function (configuration?: Configuration) {
    return {
        /**
         * 
         * @summary Create Lottery
         * @param {LotteryCreate} lotteryCreate 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createLotteryApiCreateLotteryPost: async (lotteryCreate: LotteryCreate, options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            // verify required parameter 'lotteryCreate' is not null or undefined
            assertParamExists('createLotteryApiCreateLotteryPost', 'lotteryCreate', lotteryCreate)
            const localVarPath = `/api/create_lottery`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'POST', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;


    
            localVarHeaderParameter['Content-Type'] = 'application/json';

            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};
            localVarRequestOptions.data = serializeDataIfNeeded(lotteryCreate, localVarRequestOptions, configuration)

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * 
         * @summary Create User
         * @param {UserCreate} userCreate 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createUserApiCreateUserPost: async (userCreate: UserCreate, options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            // verify required parameter 'userCreate' is not null or undefined
            assertParamExists('createUserApiCreateUserPost', 'userCreate', userCreate)
            const localVarPath = `/api/create_user`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'POST', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;


    
            localVarHeaderParameter['Content-Type'] = 'application/json';

            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};
            localVarRequestOptions.data = serializeDataIfNeeded(userCreate, localVarRequestOptions, configuration)

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * 
         * @summary Delete Lottery
         * @param {number} id 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        deleteLotteryApiDeleteLotteryDelete: async (id: number, options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            // verify required parameter 'id' is not null or undefined
            assertParamExists('deleteLotteryApiDeleteLotteryDelete', 'id', id)
            const localVarPath = `/api/delete_lottery`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'DELETE', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            if (id !== undefined) {
                localVarQueryParameter['id'] = id;
            }


    
            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * 
         * @summary Delete User
         * @param {number} id 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        deleteUserApiDeleteUserDelete: async (id: number, options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            // verify required parameter 'id' is not null or undefined
            assertParamExists('deleteUserApiDeleteUserDelete', 'id', id)
            const localVarPath = `/api/delete_user`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'DELETE', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            if (id !== undefined) {
                localVarQueryParameter['id'] = id;
            }


    
            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * 
         * @summary Read Lotteries
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        readLotteriesApiReadLotteriesGet: async (options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            const localVarPath = `/api/read_lotteries`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'GET', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;


    
            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * 
         * @summary Read Users
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        readUsersApiReadUsersGet: async (options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            const localVarPath = `/api/read_users`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'GET', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;


    
            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * 
         * @summary Update Lottery
         * @param {number} id 
         * @param {LotteryCreate} lotteryCreate 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        updateLotteryApiUpdateLotteryPut: async (id: number, lotteryCreate: LotteryCreate, options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            // verify required parameter 'id' is not null or undefined
            assertParamExists('updateLotteryApiUpdateLotteryPut', 'id', id)
            // verify required parameter 'lotteryCreate' is not null or undefined
            assertParamExists('updateLotteryApiUpdateLotteryPut', 'lotteryCreate', lotteryCreate)
            const localVarPath = `/api/update_lottery`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'PUT', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            if (id !== undefined) {
                localVarQueryParameter['id'] = id;
            }


    
            localVarHeaderParameter['Content-Type'] = 'application/json';

            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};
            localVarRequestOptions.data = serializeDataIfNeeded(lotteryCreate, localVarRequestOptions, configuration)

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * 
         * @summary Update User
         * @param {number} id 
         * @param {UserCreate} userCreate 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        updateUserApiUpdateUserPut: async (id: number, userCreate: UserCreate, options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            // verify required parameter 'id' is not null or undefined
            assertParamExists('updateUserApiUpdateUserPut', 'id', id)
            // verify required parameter 'userCreate' is not null or undefined
            assertParamExists('updateUserApiUpdateUserPut', 'userCreate', userCreate)
            const localVarPath = `/api/update_user`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'PUT', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            if (id !== undefined) {
                localVarQueryParameter['id'] = id;
            }


    
            localVarHeaderParameter['Content-Type'] = 'application/json';

            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};
            localVarRequestOptions.data = serializeDataIfNeeded(userCreate, localVarRequestOptions, configuration)

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
    }
};

/**
 * DefaultApi - functional programming interface
 * @export
 */
export const DefaultApiFp = function(configuration?: Configuration) {
    const localVarAxiosParamCreator = DefaultApiAxiosParamCreator(configuration)
    return {
        /**
         * 
         * @summary Create Lottery
         * @param {LotteryCreate} lotteryCreate 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async createLotteryApiCreateLotteryPost(lotteryCreate: LotteryCreate, options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<LotteryCreateResponse>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.createLotteryApiCreateLotteryPost(lotteryCreate, options);
            const localVarOperationServerIndex = configuration?.serverIndex ?? 0;
            const localVarOperationServerBasePath = operationServerMap['DefaultApi.createLotteryApiCreateLotteryPost']?.[localVarOperationServerIndex]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, localVarOperationServerBasePath || basePath);
        },
        /**
         * 
         * @summary Create User
         * @param {UserCreate} userCreate 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async createUserApiCreateUserPost(userCreate: UserCreate, options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<UserCreateResponse>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.createUserApiCreateUserPost(userCreate, options);
            const localVarOperationServerIndex = configuration?.serverIndex ?? 0;
            const localVarOperationServerBasePath = operationServerMap['DefaultApi.createUserApiCreateUserPost']?.[localVarOperationServerIndex]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, localVarOperationServerBasePath || basePath);
        },
        /**
         * 
         * @summary Delete Lottery
         * @param {number} id 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async deleteLotteryApiDeleteLotteryDelete(id: number, options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<any>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.deleteLotteryApiDeleteLotteryDelete(id, options);
            const localVarOperationServerIndex = configuration?.serverIndex ?? 0;
            const localVarOperationServerBasePath = operationServerMap['DefaultApi.deleteLotteryApiDeleteLotteryDelete']?.[localVarOperationServerIndex]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, localVarOperationServerBasePath || basePath);
        },
        /**
         * 
         * @summary Delete User
         * @param {number} id 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async deleteUserApiDeleteUserDelete(id: number, options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<any>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.deleteUserApiDeleteUserDelete(id, options);
            const localVarOperationServerIndex = configuration?.serverIndex ?? 0;
            const localVarOperationServerBasePath = operationServerMap['DefaultApi.deleteUserApiDeleteUserDelete']?.[localVarOperationServerIndex]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, localVarOperationServerBasePath || basePath);
        },
        /**
         * 
         * @summary Read Lotteries
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async readLotteriesApiReadLotteriesGet(options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<Array<Lotteries>>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.readLotteriesApiReadLotteriesGet(options);
            const localVarOperationServerIndex = configuration?.serverIndex ?? 0;
            const localVarOperationServerBasePath = operationServerMap['DefaultApi.readLotteriesApiReadLotteriesGet']?.[localVarOperationServerIndex]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, localVarOperationServerBasePath || basePath);
        },
        /**
         * 
         * @summary Read Users
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async readUsersApiReadUsersGet(options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<Array<Users>>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.readUsersApiReadUsersGet(options);
            const localVarOperationServerIndex = configuration?.serverIndex ?? 0;
            const localVarOperationServerBasePath = operationServerMap['DefaultApi.readUsersApiReadUsersGet']?.[localVarOperationServerIndex]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, localVarOperationServerBasePath || basePath);
        },
        /**
         * 
         * @summary Update Lottery
         * @param {number} id 
         * @param {LotteryCreate} lotteryCreate 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async updateLotteryApiUpdateLotteryPut(id: number, lotteryCreate: LotteryCreate, options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<LotteryCreateResponse>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.updateLotteryApiUpdateLotteryPut(id, lotteryCreate, options);
            const localVarOperationServerIndex = configuration?.serverIndex ?? 0;
            const localVarOperationServerBasePath = operationServerMap['DefaultApi.updateLotteryApiUpdateLotteryPut']?.[localVarOperationServerIndex]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, localVarOperationServerBasePath || basePath);
        },
        /**
         * 
         * @summary Update User
         * @param {number} id 
         * @param {UserCreate} userCreate 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async updateUserApiUpdateUserPut(id: number, userCreate: UserCreate, options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<UserCreateResponse>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.updateUserApiUpdateUserPut(id, userCreate, options);
            const localVarOperationServerIndex = configuration?.serverIndex ?? 0;
            const localVarOperationServerBasePath = operationServerMap['DefaultApi.updateUserApiUpdateUserPut']?.[localVarOperationServerIndex]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, localVarOperationServerBasePath || basePath);
        },
    }
};

/**
 * DefaultApi - factory interface
 * @export
 */
export const DefaultApiFactory = function (configuration?: Configuration, basePath?: string, axios?: AxiosInstance) {
    const localVarFp = DefaultApiFp(configuration)
    return {
        /**
         * 
         * @summary Create Lottery
         * @param {LotteryCreate} lotteryCreate 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createLotteryApiCreateLotteryPost(lotteryCreate: LotteryCreate, options?: any): AxiosPromise<LotteryCreateResponse> {
            return localVarFp.createLotteryApiCreateLotteryPost(lotteryCreate, options).then((request) => request(axios, basePath));
        },
        /**
         * 
         * @summary Create User
         * @param {UserCreate} userCreate 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createUserApiCreateUserPost(userCreate: UserCreate, options?: any): AxiosPromise<UserCreateResponse> {
            return localVarFp.createUserApiCreateUserPost(userCreate, options).then((request) => request(axios, basePath));
        },
        /**
         * 
         * @summary Delete Lottery
         * @param {number} id 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        deleteLotteryApiDeleteLotteryDelete(id: number, options?: any): AxiosPromise<any> {
            return localVarFp.deleteLotteryApiDeleteLotteryDelete(id, options).then((request) => request(axios, basePath));
        },
        /**
         * 
         * @summary Delete User
         * @param {number} id 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        deleteUserApiDeleteUserDelete(id: number, options?: any): AxiosPromise<any> {
            return localVarFp.deleteUserApiDeleteUserDelete(id, options).then((request) => request(axios, basePath));
        },
        /**
         * 
         * @summary Read Lotteries
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        readLotteriesApiReadLotteriesGet(options?: any): AxiosPromise<Array<Lotteries>> {
            return localVarFp.readLotteriesApiReadLotteriesGet(options).then((request) => request(axios, basePath));
        },
        /**
         * 
         * @summary Read Users
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        readUsersApiReadUsersGet(options?: any): AxiosPromise<Array<Users>> {
            return localVarFp.readUsersApiReadUsersGet(options).then((request) => request(axios, basePath));
        },
        /**
         * 
         * @summary Update Lottery
         * @param {number} id 
         * @param {LotteryCreate} lotteryCreate 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        updateLotteryApiUpdateLotteryPut(id: number, lotteryCreate: LotteryCreate, options?: any): AxiosPromise<LotteryCreateResponse> {
            return localVarFp.updateLotteryApiUpdateLotteryPut(id, lotteryCreate, options).then((request) => request(axios, basePath));
        },
        /**
         * 
         * @summary Update User
         * @param {number} id 
         * @param {UserCreate} userCreate 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        updateUserApiUpdateUserPut(id: number, userCreate: UserCreate, options?: any): AxiosPromise<UserCreateResponse> {
            return localVarFp.updateUserApiUpdateUserPut(id, userCreate, options).then((request) => request(axios, basePath));
        },
    };
};

/**
 * DefaultApi - object-oriented interface
 * @export
 * @class DefaultApi
 * @extends {BaseAPI}
 */
export class DefaultApi extends BaseAPI {
    /**
     * 
     * @summary Create Lottery
     * @param {LotteryCreate} lotteryCreate 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof DefaultApi
     */
    public createLotteryApiCreateLotteryPost(lotteryCreate: LotteryCreate, options?: RawAxiosRequestConfig) {
        return DefaultApiFp(this.configuration).createLotteryApiCreateLotteryPost(lotteryCreate, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * 
     * @summary Create User
     * @param {UserCreate} userCreate 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof DefaultApi
     */
    public createUserApiCreateUserPost(userCreate: UserCreate, options?: RawAxiosRequestConfig) {
        return DefaultApiFp(this.configuration).createUserApiCreateUserPost(userCreate, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * 
     * @summary Delete Lottery
     * @param {number} id 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof DefaultApi
     */
    public deleteLotteryApiDeleteLotteryDelete(id: number, options?: RawAxiosRequestConfig) {
        return DefaultApiFp(this.configuration).deleteLotteryApiDeleteLotteryDelete(id, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * 
     * @summary Delete User
     * @param {number} id 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof DefaultApi
     */
    public deleteUserApiDeleteUserDelete(id: number, options?: RawAxiosRequestConfig) {
        return DefaultApiFp(this.configuration).deleteUserApiDeleteUserDelete(id, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * 
     * @summary Read Lotteries
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof DefaultApi
     */
    public readLotteriesApiReadLotteriesGet(options?: RawAxiosRequestConfig) {
        return DefaultApiFp(this.configuration).readLotteriesApiReadLotteriesGet(options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * 
     * @summary Read Users
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof DefaultApi
     */
    public readUsersApiReadUsersGet(options?: RawAxiosRequestConfig) {
        return DefaultApiFp(this.configuration).readUsersApiReadUsersGet(options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * 
     * @summary Update Lottery
     * @param {number} id 
     * @param {LotteryCreate} lotteryCreate 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof DefaultApi
     */
    public updateLotteryApiUpdateLotteryPut(id: number, lotteryCreate: LotteryCreate, options?: RawAxiosRequestConfig) {
        return DefaultApiFp(this.configuration).updateLotteryApiUpdateLotteryPut(id, lotteryCreate, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * 
     * @summary Update User
     * @param {number} id 
     * @param {UserCreate} userCreate 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof DefaultApi
     */
    public updateUserApiUpdateUserPut(id: number, userCreate: UserCreate, options?: RawAxiosRequestConfig) {
        return DefaultApiFp(this.configuration).updateUserApiUpdateUserPut(id, userCreate, options).then((request) => request(this.axios, this.basePath));
    }
}



