<template>
  <work-manage v-if="power"/>
  <student-index v-else/>
</template>

<script lang="ts">
import WorkManage from "@/components/homework/workManage.vue";
import useAuthStore from "@/store/user.ts";
import StudentIndex from "@/components/homework/studentIndex.vue";

export default {
  name: "index",
  components: {StudentIndex, WorkManage},
  computed: {
    power() {
      const use = useAuthStore()
      return use.getUser['identity'] === 'ADMIN' || use.getUser['identity'] === 'TEACHER' || use.getUser['identity'] === 'ASSISTANT'
    },
  }
}
</script>

<style scoped>

</style>