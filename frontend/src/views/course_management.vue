<template>
    <div>1111
        </div>
    <el-button
        @click="handleLogin()"
        
      >登录</el-button>
    
    <div>
        <courseForm v-for="(item, index) in course_info" :item =item>
        </courseForm>
    </div>
</template>
  
<script lang="ts">
import { create_course_api, all_course_info_api } from "@/api/api.ts";
import courseForm from "@/components/course_management/courseForm.vue";

export default {
  name: "course_management",
  components: { courseForm },
  data() {
    return {
      course_info: null,
    };
  },
  methods: {
    async handleLogin() {
      try {
        // Call the API
        let info = await all_course_info_api();

        // Update the data property
        this.course_info = info.data.result;

        console.log("API call successful");
      } catch (error) {
        console.error("Error calling API:", error);
      }
    },
  },
};
</script>

<style scoped>
/* Your styles go here */
</style>