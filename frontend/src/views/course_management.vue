<template>  
  <el-container>
    <el-aside> 
    <el-form :model="course" ref="courseRef">  
          <el-form-item>  
            <el-button type="primary" @click="addCourse">添加课程</el-button>  
             
          </el-form-item>  
          <el-form-item label="course_name" prop="name">  
            <el-input v-model="course.name"></el-input>  
          </el-form-item>      
    </el-form>  
    </el-aside> 
    <el-main>  
      <courseForm v-for="(item, index) in course_info" :item="item" />  
    </el-main>  
  </el-container>  
</template>  
  
<script lang="ts">  
import { create_course_api, all_course_info_api } from "@/api/api.ts";  
import courseForm from "@/components/course_management/courseForm.vue";  
import { ElContainer, ElHeader, ElMain } from "element-plus";  
  
export default {  
  name: "course_management",  
  components: { courseForm },  
  data() {  
    return {  
      course_info: null,
      course:{
        name:"",
      },  
      try_course:"1234",
    };  
  },  
  created() {  
    this.handleLogin(); // Call the login function during the creation of the component  
  },  
  methods: {  
    async handleLogin() {
        // Call the API  
        await create_course_api(this.course.name).then(res => {
          this.course_info = res.data.result;
          console.log(res)

          console.log("API call successful");
        })
  
        // Update the data property  

    },
    addCourse() {
      
      this.$refs.courseRef.validate((valid) => {  
        if (valid) {  
          console.log("success");
          //course_add_api(course.name);
          this.handleLogin();
          
        } else {  
          console.log('提交失败');  
        }  
      });  
    }
  },  
};  
</script>  
  
<style scoped>  
/* Your styles go here */  
</style>