<template>  
  <el-container class="card-container">  
    <el-card class="box-card">  
      <template #header>  
        <div class="card-header">  
          <span>{{ item.course_id }}</span>  
          <el-button text @click="dialogVisible = true">  
            详细信息  
          </el-button>  
        </div>  
      </template>  
      <div class="text item">  
        {{ item.name }}  
      </div>  
    </el-card>  
  </el-container>  
  <el-dialog  
    v-model="dialogVisible"  
    title="Tips"  
    width="30%"  
  >  
    <span>  
      <el-table :data="students" style="width: 100%">  
        <el-table-column prop="id" label="id" width="90" />  
        <el-table-column prop="name" label="Name" width="90" />  
        <el-table-column prop="identity" label="identity" />  
      </el-table>  
    </span>  
    <el-form :model="student" ref="studentRef">  
          <el-form-item>  
            <el-button type="primary" @click="deleteStudent">删除学生</el-button>  
            <el-button type="primary" @click="addStudent">添加学生</el-button>  
          </el-form-item>  
          <el-form-item label="student_id" prop="id">  
            <el-input v-model="student.id"></el-input>  
          </el-form-item>      
    </el-form>
    <el-form :model="cStudent" ref="chanegeStudentRef">  
          <el-form-item>  
            <el-button type="primary" @click="changeStudent">更改身份</el-button>  
          </el-form-item>  
          <el-form-item label="student_id" prop="id">  
            <el-input v-model="cStudent.id"></el-input>  
          </el-form-item>      
          <el-form-item label="身份" prop="identity">  
            <el-input v-model="cStudent.identity"></el-input>  
          </el-form-item>    
    </el-form>
    <template #footer>  
      <span class="dialog-footer">  
        
        <el-button @click=cancelDialog()>Cancel</el-button>  
        <el-button type="primary" @click=confirmDialog()>  
          Confirm  
        </el-button>  
      </span>  
    </template>  
  </el-dialog>     
</template>      
    
<script lang="ts">    
import { ref } from 'vue'
import { ElMessageBox } from 'element-plus'
import {getCurrentInstance} from "vue";
const dialogVisible = ref(false)

export default {    
  name: 'courseForm',    
  props: {    
    item: Object,    
  },    
  data() {    
    return {    
      dialogVisible: false,    
      dialogTitle: '课程参与信息',    
      student:{
        id:"",
      },
      cStudent:{
        id:"",
        identity:"",
      },
      students: [{id:1,name:'gaosj',identity:'老师'},{id:2,name:'byc',identity:'学生'},] // 存储学生信息的数组，每个元素为 { student_id, name, identity, grade } 类型的对象    
    };    
  },    
  mounted() {    
    //this.loadStudents(); // 在组件挂载后加载学生信息    
  },    
  methods: {    
    submit() {    
      // 提交表单的逻辑在这里实现    
    },    
    loadStudents() {    
      // todo ：this.students = get_Students_API(this.item.course_id);    
    },    
    cancelDialog() { // 打开对话框的方法    
      this.dialogVisible = false;// 检查值是否被正确修改为true
    },
    confirmDialog() {
      this.dialogVisible = false;
    },
    deleteStudent() {
      this.$refs.studentRef.validate((valid) => {  
        if (valid) {  
          this.students = []//todo delete_student_api(courseid,student.id)
        } else {  
          console.log('提交失败');  
        }  
      });  
    },
    addStudent() {
      this.$refs.studentRef.validate((valid) => {  
        if (valid) {  
          this.students = [{id:3,name:"cqj",identity:"助教"}]//todo add_student_api(courseid,student.id)
        } else {  
          console.log('提交失败');  
        }  
      });  
    },
    changeStudent() {
      this.$refs.chanegeStudentRef.validate((valid) => {  
        if (valid) {  
          this.students = [{id:3,name:"cqj",identity:"老师"}]//todo add_student_api(courseid,student.id)
        } else {  
          console.log('提交失败');  
        }  
      });  
    }
  }    
};    
</script>  
<style scoped>  
/* form */  
/*:deep(.el-form-item__label)  {*/  
/*  color: white; !* 设置字体颜色为白色 *!*/  
/*}*/  
.card-container{  
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
  padding:5px;  
  margin:10px;  
}  
</style>