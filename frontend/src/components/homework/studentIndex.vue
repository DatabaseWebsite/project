<template>
  <el-collapse v-model="activeID" @change="handleChange" accordion>
    <el-collapse-item v-for="item in workData" :key="item.id" :name="item.id">
      <template #title>
        <div class="work-item" style="height: 200px">
          <div class="left-section">
            <IconDocDetail :size="50" style="margin-right: 20px; color: steelblue"/>
            <div class="name-time">
              <p class="name">{{ item.title }}</p>
              <p class="upload-time">总分：{{ item.totalScore }}</p>
              <p class="upload-time">提交截止时间：{{ displayTime(item.deadline) }}</p>
            </div>
          </div>
          <div class="right-section">
            <div v-if="item.score != ''" style="margin-right: 10px">
              <i style="font-size: 14px;color: gray;"> 得分: </i>
              <i style="font-weight: bold;color: red; font-size: large">{{ item.score }}</i>
            </div>
          </div>
        </div>
        <span class="status-tag">
          <el-tag v-if="item.upStatus == 1 || item.upStatus == 3" type="success"> <i style="padding: 5px; font-size: 15px">{{ displayStatus(item.upStatus) }}</i> </el-tag>
          <el-tag v-else-if="item.upStatus == 0" type="warning"> <i style="padding: 5px; font-size: 15px">{{ displayStatus(item.upStatus) }}</i> </el-tag>
          <el-tag v-else-if="item.upStatus == 2" type="danger"> <i style="padding: 5px; font-size: 15px">{{ displayStatus(item.upStatus) }}</i> </el-tag>
        </span>
      </template>
      <div>
        <p class="work-title">作业要求：</p>
        <md-preview :text="selectedData.description" :navigation-visible="false"/>
        <div>
          <h3>作业内容附件：</h3>
          <el-link
            v-if="selectedData.file != null"
            type="primary"
            @click="download(selectedData.file.url, selectedData.file.name)"
          >{{selectedData.file.name}}</el-link>
        </div>
        <p class="work-title">我的提交：</p>
        <md-editor v-if="selectedData.status == 1" v-model="selectedData.submitContext"/>
        <md-preview v-else :text="selectedData.submitContext" :navigation-visible="false"/>
        <h3>已提交的文件：</h3>
        <el-link
          v-if="selectedData.submitFile != null"
          type="primary"
          @click="download(selectedData.submitFile.url, selectedData.submitFile.name)"
        >{{selectedData.submitFile.name}}</el-link>
        <upload-file v-if="selectedData.status == 1" v-model:submitFile="submitFile" :file-size="10"/>
      </div>
      <el-button v-if="selectedData.status == 1" type="primary" @click="submit"> 提交作业 </el-button>
    </el-collapse-item>
  </el-collapse>
</template>

<script lang="ts">
import {
  DocDetail as IconDocDetail,
  FileEditing as IconFileEditing,
  FileRemoval as IconFileRemoval,
} from "@icon-park/vue-next";
import {get_works_info_api, student_get_work_detail_api, student_submit_work_api} from "@/api/api.ts";
import MdPreview from "@/components/markdown/mdPreview.vue";
import {saveAs} from "file-saver";
import MdEditor from "@/components/markdown/mdEditor.vue";
import UploadFile from "@/lib/uploadFile.vue";
import {ElMessage} from "element-plus";
export default {
  name: "studentIndex",
  components: {UploadFile, MdEditor, MdPreview, IconDocDetail, IconFileEditing, IconFileRemoval},
  data() {
    return {
      activeID: '',
      workData: [{ // 学生
        id: 1,
        title: '第一次作业',
        status: 1,
        upStatus: null,
        totalScore: 100,
        deadline: new Date(),
        score: 80,
      }],
      selectedData: {
        id: 1,
        title: '第一次作业',
        totalScore: 100,
        deadline: new Date(),
        score: 80,
        status: 0,
        description: 'asfdh',
        file: {
          id: 1,
          name: 'efgrw',
          url: 'ewqfgr',
        },
        submitTime: new Date(),
        submitContext: 'asfdh',
        submitFile: {
          id: 1,
          name: 'efgrw',
          url: 'ewqfgr',
        }
      },
      submitFile: [],
      timer: null,
    }
  },
  methods: {
    displayTime(date:Date) {
      return date.toLocaleString().replaceAll('/', '-')
    },
    updateStatus() {
      const curTime = new Date()
      this.workData.forEach((item) => {
        if (item.deadline < curTime) {
          item.upStatus = item.status === 1 ? 3 : 2
        } else {
          item.upStatus = item.status == 1 ? 1 : 0
        }
      })
    },
    updateSelectedStatus() {
      const curTime = new Date()
      if (this.selectedData.deadline < curTime) {
        this.selectedData.status = 1
      } else {
        this.selectedData.Status = 0
      }
    },
    displayStatus(status) {
      switch (status) {
        case 0:
          return '进行中(未提交)'
        case 1:
          return '进行中(已提交)'
        case 2:
          return '已截止(未提交)'
        case 3:
          return '已截止(已提交)'
      }
    },
    async getWorksData() {
      await get_works_info_api().then((res) => {
        this.workData = res.data.result
        this.workData.forEach((item) => {
          item.deadline = new Date(item.deadline)
        })
      })
    },
    download(fileUrl, fileName) {
      saveAs(fileUrl, fileName)
    },
    async submit() {
      const submitFile = this.submitFile.length == 0 ? '' : this.submitFile[0]
      console.log(this.submitFile)
      await student_submit_work_api(this.selectedData.id, this.selectedData.submitContext, submitFile).then(async res => {
        ElMessage.success('提交成功')
        await student_get_work_detail_api(this.activeID).then((res) => {
          this.selectedData = res.data.result
        })
        await this.getWorksData()
      })
    },
    async handleChange(val) {
      if (val !== '') {
        await student_get_work_detail_api(val).then((res) => {
          this.selectedData = res.data.result
        })
      }
    }
  },
  mounted() {
    this.getWorksData()
    this.timer = setInterval(() => {
      this.updateStatus()
      if (this.activeID !== '')
        this.updateSelectedStatus()
    }, 1000)
  },
  beforeDestroy() {
    clearInterval(this.timer);
  }
}
</script>

<style scoped>
:deep(.el-collapse-item__header) {
  color: $blue;
  height: 200px;
  display: flex;
  justify-content: flex-end;
  padding: 0;
  margin: 0;
}
.work-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
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
  margin: 0;
  text-align: left;
}
.upload-time {
  font-family: "Times New Roman", Times, serif;
  font-size: 14px;
  color: gray;
  padding: 0;
  margin: 0;
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
.status-tag {
  margin-left: auto;
}
.work-title {
  font-family: 'Arial', sans-serif;
  font-size: 1.5em;
  font-weight: bold;
  position: relative;
  display: inline-block;
  padding-bottom: 5px;
}
.work-title:after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  width: calc(100% + 80px);
  height: 3px; /* 初始下边框的高度 */
  background: linear-gradient(to right, #000 50%, rgba(0, 0, 0, 0) 100%); /* 渐变黑线 */
  transition: all 0.3s ease; /* 添加过渡效果 */
}

.work-title:hover:after {
  height: 3px; /* 悬停时下边框变细 */
  background: linear-gradient(to right, #000 50%, rgba(0, 0, 0, 0.3) 100%); /* 悬停时下边框变浅 */
}
</style>