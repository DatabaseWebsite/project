import useAuthStore from "@/store/user.ts";
import {jsonp} from "vue-jsonp";
import {record_login_log_api, record_operation_log_api} from "@/api/api.ts";

import Browser from "browser-tool";

const BrowserInfo = new Browser()
export const record = async (config, response) => {
  let api = config.url
  let method = config.method
  let requestModule = ''
  let status = response.status
  let code = response.data.message
  let username = useAuthStore().getUser.username
  if (api.startsWith('/api/login'))
    requestModule = '登录模块'
  else if (api.startsWith('/api/user/'))
    requestModule = '用户中心模块'
  else if (api.startsWith('/api/log/'))
    requestModule = '日志管理模块'
  else if (api.startsWith('/api/board/'))
    requestModule = '课程公告模块'
  else if (api.startsWith('/api/course/'))
    requestModule = '课程管理模块'
  else if (api.startsWith('/api/materials/'))
    requestModule = '课程资料模块'
  else if (api.startsWith('/api/homework/'))
    requestModule = '课程作业模块'
  else if (api.startsWith('/api/discussion/'))
    requestModule = '讨论区模块'
  else if (api.startsWith('/api/userManage/'))
    requestModule = '用户管理模块'
  else
    requestModule = '其他模块'
  let userInfo = await getUserInfo()
  userInfo = userInfo['result']
  console.log(userInfo)
  let ip = userInfo['ip']
  let address = userInfo['ad_info']['province'] + userInfo['ad_info']['city'] + userInfo['ad_info']['district']
  let date = new Date()
  let browser = BrowserInfo['browser'] + BrowserInfo['browserVersion']
  if (api === '/api/login' && status === 200) {
    await record_login_log_api(ip, address, browser, dateToString(date), username)
  }
  await record_operation_log_api(requestModule, api, ip, method, browser, status.toString(), code, dateToString(date), username)
}

function getUserInfo() {
  return new Promise((resolve, reject) => {
    jsonp('https://apis.map.qq.com/ws/location/v1/ip?key=3MMBZ-5EUCQ-ZRG5Y-2RYB6-QCBJH-7MFXN', {
      output: 'jsonp'
    }).then(res => {
      resolve(res)
    }).catch(err => {
      reject(err)
    })
  })
}
function dateToString(date: Date) {
  let year = date.getFullYear()
  let month: string | number = date.getMonth() + 1
  let day: string | number = date.getDate()
  let hour: string | number = date.getHours()
  let minute: string | number = date.getMinutes()
  let second: string | number = date.getSeconds()
  month = month < 10 ? ('0' + month) : month
  day = day < 10 ? ('0' + day) : day
  hour = hour < 10 ? ('0' + hour) : hour
  minute = minute < 10 ? ('0' + minute) : minute
  second = second < 10 ? ('0' + second) : second
  return year + '-' + month + '-' + day + 'A' + hour + ':' + minute + ':' + second
}