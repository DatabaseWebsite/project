<template>
  <!-- <el-button @click="submit"> 提交 </el-button>
  <md-editor v-model="text" />
  <md-preview :text="text" :navigation-visible="true"/> -->
  <discussionBoard/>
</template>

<script lang="ts">
import MdEditor from "@/components/markdown/mdEditor.vue";
import MdPreview from "@/components/markdown/mdPreview.vue";
import discussionBoard from "@/components/discussion/discussionBoard.vue"
export default {
  name: "discussionArea",
  components: {MdPreview, MdEditor,discussionBoard},
  submit() {

  }
}

</script>

<style scoped>

</style>