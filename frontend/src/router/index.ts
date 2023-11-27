import {createRouter, createWebHashHistory, RouteRecordRaw} from "vue-router";
import Index from "@/views/index.vue"
import UserCenter from "@/components/userCenter/index.vue"
import Login from "@/views/login.vue"
import NotFound from "@/views/404.vue"
import Reference from "@/components/materials/index.vue"
import DiscussionArea from "@/views/discussionArea.vue";
import useAuthStore from "@/store/user.ts";
import announceFormVue from "@/components/announce/announceForm.vue";
import Announcement from "@/views/announcement.vue"
const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'login',
    component: Login,
  },
  {
    path:'/',
    name: 'index',
    component: Index,
    // redirect: ; 设为课程公告页，保证一进入就渲染右侧页面
    children: [
      {
        path: '/reference',
        name: 'reference',
        component: Reference,
      },
      {
        path: '/userCenter',
        name: 'userCenter',
        component: UserCenter,
      },
      {
        path: '/discussionArea',
        name: 'discussionArea',
        component: DiscussionArea,
      },
      {
        path: '/announcement',
        name: 'announcement',
        component: Announcement,
      },
    ]
  },
  {
    path:"/:pathMatch(.*)*",
    name: 'NotFound',
    component:NotFound
  },
]
// 创建router
const router = createRouter({
  // 配置为Hash模式
  history: createWebHashHistory(),
  // 配置routes
  routes,
  // 路由跳转时返回顶部
  scrollBehavior () {
    return {top: 0}
  }
})

// 路由守卫
//@ts-ignore
router.beforeEach((to, from,next) =>{
  const userStore = useAuthStore()
  const isLogin = userStore.getAuthenticated
  const identity = userStore.getUser['identity']
  if (to.path === "/login") {
    // 若用户已登录且前往登录页，则跳转到首页
    isLogin ? next("/") : next()
  } else { // 拦截
    isLogin ? next() : next("/login")
  }
})

export {router}

