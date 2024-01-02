<template>
  <VMdPreview :text="text"></VMdPreview>
</template>

<script lang="ts">
// 这是预览时引用的
import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';
// 引入你所使用的主题 此处以 github 主题为例
import githubTheme from '@kangc/v-md-editor/lib/theme/github';
import '@kangc/v-md-editor/lib/theme/style/github.css';
// highlightjs
import hljs from 'highlight.js';
export default {
  name: "mdPreview",
  components: {VMdPreview},
  props: {
    text: {
      type: String,
      default: '',
    },
    navigationVisible: {
      type: Boolean,
      default: false,
    },
  },
  setup(_props) {
    //预览的主题
    VMdPreview.use(githubTheme, {
      Hljs: hljs,
    });
  },
}
</script>

<style scoped>

</style>