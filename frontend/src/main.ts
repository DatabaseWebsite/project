import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from './api/axios.ts'
import {router} from './router'
import {createPinia} from 'pinia'
import "@icon-park/vue-next/styles/index.css";
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate' // pinia状态可持久化
import mdEditor from "@/components/markdown/mdEditor.vue";
import mdPreview from "@/components/markdown/mdPreview.vue";

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

//注册
const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.config.globalProperties.$axios = axios;
app.use(router)
app.use(ElementPlus)
app.use(pinia)
app.component('mdPreview', mdPreview);
app.component('mdEditor', mdEditor)
app.mount('#app')
