<template>
  <el-container>
    <el-header>
      <el-input
        v-model="searchUser.personId"
        class="w-50 m-2"
        style="width: 150px; margin-right: 20px"
        placeholder="请输入用户的学号"
      />
      <el-select style="width: 100px;" v-model="searchUser.identity" placeholder="请选择身份">
        <el-option label="学生" value="STUDENT" />
        <el-option label="助教" value="ASSISTANT" />
        <el-option label="老师" value="TEACHER" />
      </el-select>
      <el-button style="margin-left: 20px" type="primary" @click="submitCreate">添加学生</el-button>
    </el-header>
    <el-main>
      <el-table :data="students" style="width: 100%">
        <el-table-column prop="id" label="序号" width="80" />
        <el-table-column prop="personId" label="学号"/>
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="identity" label="身份" />
        <el-table-column fixed="right" label="操作" width="200">
          <template #default="scope">
            <el-popover placement="bottom" :width="400" :visible="scope.row['popoverVisible']">
              <template #reference>
                <el-button link type="primary" @click="scope.row['popoverVisible']=true"><icon-edit-name size="20"/></el-button>
              </template>
              <el-select v-model="changeInfo.identity" placeholder="请选择身份">
                <el-option label="学生" value="STUDENT" />
                <el-option label="助教" value="ASSISTANT" />
                <el-option label="老师" value="TEACHER" />
              </el-select>
              <el-button type="primary" @click="submitChange(scope.row)"> 提交 </el-button>
            </el-popover>
            <el-popconfirm
              confirm-button-text="确定"
              cancel-button-text="取消"
              title="确认将该学生移除课程吗？"
              @confirm="deleteStudent(scope.row)"
            >
              <template #reference>
                <el-button link type="danger"><icon-people-delete size="20"/></el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        layout="prev, pager, next"
        :page-count="totPage"
        :page-size="10"
        :current-page="currentPage"
        @current-change="handlePageChange">
      </el-pagination>
    </el-main>
  </el-container>
</template>

<script lang="ts">
import {ref, defineProps, watch, onMounted} from 'vue';
import {all_participants_api, add_course_user_api, modify_identity_api,del_course_user_api} from "@/api/api.ts";
import {useRoute} from "vue-router";
import { EditName as IconEditName, PeopleDelete as IconPeopleDelete } from "@icon-park/vue-next";
import useAuthStore from "@/store/user.ts";

export default {
  name: 'courseDetail',
  components: {IconEditName, IconPeopleDelete},
  setup() {
    const id = ref(1)
    const courseInfoVisible = ref(false);
    const deleteVisible = ref(false); // 确认删除的对话框状态
    const currentPage = ref(1);
    const totPage = ref(1);
// const students = ref([{ id: 1, name: 'gaosj', identity: '老师' }, { id: 2, name: 'byc', identity: '学生' }, { id: 2, name: 'byc', identity: '学生' },
//  { id: 2, name: 'byc', identity: '学生' },{ id: 2, name: 'byc', identity: '学生' }, { id: 2, name: 'byc', identity: '学生' },{ id: 2, name: 'byc', identity: '学生' },
//  { id: 2, name: 'byc', identity: '学生' }, { id: 2, name: 'byc', identity: '学生' },{ id: 2, name: 'byc', identity: '学生' },{ id: 2, name: 'byc', identity: '学生' },
//  { id: 2, name: 'byc', identity: '学生' },]);
//const students = ref([]);
    const students = ref([]);
    const changeInfo = ref({});
    const currentStudent = ref({}); // 当前选中的学生
    const searchUser = ref({})
    const visible = ref(false);
// 导入学生
    const submitCreate = async () => {
      console.log("submitCreate",searchUser.value.personId,id.value, searchUser.value.identity);
      await add_course_user_api(searchUser.value.personId,id.value, searchUser.value.identity);
    };

// 删除学生
    const deleteStudent = async (row) => {
      console.log("delete",row,id.value);
      await del_course_user_api(row['personId'],id.value);
      await fetchStudents(id.value, currentPage.value);
    };
    const submitChange = async (row) => {
      // 调用接口修改学生身份
      console.log("modify",row['id'], id.value,changeInfo.value['identity']);
      await modify_identity_api(row['id'],id.value, changeInfo.value['identity']).then(res => {
        row['identity'] = changeInfo.value['identity'] === 'STUDENT' ? '学生' : changeInfo.value['identity'] === 'ASSISTANT' ? '助教' : changeInfo.value['identity'] === 'ADMIN' ? '系统管理员' : '老师';
      })
      row['popoverVisible'] = false;
    };
// 显示删除学生确认对话框
    const showDeleteConfirm = (student) => {
      deleteVisible.value = true;
      currentStudent.value = student;
    };

// 修改学生身份
    const changeStudent = (index, row) => {
      changeInfo.value = { ...row };
      currentStudent.value = row;
    };

// 提交身份修改
    

// 取消对话框
    const cancelDialog = () => {
      courseInfoVisible.value = false;
      deleteVisible.value = false;
    };

// 计算当前页面的学生列表
// const paginatedStudents = computed(() => {
//   const start = (currentPage.value - 1) * 10;
//   const end = start + 10;
//   return students.value ? students.value.slice(start, end) : [];
// });

// 处理分页变化
    const handlePageChange = (newPage) => {
      currentPage.value = newPage;
    };
    const fetchStudents = async (courseId:Number, page:Number) => {
      await all_participants_api(courseId.toString(), page.toString()).then((response) => {
        students.value = response.data.result;
        totPage.value = Number(response.data['total_pages'])
        students.value.forEach((student) => {
          student.popoverVisible = false;
          student.identity = student.identity === 'STUDENT' ? '学生' : (student.identity === 'ASSISTANT' ? '助教' : student.identity === 'ADMIN' ? '系统管理员' : '老师');
        });
      })
    };

// 点击详细信息按钮时触发
    const showCourseInfo = async () => {
      courseInfoVisible.value = true;
      console.log("showCourseInfo enter" , id.value,currentPage.value);
      await fetchStudents(id.value, currentPage.value);
    };

// 监听currentPage变化，然后重新获取学生数据
    watch(currentPage, (newPage) => {
      fetchStudents(id.value, newPage);
    });
    onMounted(async () => {
      id.value = Number(useRoute().query.id)
      // 调用接口获取课程相信信息
      await fetchStudents(id.value, currentPage.value)
    })
    return {
      students,
      currentPage,
      changeStudent,
      handlePageChange,
      cancelDialog,
      submitChange,
      submitCreate,
      deleteStudent,
      changeInfo,
      showCourseInfo,
      searchUser,
      totPage,
      visible,
    }
  }
}
</script>

<style scoped>  
.card-container {  
  display: flex;  
  justify-content: center;  
  align-items: center;  
}  
.card-header {  
  display: flex;  
  justify-content: space-between;  
  align-items: center;  
}  

.text {  
  font-size: 14px;  
}  

.item {  
  margin-bottom: 18px;  
}  

.box-card {  
  width: 90%;  
  padding: 5px;  
  margin: 10px;  
}
</style>