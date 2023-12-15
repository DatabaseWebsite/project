import Cookies from 'js-cookie'

/**
 * @description 处理cookie,cookie仅存储uuid,token，refresh
 */
const cookies = {
  /**
   * @description 存储 cookie 值
   * @param {String} name cookie name
   * @param {String} value cookie value
   * @param {Object} cookieSetting cookie setting, （可选）包括有效期 expires（单位：天），路径 path，域名 domain，安全选项 secure
   */
  set: (name = 'default', value = '', cookieSetting = {}) => {
    const currentCookieSetting = {
      expires: 1
    }
    Object.assign(currentCookieSetting, cookieSetting)
    Cookies.set(`databaseCPW-${name}`, value, currentCookieSetting)
  },
  /**
   * @description 拿到 cookie 值
   * @param {String} name cookie name
   */
  get: (name = 'default') => {
    return Cookies.get(`databaseCPW-${name}`)
  },
  /**
   * @description 拿到 cookie 全部的值
   */
  getAll: () => {
    return Cookies.getAll()
  },
  /**
   * @description 删除 cookie
   * @param {String} name cookie name
   */
  remove: (name = 'default') => {
    return Cookies.remove(`databaseCPW-${name}`)
  },
  removeAll: () => {
    const cookies = Cookies.get()
    Object.keys(cookies).forEach(name => {
      if (name.startsWith('databaseCPW-'))
        Cookies.remove(name)
    })
  }
}

export default cookies