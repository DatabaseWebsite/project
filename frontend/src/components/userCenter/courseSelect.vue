<template>
  <el-dialog
    title="切换课程"
    :model-value="courseSelectVisible"
    :show-close="false"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    width="500px"
  >
    <el-select v-model="selected" placeholder="请选择课程">
      <el-option
        v-for="item in courses"
        :key="item['course_id']"
        :label="item['name']"
        :value="item['course_id']"
      ></el-option>
    </el-select>
    <template #footer>
      <el-button @click="closeCourseSelect"> 取消 </el-button>
      <el-button
        @click="submit"
      >确认</el-button>
    </template>
  </el-dialog>
</template>

<script lang="ts">

import {get_course_list_api, get_user_select_course_api, user_select_course_api} from "@/api/api.ts";
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
      selected: ''
    }
  },
  methods: {
    closeCourseSelect() {
      this.$parent.closeCourseSelect()
    },
    async submit() {
      this.courses.forEach(item => {
        if (item['course_id'] === this.selected) {
          this.selected = item
        }
      })
      await user_select_course_api(this.selected['course_id']).then(res => {
        useAuthStore().setCourse(this.selected['course_id'], this.selected['name'])
        // location.reload()
        this.closeCourseSelect()
      })
    }
  },
  mounted() {
    get_course_list_api().then(res => {
      this.courses = res.data.result
    })
  }
}
</script>

<style scoped>

</style>