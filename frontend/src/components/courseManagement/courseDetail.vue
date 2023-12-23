<template>
  <el-container>
    <el-header>
      <el-input
        v-model="searchUser.personId"
        class="w-50 m-2"
        style="width: 150px; margin-right: 20px"
        placeholder="请输入待添加学生的学号"
      />
      <el-select style="width: 100px;" v-model="searchUser.identity" placeholder="请选择身份">
        <el-option label="学生" value="STUDENT" />
        <el-option label="助教" value="ASSITANT" />
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
        <el-table-column prop="grade" label="年级" />
        <el-table-column fixed="right" label="操作" width="200">
          <template #default="scope">
            <el-popconfirm
              confirm-button-text="确定"
              cancel-button-text="取消"
              title="确认将该学生移除课程吗？"
              @confirm="deleteStudent(scope.row)"
              style="margin: 20px"
            >
              <template #reference>
                <icon-people-delete @click="deleteStudent(scope.row)"/>
              </template>
            </el-popconfirm>
            <el-popover placement="bottom" :width="400" trigger="click">
              <template #reference>
                <el-button type="text"><icon-edit-name/></el-button>
              </template>
              <el-select v-model="changeInfo.identity" placeholder="请选择身份">
                <el-option label="学生" value="STUDENT" />
                <el-option label="助教" value="ASSITANT" />
                <el-option label="老师" value="TEACHER" />
              </el-select>
              <el-button type="primary" @click="submitChange(scope.row)"> 提交 </el-button>
            </el-popover>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        layout="prev, pager, next"
        :total="students.length"
        :page-size="10"
        :current-page="currentPage"
        @current-change="handlePageChange">
      </el-pagination>
    </el-main>
  </el-container>
</template>

<script lang="ts">
import {ref, defineProps, watch, onMounted} from 'vue';
import {all_participants_api, add_course_user_api} from "@/api/api.ts";
import {useRoute} from "vue-router";
import { EditName as IconEditName, PeopleDelete as IconPeopleDelete } from "@icon-park/vue-next";

export default {
  name: 'courseDetail',
  components: {IconEditName, IconPeopleDelete},
  setup() {
    const id = ref(1)
    const courseInfoVisible = ref(false);
    const deleteVisible = ref(false); // 确认删除的对话框状态
    const currentPage = ref(1);
// const students = ref([{ id: 1, name: 'gaosj', identity: '老师' }, { id: 2, name: 'byc', identity: '学生' }, { id: 2, name: 'byc', identity: '学生' },
//  { id: 2, name: 'byc', identity: '学生' },{ id: 2, name: 'byc', identity: '学生' }, { id: 2, name: 'byc', identity: '学生' },{ id: 2, name: 'byc', identity: '学生' },
//  { id: 2, name: 'byc', identity: '学生' }, { id: 2, name: 'byc', identity: '学生' },{ id: 2, name: 'byc', identity: '学生' },{ id: 2, name: 'byc', identity: '学生' },
//  { id: 2, name: 'byc', identity: '学生' },]);
//const students = ref([]);
    const students = ref([]);
    const changeInfo = ref({});
    const currentStudent = ref({}); // 当前选中的学生
    const searchUser = ref({})
    const course = ref({})
// 导入学生
    const submitCreate = async () => {
      // 将学号返回给后端，若不存在，报错等操作
    };

// 删除学生
    const deleteStudent = (row) => {
      // 根据row.personId移除学生
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
    const submitChange = (row) => {
      // 调用接口修改学生身份
      const student = students.value.find(s => s.id === currentStudent.value.id);
      if (student) {
        student.identity = changeInfo.value.identity;
      }
    };

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
    const fetchStudents = async (courseId, page) => {
      try {
        const response = await all_participants_api(courseId, page);
        students.value = response.data; // 假设返回的数据在data属性中
      } catch (error) {
        console.error('Failed to fetch students:', error);
        students.value = []; // 在错误情况下重置学生数组
      }
    };

// 点击详细信息按钮时触发
    const showCourseInfo = async () => {
      courseInfoVisible.value = true;
      console.log("showCourseInfo enter" , course.value.id,currentPage.value);
      await fetchStudents(course.value.id, currentPage.value);
    };

// 监听currentPage变化，然后重新获取学生数据
    watch(currentPage, (newPage) => {
      fetchStudents(course.value.id, newPage);
    });
    onMounted(async () => {
      course.value.id = Number(useRoute().query.id)
      // 调用接口获取课程相信信息
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