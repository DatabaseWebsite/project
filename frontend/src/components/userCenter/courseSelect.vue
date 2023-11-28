<template>
  <el-dialog
    title="切换课程"
    :model-value="courseSelectVisible"
    :show-close="false"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    width="500px"
  >
    <el-radio-group v-model="selected">
     <el-radio
       v-for="item in courses"
       :label="item"
       >{{item['name']}}</el-radio>
    </el-radio-group>
    <el-button @click="closeCourseSelect"> 取消 </el-button>
    <el-button
      @click="submit"
    >确认</el-button>
  </el-dialog>
</template>

<script lang="ts">

import {get_all_courses_api, user_select_course_api} from "@/api/api.ts";
import useAuthStore from "@/store/user.ts";

export default {
  name: "courseSelect",
  props: {
    courseSelectVisible: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      courses: [],
      selected: {}
    }
  },
  watch: {
    selected(val) {
      console.log(val)
    }
  },
  methods: {
    closeCourseSelect() {
      this.$parent.closeCourseSelect()
    },
    async submit() {
      console.log(this.selected)
      await user_select_course_api(this.selected['course_id']).then(res => {
        useAuthStore().setCourse(this.selected['name'])
        // location.reload()
        this.closeCourseSelect()
      })
    }
  },
  mounted() {
    get_all_courses_api().then(res => {
      this.courses = res.data.result
      console.log(this.courses)
    })
  }
}
</script>

<style scoped>

</style>