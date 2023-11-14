<template>
  <div
    class="w3l-signinform"
    :style="{background:'url(' + require('@/assets/image/bg.jpg') +') no-repeat center', backgroundSize: '100% 100%' }"
  >
    <!-- container -->
    <div class="wrapper">
      <!-- main content -->
      <div class="w3l-form-info">
        <!-- logo -->
        <img class="page-login--logo" :src="require('@/assets/image/dbcourseplat_blue.png')" width="300"/>
        <div class="w3_info">
          <el-card shadow="always" class="card">
            <h2 slot="header" style="color: black;">
                数据库课程平台
            </h2>
            <el-form
              ref="loginForm"
              label-position="top"
              :rules="rules"
              :model="formLogin"
              size="default"
            >
              <el-form-item prop="username">
                <el-input
                  type="text"
                  v-model="formLogin.username"
                  prefix-icon="el-icon-user-solid"
                  placeholder="用户名"
                >
                </el-input>
              </el-form-item>
              <el-form-item prop="password">
                <el-input
                  type="password"
                  v-model="formLogin.password"
                  prefix-icon="el-icon-s-promotion"
                  show-password
                  placeholder="密码"
                  @keyup.enter.native='submit'
                >
                </el-input>
              </el-form-item>
              <el-form-item
                prop="captcha"
                :rules="{required: true,message: '请输入验证码',trigger: 'blur'}"
              >
                <el-input
                  type="text"
                  v-model="formLogin.captcha"
                  placeholder="验证码"
                  @keyup.enter.native="submit"
                >
                  <template slot="append">
                    <img
                      alt="请检查后端是否正常~~"
                      class="login-code"
                      style="cursor: pointer;width:145px;height: 33px;"
                      height="33px"
                      width="145px"
                      slot="suffix"
                      :src="image_base"
                      @click="getCaptcha"
                    />
                  </template>
                </el-input>
              </el-form-item>
            </el-form>
            <button class="btn btn-primary btn-block" style="padding: 10px 10px;" @click="submit">登录</button>
            <component/>
          </el-card>
        </div>
      </div>
      <!-- //main content -->
    </div>
  </div>
</template>
<script>
import base from './base.vue'
export default {
  extends: base,
  name: 'page',
  mounted () {
  },
  methods: {}
}
</script>

<style lang="scss" scoped>
  @import './css/style.css';

  .copyrights {
    text-indent: -9999px;
    height: 0;
    line-height: 0;
    font-size: 0;
    overflow: hidden;
  }

  // 快速选择用户面板
  .page-login--quick {
    margin-top: 20px;
  }

  .page-login--quick-user {
    @extend %flex-center-col;
    padding: 10px 0px;
    border-radius: 4px;

    &:hover {
      background-color: $color-bg;

      i {
        color: $color-text-normal;
      }

      span {
        color: $color-text-normal;
      }
    }

    i {
      font-size: 36px;
      color: $color-text-sub;
    }

    span {
      font-size: 12px;
      margin-top: 10px;
      color: $color-text-sub;
    }
  }
</style>
