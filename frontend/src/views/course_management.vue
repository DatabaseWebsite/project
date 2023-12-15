  <template>  
    <el-container>
      <el-header style="text-align: right; font-size: 12px"> 
        <el-button  link type="primary" size="small" @click="dialogVisible = true">  
              添加课程 
            </el-button> 
        
        
      </el-header> 
      <el-main>  
        <courseForm v-for="(item, index) in course_info" :key="index" :item="item" />
      </el-main>  
    </el-container>  
    <el-dialog  
          v-model="dialogVisible"  
          title="Tips"  
          width="60%">  
          
          <el-form :model="course" ref="courseRef">    
            <el-form-item label="course_name" prop="name">  
              <el-input v-model="course.name"></el-input>  
            </el-form-item>     
            <el-form-item label="duration" prop="duration">  
              <el-input v-model="course.duration"></el-input>  
            </el-form-item>    
            <el-form-item label="description" prop="description">  
              <el-input v-model="course.description"></el-input>  
            </el-form-item>   
          </el-form>    
        
          
        <template #footer>  
          <span class="dialog-footer">  
            <el-button @click=cancelDialog()>Cancel</el-button>  
            <el-button type="primary" @click=confirmDialog()>  Confirm  </el-button>  
          </span>  
        </template>  
    </el-dialog>
  </template>  
    
    <script lang="ts">
    import { create_course_api, all_course_info_api } from "@/api/api.ts";  
    import courseForm from "@/components/course_management/courseForm.vue";  
    
    export default {  
      name: "course_management",  
      components: { courseForm },  
      data() {
        return {
          dialogVisible: false,
          course_info: [],
          course: {
            name: "",
            duration: "",
            description: ""
          },
        };
      },
      created() {
        this.handleLogin();
      },
      methods: {  
        async handleLogin() {
          try {
            //const res = await all_course_info_api();
            //this.course_info = res.data.result;
            this.course_info = [{course_id:2,name:"gsj"},{course_id:1,name:"byc"}];
            console.log("all course_info API call successful", this.course_info);
          } catch (error) {
            console.error("Error calling API:", error);
          }
        },
        async addCourse() {
          await this.$refs.courseRef.validate(async (valid) => {
            if (valid) {
              console.log("success addCourse", this.course.name);
              //await create_course_api(this.course.name);
              await this.handleLogin();
            } else {
              console.log('提交失败');
            }
          });
        },
        cancelDialog() {
          this.dialogVisible = false;
        },
        confirmDialog() {
          this.addCourse();
          this.dialogVisible = false;
        },
      },
    }
    </script>
  
<style scoped>  
 
</style>