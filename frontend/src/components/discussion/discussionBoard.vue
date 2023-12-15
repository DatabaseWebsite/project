<template>
    <div class="discussion-board">
      <button @click="showCreatePostDialog = true" class="create-post-btn">新建帖子</button>
      <create-post-dialog v-if="showCreatePostDialog" @close="showCreatePostDialog = false" />
  
      <div v-for="post in posts" :key="post.id" class="post-preview">
        <discussion-post :post="post" @click="goToPost(post.id)" />
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
    padding: 20px;
  }
  
  .create-post-btn {
    padding: 10px 20px;
    margin-bottom: 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .post-preview {
    margin-bottom: 15px;
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 4px;
  }
  </style>