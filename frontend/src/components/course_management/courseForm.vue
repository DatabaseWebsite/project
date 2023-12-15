<template>  
  <el-container class="card-container">  
    <el-header></el-header>
    <el-card class="box-card">  
      <template #header>  
        <div class="card-header">  
          <span>{{ item.course_id }}</span>  
          <el-button text @click="courseInfoVisible = true">详细信息</el-button>  
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
            <el-table-column fixed="right" label="操作" width="200">
              <template #default="scope">
                <el-button type="primary" size="small" @click="deleteStudent">
                    删除学生
                </el-button>
                <el-button type="primary" size="small" @click="changeStudent(scope.$index, scope.row)">修改身份</el-button>
              </template>
            </el-table-column>
          </el-table>  
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
        <el-form-item>
          <el-button type="primary" @click="submitCreate(editFormRef)"> 提交 </el-button>
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
</template>

<script setup lang="ts">
  import { ref, defineProps, defineEmits, withDefaults } from 'vue';
  import { ElMessage } from 'element-plus';
  
  
const courseInfoVisible = ref(false);
const createVisible = ref(false);
const changeVisible = ref(false);

const { item } = defineProps(['item']);
const students = ref([{id:1,name:'gaosj',identity:'老师'},{id:2,name:'byc',identity:'学生'},] );
const createUserInfo = ref({
  personId: '',
  username: '',
  identity: '',
});
const submitCreate = async (formEl) => {
  if (!formEl) return;
  await formEl.validate(async (valid, fields) => {
    if (valid) {
      // Handle form submission logic here
      // Example: await update_userinfo_api(editUserInfo.id, editUserInfo.personId, editUserInfo.username, editUserInfo.grade);
      // ElMessage.success('修改成功！');
      // this.resetForm();
      // this.editVisible = false;
    } else {
      ElMessage.warning('错误提交！');
    }
  });
  createVisible.value = false;
};
const submitChange = async (formEl) => {
  console.log("formEl ", formEl, changeInfo);
  const form = editFormRef;
  await form.validate(async (valid, fields) => {
    if (valid) {
      // Handle form submission logic here
      // Example: await update_userinfo_api(editUserInfo.id, editUserInfo.personId, editUserInfo.username, editUserInfo.grade);
      // ElMessage.success('修改成功！');
      // this.resetForm();
      console.log("id identity ", object.value.id, changeInfo.value.identity);
      // change_user_identity_api(object.value.id, changeInfo.value.identity);
    } else {
      ElMessage.warning('错误提交！');
    }
  });
  changeVisible.value = false;
};
const deleteStudent = () => {
  // Handle delete student logic here
  students.value = []; // TODO: delete_student_api(courseid, student.id)
};

const changeStudent = (index,row) => {
  // Handle change student logic here
  changeVisible.value = true;
  console.log("type ", typeof students)
  console.log("index row ", index, row.id)
  students.value = [{ id: 3, name: 'cqj', identity: '老师' }]; // TODO: add_student_api(courseid, student.id)
  object.value = row;
};

const cancelDialog = () => {
  courseInfoVisible.value = false;
};

const confirmDialog = () => {
  courseInfoVisible.value = false;
};

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