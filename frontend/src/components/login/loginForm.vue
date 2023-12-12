<template>
  <el-form
    ref="loginForm"
    :model="loginUser"
    :rules="rules"
    label-width="80px"
    class="loginForm sign-in-form"
  >
    <el-form-item prop="username">
      <el-input
        v-model="loginUser.username"
        placeholder="请输入学工号或教工号...">
        <template #prepend>
          <el-icon :size="20"><User/></el-icon>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item prop="password">
      <el-input
        v-model="loginUser.password"
        placeholder="请输入密码..."
        show-password
        type="password">
        <template #prepend>
          <el-icon :size="20"><Lock/></el-icon>
        </template>
      </el-input>
    </el-form-item>
  </el-form>
  <div id="login-box">
    <button @click="handleLogin('loginForm')">登录</button>
  </div>
</template>

<script lang="ts">
import {getCurrentInstance} from "vue";
import useAuthStore from "@/store/user.ts";
import {user_info_api, user_login_api} from "@/api/api.ts";
import cookies from "@/lib/cookies.ts";
import {router} from "@/router";
import {Lock, User} from "@element-plus/icons-vue";

export default {
  name: 'loginForm',
  components: {Lock, User},
  emits: ['toResetPwd'],
  props: {
    loginUser: {
      type: Object,
      required: true,
    },
    rules: {
      type: Object,
      required: true,
    },
  },
  setup(_props, {emit}) {
    // @ts-ignore
    const { ctx } = getCurrentInstance();
    const userStore = useAuthStore()
    // 触发登录方法
    const handleLogin = (formName: string) => {
      ctx.$refs[formName].validate(async (valid: boolean) => {
        if (valid) {
          await user_login_api(ctx.loginUser.username, ctx.loginUser.password).then(async (res) => {
            if (res.data["code"] === 200) {
              res = res.data
              cookies.set('uuid', res["userId"])
              cookies.set('token', res["access"])
              cookies.set('refreshToken', res["refresh"])
              userStore.loginSuccess()
              let userInfoRes = await user_info_api()
              userStore.setUserinfo(userInfoRes.data)
              router.push('/')// todo：跳转到首页
            }
          })
        } else {
          console.log("error submit!!");
          return false;
        }
      })
    }
    return {
      handleLogin,
    };
  },
};
</script>
<style scoped>
/* form */
/*:deep(.el-form-item__label)  {*/
/*  color: white; !* 设置字体颜色为白色 *!*/
/*}*/
.loginForm {
  margin-top: 20px;
  /*background-color: #fff;*/
  padding: 20px 40px 20px 20px;
}
:deep(input::-webkit-input-placeholder) {
  color: #17a1e5;
  font-size: 15px;
}
:deep(input::-webkit-input-placeholder) {
  color: rgb(255, 255, 255, 0.8);
  font-size: 15px;
  border-bottom:2px solid white;
}
:deep(.el-input) {
  --el-input-bg-color: rgb(0, 0, 0, 0);
  --el-input-border-color: rgb(0, 0, 0, 0);
}
:deep(.el-input__inner) {
  color: white;
}
:deep(.el-input-group__append), :deep(.el-input-group__prepend) {
  background-color: rgb(0, 0, 0, 0);
  color: white;
  }
#login-box button{
  margin-left: 100px;
  width: 120px;
  height: 35px;
  border-radius:18px ;
  outline: none;
  border: none;
  background-image: linear-gradient(120deg, #a6c0fe 0%, #f68084 100%);
  color: #FFFFFF;
}

#login-box button:hover{
  background-image: linear-gradient(120deg, #30cfd0 0%, #330867 100%);
}
#login-box .input-box i{
  color: #FFFFFF;
}
</style>