<template>
  <div class="discussion-board">
    <!-- 新建帖子按钮移到了右上角 -->
    <button @click="showCreatePostDialog = true" class="create-post-btn">新建帖子</button>
    
    <!-- 新建帖子对话框 -->
    <create-post-dialog v-if="showCreatePostDialog" @close="showCreatePostDialog = false" />

    <!-- 帖子内容列表，当显示创建对话框时不显示 -->
    <div v-if="!showCreatePostDialog">
      <div v-for="post in posts" :key="post.id" class="post-preview">
        <discussion-post :post="post" @click="goToPost(post.id)" />
      </div>
    </div>
  </div>
</template>
  <script>
  import DiscussionPost from './DiscussionPost.vue';
  import CreatePostDialog from './CreatePostDialog.vue';
  
  export default {
    components: {
      DiscussionPost,
      CreatePostDialog
    },
    data() {
      return {
        posts: [
          // 示例帖子数据
          { id: "1", title: "database", summary: "database too hard ", author: "gsj", timestamp: "2023-01-01" },
          // 可以添加更多帖子
          { id: "2", title: "compile", summary: "compile too simple ", author: "byc", timestamp: "2100-01-01" },
        ],
        showCreatePostDialog: false
      };
    },
    methods: {
      goToPost(postId) {
        this.$router.push({ name: 'PostDetail', params: { id: postId } });
      }
    }
  };
  </script>
  
  <style scoped>
.discussion-board {
  position: relative; /* 相对定位，为了绝对定位新建帖子按钮 */
  padding-top: 60px; /* 添加足够的上边距来防止重叠 */
  max-width: 800px;
  margin: auto;
}

.post-container {
  margin-bottom: 20px;
}

.post-item {
  background-color: #fff;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 10px;
}

.post-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.post-content {
  font-size: 14px;
  color: #666;
  margin-top: 8px;
  margin-bottom: 12px;
}

.post-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.post-author {
  font-size: 12px;
  color: #888;
}

.post-timestamp {
  font-size: 12px;
  color: #888;
}

.post-actions button {
  padding: 6px 12px;
  background-color: #4CAF50;
  border: none;
  border-radius: 4px;
  color: white;
  cursor: pointer;
}
.post-preview {
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 15px;
}
.create-post-btn {
  position: fixed; /* 使用固定定位，相对于视窗定位按钮 */
  top: 100px; /* 距离顶部的距离 */
  right: 100px; /* 距离右侧的距离 */
  padding: 10px 20px;
  background-color: #4CAF50;
  border: none;
  border-radius: 4px;
  color: white;
  cursor: pointer;
  font-size: 14px;
  z-index: 1000; /* 确保按钮在最上层 */
}
</style>