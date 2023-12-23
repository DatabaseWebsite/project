<template>
  <el-container>
    <el-header>
      <el-button type="primary" @click="createWorkVisible = true"> <el-icon><Plus/></el-icon> 发布作业 </el-button>
    </el-header>
    <el-main>
      <div v-for="item in workData">
        <el-card style="margin: 0; padding: 0" shadow="hover" @click.native="goWorkDetail(item.id)">
          <div class="work-item">
            <div class="left-section">
              <IconDocDetail :size="50" style="margin-right: 20px; color: steelblue"/>
              <div class="name-time">
                <p class="name">{{ item.title }}</p>
                <p class="upload-time">总分：{{ item.totalScore }}</p>
                <p class="upload-time">提交截止时间：{{ displayTime(item.deadline) }}</p>
              </div>
            </div>
            <div class="right-section">
              <icon-file-editing :size="30" style="margin: 20px" @click.stop="editWork(item)" />
              <el-popconfirm
                confirm-button-text="确定"
                cancel-button-text="取消"
                title="确定删除该作业吗？"
                @confirm.stop="deleteWork(item.id)"
                style="margin: 20px">
                <template #reference>
                  <el-button type="text" @click.stop><icon-file-removal :size="30" style="color:darkred"/></el-button>
                </template>
              </el-popconfirm>
            </div>
          </div>
        </el-card>
      </div>
    </el-main>
  </el-container>
  <create-work :createWorkVisible="createWorkVisible" @closeDialog="closeCreateWork"/>
<!--  修改作业-->
  <el-dialog
    title="修改作业"
    v-model="modifyWorkVisible"
    width="90%"
    style="padding: 30px"
  >
    <el-form ref="modifyWorkFormRef" :model="selectedWork" :rules="modifyWorkRules" label-width="80">
      <el-form-item label="作业标题" prop="title">
        <el-input v-model="selectedWork.title" placeholder="请输入作业标题"></el-input>
      </el-form-item>
      <el-form-item label="作业描述">
        <md-editor v-model="selectedWork.description"/>
      </el-form-item>
      <el-form-item label="作业文件">
        <upload-file v-if="selectedWork.file !== ''" v-model:submit-file="submitFile.file"/>
        <div v-else>
          <el-link type="primary" @click="download(selectedWork.file.url, selectedWork.file.name)"> {{ selectedWork.file.name }} </el-link>
          <el-button type="text" @click="removeSelectedFile" style="margin-left: 20px; color: red">删除</el-button>
        </div>
      </el-form-item>
      <el-form-item label="作业总分" prop="totalScore" style="width: 300px;">
        <el-input v-model="selectedWork.totalScore" placeholder="请输入作业总分"></el-input>
      </el-form-item>
      <el-form-item label="截止时间" prop="deadline">
        <el-date-picker v-model="selectedWork.deadline" type="datetime" placeholder="请选择截止时间"/>
      </el-form-item>
      <el-form-item>
        <el-button @click="modifyWorkVisible=false"> 取消 </el-button>
        <el-button type="primary" @click="submitForm(modifyWorkFormRef)"> 提交 </el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script lang="ts">
import {Plus, UploadFilled} from "@element-plus/icons-vue";
import CreateWork from "@/components/homework/createWork.vue";
import {
  DocDetail as IconDocDetail,
  FileEditing as IconFileEditing,
  FileRemoval as IconFileRemoval,
  Delete as IconDelete,
} from "@icon-park/vue-next";
import {delete_work_api, get_works_info_api, modify_work_api} from "@/api/api.ts";
import {ElMessage, FormInstance} from "element-plus";
import {reactive, ref} from "vue";
import MdEditor from "@/components/markdown/mdEditor.vue";
import UploadFile from "@/lib/uploadFile.vue";
import {saveAs} from "file-saver";
import {useRouter} from "vue-router";

interface ModifyWorkRuleForm {
  id: number
  title: string,
  file: any,
  description: string,
  totalScore: number,
  deadline: any,
}
interface SubmitFile {
  file: any
}

