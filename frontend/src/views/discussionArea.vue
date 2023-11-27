<template>
  <el-button @click="submit"> 提交 </el-button>
  <md-editor v-model="text" />
  <md-preview :text="text" :navigation-visible="true"/>
</template>

<script>
import MdEditor from "@/components/markdown/mdEditor.vue";
import MdPreview from "@/components/markdown/mdPreview.vue";

export default {
  name: "discussionArea",
  components: {MdPreview, MdEditor},
  data() {
    return {
      text: '',
    }
  },
  methods: {
    submit() {

    }
  }
}
</script>

<style scoped>

</style>