<template>  
  <el-container class="card-container">  
    <el-header></el-header>
    <el-card class="box-card">  
      <template #header>  
        <div class="card-header">  
          <span>{{ item.course_id }}</span>  
          <el-button text @click="showCourseInfo">详细信息</el-button>  
        </div>  
      </template>  
      <div class="text item">{{ item.name }}</div>  
    </el-card>  
  
    
  </el-container>
  <el-dialog  
      v-model="courseInfoVisible"  
      title="详细信息"  
      width="60%">  
      <el-container>
        <el-header>
          <el-button type="primary" size="small" @click="createVisible = true">添加学生</el-button>
        </el-header>
        <el-main>
          <el-table :data="students" style="width: 100%">  
            <el-table-column prop="id" label="id" width="90" />  
            <el-table-column prop="name" label="Name" width="90" />  
            <el-table-column prop="identity" label="identity" />  
            <el-table-column prop="email" label="email" />  
            <el-table-column fixed="right" label="操作" width="200">
              <template #default="scope">
                <el-button type="primary" size="small" @click="showDeleteConfirm(scope.row)">
                  删除学生
                </el-button>
                <el-button type="primary" size="small" @click="changeStudent(scope.$index, scope.row)">
                  修改身份
                </el-button>
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
      <template #footer>  
        <span class="dialog-footer">  
          <el-button @click="cancelDialog">Cancel</el-button>  
          <el-button type="primary" @click="confirmDialog">Confirm</el-button>  
        </span>  
      </template> 
    </el-dialog>
       
    <el-dialog title="添加学生信息" v-model="createVisible" >
      <el-form ref="editFormRef" :model="createUserInfo" :label-width="50">
        <el-form-item label="学号" prop="personId">
          <el-input v-model="createUserInfo.personId" placeholder="请输入学号"></el-input>
        </el-form-item>
        <el-form-item label="姓名" prop="username">
          <el-input v-model="createUserInfo.username" placeholder="请输入姓名"></el-input>
        </el-form-item>
        <el-form-item label="身份" prop="identity">
          <el-input v-model="createUserInfo.identity" placeholder="请TEACHER,ASSISTANT,STUDENT"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="createUserInfo.email" placeholder="请输入邮箱"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitCreate"> 提交 </el-button>
        </el-form-item>
      </el-form>
      
    </el-dialog>

    <el-dialog title="身份设置" v-model="changeVisible">
      <el-form ref="changeFormRef" :model="changeInfo" :label-width="80">
        <el-form-item label="身份" prop="identity">
          <el-input v-model="changeInfo.identity" placeholder="新身份"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitChange(changeFormRef)"> 提交 </el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog v-model="deleteVisible" title="确认删除" width="30%">
      <span>确定要删除这位学生吗？</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="cancelDialog">取消</el-button>
          <el-button type="primary" @click="deleteStudent">确认删除</el-button>
        </span>
      </template>
    </el-dialog>
</template>

<script setup lang="ts">
import { ref, defineProps,computed,watch  } from 'vue';
import {all_participants_api, add_course_user_api} from "@/api/api.ts";  
const courseInfoVisible = ref(false);
const createVisible = ref(false);
const changeVisible = ref(false);
const deleteVisible = ref(false); // 确认删除的对话框状态
const currentPage = ref(1);
const { item } = defineProps(['item']);
// const students = ref([{ id: 1, name: 'gaosj', identity: '老师' }, { id: 2, name: 'byc', identity: '学生' }, { id: 2, name: 'byc', identity: '学生' },
//  { id: 2, name: 'byc', identity: '学生' },{ id: 2, name: 'byc', identity: '学生' }, { id: 2, name: 'byc', identity: '学生' },{ id: 2, name: 'byc', identity: '学生' },
//  { id: 2, name: 'byc', identity: '学生' }, { id: 2, name: 'byc', identity: '学生' },{ id: 2, name: 'byc', identity: '学生' },{ id: 2, name: 'byc', identity: '学生' }, 
//  { id: 2, name: 'byc', identity: '学生' },]);
//const students = ref([]);
const students = ref([]);
const createUserInfo = ref({ personId: '', username: '', identity: '',email:'' });
const changeInfo = ref({});
let currentStudent = ref({}); // 当前选中的学生

// 创建学生
const submitCreate = async () => {
  //students.value.push({ id: createUserInfo.value.personId, name: createUserInfo.value.username, identity: createUserInfo.value.identity,email : createUserInfo.value.email});
  
  try {
    console.log("add course user api start",createUserInfo.value.personId,createUserInfo.value.username,createUserInfo.value.identity,createUserInfo.value.email,item.course_id);
    await add_course_user_api(createUserInfo.value.personId,createUserInfo.value.username,createUserInfo.value.identity,createUserInfo.value.email,item.course_id);
    //students.value = response.data; // 假设返回的数据在data属性中
    console.log("add course user api success");
  } catch (error) {
    console.error('Failed to fetch students:', error);
    students.value = []; // 在错误情况下重置学生数组
  }
  console.log("after add",item.course_id, currentPage);
  //fetchStudents(item.course_id, currentPage);
  createUserInfo.value = { personId: '', username: '', identity: '',email:'' };
  createVisible.value = false;
};

// 删除学生
const deleteStudent = () => {
  students.value = students.value.filter(student => student.id !== currentStudent.value.id);
  deleteVisible.value = false;
};

// 显示删除学生确认对话框
const showDeleteConfirm = (student) => {
  deleteVisible.value = true;
  currentStudent.value = student;
};

// 修改学生身份
const changeStudent = (index, row) => {
  changeVisible.value = true;
  changeInfo.value = { ...row };
  currentStudent.value = row;
};

// 提交身份修改
const submitChange = () => {
  const student = students.value.find(s => s.id === currentStudent.value.id);
  if (student) {
    student.identity = changeInfo.value.identity;
  }
  changeVisible.value = false;
};

// 取消对话框
const cancelDialog = () => {
  courseInfoVisible.value = false;
  deleteVisible.value = false;
  changeVisible.value = false;
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
  console.log("showCourseInfo enter" , item.course_id,currentPage.value);
  await fetchStudents(item.course_id, currentPage.value);
};

// 监听currentPage变化，然后重新获取学生数据
watch(currentPage, (newPage) => {
  fetchStudents(item.course_id, newPage);
});
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