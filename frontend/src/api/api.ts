import cookies from "@/lib/cookies.ts";
import {request} from "@/api/service.ts";

/**
 * @api {post} /user/refresh-token 刷新token
 */
export const user_refresh_token_api = () => {
  const refresh = cookies.get('refreshToken');
  return request({
    url: 'api/refresh-token/',
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
/*
 * @api {post} /upload-file/ 上传文件
 * @param files: {{name, raw}*}
 * @param uploadType: string 上传类型, 例如 '课程资料',
 * 另外，上传的课程id即为该用户的默认课程id
 * 需要后端记录上传时间
 */
export const upload_file_api = (data) => {
  return request({
    url: 'api/upload-file/',
    method: 'post',
    data
  })
}

export const get_materials_api = () => {
  return request({
    url: 'api/get-materials/',
    method: 'get',
    params: {}
  })
}

/*
 * @api {post} /upload-image/ 上传图片
 * 'image': raw
 * @return {string} url, {string} name
 */
export const upload_image_api = (data) => {
  return request({
    url: 'api/upload-image/',
    method: 'post',
    data
  })
}

