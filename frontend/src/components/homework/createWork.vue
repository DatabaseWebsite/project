<template>
  <el-dialog
    title="发布作业"
    :model-value="createWorkVisible"
    :show-close="false"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    width="90%"
    style="padding: 30px"
  >
    <el-form ref="workFormRef" :model="workInfo" :rules="workRules" label-width="80">
      <el-form-item label="作业标题" prop="title">
        <el-input v-model="workInfo.title" placeholder="请输入作业标题"></el-input>
      </el-form-item>
      <el-form-item label="作业描述">
        <md-editor v-model="workInfo.description"/>
      </el-form-item>
      <el-form-item label="作业文件">
        <upload-file v-model:submitFile="workInfo.file"/>
      </el-form-item>
      <el-form-item label="作业总分" prop="totalScore">
        <el-input v-model="workInfo.totalScore" placeholder="请输入作业总分"></el-input>
      </el-form-item>
      <el-form-item label="截止时间" prop="deadline">
        <el-date-picker v-model="workInfo.deadline" type="datetime" placeholder="请选择截止时间"/>
      </el-form-item>
      <el-form-item>
        <el-button @click="cancel"> 取消 </el-button>
        <el-button type="primary" @click="submitForm(workFormRef)"> 提交 </el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script lang="ts">
import {reactive, ref} from "vue";
import {ElMessage, FormInstance} from "element-plus";
import {create_work_api} from "@/api/api.ts";
import {UploadFilled} from "@element-plus/icons-vue";
import MdEditor from "@/components/markdown/mdEditor.vue";
import UploadFile from "@/lib/uploadFile.vue";


interface WorkRuleForm {
  title: string,
  file: any,
  description: string,
  totalScore: number,
  deadline: any,
}
export default {
  name: "createWork",
  components: {UploadFile, MdEditor, UploadFilled},
  props: {
    createWorkVisible: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      fileType: ['.doc', '.docx', '.pdf', '.ppt', '.txt', '.xls','.xlsx', '.zip', '.rar'],
      accept: '',
    }
  },
  setup(_props, context) {
    const workFormRef = ref<FormInstance>()
    const workInfo = reactive<WorkRuleForm>({
      title: '',
      file: '',
      description: '',
      totalScore: 100,
      deadline: '',
    })
    const workRules = reactive({
      title: [
        {required: true, message: '请输入作业标题', trigger: 'blur'},
      ],
      totalScore: [
        {required: true, message: '请输入作业总分', trigger: 'blur'},
      ],
      deadline: [
        {required: true, message: '请选择截止日期', trigger: 'blur'}
      ]
    })
    const handleExceed = () => {
      ElMessage.warning('待上传文件数量超出限制，请分批次上传！')
    }
    const handleChange = (file, uploadFiles) => {
       workInfo.file = uploadFiles
    }
    const handleRemove = (file, uploadFiles) => {
      workInfo.file = uploadFiles
    }
    const handleBeforeUpload = (file) =>  {
      if (this.fileType) {
        let fileExtension = "";
        if (file.name.lastIndexOf(".") > -1) {
          fileExtension = file.name.slice(file.name.lastIndexOf("."));
        }
        const isTypeOk = this.fileType.some((type) => {
          if (file.type.indexOf(type) > -1) return true;
          return fileExtension && fileExtension.indexOf(type) > -1;

        });
        if (!isTypeOk) {
          ElMessage.error(`文件格式不正确, 请上传${this.fileType.join("/")}格式文件!`);
          return false;
        }
      }
      // 校检文件大小
      if (this.fileSize) {
        const isLt = file.size / 1024 / 1024 < 20;
        if (!isLt) {
          ElMessage.error(`上传文件大小不能超过 20 MB!`);
          return false;
        }
      }
      return true;
    }
    const submitForm = async(formEl: FormInstance | undefined) => {
      if (!formEl) return
      await formEl.validate(async (valid) => {
        if (valid) {
          console.log(workInfo)
          const data:FormData = new FormData()
          data.append('file', workInfo.file.raw)
          data.append('title', workInfo.title)
          data.append('description', workInfo.description)
          data.append('totalScore', workInfo.totalScore.toString())
          data.append('deadline', workInfo.deadline.toISOString())
          await create_work_api(data).then(res => {
            ElMessage.success('创建成功！')
            cancel()
          })
        } else {
          ElMessage.warning('错误提交！！')
        }
      })
    }
    const cancel = () => {
      workInfo.title = ''
      workInfo.description = ''
      workInfo.totalScore = 100
      workInfo.deadline = ''
      workInfo.file = ''
      context.emit('closeDialog', false)
    }
    return {
      workFormRef,
      workInfo,
      workRules,
      submitForm,
      handleExceed,
      handleChange,
      handleRemove,
      handleBeforeUpload,
      cancel
    }
  },
  created() {
    this.fileType.forEach(el => {
      this.accept += el + ','
    })
    this.fileType.slice(0, this.fileType.length - 2)
  }
}
</script>

<style scoped>

</style>