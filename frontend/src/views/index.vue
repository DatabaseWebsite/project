<template>
  <el-affix class="head">
    <div class="title">
      <div>
        <i>{{menuTitle}}</i>
      </div>
      <div>
        <i>{{currentTime}} {{timeState}}好，{{user['username']}}</i>
        <icon-comments :size="30" style="padding: 0; margin-left: 15px; margin-right: 10px;"/>
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
        <el-menu-item index="/">
          <el-icon><Notification /></el-icon>
          <template #title><span>课程公告</span></template>
        </el-menu-item>
        <el-menu-item index="/">
          <el-icon><Grid /></el-icon>
          <template #title><span>课程管理</span></template>
        </el-menu-item>
        <el-menu-item index="/reference">
          <el-icon><Files /></el-icon>
          <template #title><span>课程资料</span></template>
        </el-menu-item>
        <el-menu-item index="/">
          <el-icon><Document /></el-icon>
          <template #title><span>课程作业</span></template>
        </el-menu-item>
        <el-menu-item index="/discussionArea">
          <el-icon><ChatSquare /></el-icon>
          <template #title><span>讨论区</span></template>
        </el-menu-item>
        <el-menu-item index="/userManage">
          <el-icon><Tools /></el-icon>
          <template #title><span>用户管理</span></template>
        </el-menu-item>
        <el-menu-item index="/">
          <el-icon><List /></el-icon>
          <template #title><span>日志管理</span></template>
        </el-menu-item>
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
  User
} from "@element-plus/icons-vue";
import {
  Comments as IconComments,
} from "@icon-park/vue-next";
import useAuthStore from "@/store/user.ts";

export default {
  name: "index",
  components: {
    Tools, ArrowRightBold, ArrowRight, ArrowLeftBold, User, List, ChatSquare, Document, Grid, Notification, Files, IconComments },
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
        case "/":
          this.menuTitle = '课程公告'
          break
        case "2":
          this.menuTitle = '课程管理'
          break
        case "/reference":
          this.menuTitle = '课程资料'
          break
        case "4":
          this.menuTitle = '课程作业'
          break
        case "/discussionArea":
          this.menuTitle = '讨论区'
          break
        case '/userManage':
          this.menuTitle = '用户管理'
          break
        case "7":
          this.menuTitle = '日志管理'
          break
        case "/userCenter":
          this.menuTitle = '个人中心'
          break
      }
    }
  },
  mounted() {
    setInterval(() => {
      let timeNow = new Date()
      this.currentTime = timeNow.toLocaleString();
      let hours = timeNow.getHours();
      if (hours >= 6 && hours <= 10) this.timeState = '早上'
      else if (hours > 10 && hours <= 14) this.timeState = '中午'
      else if (hours > 14 && hours <= 18) this.timeState = '下午'
      else this.timeState = '晚上'
    }, 1000);
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