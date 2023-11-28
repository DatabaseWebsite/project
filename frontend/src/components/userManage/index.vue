<template>
  <el-container>
    <el-header style="overflow-y:scroll;overflow-x:hidden;height:140px">
      <el-form :inline="true" :model="searchInfo" label-width="40px" size="small">
        <el-form-item label="学号" style="width: 180px;">
          <el-input v-model="searchInfo.personId" placeholder="请输入学号"></el-input>
        </el-form-item>
        <el-form-item label="姓名" style="width: 180px;">
          <el-input v-model="searchInfo.username" placeholder="请输入姓名"></el-input>
        </el-form-item>
        <el-form-item label="年级" style="width: 180px;">
          <el-input v-model="searchInfo.grade" placeholder="请输入年级,如 2021"></el-input>
        </el-form-item>
        <el-form-item label="课程" style="width: 220px;">
          <el-select v-model="searchInfo.course" placeholder="请选择课程" clearable>
            <el-option
              v-for="item in courseInfo"
              :label="item['name']"
              :value="item['course_id'].toString()"
            ></el-option>
          </el-select>
        </el-form-item >
        <el-form-item label="身份" style="width: 120px;">
          <el-select v-model="searchInfo.identity" placeholder="请选择身份" clearable>
            <el-option
              v-for="item in ['学生', '助教', '老师']"
              :label="item"
              :value="item === '学生' ? 'STUDENT' : item === '助教' ? 'ASSISTANT' : 'TEACHER'"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm"> 查询 </el-button>
          <el-button type="info" @click="resetForm"> 重置 </el-button>
        </el-form-item>
      </el-form>
      <el-button size="small" type="primary" @click="createVisible=true"> <icon-add-user/>新增 </el-button>
      <el-button size="small" type="danger" @click="batchDelete"> <el-icon><Delete/> </el-icon>批量删除 </el-button>
      <el-button size="small" type="warning" @click="onExport"> <el-icon><Download/></el-icon>导出 </el-button>
      <el-button size="small" type="success" @click="batchCreationVisible=true"> <el-icon><UploadFilled/></el-icon>批量创建 </el-button>
    </el-header>
    <el-main>
      <el-table ref="multipleTableRef" :data="tableData" border @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="50"></el-table-column>
        <el-table-column prop="id" label="ID" width="70"></el-table-column>
        <el-table-column prop="person_id" label="学号" width="140"></el-table-column>
        <el-table-column prop="username" label="姓名" min-width="100"></el-table-column>
        <el-table-column prop="grade" label="年级" width="80"></el-table-column>
        <el-table-column prop="courses" label="参与课程及身份" min-width="300"></el-table-column>
        <el-table-column fixed="right" label="操作" width="200">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleEdit(scope.$index, scope.row)">
              <icon-edit-name size="15"/>
            </el-button>
            <el-button type="danger" size="small" @click="deleteOne(scope.$index, scope.row)">
              <icon-people-delete-one size="15"/>
            </el-button>
            <el-button link type="primary" size="small" @click="resetPassword">重置密码</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div>
       <el-pagination layout="prev, pager, next" :page-count="totPage" :current-page="curPage" page-size=10 @current-change="changePage" style="margin: 10px;"/>
      </div>
    </el-main>
  </el-container>
  <el-dialog title="新增用户" v-model="createVisible">
    <el-form ref="registerFormRef" :model="registerUser" :rules="registerRules" label-width="80">
      <el-form-item label="学号" prop="personId">
        <el-input v-model="registerUser.personId" placeholder="请输入学号"></el-input>
      </el-form-item>
      <el-form-item label="姓名" prop="username">
        <el-input v-model="registerUser.username" placeholder="请输入姓名"></el-input>
      </el-form-item>
      <el-form-item label="年级" prop="grade">
        <el-input v-model="registerUser.grade" placeholder="请输入年级,如 2021"></el-input>
      </el-form-item>
      <el-form-item label="加入课程" prop="course">
        <el-select v-model="registerUser.course" placeholder="请选择课程" clearable>
          <el-option
            v-for="item in courseInfo"
            :label="item['name']"
            :value="item['course_id'].toString()"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="身份" prop="identity">
        <el-select v-model="registerUser.identity" placeholder="请选择身份">
          <el-option
            v-for="item in ['学生', '助教', '老师']"
            :label="item"
            :value="item === '学生' ? 'STUDENT' : item === '助教' ? 'ASSISTANT' : 'TEACHER'"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitCreate(registerFormRef)"> 提交 </el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
  <el-dialog title="批量创建用户" v-model="batchCreationVisible">
    <uploadExcel @file-uploaded="handleFileUploaded"/>
    <el-form v-model="batchCreationInfo" label-width="80">
      <el-form-item label="加入课程" prop="course">
        <el-select v-model="batchCreationInfo.course" placeholder="请选择课程" clearable>
          <el-option
            v-for="item in courseInfo"
            :label="item['name']"
            :value="item['course_id'].toString()"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="身份" prop="identity">
        <el-select v-model="batchCreationInfo.identity" placeholder="请选择身份">
          <el-option
            v-for="item in ['学生', '助教', '老师']"
            :label="item"
            :value="item === '学生' ? 'STUDENT' : item === '助教' ? 'ASSISTANT' : 'TEACHER'"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitBatchCreation"> 提交 </el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
  <el-dialog title="编辑用户基本信息" v-model="editVisible">
    <el-form ref="editFormRef" :model="editUserInfo" :rules="editRules" label-width="80">
      <el-form-item label="学号" prop="personId">
        <el-input v-model="editUserInfo.personId" placeholder="请输入学号"></el-input>
      </el-form-item>
      <el-form-item label="姓名" prop="username">
        <el-input v-model="editUserInfo.username" placeholder="请输入姓名"></el-input>
      </el-form-item>
      <el-form-item label="年级" prop="grade">
        <el-input v-model="editUserInfo.grade" placeholder="请输入年级,如2021"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitEdit(editFormRef)"> 提交 </el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script lang="ts">
