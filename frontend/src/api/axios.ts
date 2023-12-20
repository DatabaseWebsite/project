import axios from 'axios'
import cookies from "@/lib/cookies.ts";
import {router} from "@/router";
import {ElLoading, ElMessage} from "element-plus";
import {user_refresh_token_api} from "@/api/api.ts";
import useAuthStore from "@/store/user.ts";
import {record} from "@/api/record.ts";

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

// 设置接口超时时间
axios.defaults.timeout = 60000;

axios.defaults.baseURL = 'http://127.0.0.1:8000/';
// http request 拦截器
axios.interceptors.request.use(function (config){
  // 在发送请求前做些什么
  startLoading();
  let token = cookies.get('token')
  config.headers.Authorization = "Bearer " + token
  console.log(config)
  return config;
},function (error) {
  // 对请求错误做些什么
  console.log(error)
  return Promise.reject(error);
});

// 添加响应拦截器
axios.interceptors.response.use(async function (response) {
  // 2xx 范围内的状态码都会触发该函数。
  // 对响应数据做点什么
  endLoading()
  let dataAxios = response || null;
  // 这个状态码是和后端约定的
  let status = response.status
  switch (status) {
    case 200:
      // success
      if (!response.config.url.startsWith('api/log/'))
        await record(response.config, response)
      return dataAxios
    case 201:
      if (response.config.url === 'api/user/login/') {
        ElMessage.error(dataAxios.data['error'])
        await record(response.config, response)
        break
      }
      let res = await user_refresh_token_api()
      let config = response.config
      cookies.set('token', res.data.access)
      config.headers.Authorization = 'Bearer ' + res.data.access
      config["__retryCount"] = config["__retryCount"] || 0
      if (config["__retryCount"] >= config["retry"]) {
        // 如果重试次数超过3次则跳转登录页面
        cookies.removeAll()
        router.push({path: '/login'})
        ElMessage.error('认证已失效,请重新登录~')
        break
      }
      config["__retryCount"] += 1
      return axios(config)
    default:
      ElMessage.error(dataAxios.data['error'])
      break
  }
  return response
}, async function (error) {
  // 超出 2xx 范围的状态码都会触发该函数。
  // 对响应错误做点什么
  console.log(error)
  endLoading()
  if (!error.response.config.url.startsWith('api/log/'))
    await record(error.config, error.response)
  const {status} = error.response
  switch (status) {
    case 401:
      cookies.removeAll()
      useAuthStore().logout()
      router.push({ path: '/login' })
      error.response.error = '认证已失效,请重新登录~'
      break
    case 403:
      error.response.error = '拒绝访问'
      break
    case 404:
      error.response.error = `请求地址出错: ${error.response.config.url}`
      break
    case 408:
      error.response.error = '请求超时'
      break
    case 500:
      error.response.error = '服务器内部错误'
      break
    case 501:
      error.response.error = '服务未实现'
      break
    case 502:
      error.response.error = '网关错误'
      break
    case 503:
      error.response.error = '服务不可用'
      break
    case 504:
      error.response.error = '网关超时'
      break
    case 505:
      error.response.error = 'HTTP版本不受支持'
      break
    default:
      break
  }
  ElMessage.error(error.response.error)
  return Promise.reject(error)
});

export default axios