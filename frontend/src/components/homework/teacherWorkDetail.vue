<template>
  <div>
    <p class="work-title"> {{workData.title}} </p>
    <el-descriptions border :column="2">
      <el-descriptions-item label="作业状态">
        <el-tag v-if="workData.status === '进行中'" type="success"> 进行中 </el-tag>
        <el-tag v-else type="danger"> 已截止 </el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="截止时间">
        {{workData.deadline}}
      </el-descriptions-item>
      <el-descriptions-item label="作业总分">
        {{workData.totalScore}}
      </el-descriptions-item>
      <el-descriptions-item label="提交人数">
        {{workData.submitPeople}} / {{workData.totalPeople}}
      </el-descriptions-item>
    </el-descriptions>
    <div class="box-shadow">
      <div v-if="workData.file !== undefined">
        <i class="title2">作业附件：</i>
        <el-link :underline="true" type="primary" @click="download(workData.file.url, workData.file.name)"> {{ workData.file.name }} </el-link>
      </div>
      <p class="title2">作业描述：</p>
      <md-preview :text="workData.description" :navigation-visible="true"/>
    </div>
    <el-table :data="submitData" border>
      <el-table-column prop="id" label="序号" width="70"/>
      <el-table-column prop="studentID" label="学号" min-width="140" sortable/>
      <el-table-column prop="studentName" label="姓名" min-width="160"/>
      <el-table-column prop="submitTime" label="提交时间" min-width="180" sortable/>
      <el-table-column prop="score" label="批改分数" min-width="160" sortable/>
      <el-table-column prop="markingPerson" label="批改人" min-width="180"/>
      <el-table-column fixed="right" label="操作" width="100">
        <template #default="scope">
          <el-button type="primary" size="small" @click="handleCorrect(scope.$index, scope.row)">
            批改
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <div>
      <el-pagination layout="prev, pager, next" :page-count="totalPage" :current-page="curPage" page-size=10 @current-change="changePage" style="margin: 10px;"/>
    </div>
  </div>
  <el-dialog
    v-model="correctVisible"
    title="批改作业"
    width="70%"
  >
    <div>
      <div v-if="selectedInfo.file !== undefined">
<!--        <pdf-preview :pdf-url="selectedInfo.file.url"/>-->
      </div>
      <div v-if="selectedInfo.context !== ''">
        <md-preview :text="selectedInfo.context" :navigation-visible="false"/>
      </div>
      <el-form>
        <el-form-item label="分数">
          <el-input-number v-model="selectedInfo.score" :min="0" :max="workData.totalScore" :step="1"/>
        </el-form-item>
      </el-form>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="correctVisible = false; submitCorrect"> 提交批改 </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script lang="ts">
import {
  get_one_work_api,
  get_work_submissions_api, submit_work_score_api,
} from "@/api/api.ts";
import MdPreview from "@/components/markdown/mdPreview.vue";
import {saveAs} from "file-saver";
import {ElMessage} from "element-plus";

export default {
  name: "teacherWorkDetail",
  components: {MdPreview},
  data() {
    return {
      id: 1,
      workData: {
        id: 1,
        title: '第一次作业',
        totalScore: 100,
        deadline: new Date(),
        status: '已截止',
        file: {
          id: 1,
          name: 'dfa',
          url: 'wewg',
        },
        description: 'abadfjfqgerqg',
        submitPeople: 100,
        totalPeople: 110,
      },
      submitData: [
        {
          id: 1, // 提交id
          studentID: 21373032,
          studentName: '张三',
          submitTime: '2023-10-24 12:00:00',
          score: 100, // 为空表示未批改
          markingPerson: '李四',
        }
      ],
      curPage: 1,
      pageSize: 10,
      totalPage: 1,
      selectedInfo: {
        id: 2,
        file: {
          id: 2,
          name: '1fe',
          url: 'efwg',
        },
        context: 'sfgd',
        score: null,
      },
      correctVisible: false,
    }
  },
  methods: {
    download(url: string, name: string) {
      saveAs(url, name)
    },
    async querySubmit() {
        await get_work_submissions_api(this.id, this.curPage).then(res => {
          this.submitData = res.data['result']
          this.totalPage = res.data['total_page']
        })
    },
    async handleCorrect(index: number, row: any) {
      // await get_work_submissions_by_id_api(row['id']).then(res => {
      //   this.selectedInfo = res.data['result']
      //   this.correctVisible = true
      // })
      this.correctVisible = true
    },
    changePage(page: number) {
      this.curPage = page
      this.querySubmit()
    },
    async submitCorrect() {
      await submit_work_score_api(this.selectedInfo.id, this.selectedInfo.score).then(res => {
        ElMessage.success('批改成功')
        this.correctVisible = false
        this.querySubmit()
      })
    }
  },
  async mounted() {
    this.id = this.$router.query.id
    await get_one_work_api(this.id).then(res => {
      this.workData = res.data.result
    })
    await this.querySubmit()
  }
}
</script>

<style lang="scss" scoped>
.work-title {
  font-family: 'Arial', sans-serif;
  font-size: 2em;
  font-weight: bold;
  color: transparent;
  text-align: center;
  position: relative;
  display: inline-block;
  background: linear-gradient(to bottom, #003366 50%, #66ccff 50%);
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
  animation: scaleUp 2s infinite alternate;
}
.title2 {
  font-family: 'Arial', sans-serif;
  font-size: 20px;
  font-weight: bold;
}
.box-shadow {
  margin-top: 10px;
  margin-bottom: 10px;
  box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px;
  border-radius: 10px;
  padding: 10px;
}
</style>