import {
  del_user_api, del_users_api, excel_create_users_api,
  get_all_courses_api, get_all_user_list_api,
  get_user_list_api, reset_user_password_api, search_all_user_api,
  search_user_api,
  signup_api,
  update_userinfo_api
} from "@/api/api.ts";
import {ElMessage, ElMessageBox, ElTable, FormInstance} from "element-plus";
import {
  EditName as IconEditName,
  AddUser as IconAddUser,
  PeopleDeleteOne as IconPeopleDeleteOne,
} from "@icon-park/vue-next";
import {
  Delete,
  Download,
  UploadFilled
} from "@element-plus/icons-vue";
import {ref} from "vue";
import {registerRules, registerUser} from "@/components/userManage/registerForm.ts";
import {editRules, editUserInfo} from "@/components/userManage/EditUserInfo.ts";
import uploadExcel from "@/components/userManage/uploadExcel.vue";
import {exportExcel} from "@/components/userManage/exportExcel.ts";

export default {
  name: "userManage",
  computed: {
    editRules() {
      return editRules
    },
    editUserInfo() {
      return editUserInfo
    },
    registerRules() {
      return registerRules
    },
    registerUser() {
      return registerUser
    }
  },
  components: {
    IconEditName, IconAddUser, IconPeopleDeleteOne,
    Delete, Download, UploadFilled, uploadExcel
  },
  data() {
    return {
      searchInfo: {
        personId: '',
        username: '',
        grade: '',
        course: '',
        identity: '',
      },
      courseInfo: [],
      isSearching: false,
      tableData: [
        {
          id: 1,
          person_id: '2019210000',
          username: '张三',
          grade: '2019',
          courses: '计算机网络（学生）,编译原理（学生）',
        }, {
           id: 2,
            person_id: '2019210001',
            username: '李四',
            grade: '2019',
            courses: '计算机网络（助教）',
          }, {
            id: 3,
            person_id: '2019210002',
            username: '王五',
            grade: '2019',
            courses: '计算机网络（老师）',
        }, {
          id: 4,
          person_id: '2019210003',
          username: '赵六',
          grade: '2019',
          courses: '计算机网络（学生）',
        }, {
          id: 5,
          person_id: '2019210004',
          username: '孙七',
          grade: '2019',
          courses: '计算机网络（学生）',
        }
      ],
      curPage: 1,
      totPage: 1,
      createVisible: false,
      batchCreationVisible: false,
      editVisible: false,
      batchCreationInfo: {
        file: [],
        course: '',
        identity: ''
      }
    }
  },
  methods: {
    getRequest() {
      const result = {}
      const query = window.location.href.split('?')[1]
      if (query) {
        const queryArr = query.split('&')
        queryArr.forEach(item => {
          const value = decodeURIComponent(item.split('=')[1])
          console.log(value)
          const key = item.split('=')[0]
          const results = result as any
          results[key] = value
        })
      }
      if (result['personId'] != null) {
        this.searchInfo.personId = result['personId']
        this.searchInfo.username = result['username']
        this.searchInfo.grade = result['grade']
        this.searchInfo.course = result['course']
        this.searchInfo.identity = result['identity']
        this.isSearching = true
        this.curPage = result['page']
      } else {
        this.isSearching = false
        this.curPage = result['page']
      }
    },
    async queryUsers() {
      if (this.isSearching) {
        window.location.href = `/#/userManage?personId=${this.searchInfo.personId}&username=${this.searchInfo.username}&grade=${this.searchInfo.grade}&course=${this.searchInfo.course}&identity=${this.searchInfo.identity}&page=${this.curPage}`
        await search_user_api(this.searchInfo.personId, this.searchInfo.username, this.searchInfo.grade, this.searchInfo.course, this.searchInfo.identity, this.curPage).then(res => {
          this.tableData = res.data['result']
          this.totPage = res.data['total_page']
        })
      } else {
        const page = this.curPage || 1
        window.location.href = `/#/userManage?page=${page}`
        await get_user_list_api(this.curPage).then(res => {
          this.tableData = res.data['result']
          this.totPage = res.data['total_page']
        })
      }
    },
    async submitForm() {
      let isValid = true
      if (this.searchInfo.personId=='' && this.searchInfo.username=='' && this.searchInfo.course=='' && this.searchInfo.identity=='' && this.searchInfo.grade=='' ) {
        isValid = false
        ElMessage.warning('查询条件不能全为空')

      }
      if (this.searchInfo.course=='' && this.searchInfo.identity!='') {
        isValid = false
        ElMessage.warning('身份必须基于课程查询')
      }
      if(isValid) {
        this.curPage = 1
        this.isSearching = true
        await this.queryUsers()
      }
    },
    async resetForm() {
      this.isSearching = false
      this.curPage = 1
      this.searchInfo = {
        personId: '',
        username: '',
        grade: '',
        course: '',
        identity: ''
      }
      await this.queryUsers()
    },
    async changePage(currentPage) {
      this.curPage = currentPage
      await this.queryUsers()
    },
    handleEdit(index, row) {
      this.editUserInfo.id = row['id']
      this.editUserInfo.personId = row['person_id']
      this.editUserInfo.username = row['username']
      this.editUserInfo.grade = row['grade']
      this.editVisible = true
      this.queryUsers()
    },
    onExport() {
      ElMessageBox.confirm('此操作将导出当前查询结果, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async() => {
        if (this.isSearching) {
          await search_all_user_api(this.searchInfo.personId, this.searchInfo.username, this.searchInfo.grade, this.searchInfo.course, this.searchInfo.identity).then(res => {
            const title = ['ID', '学号', '姓名', '年级', '参与课程及身份']
            exportExcel(res.data['result'], '用户信息', title, 'sheetName')
            ElMessage.success('导出成功！')
          })
        } else {
          const title = ['ID', '学号', '姓名', '年级', '参与课程及身份']
          exportExcel(this.tableData, '用户信息', title, 'sheetName')
          ElMessage.success('导出成功！')
          // await get_all_user_list_api().then(res => {
          //   const title = ['ID', '学号', '姓名', '年级', '参与课程及身份']
          //   exportExcel(res.data['result'], '用户信息', title, 'sheetName')
          //   ElMessage.success('导出成功！')
          // })
        }
      })
    },
    deleteOne(index, row) {
      ElMessageBox.confirm('此操作将永久删除该用户, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async() => {
        await del_user_api(row['id']).then(res => {
          ElMessage.success('删除成功！')
          this.queryUsers()
        })
      })
    },
    resetPassword(index, row) {
      ElMessageBox.confirm('此操作将重置该用户密码, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async() => {
        await reset_user_password_api(row['id']).then(res => {
          ElMessage.success('重置成功！')
        })
      })
    },
    handleFileUploaded(file) {
      this.batchCreationInfo.file = file
    },
    async submitBatchCreation() {
      let data = new FormData()
      data.append('xlsxFile', this.batchCreationInfo.file[0].raw)
      await excel_create_users_api(data, this.batchCreationInfo.course, this.batchCreationInfo.identity).then(res => {
        ElMessage.success('批量创建成功！')
        this.batchCreationVisible = false
        this.queryUsers()
      })
    }
  },
  setup(_props) {
    const registerFormRef = ref<FormInstance>()
    const editFormRef = ref<FormInstance>()
    const multipleTableRef = ref<InstanceType<typeof ElTable>>()
    const multipleSelection = ref([])
    const submitCreate = async(formEl: FormInstance | undefined) => {
      if (!formEl) return
      await formEl.validate(async (valid, fields) => {
        if (valid) {
          await signup_api(registerUser.personId, registerUser.username, registerUser.grade, registerUser.course, registerUser.identity).then(res => {
            ElMessage.success('创建成功！')
            this.resetForm()
            this.createVisible = false
          })
        } else {
          ElMessage.warning('错误提交！！')
        }
      })
    }
    const submitEdit = async(formEl: FormInstance | undefined) => {
      if (!formEl) return
      await formEl.validate(async (valid, fields) => {
        if (valid) {
          await update_userinfo_api(editUserInfo.id, editUserInfo.personId, editUserInfo.username, editUserInfo.grade).then(res => {
            ElMessage.success('修改成功！')
            this.resetForm()
            this.editVisible = false
          })
        } else {
          ElMessage.warning('错误提交！！')
        }
      })
    }
    const handleSelectionChange = (val) => {
      multipleSelection.value = val
    }
    const batchDelete = () => {
    if (multipleSelection.value.length === 0) {
        ElMessage.warning('请至少选择一项')
      } else {
        ElMessageBox.confirm('此操作将永久删除该用户, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(async() => {
          let data = []
          for (let i = 0; i < multipleSelection.value.length; i++) {
            data.push(multipleSelection.value[i]['id'])
          }
          await del_users_api(data).then(res => {
            ElMessage.success('删除成功！')
            this.queryUsers()
          })
        })
      }
    }
    return {
      registerFormRef,
      submitCreate,
      editFormRef,
      submitEdit,
      multipleTableRef,
      handleSelectionChange,
      batchDelete,
    }
  },
  async mounted() {
    await get_all_courses_api().then(res => {
      this.courseInfo = res.data['result']
    })
    this.getRequest()
    await this.queryUsers()
  }
}
</script>

<style scoped>

</style>