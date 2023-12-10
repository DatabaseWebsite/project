<template>
  <el-collapse v-model="activeID" accordion>
    <el-collapse-item v-for="item in workData" :key="item.id" :name="item.id">
      <template #title>
        <div class="work-item" style="height: 200px">
          <div class="left-section">
            <IconDocDetail :size="50" style="margin-right: 20px; color: steelblue"/>
            <div class="name-time">
              <p class="name">{{ item.title }}</p>
              <p class="upload-time">总分：{{ item.totalScore }}</p>
              <p class="upload-time">提交截止时间：{{ item.deadline }}</p>
            </div>
          </div>
          <div class="right-section">
            <p v-if="item.score != ''" style="margin-right: 10px"> 得分:
              <i style="font-weight: bold;color: red; font-size: large">{{ item.score }}</i>
            </p>
            <el-tag v-if="item.status === '已提交'" type="success"> {{ item.status }} </el-tag>
            <el-tag v-else-if="item.status === '未提交'" type="warning"> {{ item.status }} </el-tag>
            <el-tag v-else-if="item.status === '已截止'" type="danger"> {{item.status}} </el-tag>
          </div>
        </div>
      </template>
      <div>
        <h2 style="background-color: #cdd1d3">作业描述：</h2>
        <md-preview :text="selectedData.description" :navigation-visible="true"/>
        <el-link
          v-if="selectedData.file != null"
          type="primary"
          @click="download(selectedData.file.url, selectedData.file.name)"
        >作业内容附件：{{selectedData.file.name}}</el-link>
        <h2 style="background-color: #cdd1d3">我的提交：</h2>
        <md-editor v-model="selectedData.submitContext"/>
        <h3>已提交的文件：</h3>
        <el-link
          v-if="selectedData.submitFile != null"
          type="primary"
          @click="download(selectedData.submitFile.url, selectedData.submitFile.name)"
        >{{selectedData.submitFile.name}}</el-link>
        <upload-file v-model="submitFile" :file-size="10"/>
      </div>
      <el-button type="primary" @click="submit"> 提交作业 </el-button>
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
        totalScore: 100,
        deadline: new Date(),
        status: '已提交',
        score: 80,
      }],
      selectedData: {
        id: 1,
        title: '第一次作业',
        totalScore: 100,
        deadline: new Date(),
        status: '已提交',
        score: 80,
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
      submitFile: '',
    }
  },
  methods: {
    async getWorksData() {
      await get_works_info_api().then((res) => {
        this.workData = res.data.result
      })
    },
    download(fileUrl, fileName) {
      saveAs(fileUrl, fileName)
    },
    async submit() {
      await student_submit_work_api(this.selectedData.id, this.selectedData.submitContext, this.submitFile).then(async res => {
        ElMessage.success('提交成功')
        await student_get_work_detail_api(this.activeID).then((res) => {
          this.selectedData = res.data.result
        })
      })
    }
  },
  watch: {
    activeID: {
      updateWorkDetail: async function (newVal, oldVal) {
        await student_get_work_detail_api(newVal).then((res) => {
          this.selectedData = res.data.result
        })
      }
    }
  },
  mounted() {
    // this.getWorksData()
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
</style>