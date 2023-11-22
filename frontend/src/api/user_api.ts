import cookies from "@/lib/cookies.ts";
import {request} from "@/api/service.ts";

/**
 * @api {post} /user/refresh-token 刷新token
 */
export const refreshToken = () => {
  const refresh = cookies.get('refresh');
  return request({
    url: 'user/refresh-token/',
    method: 'post',
    data: {
      refresh: refresh
    }
  })
}
export const user_login_api = (data) => {
  return request({
    url: 'api/login/',
    method: 'post',
    data
  })
}

export const user_info_api = () => {
  return request({
    url: 'api/user-info/',
    method: 'get',
    params: {}
  })
}