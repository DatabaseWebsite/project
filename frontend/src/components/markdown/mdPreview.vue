<template>
  <el-container v-if="navigationVisible">
    <el-aside style="width: 60px;">
      <div
        v-for="anchor in titles"
        :style="{ padding: `10px 0 10px ${anchor.indent * 20}px` }"
        @click="handleAnchorClick(anchor)"
      >
        <a style="cursor: pointer">{{ anchor.title }}</a>
      </div>
    </el-aside>
    <el-main>
      <!--  预览-->
      <VMdPreview :text="text" ref="preview"></VMdPreview>
    </el-main>
  </el-container>
  <VMdPreview :text="text" v-else></VMdPreview>
</template>

<script>
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
  data() {
    return {
      titles: [],
    }
  },
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
  mounted() {
    const anchors = this.$refs.preview.$el.querySelectorAll('h1,h2,h3,h4,h5,h6');
    const titles = Array.from(anchors).filter((title) => !!title.innerText.trim());

    if (!titles.length) {
      this.titles = [];
      return;
    }
    const hTags = Array.from(new Set(titles.map((title) => title.tagName))).sort();

    this.titles = titles.map((el) => ({
      title: el.innerText,
      lineIndex: el.getAttribute('data-v-md-line'),
      indent: hTags.indexOf(el.tagName),
    }));
  },
  methods: {
    handleAnchorClick(anchor) {
      const { preview } = this.$refs;
      const { lineIndex } = anchor;

      const heading = preview.$el.querySelector(`[data-v-md-line="${lineIndex}"]`);

      if (heading) {
        // 注意：如果你使用的是编辑组件的预览模式,则这里的方法名改为 previewScrollToTarget
        preview.scrollToTarget({
          target: heading,
          scrollContainer: window,
          top: 60,
        });
      }
    },
  },
}
</script>

<style scoped>

</style>