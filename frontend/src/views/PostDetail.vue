<template>
  <div class="discussion-thread">
    <!-- Post Card -->
    <div class="post-card">
      <div class="post-header">
        <h2>{{ post.title }}</h2>
        <div class="post-actions">
          <button v-if="this.post.subscribe" @click="disSubscribePost">已订阅</button>
          <button v-if="this.post.subscribe==false" @click="subscribePost">订阅</button>
          <button v-if="this.post.like" @click="disLikePost">已点赞</button>
          <button v-if="this.post.like==false" @click="likePost">点赞</button>
          <button v-if="this.post.elite" @click="disHighlightPost" class="highlight-post">已加精</button>
          <button v-if="this.post.elite==false" @click="highlightPost" class="highlight-post">加精</button>
          <button v-if="this.post.top" @click="disPinPost" class="pin-post">已置顶</button>
          <button v-if="this.post.top==false" @click="pinPost" class="pin-post">置顶</button>
        </div>
      </div>
      <div class="post-meta">
        <span class="author">{{ post.author }}</span> |
        <span class="timestamp">{{ formatTimestamp(post.timestamp) }}</span>
      </div>
      <md-preview :text="post.content" class="post-content"></md-preview>
      <button class="reply-button icon" @click="showReplyDialog = true">&#128172;</button>
    </div>

    <!-- Replies List -->
    <div class="replies-list">
      <h3>回复:</h3>
      <div v-for="reply in replies" :key="reply.id" class="reply-card">
        <div class="reply-meta">
          <div>
            <span class="author">{{ reply.author }}</span> |
            <span class="timestamp">{{ formatTimestamp(reply.timestamp) }}</span>
          </div>
          <div class="reply-actions">
            <button v-if="reply.like" @click="disLikeReply">已点赞</button>
            <button v-if="reply.like==false" @click="likeReply">点赞</button>
          </div>
        </div>
        <md-preview :text="reply.content" class="reply-content"></md-preview>
        <button class="reply-button icon" @click="showReplyDialog = true">&#128172;</button>
      </div>
    </div>

    <!-- Reply Dialog -->
    <el-dialog v-model="showReplyDialog" title="创建回复" width="60%">
      <md-editor v-model="newReplyContent"></md-editor>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showReplyDialog = false">取消</el-button>
        <el-button type="primary" @click="addReply">确认回复</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import {ref} from 'vue';
import MdEditor from "@/components/markdown/mdEditor.vue";
import MdPreview from "@/components/markdown/mdPreview.vue";
import {
  get_post_api, topping_post_api, cancel_topping_post_api, subscribe_post_api, cancel_subscribe_post_api,
  like_reply_api, dislike_reply_api, like_post_api, dislike_post_api, elite_post_api, cancel_elite_post_api,
    create_reply_api,
} from "@/api/api.ts";
import {useRoute} from 'vue-router';

export default {
  components: {MdEditor, MdPreview},
  data() {
    return {
      post: {},
      replies: [],
      showReplyDialog: false,
      newReplyContent: ''
    };
  },
  created() {
    this.loadPosts();
  },
  mounted() {
    this.loadPosts();
  },
  methods: {
    formatTimestamp(timestamp) {
      const date = new Date(timestamp);
      const year = date.getFullYear();
      const month = (date.getMonth() + 1).toString().padStart(2, '0');
      const day = date.getDate().toString().padStart(2, '0');
      const hours = date.getHours().toString().padStart(2, '0');
      const minutes = date.getMinutes().toString().padStart(2, '0');
      const seconds = date.getSeconds().toString().padStart(2, '0');

      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    },
    async loadPosts() {
      const route = useRoute(); // 获取当前路由实例
      const postId = route.params.id; // 假设路由参数名postId
      console.log(route.params)
      try {
        console.log("load Post");
        const response = await get_post_api(postId); // 使用 postId 调用 API
        this.post = response.data.result.post;
        this.replies = response.data.result.replies;
        console.log(this.post)
      } catch (error) {
        console.error('load Post:', error);
        this.post = {}; // 在错误情况下重置帖子对象
      }
    },
    async subscribePost() {
      try {
        console.log("sub Post");
        await subscribe_post_api(this.post.id)
      } catch (error) {
        console.error('sub Post:', error);
        //students.value = []; // 在错误情况下重置学生数组
      }
      this.loadPosts();
      location.reload();
    },
    async disSubscribePost() {
      try {
        console.log("dissub Post");
        await cancel_subscribe_post_api(this.post.id)
      } catch (error) {
        console.error('dissub Post:', error);
        //students.value = []; // 在错误情况下重置学生数组
      }
      this.loadPosts();
      location.reload();
    },
    async likePost() {
      try {
        console.log("like Post");
        await like_post_api(this.post.id)
      } catch (error) {
        console.error('like Post:', error);
        //students.value = []; // 在错误情况下重置学生数组
      }
      this.loadPosts();
      location.reload();
    },
    async disLikePost() {
      try {
        console.log("dislike Post");
        await dislike_post_api(this.post.id)
      } catch (error) {
        console.error('disLike Post:', error);
        //students.value = []; // 在错误情况下重置学生数组
      }
      this.loadPosts();
      location.reload();
    },

    async highlightPost() {
      try {
        console.log("high Post");
        await elite_post_api(this.post.id)
      } catch (error) {
        console.error('high Post:', error);
        //students.value = []; // 在错误情况下重置学生数组
      }
      this.loadPosts();
      location.reload();
    },
    async disHighlightPost() {
      try {
        console.log("disHIgh Post");
        await cancel_elite_post_api(this.post.id)
      } catch (error) {
        console.error('dishigh Post:', error);
        //students.value = []; // 在错误情况下重置学生数组
      }
      this.loadPosts();
      location.reload();
    },
    async pinPost() {
      try {
        console.log("pin Post");
        await topping_post_api(this.post.id)
      } catch (error) {
        console.error('pin Post:', error);
        //students.value = []; // 在错误情况下重置学生数组
      }
      this.loadPosts();
      location.reload();
    },
    async disPinPost() {
      try {
        console.log("disPin Post");
        await cancel_topping_post_api(this.post.id)
      } catch (error) {
        console.error('disPin Post:', error);
        //students.value = []; // 在错误情况下重置学生数组
      }
      this.loadPosts();
      location.reload();
    },
    async addReply() {
      await create_reply_api(this.post.id, this.newReplyContent)

      this.newReplyContent = '';
      this.showReplyDialog = false;
      this.loadPosts();
      location.reload();
    },
    async likeReply() {
      try {
        console.log("like Reply");
        await like_reply_api(this.post.id)
      } catch (error) {
        console.error('like Post:', error);
        //students.value = []; // 在错误情况下重置学生数组
      }
      this.loadPosts();
      location.reload();
    },
    async disLikeReply() {
      try {
        console.log("dislike Reply");
        await dislike_reply_api(this.post.id)
      } catch (error) {
        console.error('disLike Post:', error);
        //students.value = []; // 在错误情况下重置学生数组
      }
      this.loadPosts();
      location.reload();
    },
  }
};
</script>

