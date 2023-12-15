import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import {resolve} from 'path'
import { prismjsPlugin } from 'vite-plugin-prismjs'

// https://vitejs.dev/config/
export default defineConfig({
  base: './',
  plugins: [
    vue(),
    prismjsPlugin({
      languages: ['javascript', 'css', 'markup', 'typescript', 'go', 'python', 'java', 'php', 'csharp', 'cpp', 'bash', 'nginx', 'sql', 'json', 'yaml', 'docker', 'markdown', 'git', 'ini', 'less', 'scss', 'stylus', 'vim', 'makefile', 'powershell', 'shell', 'shell-session', 'http', 'toml', 'xml', 'yaml'],
      plugins: ['line-numbers'],
    })
  ],
  resolve: {
    alias: {
      "@":resolve(__dirname, 'src')
    }
  },
  server: {
    cors: true,
    open: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000/',   //代理接口
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  build: {
    outDir: resolve('./dist'),
    // 指定生成静态资源的存放路径(相对于 build.outDir), 默认assets。
    assetsDir: 'static',
    manifest: true,
    emptyOutDir: true,
    // 设置最终构建的浏览器兼容目标。
    target: 'es2015',
    rollupOptions: {
      input: {
        index: resolve(__dirname, 'index.html'),
        main: resolve('./src/main.ts'),
      },
    }
  },
})
