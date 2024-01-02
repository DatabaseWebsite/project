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
            发布帖子
          </el-button>
        </el-main>
      </el-container>
    </el-header>
      <!-- <el-button link type="primary" @click="showCreatePostDialog = true" class="create-post-btn">新建帖子</el-button> -->
    <el-main>
      <el-image :src="wordCloudMap" style="text-align: center"/>
      <el-row :gutter="35">
        <el-col :span="8" v-for="post in posts" :key="post['id']">
          <el-card style="padding: 10px; height: 320px; margin-bottom: 40px" @click="goToPost(post['id'])">
            <el-container style="position: relative; height: 300px">
              <el-header style="height: 20px; margin-top: 15px; display: flex; justify-content: space-between;">
                <div>
                  <el-tag style="padding-left: 10px; padding-right: 10px; margin-right: 15px;" effect="dark" type="danger" v-if="post['top'] === true">置顶</el-tag>
                  <el-tag style="padding-left: 10px; padding-right: 10px; margin-right: 15px;" effect="dark" type="warning" v-if="post['elite'] === true">加精</el-tag>
                  <el-tag style="padding-left: 10px; padding-right: 10px; margin-right: 15px;" effect="dark" type="success" v-if="post['elite'] !== true && post['top'] !== true">普通</el-tag>
                  <el-tag style="padding-left: 10px; padding-right: 10px; margin-right: 15px;" effect="dark" :color="postLikesColor(post['likes'])">{{post['likes']}} 喜欢 </el-tag>
                </div>
                <div>
                  <el-tag style="padding-left: 10px; padding-right: 10px; margin-right: 15px;" effect="dark" :color="getColor(post['like'])" @click.stop="handleLike(post)"> <icon-like size="17"/> </el-tag>
                  <el-tag style="padding-left: 10px; padding-right: 10px; margin-right: 15px;" effect="dark" :color="getColor(post['subscribe'])" @click.stop="handleSubscribe(post)"> <icon-rss size="17"/> </el-tag>
                  <el-button v-if="identity !== 'STUDENT'" style="padding-left: 10px; padding-right: 10px; margin-right: 15px;" type="danger" size="small" @click.stop="handleDelete(post)"> 删除 </el-button>
                </div>
              </el-header>
              <el-main>
                <p style="font-weight: bold; font-size: 20px">{{post['title']}}</p>
                <el-text line-clamp="5" style="font-size: 14px; color: gray; margin-top: 10px;">{{post['content']}}</el-text>
              </el-main>
              <el-footer style="height: 30px; position: absolute; bottom: 0">
                <i style="font-size: 13px; color: gray;"> 作者：{{post['author']}}</i>
                <i style="font-size: 13px; color: gray; margin-left: 20px;">发布时间：{{post['timestamp']}}</i>
              </el-footer>
            </el-container>
          </el-card>
        </el-col>
      </el-row>
    </el-main> 
  </el-container>
  <el-dialog v-model="showCreatePostDialog" title="发布帖子" width="70%">
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

<script lang="ts">
  import DiscussionPost from './DiscussionPost.vue';
  import CreatePostDialog from './CreatePostDialog.vue';
  import MdEditor from "@/components/markdown/mdEditor.vue";
  import {
    Like as IconLike,
    Unlike as IconUnlike,
    Rss as IconRss,
  } from "@icon-park/vue-next";
  import {
    post_list_api,
    create_post_api,
    search_posts_api,
    dislike_post_api,
    like_post_api,
    cancel_subscribe_post_api, subscribe_post_api, delete_post_api, word_cloud_map_api
  } from '@/api/api.ts';
  import useAuthStore from "@/store/user.ts";
  import {ElMessage, ElMessageBox} from "element-plus";

  export default {
    components: {
      DiscussionPost,
      CreatePostDialog,MdEditor,
      IconLike, IconUnlike, IconRss
      //,ElIcon, ElSearch
    },
    
    data() {
      return {
        posts: [
        ],
        showCreatePostDialog: false,
        createItem: { title: '', content: ''},
        searchInput:'',
        identity: useAuthStore().getUser['identity'],
        wordCloudMap: '',
      };
    },
    async mounted() {
      await this.loadPosts();
      await word_cloud_map_api().then(res => {
        this.wordCloudMap = res.data['img_url']
        console.log(this.wordCloudMap)
      })
    },
    methods: {
      postLikesColor(likes) {
        if (likes > 20)
          return '#c21f30'
        else if (likes > 15)
          return '#ed556a'
        else if (likes > 10)
          return '#f68c60'
        else if (likes > 5)
          return '#f09c5a'
        else
          return '#d4c4b7'
      },
      getColor(flag) {
      if (flag)
          return 'red'
        else
          return 'grey'
      },
      async handleLike(post) {
        if (post['like']) {
          await dislike_post_api(post['id']).then((res)=>{
            this.posts.forEach((item) => {
              if (item['id'] === post['id']) {
                item['like'] = false;
                item['likes'] -= 1;
              }
            })
          })
        } else {
          await like_post_api(post['id']).then((res)=>{
            this.posts.forEach((item) => {
              if (item['id'] === post['id']) {
                item['like'] = true;
                item['likes'] += 1;
              }
            })
          })
        }
      },
      handleSubscribe: async function (post) {
        if (post['subscribe']) {
          await cancel_subscribe_post_api(post['id']).then((res) => {
            this.posts.forEach((item) => {
              if (item['id'] === post['id']) {
                item['subscribe'] = false;
              }
            })
          })
        } else {
          await subscribe_post_api(post['id']).then((res) => {
            this.posts.forEach((item) => {
              if (item['id'] === post['id']) {
                item['subscribe'] = true;
              }
            })
          })
        }
      },
      handleDelete(post) {
        ElMessageBox.confirm(
          '确认删除该条帖子？',
          'Warning',
          {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning',
          }
        ).then(async () => {
          await delete_post_api(post['id']).then((res) => {
            this.posts = this.posts.filter((item) => item['id'] !== post['id']);
          })
          ElMessage({
            type: 'success',
            message: '删除成功',
          })
        })
      },
      goToPost(postId) {
        this.$router.push({ name: 'PostDetail', params: { id: postId } });
      },
      async loadPosts(){
        await post_list_api().then((res)=>{
          this.posts = res.data.result;
        });
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
        await this.loadPosts();
        this.cancelCreate();
      },
      
      async submitSearch(string) {
        await search_posts_api(string).then(res => {
          this.posts = res.data.result;
        })

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