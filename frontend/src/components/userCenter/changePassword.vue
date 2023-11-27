<template>
  <el-dialog
    title="修改密码"
    :model-value="changePwdVisible"
    :show-close="false"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    width="500px"
  >
    <el-form
      ref="resetPwdRef"
      :model="resetPwdForm"
      :rules="rules"
      style="display: grid; place-items: center;"
    >
      <el-form-item label="旧密码" prop="oldPwd">
        <el-input style="width: 200px" v-model="resetPwdForm.oldPwd" type="password" placeholder="Enter Old Password..." show-password></el-input>
      </el-form-item>
      <el-form-item label="新密码" prop="newPwd">
        <el-input style="width: 200px" v-model="resetPwdForm.newPwd" type="password" placeholder="Enter New Password..." show-password></el-input>
      </el-form-item>
      <el-form-item label="确认密码" prop="checkPwd">
        <el-input style="width: 200px" v-model="resetPwdForm.checkPwd" type="password" placeholder="Enter New Password..." show-password></el-input>
      </el-form-item>
      <br/>
      <el-form-item>
        <el-button @click="closeChangePwd"> 取消 </el-button>
        <el-button
          @click="handleResetPwd"
        >确认修改</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script lang="ts">

import useAuthStore from "@/store/user.ts";
import {reactive, ref, toRefs} from "vue";
import {router} from "@/router/index.ts";
import {ElMessage} from "element-plus";
import cookies from "@/lib/cookies.ts";
import {user_change_password_api} from "@/api/api.ts";

type VoidNoop = (arg0?: Error) => void
interface stateType {
  resetPwdForm: {
    oldPwd:string
    newPwd:string
    checkPwd:string
  }
}

export default {
  name: "changePassword",
  props: {
    changePwdVisible: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    closeChangePwd() {
      this.$parent.closeChangePwd()
      Object.assign(this.$data, this.$options.data())
    }
  },
  setup(_props, {emit}) {
    const userStore = useAuthStore()
    const resetPwdRef = ref()
    const state = reactive<stateType>({
      resetPwdForm: {
        oldPwd:'',
        newPwd:'',
        checkPwd:''
      }
    })
    const handleToLogin = () => {
      cookies.removeAll()
      userStore.logout()
      router.replace('/login')
      ElMessage.success('修改密码成功,请重新登录')
    }
    const handleResetPwd = async() => {
      resetPwdRef.value.validate(async (valid: any) => {
        if (valid) {
          try {
            const {oldPwd, newPwd} = state.resetPwdForm
            console.log(oldPwd, newPwd)
            await user_change_password_api(oldPwd, newPwd).then(response => {
              handleToLogin()
            })
          } catch (error) {
            ElMessage.error(error)
          }
        }
        return false
      })
    }
    const validatePass2 = (rule: any, value: string, callback: VoidNoop) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== state.resetPwdForm.newPwd) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    const validatePass = (rule: any, value: string, callback: VoidNoop) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        if (state.resetPwdForm.checkPwd !== '') {
          resetPwdRef.value.validateField('checkPass')
        }
        callback()
      }
    }
    const rules = {
      oldPwd: [
        { required: true, message: "密码不能为空", trigger: "blur"},
        { min: 5, max: 16, message: '长度在5到16个字符之间', trigger: 'blur' }
      ],
      newPwd: [
        { required: true, message: "密码不能为空", trigger: "blur"},
        { validator: validatePass, trigger: 'blur' },
        { min: 5, max: 16, message: '长度在5到16个字符之间', trigger: 'blur' }
      ],
      checkPwd: [
        { required: true, message: "密码不能为空", trigger: "blur"},
        { validator: validatePass2, trigger: 'blur' },
      ],
    }
    return {
      ...toRefs(state),
      rules,
      resetPwdRef,
      handleResetPwd,
      handleToLogin,
    }
  }
}
</script>

<style scoped>
</style>