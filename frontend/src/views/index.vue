<template>
  <el-affix class="head">
    <div class="title">
      <div>
        <i>{{menuTitle}}</i>
      </div>
      <div style="display: flex; align-items: center;">
        <i>{{currentTime}} {{timeState}}好，{{user['username']}}</i>
        <message/>
      </div>
    </div>
    <el-divider style="margin: 0; padding: 0;"/>
  </el-affix>
  <el-container class="all">
    <el-aside class="aside" style="width:70px">
      <el-menu
        default-active="1"
        :collapse="true"
        @select="menuSelect"
        router
        >
        <el-menu-item index="/announcement">
          <el-icon><Notification /></el-icon>
          <template #title><span>课程公告</span></template>
        </el-menu-item>
        <el-menu-item v-if="user['identity'] !== 'STUDENT'" index="/courseManagement">
          <el-icon><Grid /></el-icon>
          <template #title><span>课程管理</span></template>
        </el-menu-item>
        <el-menu-item index="/reference">
          <el-icon><Files /></el-icon>
          <template #title><span>课程资料</span></template>
        </el-menu-item>
        <el-menu-item index="/homework">
          <el-icon><Document /></el-icon>
          <template #title><span>课程作业</span></template>
        </el-menu-item>
        <el-menu-item index="/discussionArea">
          <el-icon><ChatSquare /></el-icon>
          <template #title><span>讨论区</span></template>
        </el-menu-item>
        <el-menu-item v-if="user['identity'] === 'ADMIN'" index="/userManage">
          <el-icon><Tools /></el-icon>
          <template #title><span>用户管理</span></template>
        </el-menu-item>
        <el-sub-menu v-if="user['identity'] === 'ADMIN'">
          <template #title>
            <el-icon><Management /></el-icon>
            <span>日志管理</span>
          </template>
          <el-menu-item index="/loginLog">
            <el-icon><List/></el-icon>
            <template #title><span>登录日志</span></template>
          </el-menu-item>
          <el-menu-item index="/operationLog">
            <el-icon><DocumentChecked /></el-icon>
            <template #title><span>操作日志</span></template>
          </el-menu-item>
        </el-sub-menu>
        <el-menu-item index="/userCenter">
          <el-icon><User /></el-icon>
          <template #title><span>个人中心</span></template>
        </el-menu-item>
      </el-menu>
      <div class="only-avatar">
        <el-avatar class="avatar-else" :src="user['avatar']"/>
      </div>
    </el-aside>
    <el-main style="position: absolute; left: 70px;width: calc(100% - 70px); top: 80px">
      <router-view/>
    </el-main>
  </el-container>
</template>

<script lang="ts">
import {
  ArrowLeftBold,
  ArrowRight, ArrowRightBold,
  ChatSquare,
  Document,
  Files,
  Grid,
  List,
  Notification, Tools,
  User,
  Management,
  DocumentChecked
} from "@element-plus/icons-vue";
import {
  Comments as IconComments,
} from "@icon-park/vue-next";
import useAuthStore from "@/store/user.ts";
import Message from "@/components/Message/message.vue";

export default {
  name: "index",
  components: {
    Message,
    Tools, ArrowRightBold, ArrowRight, ArrowLeftBold, User, List, ChatSquare, Document, Grid, Notification, Files, Management, DocumentChecked, IconComments },
  data() {
    return {
      currentTime: '',
      timeState: '',
      menuTitle: '课程公告',
      user: useAuthStore().getUser
    };
  },
  methods: {
    menuSelect(index) {
      switch (index) {
        case "/announcement":
          this.menuTitle = '课程公告'
          break
        case "/courseManagement":
          this.menuTitle = '课程管理'
          break
        case "/reference":
          this.menuTitle = '课程资料'
          break
        case "/homework":
          this.menuTitle = '课程作业'
          break
        case "/discussionArea":
          this.menuTitle = '讨论区'
          break
        case '/userManage':
          this.menuTitle = '用户管理'
          break
        case "/loginLog":
          this.menuTitle = '日志管理/登录日志'
          break
        case "/operationLog":
          this.menuTitle = '日志管理/操作日志'
          break
        case "/userCenter":
          this.menuTitle = '个人中心'
          break
      }
    }
  },
  async mounted() {
    setInterval(() => {
      let timeNow = new Date()
      this.currentTime = timeNow.toLocaleString().replaceAll('/', '-');
      let hours = timeNow.getHours();
      if (hours >= 6 && hours <= 10) this.timeState = '早上'
      else if (hours > 10 && hours <= 14) this.timeState = '中午'
      else if (hours > 14 && hours <= 18) this.timeState = '下午'
      else this.timeState = '晚上'
    }, 1000)
  },
}

</script>

<style lang="scss" scoped>
.head {
  padding: 0;
  height: 60px;
  position: absolute;
  top:0;
  left: 70px;
  width: calc(100% - 70px);
}
.aside {
  height: 100%;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  .user-info {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 180px;
    height: 70px;
    margin: 10px;
    .aside {
      width: 70px;
      height: 70px;
      position: absolute;
      left: 0;
      .avatar {
        width: 60px;
        height: 60px;
      }
    }
  }
  .only-avatar {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 70px;
    .avatar-else {
      margin: 10px;
      width: 60px;
      height: 60px;
    }
  }
}
.title {
  background-color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 0.5%;
  font-family: "Microsoft YaHei",cursive;
  font-size: 18px;
  color: dimgray;
}
</style>