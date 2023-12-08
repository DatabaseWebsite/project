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
          <el-button type="primary" @click="submitForm"> <el-icon><Search/></el-icon>查询 </el-button>
          <el-button type="info" @click="resetForm"> <el-icon><Refresh/></el-icon>重置 </el-button>
        </el-form-item>
      </el-form>
      <el-button size="small" type="primary" @click="createVisible=true;"> <icon-add-user/>新增 </el-button>
      <el-button size="small" type="danger" @click="batchDelete"> <el-icon><Delete/> </el-icon>批量删除 </el-button>
      <el-button size="small" type="warning" @click="onExport"> <el-icon><Download/></el-icon>导出 </el-button>
      <el-button size="small" type="success" @click="batchCreationVisible=true"> <el-icon><UploadFilled/></el-icon>批量创建 </el-button>
    </el-header>
    <el-main>
      <el-table ref="multipleTableRef" :data="tableData" border @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="50"></el-table-column>
        <el-table-column prop="id" label="序号" width="70"></el-table-column>
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
        <el-select v-model="batchCreationInfo.course_id" placeholder="请选择课程" clearable>
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
  UploadFilled,
  Search,
  Refresh
} from "@element-plus/icons-vue";
import {onMounted, ref, watch} from "vue";
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
    Delete, Download, UploadFilled, uploadExcel, Search, Refresh
  },
  setup(_props) {
    const registerFormRef = ref<FormInstance>()
    const editFormRef = ref<FormInstance>()
    const multipleTableRef = ref<InstanceType<typeof ElTable>>()
    const multipleSelection = ref([])
    const searchInfo = ref({
      personId: '',
      username: '',
      grade: '',
      course: '',
      identity: '',
    })
    const courseInfo = ref([])
    const isSearching = ref(false)
    const tableData = ref([])
    const curPage = ref(1)
    const totPage = ref(1)
    const createVisible = ref(false)
    const batchCreationVisible = ref(false)
    const editVisible = ref(false)
    const batchCreationInfo = ref({
      file: [],
      course_id: '',
      identity: '',
    })

    const submitCreate = async(formEl: FormInstance | undefined) => {
      if (!formEl) return
      await formEl.validate(async (valid, fields) => {
        if (valid) {
          await signup_api(registerUser.personId, registerUser.username, registerUser.grade, registerUser.course, registerUser.identity).then(async res => {
            ElMessage.success('创建成功！')
            isSearching.value = false
            curPage.value = 1
            searchInfo.value = {
              personId: '',
              username: '',
              grade: '',
              course: '',
              identity: ''
            }
            await queryUsers()
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
          await update_userinfo_api(editUserInfo.id, editUserInfo.personId, editUserInfo.username, editUserInfo.grade).then(async res => {
            ElMessage.success('修改成功！')
            isSearching.value = false
            curPage.value = 1
            searchInfo.value = {
              personId: '',
              username: '',
              grade: '',
              course: '',
              identity: ''
            }
            await queryUsers()
            editVisible.value = false
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
          await del_users_api(data).then(async res => {
            ElMessage.success('删除成功！')
            await queryUsers()
          })
        })
      }
    }
    function getRequest() {
      const result = {}
      const query = window.location.href.split('?')[1]
      if (query) {
        const queryArr = query.split('&')
        queryArr.forEach(item => {
          const value = decodeURIComponent(item.split('=')[1])
          const key = item.split('=')[0]
          const results = result as any
          results[key] = value
        })
      }
      if (!query.indexOf('personId')) {
        isSearching.value = false
        curPage.value = result['page'] || 1
      } else {
        searchInfo.value['personId'] = result['personId']
        searchInfo.value['username'] = result['username']
        searchInfo.value['grade'] = result['grade']
        searchInfo.value['course'] = result['course']
        searchInfo.value['identity'] = result['identity']
        isSearching.value = true
        curPage.value = result['page']
      }
    }
    async function queryUsers() {
      if (isSearching.value) {
        window.location.href = `/#/userManage?personId=${searchInfo.value.personId}&username=${searchInfo.value.username}&grade=${searchInfo.value.grade}&course=${searchInfo.value.course}&identity=${searchInfo.value.identity}&page=${curPage.value}`
        await search_user_api(searchInfo.value.personId, searchInfo.value.username, searchInfo.value.grade, searchInfo.value.course, searchInfo.value.identity, curPage.value).then(res => {
          tableData.value = res.data['result']
          totPage.value = res.data['total_page']
        })
      } else {
        const page = curPage.value || 1
        window.location.href = `/#/userManage?page=${page}`
        await get_user_list_api(curPage.value).then(res => {
          tableData.value = res.data['result']
          totPage.value = res.data['total_page']
        })
      }
    }
    async function submitForm() {
      let isValid = true
      if (searchInfo.value.personId=='' && searchInfo.value.username=='' && searchInfo.value.course=='' && searchInfo.value.identity=='' && searchInfo.value.grade=='' ) {
        isValid = false
        ElMessage.warning('查询条件不能全为空')

      }
      if (searchInfo.value.course=='' && searchInfo.value.identity!='') {
        isValid = false
        ElMessage.warning('身份必须基于课程查询')
      }
      if(isValid) {
        curPage.value = 1
        isSearching.value = true
        await queryUsers()
      }
    }
    async function changePage(currentPage) {
      curPage.value = currentPage
      await queryUsers()
    }
    async function handleEdit(index, row) {
      editUserInfo.id = row['id']
      editUserInfo.personId = row['person_id']
      editUserInfo.username = row['username']
      editUserInfo.grade = row['grade']
      editVisible.value = true
      await queryUsers()
    }
    function onExport() {
      ElMessageBox.confirm('此操作将导出当前查询结果, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async() => {
        if (isSearching.value) {
          await search_all_user_api(searchInfo.value.personId, searchInfo.value.username, searchInfo.value.grade, searchInfo.value.course, searchInfo.value.identity).then(res => {
            const title = ['序号', '学号', '姓名', '参与课程及身份']
            exportExcel(res.data['result'], '用户信息', title, 'sheetName')
            ElMessage.success('导出成功！')
          })
        } else {
          await get_all_user_list_api().then(res => {
            const title = ['序号', '学号', '姓名', '参与课程及身份']
            exportExcel(res.data['result'], '用户信息', title, 'sheetName')
            ElMessage.success('导出成功！')
          })
        }
      })
    }
    function deleteOne(index, row) {
      ElMessageBox.confirm('此操作将永久删除该用户, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async() => {
        await del_user_api(row['id']).then(res => {
          ElMessage.success('删除成功！')
          queryUsers()
        })
      })
    }
    function resetPassword(index, row) {
      ElMessageBox.confirm('此操作将重置该用户密码, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async() => {
        await reset_user_password_api(row['id']).then(res => {
          ElMessage.success('重置成功！')
        })
      })
    }
    function handleFileUploaded(file) {
      batchCreationInfo.value.file = file
    }
    async function submitBatchCreation() {
      let data = new FormData()
      data.append('xlsxFile', batchCreationInfo.value.file[0].raw)
      await excel_create_users_api(data, batchCreationInfo.value.course_id, batchCreationInfo.value.identity).then(res => {
        ElMessage.success('批量创建成功！')
        batchCreationVisible.value = false
        queryUsers()
      })
    }
    async function resetForm() {
      isSearching.value = false
      curPage.value = 1
      searchInfo.value = {
        personId: '',
        username: '',
        grade: '',
        course: '',
        identity: ''
      }
      await queryUsers()
    }
    watch(createVisible, async (newVal, oldVal) => {
      if (newVal) {
        await get_all_courses_api().then(res => {
          registerUser.identity = ''
          registerUser.course = ''
          registerUser.grade = ''
          registerUser.personId = ''
          registerUser.username = ''
          courseInfo.value = res.data['result']
          console.log('获取课程信息成功！')
        })
      }
    })
    onMounted(async () => {
      await queryUsers()
    })
    return {
      registerFormRef,
      submitCreate,
      editFormRef,
      submitEdit,
      multipleTableRef,
      handleSelectionChange,
      batchDelete,
      searchInfo,
      courseInfo,
      isSearching,
      tableData,
      curPage,
      totPage,
      createVisible,
      batchCreationVisible,
      editVisible,
      batchCreationInfo,
      getRequest,
      resetPassword,
      resetForm,
      handleEdit,
      handleFileUploaded,
      submitForm,
      submitBatchCreation,
      deleteOne,
      onExport,
      changePage
    }
  }
}
</script>

<style scoped>

</style>