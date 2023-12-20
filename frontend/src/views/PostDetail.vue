<template>
  <div class="discussion-thread">
    <!-- Post Card -->
    <div class="post-card">
      <div class="post-header">
        <h2>{{ post.title }}</h2>
        <div class="post-actions">
          <button @click="subscribePost">订阅</button>
          <button @click="likePost">点赞</button>
          <button @click="highlightPost">加精</button>
          <button @click="pinPost">置顶</button>
        </div>
      </div>
      <div class="post-meta">
        <span class="author">{{ post.author }}</span> |
        <span class="timestamp">{{ formatTimestamp(post.timestamp) }}</span>
      </div>
      <p class="post-content">{{ post.content }}</p>
      <button class="reply-button icon" @click="showReplyDialog = true">&#128172;</button>
    </div>

    <!-- Replies List -->
    <div class="replies-list">
      <h3>回复:</h3>
      <div v-for="reply in replies" :key="reply.id" class="reply-card">
        <div class="reply-meta">
          <span class="author">{{ reply.author }}</span> |
          <span class="timestamp">{{ formatTimestamp(reply.timestamp) }}</span>
        </div>
        <p class="reply-content">{{ reply.content }}</p>
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

<script>
import { ref } from 'vue';
import MdEditor from "@/components/markdown/mdEditor.vue";
import MdPreview from "@/components/markdown/mdPreview.vue";

export default {
  components: { MdEditor,MdPreview },
  data() {
    return {
      post: {
        id: 1,
        title: '数据库作业难度太大',
        content: '我觉得数据库的作业难度太大了，不知道大家怎么看。',
        author: '张三',
        timestamp: new Date('2023-01-01 10:00:00')
      },
      replies: [{
        title: '数据库作业难度太大',
        content: '确实。',
        author: '张三',
        timestamp: new Date('2023-01-01 10:00:00')
      }],
      showReplyDialog: false,
      newReplyContent: ''
    };
  },
  methods: {
    formatTimestamp(timestamp) {
      return timestamp.toLocaleString();
    },
    subscribePost() {
      // Implement subscription logic
    },
    likePost() {
      // Implement like logic
    },
    highlightPost() {
      // Implement highlight logic
    },
    pinPost() {
      // Implement pin logic
    },
    addReply() {
      this.replies.push({
        id: this.replies.length + 1,
        author: '当前用户',
        content: this.newReplyContent,
        timestamp: new Date()
      });
      this.newReplyContent = '';
      this.showReplyDialog = false;
    }
  }
};
</script>

<style scoped>
.discussion-thread {
  background: #f5f5f5;
  border-radius: 4px;
  padding: 20px;
  margin: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
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
.post-meta, .reply-meta {
  color: #888;
  font-size: 0.85em;
  margin-bottom: 10px;
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
  right: 10px;
  bottom: 10px;
  background: none;
  border: none;
  color: #409EFF;
  cursor: pointer;
  font-size: 20px; /* 调整大小 */
}
.reply-card {
  position: relative;
  border-top: 1px solid #eaeaea;
  padding-top: 10px;
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
</style>