export default {
  name: "workManage",
  components: {UploadFile, MdEditor, UploadFilled, CreateWork, Plus, IconDocDetail, IconFileEditing, IconFileRemoval, IconDelete},
  data() {
    return {
      createWorkVisible: false,
      workData: [], // admin，老师，助教
      fileType: ['.doc', '.docx', '.pdf', '.ppt', '.txt', '.xls','.xlsx', '.zip', '.rar'],
      accept: '',
    }
  },
  methods: {
    displayTime(date:Date) {
      return date.toLocaleString().replaceAll('/', '-')
    },
    closeCreateWork(e) {
      this.createWorkVisible = e
      this.getWorkList()
    },
    async deleteWork(id) {
      await delete_work_api(id).then(res => {
        ElMessage.success('删除成功')
        this.getWorkList()
      })
    },
    async getWorkList() {
      await get_works_info_api().then(res => {
        this.workData = res.data.result
        this.workData.forEach(el => {
          el.deadline = new Date(el.deadline)
        })
      })
    },
    download(fileUrl, fileName) {
      saveAs(fileUrl, fileName)
    }
  },
  setup(props, context) {
    const modifyWorkFormRef = ref<FormInstance>()
    const modifyWorkVisible = ref(false)
    const selectedWork = reactive<ModifyWorkRuleForm>({
      id: 1,
      title: '',
      file: '',
      description: '',
      totalScore: 100,
      deadline: '',
    })
    const router = useRouter()
    const submitFile = reactive<SubmitFile>({ file: [] })
    const editWork = (work) => {
      modifyWorkVisible.value = true
      selectedWork.id = work.id
      selectedWork.title = work.title
      selectedWork.description = work.description
      selectedWork.file = work.file
      selectedWork.deadline = work.deadline
      selectedWork.totalScore = work.totalScore
    }
    const modifyWorkRules = reactive({
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
    const removeSelectedFile = () => {
      selectedWork.file = ''
    }
    const submitForm = async(formEl: FormInstance | undefined) => {
      if (!formEl) return
      await formEl.validate(async (valid) => {
        if (valid) {
          const data:FormData = new FormData()
          data.append('id', selectedWork.id.toString())
          let fileOperation = 2 // 没有修改文件
          if (submitFile.file.length != 0) { // 覆盖新文件
            fileOperation = 0
            data.append('file', submitFile.file[0].raw)
          } else if (selectedWork.file === '') // 删除旧文件
              fileOperation = 1
          console.log(selectedWork.deadline.toISOString())
          data.append('file_operation', fileOperation.toString())
          data.append('title', selectedWork.title)
          data.append('description', selectedWork.description)
          data.append('totalScore', selectedWork.totalScore.toString())
          data.append('deadline', selectedWork.deadline.toISOString())
          await modify_work_api(data).then(res => {
            ElMessage.success('修改成功！')
          })
        } else {
          ElMessage.warning('错误提交！！')
        }
      })
    }
    const goWorkDetail = (id) => {
      router.push({path: `/homework/workdetail`, query:{id: id} })
    }
    return {
      submitFile,
      modifyWorkFormRef,
      selectedWork,
      modifyWorkRules,
      modifyWorkVisible,
      submitForm,
      editWork,
      removeSelectedFile,
      goWorkDetail
    }
  },
  created() {
    this.fileType.forEach(el => {
      this.accept += el + ','
    })
    this.fileType.slice(0, this.fileType.length - 2)
  },
  mounted() {
    this.getWorkList()
  }
}
</script>

<style scoped>
.work-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
}

.left-section {
  display: flex;
  align-items: center;
}

.name {
  font-family: "Microsoft YaHei",cursive;
  font-size: 18px;
  font-weight: bold;
  padding: 0;
  margin: 10px 0 0 0;
  text-align: left;
}
.upload-time {
  font-family: "Times New Roman", Times, serif;
  font-size: 14px;
  color: gray;
  padding: 0;
  margin: 0 0 10px 0;
  text-align: left;
}
.name-time {
  display: flex;
  flex-direction: column;
}

.right-section {
  display: flex;
  text-align: right;
  align-items: center;
}
</style>