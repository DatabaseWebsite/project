import cookies from "@/lib/cookies.ts";
import axios from "@/api/axios.ts";

/**
 * @api {get} /user/refresh-token 刷新token
 */
export const user_refresh_token_api = () => {
  cookies.set('token', cookies.get('refresh'));
  return axios.get('api/refresh-token/')
}
export const user_login_api = (username:string, password: string) => {
  const data = new URLSearchParams();
  data.append('username', username);
  data.append('password', password);
  return axios.post('api/login/', data)
}

export const user_logout_api = () => {
  return axios.get('api/logout/')
}
export const user_update_avatar_api = (avatar: FormData) => {
  return axios.post('api/update-avatar/', avatar)
}

export const user_info_api = () => {
  return axios.get('api/user-info/')
}

export const user_change_password_api = (oldPassword: string, newPassword: string) => {
  let data = new URLSearchParams();
  data.append('old_password', oldPassword);
  data.append('new_password', newPassword);
  return axios.post('api/change-password/', data)
}

/*
 * @api {post} /upload-materials/ 上传文件
 * @param files: {{name, raw}*}
 * @param uploadType: string 上传类型, 例如 '课程资料'（支持复用接口）
 * 另外，上传的课程id即为该用户的默认课程(即在用户信息栏里边要记录用户当前使用的course)
 * 需要后端记录上传时间
 */
export const upload_materials_api = (files: FormData) => {
  return axios.post('api/upload-materials/', files)
}

/*
 * @api {get} /get-materials/ 获取课程资料
 * 根据用户当前课程获取课程资料
 * @return materials
 */
export const get_materials_api = () => {
  return axios.get('api/get-materials/')
}

/*
 * @api {post} /del-material/ 删除课程资料
 * @param id: int 资料id
 * @return null
 */
export const del_material_api = () => {
}

/*
 * @api {post} /upload-image/ 上传图片
 * 'image': file
 * @return {string} url, {string} name
 */
export const upload_image_api = (image: FormData) => {
  return axios.post('api/upload-image/', image)
}

