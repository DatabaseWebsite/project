<template>
  <el-container>
    <el-header style="display: flex; justify-content: space-between; align-items: center;">
      <el-container>
        <el-aside width = 50%>
          <el-input v-model="searchInput" placeholder="搜索" style="width: 50%;"></el-input>
          <el-button icon="search" @click="submitSearch(searchInput)" style="margin-left: 10px;"></el-button>
        </el-aside>
        <el-main>
          <el-button type="primary" @click="showCreatePostDialog = true" class="create-post-btn">
            新建帖子
          </el-button>
        </el-main>
      </el-container>
    </el-header>
      <!-- <el-button link type="primary" @click="showCreatePostDialog = true" class="create-post-btn">新建帖子</el-button> -->
    <el-main>
      <div v-for="post in posts" :key="post.id">
        <discussion-post :post="post" @click="goToPost(post.id)" />
      </div>
    </el-main> 
  </el-container>
  <el-dialog v-model="showCreatePostDialog" title="编辑公告" width="70%">
    <div>
      <span style="font-size: 18px; font-weight: bold;">标题</span>
      <el-input v-model="createItem['title']" placeholder="请输入标题" style="margin-bottom: 10px;"/>
    </div>
    <md-editor v-model="createItem['content']"/>
    <template #footer>  
      <span class="dialog-footer">  
        <el-button type="primary" @click="submitCreate">  确认  </el-button>
        <el-button type="primary" @click="cancelCreate">  取消  </el-button>
      </span>  
    </template>  
  </el-dialog>
  <!--create-post-dialog v-if="showCreatePostDialog" @close="showCreatePostDialog = false" /-->
</template>

<script>
  import DiscussionPost from './DiscussionPost.vue';
  import CreatePostDialog from './CreatePostDialog.vue';
  import MdEditor from "@/components/markdown/mdEditor.vue";
  import {Star,Bell,Search,Plus} from '@element-plus/icons-vue';
  import {post_list_api,create_post_api,search_posts_api} from '@/api/api.ts';
  // import { ElIcon, ElSearch } from 'element-plus';

  export default {
    components: {
      DiscussionPost,
      CreatePostDialog,MdEditor
      //,ElIcon, ElSearch
    },
    
    data() {
      return {
        posts: [
        ],
        showCreatePostDialog: false,
        createItem: { title: '', content: ''},
        searchInput:''
      };
    },
    async created () {
      await this.loadPosts();
    },
    async mounted() {
      await this.loadPosts();
    },
    methods: {
      goToPost(postId) {
        this.$router.push({ name: 'PostDetail', params: { id: postId } });
      },
      async loadPosts(){
        try {
          this.posts = (await post_list_api()).data.result;
        } catch (error) {
          console.error('load Posts:', error);
          //students.value = []; // 在错误情况下重置学生数组
        }
      },
      cancelCreate() {
        this.createItem['content'] = '';
        this.createItem['title'] = '';
        this.showCreatePostDialog = false;
      },
      async submitCreate(){
        console.log("create submit",this.createItem['title'],this.createItem['content']);
        try {
          console.log("create submit",this.createItem['title'],this.createItem['content']);
          await create_post_api(this.createItem['title'],this.createItem['content']);
          //students.value = response.data; // 假设返回的数据在data属性中
        } catch (error) {
          console.error('Failed to submit create:', error);
          //students.value = []; // 在错误情况下重置学生数组
        }
        this.loadPosts();
        this.cancelCreate();
      },
      
      async submitSearch(string) {
        console.log("sumbit input", string);
        try {
          console.log("search submit",string);
          this.posts = await search_posts_api(string);
          //students.value = response.data; // 假设返回的数据在data属性中
        } catch (error) {
          console.error('Failed to submit search:', error);
          //students.value = []; // 在错误情况下重置学生数组
        }
      }
    }
  };
  </script>
  
  <style scoped>


.icon {
  width: 20px; /* 调整图标大小 */
  height: 20px; /* 调整图标大小 */
  margin-right: 5px;
}


.post-search {
  width:500px;
}

.create-post-btn {
  position: fixed; /* 使用固定定位，相对于视窗定位按钮 */
  top: 100px; /* 距离顶部的距离 */
  right: 100px; /* 距离右侧的距离 */
}
</style>