<template xmlns="http://www.w3.org/1999/html">
  <div>
    <el-card>
      <template #header>
        <div class="card-header">
          <span class="nickname">申屠阿玉</span>
        </div>
      </template>
      <el-container>
        <el-main>
          <el-container>
            <el-aside style="width: 50%">
              <div class="avatar-container">
                <el-avatar
                  :size="150"
                  src="/src/assets/img/avatar.jpg"
                  @mouseenter="rotateAvatar"
                  @mouseleave="resetRotation"
                />
              </div>
              <el-button type="primary" text @click="dialogVisible = true" style="float: left; margin-left: 60px"><icon-upload-picture :size="20" style="padding: 5px"/> 编辑头像</el-button>
            </el-aside>
            <el-main style="width: 50%;">
              <div style="padding-bottom: 20px">
                <div style="display: flex; align-items: center;">
                  <icon-people :size="30" style="margin-right: 10px;"/>
                  <div>
                    <i style="display: block; text-align: left; color:gray; font-size: 14px">学工号</i>
                    <i style="display: block;">21373032</i>
                  </div>
                </div>
              </div>
              <div style="padding-bottom: 20px">
                <div style="display: flex; align-items: center;">
                  <icon-permissions size="30" style="margin-right: 10px;"/>
                  <div>
                    <i style="display: block; text-align: left; color:gray; font-size: 14px">用户身份</i>
                    <i style="display: block;">学生</i>
                  </div>
                </div>
              </div>
              <div style="padding-bottom: 20px">
                <div style="display: flex; align-items: center;">
                  <icon-book :size="30" style="margin-right: 10px;"/>
                  <div>
                    <i style="display: block; text-align: left; color:gray; font-size: 14px">当前课程</i>
                    <i style="display: block;">2023数据库原理</i>
                  </div>
                </div>
              </div>
            </el-main>
          </el-container>
        </el-main>
        <el-divider style="width: 100%; margin: 0; padding-bottom: 10px"/>
        <el-footer class="footer">
          <el-row :gutter="20">
            <el-col :span="6"><el-button type="primary" text>切换课程</el-button></el-col>
            <el-col :span="6"><el-button type="danger" text>修改密码</el-button></el-col>
            <el-col :span="6"><el-button type="danger" text>退出登录</el-button></el-col>
          </el-row>
        </el-footer>
      </el-container>
    </el-card>
  </div>
  <AvatarEdit v-if="dialogVisible" :dialogVisible.sync="dialogVisible"/>
</template>

<script>
import AvatarEdit from "@/components/userCenter/avatarEdit.vue";
import {ref} from "vue";
import {
  Permissions as IconPermissions,
  People as IconPeople,
  UploadPicture as IconUploadPicture,
  Book as IconBook
} from "@icon-park/vue-next";

export default {
  name: "stuCenter",
  components: {AvatarEdit, IconPermissions, IconPeople, IconUploadPicture, IconBook},
  data() {
  },
  methods: {
  },
  setup(_props) {
    const dialogVisible = ref(false)
    const rotated = ref(false)
    const closeAvatarEdits = () => {
      dialogVisible.value = false;
    };

    const rotateAvatar = () => {
      rotated.value = true;
    };

// Function to reset the rotation on mouse leave
    const resetRotation = () => {
      rotated.value = false;
    };
    return {
      dialogVisible,
      closeAvatarEdits,
      rotateAvatar,
      resetRotation
    };
  },
}
</script>

<style lang="scss" scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.nickname {
  font-family: "Microsoft YaHei",cursive;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
  max-height: 2em;
  font-size: 30px;
  color:gray;
  font-weight: bold;
  text-align: center;
  padding-left: 20px;
}
.avatar-container {
  float:left;
  margin-left: 50px;
  margin-bottom: 20px;
  display: inline-block;
  transition: transform 0.5s ease-in-out;
  transform: rotate(0deg);
}

.avatar-container:hover {
  transform: rotate(360deg);
}

</style>