import {defineStore} from "pinia"
import {reactive, ref} from "vue";

export const useAuthStore = defineStore('auth', {
    persist: true,
    state: () => {
        return {
            isAuthenticated:ref(false), // 登录状态，默认为未登录
            user: reactive({"username": '', "email":'', "avatar":'', "motto": '这个人很懒，什么也没有留下。。。'}) // 存储用户信息
        }
    },

    getters: {
        getAuthenticated: (state) => state.isAuthenticated,
        getUser: (state) => state.user,
    },

    actions: {
        loginSuccess() {
            this.isAuthenticated = true
        },
        login(user:any) {
            this.user['username'] = user['username']
            this.user['email'] = user['email']
            if (user['avatar'] != '') this.user['avatar'] = user['avatar']
            if (user['motto'] != 'nothing') this.user['motto'] = user['motto']
        },
        logout() {
            this.isAuthenticated = false
            this.user = {"username": '', "email":'', "avatar":'', "motto": '这个人很懒，什么也没有留下。。。'}
        },
        setEmail(email:string) {
            this.user['email'] = email
        },
        setUsername(username:string) {
            this.user['username'] = username
        },
        setMotto(motto:string) {
            this.user['motto'] = motto
        },
        setAvatar(avatar:string) {
            this.user['avatar'] = avatar
        }
    }
})
export default useAuthStore