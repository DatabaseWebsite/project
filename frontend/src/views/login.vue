<template>
<!--  <img src="@/assets/img/loginBackground.png" alt="" class="backpage">-->
  <iframe src="src/components/canvas/whirlpool.html" :width="width" :height="height" style="position: absolute; top:0; left:0"/>
  <div class="container">
      <!-- 登录 -->
    <div style="font-size:40px; color:white; font-weight: bold; margin-top:50px; margin-bottom: 50px">
      欢迎来到数据库课程平台
    </div>
    <div style="width:500px; flex-direction: column;justify-content: center;align-items: center;">
      <LoginForm :loginUser="loginUser" :rules="rules" />
      <div style="margin-top:50px; text-align: right; font-size: 15px; color: white;">
        忘记密码请联系老师或助教
      </div>
    </div>

  </div>
</template>
<script lang="ts">
import { loginUser, rules} from "@/components/login/loginValidators.ts";
import LoginForm from "@/components/login/loginForm.vue";
import {onMounted, ref} from "vue";

export default {
  name: "login",
  components: { LoginForm },
  setup() {
    const width = ref(0)
    const height = ref(0)
    onMounted(() => {
      getWindowResize()
      window.addEventListener('resize', getWindowResize)
    })
    const getWindowResize = function () {
      width.value = window.innerWidth
      height.value = window.innerHeight
    }
    return {
      loginUser,
      rules,
      width,
      height
    };
  },
};
</script>

<style scoped>
.backpage {
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  position:fixed;
  z-index: -1;
}
.background-container {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: -1; /* 将背景组件放在其他内容下面 */
}
* {
  box-sizing: border-box;
}
body {
  font-family: 'Montserrat',sans-serif;
  background-image: linear-gradient(120deg,#3498db,#8e44ad);;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: -20px 0 50px;
}

h1 {
  font-weight: bold;
  margin: 0;
}
p {
  font-size: 14px;
  line-height: 20px;
  letter-spacing: .5px;
  margin: 20px 0 30px;
}
span {
  font-size: 12px;
}
a {
  color: #333;
  font-size: 14px;
  text-decoration: none;
  margin: 15px 0;
}
.return-button {
  position: relative;
  margin-bottom: 50px;
}
.container {
  /*background: #fff;*/
  /*backdrop-filter: saturate(180%) blur(5px)!important;*/
  /*-webkit-backdrop-filter: saturate(180%) blur(5px)!important;*/
  /* 磨砂的背景颜色 */
  backdrop-filter: blur(10);
  /*background-color: rgb(16, 31, 48, 0.3);*/
  border-radius: 10px;
  box-shadow: rgba(0, 0, 0, 0.4) 0 2px 4px, rgba(0, 0, 0, 0.3) 0 7px 13px -3px, rgba(0, 0, 0, 0.2) 0 -3px 0 inset;  position: relative;
  overflow: hidden;
  width: 600px;
  max-width: 100%;
  min-height: 480px;
  text-align: center;
}
.form-container form {
  /*background: #fff;*/
  display: flex;
  flex-direction: column;
  padding: 0 50px;
  height: 100%;
  justify-content: center;
  text-align: center;
}
.social-container {
  margin: 20px 0;
}

.social-container a {
  border: 1px solid #ddd;
  border-radius: 50%;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  margin: 0 5px;
  height: 40px;
  width: 40px;
}

.social-container a:hover {
  background-color: #eee;

}

.txtb {
  border-bottom: 2px solid #adadad;
  position: relative;
  margin: 10px 0;
}

.txtb input {
  font-size: 15px;
  color: #333;
  border: none;
  width: 100%;
  outline: none;
  background: none;
  padding: 0 3px;
  height: 35px;
}

.txtb span::before {
  content: attr(data-placeholder);
  position: absolute;
  top: 50%;
  left: 5px;
  color: #adadad;
  transform: translateY(-50%);
  transition: .5s;
}
.txtb span::after {
  content: '';
  position: absolute;
  left: 0%;
  top: 100%;
  width: 0%;
  height: 2px;
  background-image: linear-gradient(120deg,#3498db,#8e44ad);
  transition: .5s;
}

.focus + span::before {
  top: -5px;
}

.focus + span::after {
  width: 100%;
}

button {
  border-radius: 20px;
  border: 1px solid #ff4b2b;
  background: #ff4b2b;
  color: #fff;
  font-size: 12px;
  font-weight: bold;
  padding: 12px 45px;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: transform 80ms ease-in;
  cursor: pointer;
}

button:active {
  transform: scale(.95);
}

button:focus {
  outline: none;
}

button.ghost {
  background: transparent;
  border-color: #fff;
}

.form-container {
  position: absolute;
  top: 0;
  height: 100%;
  transition: all .6s ease-in-out;
}

.form-container button {
  background: linear-gradient(120deg, #3498db, #8e44ad);
  border: none;
  background-size: 200%;
  color: #fff;
  transition: .5s;
}

.form-container button:hover {
  background-position: right;
}

.sign-in-container {
  left: 0;
  width: 50%;
  z-index: 2;
}
.sign-in-container form a {
  position: relative;
  left: 100px;
}
.sign-up-container {
  left: 0;
  width: 50%;
  z-index: 1;
  opacity: 0;
}
.sign-up-container button {
  margin-top: 20px;
}
.overlay-container {
  position:absolute;
  top: 0;
  left: 50%;
  width: 50%;
  height: 100%;
  overflow: hidden;
  transition: transform .6s ease-in-out;
  z-index: 100;
}
.overlay {
  color: #fff;
  position: relative;
  left: -100%;
  height: 100%;
  width: 200%;
  transform: translateY(0);
  transition: transform .6s ease-in-out;
}
.overlay-panel {
  position: absolute;
  top: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 0 40px;
  height: 100%;
  width: 50%;
  text-align: center;
  transform: translateY(0);
  transition: transform .6s ease-in-out;
}
.overlay-right {
  right: 0;
  transform: translateY(0);

}

.overlay-left {
  transform: translateY(-20%);
}

.container.right-panel-active .sign-in-container {
  transform: translateY(100%);
}

.container.container.right-panel-active .overlay-container {
  transform: translateX(-100%);
}
.container.right-panel-active .sign-up-container {
  transform: translateX(100%);
  opacity: 1;
  z-index: 5;
}
.container.container.right-panel-active .overlay {
  transform: translateX(50%);
}
.container.container.right-panel-active .overlay-left {
  transform: translateY(0);
}
.container.container.right-panel-active .overlay-right {
  transform: translateY(20%);
}
</style>