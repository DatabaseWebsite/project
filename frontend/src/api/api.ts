import cookies from "@/lib/cookies.ts";
import axios from "@/api/axios.ts";

/**
 * @api {get} /user/refresh-token 刷新token
 */
export const user_refresh_token_api = () => {
  cookies.set('token', cookies.get('refresh'));
  return axios.get('api/user/refresh-token/')
}
export const user_login_api = (username:string, password: string) => {
  const data = new URLSearchParams();
  data.append('username', username);
  data.append('password', password);
  return axios.post('api/user/login/', data)
}

export const user_logout_api = () => {
  return axios.get('api/user/logout/')
}
export const user_update_avatar_api = (avatar: FormData) => {
  return axios.post('api/user/update-avatar/', avatar)
}

export const user_info_api = () => {
  return axios.get('api/user/user-info/')
}

export const user_change_password_api = (oldPassword: string, newPassword: string) => {
  let data = new URLSearchParams();
  data.append('old_password', oldPassword);
  data.append('new_password', newPassword);
  return axios.post('api/user/change-password/', data)
}

/*
 * @api {get} /all-course-info/ 获取所有课程信息
 * @return result: 每条信息包含course_id, name
 */
export const get_all_courses_api = () => {
  return axios.get('api/userManage/all-course-info/')
}
export const get_user_select_course_api = () => {
  return axios.get('api/user/user-selected-course/')
}

export const user_select_course_api = (courseId: number) => {
 let data = new URLSearchParams();
  data.append('course_id', courseId.toString());
  return axios.post('api/user/update-current-course/', data)
}


/*
 * @api {post} /upload-materials/ 上传文件
 * @param files: {{name, raw}*}
 * 另外，上传的课程id即为该用户的当前课程
 * 需要后端记录上传时间
 */
export const upload_materials_api = (files: FormData) => {
  return axios.post('api/material/upload-materials/', files)
}

/*
 * @api {get} /get-materials/ 获取课程资料
 * 根据用户当前课程获取课程资料
 * @return materials
 */
export const get_materials_api = () => {
  return axios.get('api/material/material-list/')
}

/*
 * @api {post} /del-material/ 删除课程资料
 * @param material_id: int 资料id
 * @return null
 */
export const del_material_api = (id:number) => {
  let data = new URLSearchParams();
  data.append('material_id', id.toString());
  return axios.post('api/material/del-material/', data)
}

/*
 * @api {post} /upload-image/ 上传图片
 * 'image': file
 * @return {string} url, {string} name
 */
export const upload_image_api = (image: FormData) => {
  return axios.post('api/upload-image/', image)
}

/*
  * @api {get} /user-list/ 获取用户列表
  * @return result: 每条信息包含id, personId, username, grade, course, courses:{course_name, identity}
 */
export const get_user_list_api = (page:number=1) => {
return axios.get('api/userManage/user-list/?page=' + page.toString())
}

export const get_all_user_list_api = () => {
  return axios.get('api/userManage/user-list/page=')
}

/*
 * @api {post} /signup/ 单用户注册
 */
export const signup_api = (personId: string, username: string, grade: string, course: string, identity: string) => {
  let data = new URLSearchParams();
  data.append('person_id', personId)
  data.append('username', username) // 密码默认为personId
  data.append('grade', grade)
  data.append('course_id', course)
  data.append('identity', identity)
  return axios.post('api/userManage/create-single-user/', data)
}

/*
 * @api {post} /del-user/ 删除用户
 */
export const del_user_api = (id: number) => {
  let data = new URLSearchParams();
  data.append('id', id.toString())
  return axios.post('api/userManage/del-user/', data)
}

/*
 * @api {post} /update-user/ 更新用户信息
 */
export const update_userinfo_api = (id: number, personId: string, username: string, grade: string) => {
  let data = new URLSearchParams();
  data.append('id', id.toString())
  data.append('person_id', personId)
  data.append('username', username)
  data.append('grade', grade)
  return axios.post('api/userManage/update-user-info/', data)
}

/*
 * @api {post} /reset-user-password/ 重置用户密码
 * 密码重置为personId
 */
export const reset_user_password_api = (id: number) => {
  let data = new URLSearchParams();
  data.append('id', id.toString())
  return axios.post('api/userManage/reset-user-password/', data)
}

/*
  * @api {post} /excel-create-users/ 批量注册
  * @param excel: FormData: 通过xlsxFile获取，excel内包含学号，姓名，年级
  * @param course: string: 课程名
  * @param identity: string: 身份
 */
export const excel_create_users_api = (excel: FormData, course_id:string, identity: string) => {
  let data = new URLSearchParams();
  data.append('course_id', course_id)
  data.append('identity', identity)
  return axios.post('api/userManage/xlsx-create-users/', excel, {params: data})
}

/*
  * @api {post} /del-users/ 批量删除用户
  * @param ids: number[]: 用户id列表
 */
export const del_users_api = (ids: number[]) => {
  return axios.post('api/userManage/del-users/', {ids})
}

