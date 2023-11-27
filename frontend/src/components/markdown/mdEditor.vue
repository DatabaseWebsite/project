<template>
  <VueMarkdownEditor
    v-model="(text)"
    ref="editor"
    height="400px"
    @upload-image="uploadImg"
    @change="change"
  ></VueMarkdownEditor>
</template>

<script>
// v-md-editor
import VueMarkdownEditor from '@kangc/v-md-editor';
import '@kangc/v-md-editor/lib/style/base-editor.css';
import vuepressTheme from '@kangc/v-md-editor/lib/theme/vuepress.js';
import '@kangc/v-md-editor/lib/theme/style/vuepress.css';
import Prism from 'prismjs';
import {upload_image_api} from "@/api/api.ts";

export default {
  name: "mdEditor",
  props: {
    text: {
      type: String,
      default: '',
    }
  },
  components: {VueMarkdownEditor},
  methods: {
    async uploadImg(event, insertImage, files) {
      let res = await upload_image_api({
        'image': files[0],
      })
      insertImage({
        url: res.data.url,
        desc: res.data.name,
      })
    },
    change() {
      this.$emit('change', this.text)
    }
  },
  setup(_props) {
    //编辑器的主题
    VueMarkdownEditor.use(vuepressTheme, {
      Prism,
    });
  }
}
</script>

<style scoped>
</style>