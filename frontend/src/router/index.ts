import {createRouter, createWebHashHistory, RouteRecordRaw} from "vue-router";
import Index from "@/views/index.vue"
const index: RouteRecordRaw[] = [
  {
    path: "/",
    name: "index",
    component: Index,
  }
]
// 创建router
export const router = createRouter({
  // 配置为Hash模式
  history: createWebHashHistory(),
  // 配置routes
  routes: index,
  // 路由跳转时返回顶部
  scrollBehavior () {
    return {top: 0}
  }
})