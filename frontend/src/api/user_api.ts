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