<style scoped>
.discussion-thread {
  background: #f5f5f5;
  border-radius: 4px;
  padding: 20px;
  margin: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  font-family: 'Microsoft YaHei', sans-serif;
}

.post-card, .replies-list {
  position: relative;
  background: white;
  border-radius: 4px;
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #dcdcdc;
}

.post-header {
  display: flex;
  justify-content: space-between;
}

.post-actions button {
  margin-left: 10px;
}

.post-actions .highlightPost {
  background-color: orange;
  color: white;
}

.post-actions .pinPost {
  background-color: skyblue;
  color: white;
}

.post-meta {
  color: #888;
  font-size: 0.85em;
  margin-bottom: 10px;
}

.reply-meta {
  border: 1px;
  display: flex;
  justify-content: space-between;
  color: #888;
  font-size: 0.85em;
  margin-bottom: 10px;
}

.reply-actions button {
  margin-left: 10px;
}

.post-content, .reply-content {
  font-size: 0.95em;
  color: #333;
}

.reply-button {
  background: none;
  border: none;
  color: #409EFF;
  cursor: pointer;
}

.reply-button.icon {
  position: absolute;
  right: 3px;
  bottom: 3px;
  background: none;
  border: none;
  color: #409EFF;
  cursor: pointer;
  font-size: 20px; /* 调整大小 */
}

.reply-card {
  position: relative;
  border: 1px solid #dcdcdc; /* 添加边框 */
  padding: 10px;
  margin-top: 10px; /* 为每个回复添加一些间隔 */
  border-radius: 4px; /* 如果需要，可以添加圆角 */
  background: white;
}

.reply-card:first-of-type {
  border-top: none;
}

.dialog-footer {
  text-align: right;
}

.create-announce-btn {
  position: absolute;
  top: 10px;
  right: 10px;
}

.highlight-post {
  background-color: #FFC107; /* 橙黄色背景 */
  color: white; /* 白色文字 */
  border: none; /* 无边框 */
  padding: 10px 20px; /* 上下10px，左右20px的内边距 */
  border-radius: 5px; /* 轻微的圆角 */
  cursor: pointer; /* 鼠标悬停时的指针样式 */
  font-size: 16px; /* 文字大小 */
  margin-right: 10px; /* 与相邻元素的右边距 */
}

.pin-post {
  background-color: #03A9F4; /* 蓝色背景 */
  color: white; /* 白色文字 */
  border: none; /* 无边框 */
  padding: 10px 20px; /* 上下10px，左右20px的内边距 */
  border-radius: 5px; /* 轻微的圆角 */
  cursor: pointer; /* 鼠标悬停时的指针样式 */
  font-size: 16px; /* 文字大小 */
}

button:hover {
  opacity: 0.9; /* 鼠标悬停时的透明度变化 */
}

button:active {
  transform: scale(0.98); /* 鼠标点击时的微缩效果 */
}
</style>