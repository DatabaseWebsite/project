<template>
  <el-container class="all">
    <el-aside v-if="!isMenuHide" class="aside" :style="{width: isCollapse ? '70px': '180px'}">
      <el-menu
        default-active="1"
        class="menu"
        :collapse="isCollapse"
        >
        <router-link to="">
          <el-menu-item index="1">
            <el-icon><Notification /></el-icon>
            <template #title><span>课程公告</span></template>
          </el-menu-item>
        </router-link>
        <router-link to="">
          <el-menu-item index="2">
            <el-icon><Grid /></el-icon>
            <template #title><span>课程管理</span></template>
          </el-menu-item>
        </router-link>
        <router-link to="">
          <el-menu-item index="3">
            <el-icon><Files /></el-icon>
            <template #title><span>课程资料</span></template>
          </el-menu-item>
        </router-link>
        <router-link to="">
          <el-menu-item index="4">
            <el-icon><Document /></el-icon>
            <template #title><span>课程作业</span></template>
          </el-menu-item>
        </router-link>
        <router-link to="">
          <el-menu-item index="5">
            <el-icon><ChatSquare /></el-icon>
            <template #title><span>讨论区</span></template>
          </el-menu-item>
        </router-link>
        <router-link to="">
          <el-menu-item index="6">
            <el-icon><Tools /></el-icon>
            <template #title><span>用户管理</span></template>
          </el-menu-item>
        </router-link>
        <router-link to="">
          <el-menu-item index="7">
            <el-icon><List /></el-icon>
            <template #title><span>日志管理</span></template>
          </el-menu-item>
        </router-link>
        <router-link to="/userCenter">
          <el-menu-item index="8">
            <el-icon><User /></el-icon>
            <template #title><span>个人中心</span></template>
          </el-menu-item>
        </router-link>
      </el-menu>
      <el-container v-if="!isCollapse" class="user-info">
        <el-aside class= "aside">
          <el-avatar class="avatar" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"/>
        </el-aside>
        <el-main class="main">
          <i class="nickname"> 申屠阿玉</i>
        </el-main>
      </el-container>
      <div  v-else class="only-avatar">
        <el-avatar class="avatar-else" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"/>
      </div>
    </el-aside>
    <el-container>
      <el-header class="head" :style="{left: isMenuHide ? '0' : (isCollapse ? '70px' : '180px'), width: isMenuHide ? '100%': (isCollapse ? 'calc(100% - 70px)': 'calc(100% - 180px)')} ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 0.5%">
          <el-button v-if="isMenuHide" @click="isMenuHide=!isMenuHide" text><el-icon><ArrowRightBold /></el-icon></el-button>
          <el-button v-else @click="isMenuHide=!isMenuHide" text><el-icon><ArrowLeftBold /></el-icon></el-button>
          <i>{{currentTime}} {{timeState}}好，申屠阿玉</i>
          <el-icon :size="30"><ChatLineSquare /></el-icon>
        </div>
        <el-divider style="margin: 0; padding: 0;"/>
      </el-header>
      <el-main>
        <el-scrollbar style="height: 100%; overflow-y: hidden;">
          <router-view></router-view>
        </el-scrollbar>
      </el-main>
    </el-container>
  </el-container>
</template>

<script lang="ts">
import {
  ArrowLeftBold,
  ArrowRight, ArrowRightBold, ChatLineSquare,
  ChatSquare,
  Document,
  Files,
  Grid,
  List,
  Notification, Tools,
  User
} from "@element-plus/icons-vue";

export default {
  name: "index",
  components: {
    Tools,
    ChatLineSquare,
    ArrowRightBold, ArrowRight, ArrowLeftBold, User, List, ChatSquare, Document, Grid, Notification, Files},
  data() {
    return {
      isCollapse: false,
      isMenuHide: false,
      currentTime: '',
      timeState: '',
    };
  },
  methods: {
    toggleCollapse() {
      this.isCollapse = window.innerWidth < 1000;
    },
  },
  mounted() {
    window.addEventListener("resize", this.toggleCollapse);
    this.toggleCollapse();
    setInterval(() => {
      let timeNow = new Date()
      this.currentTime = timeNow.toLocaleString();
      let hours = timeNow.getHours();
      if (hours >= 6 && hours <= 10) this.timeState = '早上'
      else if (hours <= 14) this.timeState = '中午'
      else if (hours <= 18) this.timeState = '下午'
      else this.timeState = '晚上'
    }, 1000);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.toggleCollapse);
  }
}

</script>

<style lang="scss" scoped>
.all {
  height: 100%;
  width: 100%;
}
.head {
  padding: 0;
  height: 60px;
  position: fixed;
  top:0;
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
    .main {
      width: 110px;
      height: 70px;
      position: absolute;
      right: 10px;
      .nickname {
        font-family: "Microsoft YaHei",cursive;
        white-space: nowrap;
        text-overflow: ellipsis;
        overflow: hidden;
        max-height: 2em;
        font-size: 15px;
        color:gray;
        font-weight: bold;
        text-align: center;
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

</style>