<template>
  <div>
    <p class="work-title"> {{workData.title}} </p>
    <el-descriptions border :column="2">
      <el-descriptions-item label="作业状态">
        <el-tag v-if="workData.status === '进行中'" type="success"> 进行中 </el-tag>
        <el-tag v-else type="danger"> 已截止 </el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="截止时间">
        {{displayTime(workData.deadline)}}
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
    <el-table
      :data="paginateData"
      @sort-change="sortChange"
      border
    >
      <el-table-column prop="id" label="序号" width="70"/>
      <el-table-column prop="studentID" label="学号" min-width="140" sortable="custom"/>
      <el-table-column prop="studentName" label="姓名" min-width="160"/>
      <el-table-column prop="submitTime" label="提交时间" min-width="180" sortable="custom"/>
      <el-table-column prop="score" label="得分" min-width="160" sortable="custom"/>
      <el-table-column prop="markingPerson" label="批改人" min-width="180"/>
      <el-table-column fixed="right" label="操作" width="100">
        <template #default="scope">
          <el-button type="primary" size="small" @click="handleCorrect(scope.$index, scope.row)">
            批改
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination layout="prev, pager, next" :current-page="curPage" :page-size='10' :total="total" @current-change="changePage" style="margin: 10px;"/>
  </div>
  <el-dialog
    v-model="correctVisible"
    title="批改作业"
    width="70%"
  >
    <div>
      <div v-if="selectedInfo.file != undefined">
        <md-preview v-if="selectedInfo.context !== ''" :text="selectedInfo.context"/>
        <pdf-preview v-if="selectedInfo.file.url.endsWith('pdf')" :pdf="selectedInfo.file.url"/>
        <docx-preview
          v-else-if="selectedInfo.file.url.endsWith('docx') || selectedInfo.file.url.endsWith('doc')"
          :docx="selectedInfo.file.url"/>
        <excel-preview
          v-else-if="selectedInfo.file.url.endsWith('xlsx') || selectedInfo.file.url.endsWith('xls')"
          :excel="selectedInfo.file.url"/>
        <div v-else>
          <el-link :underline="true" type="primary" @click="download(selectedInfo.file.url, selectedInfo.file.name)"> {{ selectedInfo.file.name }} </el-link>
          暂不支持该文件类型预览
        </div>
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
  get_one_work_api, get_work_submission_by_id_api,
  get_work_submissions_api, submit_work_score_api,
} from "@/api/api.ts";
import MdPreview from "@/components/markdown/mdPreview.vue";
import {saveAs} from "file-saver";
import {ElMessage} from "element-plus";
import {useRoute} from "vue-router";
import PdfPreview from "@/lib/pdfPreview.vue";
import DocxPreview from "@/lib/docxPreview.vue";
import ExcelPreview from "@/lib/excelPreview.vue";
import {onMounted, reactive, ref} from "vue";

export default {
  name: "teacherWorkDetail",
  components: {ExcelPreview, DocxPreview, PdfPreview, MdPreview},
  setup() {
    const id = ref(1)
    const workData = ref({
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
    })
    const submitData = ref([
      {
        id: 1, // 提交id
        studentID: 21373032,
        studentName: '张三',
        submitTime: '2023-10-24 12:00:00',
        score: 100, // 为空表示未批改
        markingPerson: '李四',
      }
    ])
    const paginateData = ref([])
    const total = ref(0)
    const curPage = ref(1)
    const selectedInfo = ref({
      id: 2,
      file: {
        id: 2,
        name: 'test6',
        url: 'http://static.shanhuxueyuan.com/test6.docx',
      },
      context: 'sfgd',
      score: null,
    })
    const correctVisible = ref(false)
    const querySubmit = async () => {
      await get_work_submissions_api(id.value).then(res => {
        submitData.value = res.data['result']
        total.value = submitData.value.length
        initTable()
      })
    }
    const initTable = () => {
      const res = submitData.value
      let start = curPage.value > 1 ? (curPage.value - 1) * 10 : 0
      let end = curPage.value * 10
      paginateData.value = res.slice(start, end)
    }
    const handleCorrect = async (index: number, row: any) => {
      await get_work_submission_by_id_api(row['id']).then(res => {
        selectedInfo.value = res.data['result']
        correctVisible.value = true
      })
    }
    const changePage = (page: number) => {
      curPage.value = page
      initTable()
    }
    const sortChange = ({prop, order}) => {
      function compare(pr: any) {
        // 默认传入两个参数，即为数组中要比较的两项
        return function (a: any, b: any) {
          const value1 = a[pr];
          const value2 = b[pr];
          return value1 - value2;
        }
      }
      submitData.value.sort(compare(prop))
      if (order === 'descending') {
        submitData.value.reverse()
      }
      initTable()
    }
    const submitCorrect = async () => {
      await submit_work_score_api(selectedInfo.value.id, selectedInfo.value.score).then(res => {
        ElMessage.success('批改成功')
        querySubmit()
      })
    }
    onMounted(async () => {
      id.value = Number(useRoute().query.id)
      await get_one_work_api(id.value).then(res => {
        workData.value = res.data.result
      })
      await querySubmit()
    })
    return {
      id,
      workData,
      submitData,
      paginateData,
      total,
      curPage,
      selectedInfo,
      correctVisible,
      querySubmit,
      initTable,
      handleCorrect,
      changePage,
      submitCorrect,
      sortChange,
    }
  },

  methods: {
    displayTime(date:Date) {
      return date.toLocaleString().replaceAll('/', '-')
    },
    download(url: string, name: string) {
      saveAs(url, name)
    }
  }
}
</script>

<style lang="scss" scoped>
.work-title {
  font-family: 'Arial', sans-serif;
  font-size: 2em;
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
  width: calc(100% + 100px);
  height: 3px; /* 初始下边框的高度 */
  background: linear-gradient(to right, #000 50%, rgba(0, 0, 0, 0) 100%); /* 渐变黑线 */
  transition: all 0.3s ease; /* 添加过渡效果 */
}

.work-title:hover:after {
  height: 3px; /* 悬停时下边框变细 */
  background: linear-gradient(to right, #000 50%, rgba(0, 0, 0, 0.3) 100%); /* 悬停时下边框变浅 */
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