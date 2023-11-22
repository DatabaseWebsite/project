import axios from 'axios'
import cookies from "@/lib/cookies.ts";
import {router} from "@/router";
import {ElLoading, ElMessage} from "element-plus";
import {refreshToken} from "@/api/user_api.ts";
import qs from 'qs';
import {get} from "lodash";
/**
 * @description: 创建axios实例
 */
let loading: any;
const startLoading = () => {

    interface Options {
        lock: boolean;
        text: string;
        background: string;
    }

    const options: Options = {
        lock: true,
        text: "加载中...",
        background: 'rgba(0,0,0,0.7)'
    }
    loading = ElLoading.service(options);
}

const endLoading = () => {
    loading.close();
}
export function getErrorMessage (msg) {
    if (typeof msg === 'string') {
        return msg
    }
    if (typeof msg === 'object') {
        if (msg.code === 'token_not_valid') {
            cookies.remove('token')
            cookies.remove('uuid')
            router.push({ path: '/login' })
            router.go(0)
            return '登录超时，请重新登录！'
        }
        if (msg.code === 'user_not_found') {
            cookies.remove('token')
            cookies.remove('uuid')
            router.push({ path: '/login' })
            router.go(0)
            return '用户无效，请重新登录！'
        }
        return Object.values(msg)
    }
    if (Object.prototype.toString.call(msg).slice(8, -1) === 'Array') {
        return msg
    }
    return msg
}

function createService() {
    // 创建一个 axios 实例
    const service = axios.create({
        baseURL: 'http://127.0.0.1:8000/',
        timeout: 60000,
        paramsSerializer: (params) => qs.stringify(params, { indices: false }) // 参数序列化
    })
// http request 拦截器
    service.interceptors.request.use(function (config){
        // 在发送请求前做些什么
        startLoading();
        return config;
    },function (error) {
        // 对请求错误做些什么
        console.log(error)
        return Promise.reject(error);
    });
// 添加响应拦截器
    service.interceptors.response.use(async function (response) {
        // 2xx 范围内的状态码都会触发该函数。
        // 对响应数据做点什么
        endLoading()
        let dataAxios = response.data || null;
        if (response.headers['content-disposition']) { // todo: 处理文件下载
            dataAxios = response
        }
        // 这个状态码是和后端约定的
        const {code} = dataAxios
        switch (code) {
            case 200:
                // success
                return dataAxios
            case 401:
                if (response.config.url === 'api/login/') {
                    getErrorMessage(dataAxios['error'])
                    break
                }
                let res = await refreshToken()
                let config = response.config
                cookies.set('token', res.data.access)
                config.headers.Authorization = 'Bearer ' + res.data.access
                config["__retryCount"] = config["__retryCount"] || 0
                if (config["__retryCount"] >= config["retry"]) {
                    // 如果重试次数超过3次则跳转登录页面
                    cookies.remove('token')
                    cookies.remove('uuid')
                    router.push({path: '/login'})
                    ElMessage.error('认证已失效,请重新登录~')
                    break
                }
                config["__retryCount"] += 1
                return service(config)
            default:
                ElMessage.error(getErrorMessage(dataAxios.msg))
                break
        }
        return response
    }, async function (error) {
        // 超出 2xx 范围的状态码都会触发该函数。
        // 对响应错误做点什么
        endLoading()
        const {status} = error.response
        switch (status) {
            case 400:
                error.message = '请求错误'
                break
            case 401:
                cookies.remove('token')
                cookies.remove('uuid')
                cookies.remove('refresh')
                router.push({ path: '/login' })
                error.message = '认证已失效,请重新登录~'
                break
            case 403:
                error.message = '拒绝访问'
                break
            case 404:
                error.message = `请求地址出错: ${error.response.config.url}`
                break
            case 408:
                error.message = '请求超时'
                break
            case 500:
                error.message = '服务器内部错误'
                break
            case 501:
                error.message = '服务未实现'
                break
            case 502:
                error.message = '网关错误'
                break
            case 503:
                error.message = '服务不可用'
                break
            case 504:
                error.message = '网关超时'
                break
            case 505:
                error.message = 'HTTP版本不受支持'
                break
            default:
                break
        }
        ElMessage.error(error.message)
        return Promise.reject(error)
    })
    return service
}
/**
 * @description 创建请求方法
 * @param {Object} service axios 实例
 */
function createRequestFunction (service) {
    // 校验是否为租户模式。租户模式把域名替换成 域名 加端口
    return function (config) {
        const token = cookies.get('token')
        // 进行布尔值兼容
        let params = get(config, 'params', {})
        for (const key of Object.keys(params)) {
            if (String(params[key]) === 'true') {
                params[key] = 1
            }
            if (String(params[key]) === 'false') {
                params[key] = 0
            }
        }
        const configDefault = {
            headers: {
                Authorization: 'Bearer ' + token,
            },
            timeout: 60000,
            baseURL: 'http://127.0.0.1:8000/',
            data: {},
            params: params,
            retry: 3, // 重新请求次数
            retryDelay: 1000 // 重新请求间隔
        }
        return service(Object.assign(configDefault, config))
    }
}
export const service = createService()
export const request = createRequestFunction(service)