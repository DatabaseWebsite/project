import {defineStore} from "pinia"
import {reactive, ref} from "vue";

export const useAuthStore = defineStore('auth', {
    persist: true,
    state: () => {
        return {
            isAuthenticated:ref(false), // 登录状态，默认为未登录
            user: reactive({"username": '', "personID": '', "avatar":'', "identity": '', "course": ''}) // 存储用户信息
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
        setUserinfo(user:any) {
            this.user['username'] = user['username']
            this.user['personID'] = user['personID']
            this.user['avatar'] = user['avatar']
            this.user['identity'] = user['identity']
            this.user['course'] = user['course']
        },
        logout() {
            this.isAuthenticated = false
            this.user = {"username": '', "personID": '', "avatar":'', "identity": '', "course": ''}
        },
        setAvatar(avatar:string) {
            this.user['avatar'] = avatar
        },
        setCourse(course:string) {
            this.user['course'] = course
        }
    }
})
export default useAuthStore