<template>
  <el-form
    ref="loginForm"
    :model="loginUser"
    :rules="rules"
    label-width="80px"
    class="loginForm sign-in-form"
  >
    <h2>登录</h2>
    <el-form-item label="用户名" prop="username">
      <el-input
        v-model="loginUser.username"
        placeholder="请输入学工号或教工号..."
      ></el-input>
    </el-form-item>
    <el-form-item label="密码" prop="password">
      <el-input
        v-model="loginUser.password"
        placeholder="请输入密码..."
        show-password
        type="password"
      ></el-input>
    </el-form-item>

    <el-form-item>
      <el-button
        @click="handleLogin('loginForm')"
        class="submit-btn"
      >登录</el-button>
	  </el-form-item>

    <!-- 找回密码 -->
    <div class="tiparea">
      忘记密码请联系老师或助教
    </div>
  </el-form>
</template>

<script lang="ts">
import {getCurrentInstance} from "vue";
import useAuthStore from "@/store/user.ts";
import {user_info_api, user_login_api} from "@/api/api.ts";
import cookies from "@/lib/cookies.ts";
import {router} from "@/router";

export default {
  name: 'loginForm',
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
            res = res.data
            cookies.set('uuid', res["userId"])
            cookies.set('token', res["access"])
            cookies.set('refreshToken', res["refresh"])
            userStore.loginSuccess()
            let userInfoRes = await user_info_api()
            userStore.setUserinfo(userInfoRes.data)
            router.push('/')// todo：跳转到首页
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
  border-radius: 5px;

}

.submit-btn {
  width: 100%;
}
.tiparea {
  text-align: right;
  font-size: 12px;
  color: #333;
}
</style>