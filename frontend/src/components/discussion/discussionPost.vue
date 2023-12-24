<template>
  <div class="post-item">
    <div class="post-header">
        <div class="post-content"  @click="onClickPost">
          <img :src="post.authorAvatar" alt="Author's Avatar" class="author-avatar"/>
          <div class="post-title-author">
            <div class="post-title">{{ post.title }}</div>
            <div class="post-author-summary">
              <span class="post-author">{{ post.author }}</span> -- <span class="post-summary">{{ post.summary }}</span>
            </div>
          </div>
        </div>
        <div class="post-stats">
          <div class="likes-subscribes">
            <el-button v-if="post.like" @click.stop="disLike()" type="primary">
              <el-icon><StarFilled /></el-icon> 
            </el-button>
            <el-button v-if="post.like==false" @click.stop="addLike()" type="primary">
              <el-icon><Star /></el-icon> 
            </el-button>
            <el-button v-if="post.subscribe" @click.stop="disSub()" type="primary">
              <el-icon><Aim/></el-icon> 
            </el-button>
            <el-button v-if="post.subscribe==false" @click.stop="addSub()" type="primary">
              <el-icon><Bell /></el-icon> 
            </el-button>
          </div>
          <div class="post-timestamp">{{ post.timestamp }}</div>
        </div>
      </div>
  </div>
</template>

<script>
import {
  like_post_api,
  dislike_post_api,
  subscribe_post_api,
  cancel_subscribe_post_api,
  get_post_api,
} from "@/api/api.ts"
import {Star,Bell,Search,Plus,StarFilled,Aim} from '@element-plus/icons-vue';
export default {
  props: {
    post: Object
  },
  methods: {
    onClickPost() {
      this.$emit('click');
    },
    async addLike() {
        console.log("add like",this.post.id);
        await like_post_api(this.post.id);
        //await get_post_api(this.post.id);
      location.reload();
    },
    async addSub() {
        console.log("add sub",this.post.id);
        await subscribe_post_api(this.post.id);
      //await get_post_api(this.post.id);
      location.reload();
    },
    async disLike() {
        console.log("add like",this.post.id);
        await dislike_post_api(this.post.id);
      //await get_post_api(this.post.id);
      location.reload();
    },
    async disSub() {
        console.log("add sub",this.post.id);
        await cancel_subscribe_post_api(this.post.id);
      //await get_post_api(this.post.id);
      location.reload();
    },
    async loadPosts() {
      try {
        console.log("load Post");
        this.post = await get_post_api();
      } catch (error) {
        console.error('load Post:', error);
        //students.value = []; // 在错误情况下重置学生数组
      }
    },
  }
};
</script>

<style scoped>
.author-avatar {
width: 50px; /* 头像大小 */
height: 50px; /* 头像大小 */
border-radius: 50%; /* 圆形头像 */
margin-right: 10px; /* 与标题的间距 */
}

.post-preview {
display: flex; /* 使用弹性布局 */
align-items: center; /* 垂直居中对齐 */
border: 1px solid #ccc;
padding: 10px;
border-radius: 4px;
margin-bottom: 15px;
}

.post-header {
border: 1px solid #ccc;
padding: 10px;
margin-top: 10px;
display: flex;
align-items: center;
}

.post-title-author {
display: flex;
flex-direction: column;
justify-content: space-between;
height: 100%;
}

.post-title {
font-size: 18px;
font-weight: bold;
color: #333;
margin-bottom: 5px; /* 标题与作者/摘要的间距 */
}

.post-author-summary {
font-size: 14px;
display: flex;
align-items: center;
}

.post-author {
font-weight: bold;
color: #888;
margin-right: 5px; /* 作者与摘要的间距 */
}

.post-summary {
font-size: 14px;
color: #666;
overflow: hidden;
text-overflow: ellipsis;
white-space: nowrap; /* 防止内容折行 */
}
.create-post-btn {
position: fixed; /* 使用固定定位，相对于视窗定位按钮 */
top: 100px; /* 距离顶部的距离 */
right: 100px; /* 距离右侧的距离 */
}

.post-item {
cursor: pointer;
}


.post-content {
width: 70%;
display: flex;
align-items: center;
}

.post-stats {
width: 30%;
display: flex;
flex-direction: column;
justify-content: space-between;
align-items: flex-end; /* 对齐到右侧 */
}

.likes-subscribes {
display: flex;
align-items: center;
}

.post-timestamp {
font-size: 12px;
color: #888;
}
</style>