/*
 *@api {get} /search-user/ 搜索用户
 * @params personId: string, username: string, grade: string, course: number, identity: string
 * return result: 每条包含 id, personId, username, grade, course, courses:{course_name, identity}
 */
export const search_user_api = (personId: string, username: string, grade: string, course:string, identity: string, page: number) => {
  let data = new URLSearchParams();
  data.append('person_id', personId)
  data.append('username', username)
  data.append('grade', grade)
  data.append('course', course)
  data.append('identity', identity)
  data.append('page', page.toString())
  return axios.post('api/userManage/search-users/', data)
}

export const search_all_user_api = (personId: string, username: string, grade: string, course:string, identity: string) => {
  let data = new URLSearchParams();
  data.append('person_id', personId)
  data.append('username', username)
  data.append('grade', grade)
  data.append('course', course)
  data.append('identity', identity)
  return axios.post('api/userManage/search-users/', data)
}

export const get_login_log_api = (page: number) => {
  return axios.get('api/log/login-log/?page=' + page.toString())
}

export const search_login_log_api = (username: string, ip: string, startTime:string, endTime:string, page: number) => {
  let data = new URLSearchParams();
  data.append('username', username)
  data.append('ip', ip)
  data.append('start_time', startTime)
  data.append('end_time', endTime)
  data.append('page', page.toString())
  return axios.post('api/log/search-login-log/', data)
}

export const get_operation_log_api = (page: number) => {
  return axios.get('api/log/operation-log/?page=' + page.toString())
}

export const search_operation_log_api = (requestModule:string, api: string, ip: string, username: string, operation: string, starTime: string, endTime: string, page: number) => {
  let data = new URLSearchParams();
  data.append('request_module', requestModule)
  data.append('ip', ip)
  data.append('username', username)
  data.append('operation', operation)
  data.append('start_time', starTime)
  data.append('end_time', endTime)
  data.append('page', page.toString())
  data.append('api', api)
  return axios.post('api/log/search-operation-log/', data)
}

export const record_login_log_api = (ip:string, address: string, browser: string, time:string, username: string) => {
  let data = new URLSearchParams();
  data.append('ip', ip)
  data.append('address', address)
  data.append('browser', browser)
  data.append('time', time)
  data.append('username', username)
  return axios.post('api/log/record-login-log/', data)
}

export const record_operation_log_api = (requestModule:string, api: string, ip: string, operation: string, browser: string, status: string, code: string, time: string, username: string) => {
  let data = new URLSearchParams();
  data.append('request_module', requestModule)
  data.append('api', api)
  data.append('operation', operation)
  data.append('ip', ip)
  data.append('time', time)
  data.append('browser', browser)
  data.append('status', status)
  data.append('code', code)
  data.append('username', username)
  return axios.post('api/log/record-operation-log/', data)
}

export const create_course_api = (name: string) => {
  const data = new URLSearchParams();
  data.append('course_name', name)
  return axios.post('api/course/create-course/', data)
}

export const all_course_info_api = () => {
  return axios.get('api/userManage/all-course-info/')
}

/*
 * title: string
 * file: files
 * description: string
 * totalScore: string
 * deadline: string // 后端：datetime.fromisoformat(deadline)
 */
export const create_work_api = (data : FormData) => {
  return axios.post('api/homework/create-work', data)
}
/*
 * id: string
 * title: string
 * file: file
 * description: string
 * totalScore: string
 * deadline: string // 后端：datetime.fromisoformat(deadline)
 */
export const modify_work_api = (data : FormData) => {
  return axios.post('api/homework/modify-work', data)
}
export const delete_work_api = (id : number) => {
  return axios.post('api/homework/remove-work', id.toString())
}
/*
 * 根据身份判断返回信息
 * 老师等返回创建时的所有信息,files返回id, name, url
 * 学生：返回id,title, totalScore, deadline, status, score
 */
export const get_works_info_api = () => {
  return axios.get('api/homework/works-info')
}

export const get_one_work_api = (id: number) => {
  let data = new URLSearchParams()
  data.append('id', id.toString())
  return axios.post('api/homework/work-detail/', data)
}

export const get_work_submissions_api = (page: number) => {
  return axios.get('api/homework/work-submissions/?page=' + page.toString())
}

export const get_work_submission_by_id_api = (id: any) => {
  let data = new URLSearchParams()
  data.append('id', id.toString())
  return axios.post('api/homework/work-submissions-detail/', data)
}

export const submit_work_score_api = (id: number, score: number) => {
  let data = new URLSearchParams()
  data.append('id', id.toString())
  data.append('score', score.toString())
  return axios.post('api/homework/submit-work-score/', data)
}

export const student_get_work_detail_api = (id: number) => {
  let data = new URLSearchParams()
  data.append('id', id.toString())
  return axios.post('api/homework/student-work-detail', data)
}

export const student_submit_work_api = (id: number, context: string, file: any) => {
  let data = new FormData()
  data.append('id', id.toString())
  data.append('context', context)
  data.append('file', file.raw)
  return axios.post('api/homework/student-submit-work', data)
}
