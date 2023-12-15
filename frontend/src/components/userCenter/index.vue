<template xmlns="http://www.w3.org/1999/html">
  <div>
    <el-card>
      <template #header>
        <div class="card-header">
          <span class="nickname">{{user['username']}}</span>
        </div>
      </template>
      <el-container>
        <el-main>
          <el-container>
            <el-aside style="width: 50%">
              <div class="avatar-container">
                <el-avatar
                  :size="150"
                  :src="user['avatar']"
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
                    <i style="display: block; text-align: left; color:gray; font-size: 14px" v-if="user['identity'] === 'TEACHER'">教工号</i>
                    <i style="display: block; text-align: left; color:gray; font-size: 14px" v-else>学工号</i>
                    <i style="display: block;">{{user['personID']}}</i>
                  </div>
                </div>
              </div>
              <div style="padding-bottom: 20px">
                <div style="display: flex; align-items: center;">
                  <icon-permissions size="30" style="margin-right: 10px;"/>
                  <div>
                    <i style="display: block; text-align: left; color:gray; font-size: 14px">用户身份</i>
                    <i style="display: block;">{{identity}}</i>
                  </div>
                </div>
              </div>
              <div style="padding-bottom: 20px">
                <div style="display: flex; align-items: center;">
                  <icon-book :size="30" style="margin-right: 10px;"/>
                  <div>
                    <i style="display: block; text-align: left; color:gray; font-size: 14px">当前课程</i>
                    <i style="display: block;">{{user['course']}}</i>
                  </div>
                </div>
              </div>
            </el-main>
          </el-container>
        </el-main>
        <el-divider style="width: 100%; margin: 0; padding-bottom: 10px"/>
        <el-footer class="footer">
          <el-row :gutter="20">
            <el-col :span="6"><el-button type="primary" text @click="courseSelectVisible=true;">切换课程</el-button></el-col>
            <el-col :span="6"><el-button type="danger" text @click="changePwdVisible=true">修改密码</el-button></el-col>
            <el-col :span="6"><el-button type="danger" text @click="openLogout">退出登录</el-button></el-col>
          </el-row>
        </el-footer>
      </el-container>
    </el-card>
  </div>
  <ChangePassword v-if="changePwdVisible" :changePwdVisible.sync="changePwdVisible"/>
  <AvatarEdit v-if="dialogVisible" :dialogVisible.sync="dialogVisible"/>
  <CourseSelcet v-if="courseSelectVisible" :courseSelectVisible.sync="courseSelectVisible"/>
</template>

<script lang="ts">
import AvatarEdit from "@/components/userCenter/avatarEdit.vue";
import {ref} from "vue";
import {
  Permissions as IconPermissions,
  People as IconPeople,
  UploadPicture as IconUploadPicture,
  Book as IconBook
} from "@icon-park/vue-next";
import useAuthStore from "@/store/user.ts";
import cookies from "@/lib/cookies.ts";
import {user_logout_api} from "@/api/api.ts";
import {router} from "@/router/index.ts";
import {ElMessageBox} from "element-plus";
import ChangePassword from "@/components/userCenter/changePassword.vue";
import CourseSelcet from "@/components/userCenter/courseSelect.vue";

export default {
  name: "stuCenter",
  components: {CourseSelcet, ChangePassword, AvatarEdit, IconPermissions, IconPeople, IconUploadPicture, IconBook},
  setup(_props) {
    const dialogVisible = ref(false)
    const changePwdVisible = ref(false)
    const courseSelectVisible = ref(false)
    const rotated = ref(false)
    const user = useAuthStore().getUser
    const identity = user['identity'] === 'TEACHER' ? '教师' :
                    (user['identity'] === 'STUDENT' ? '学生' :
                     user['identity'] === 'ADMIN' ? '管理员' : '助教')
    const closeAvatarEdits = () => {
      dialogVisible.value = false;
    };
    const closeChangePwd = () => {
      changePwdVisible.value = false;
    };
    const closeCourseSelect = () => {
      courseSelectVisible.value = false;
    };
    const rotateAvatar = () => {
      rotated.value = true;
    };

// Function to reset the rotation on mouse leave
    const resetRotation = () => {
      rotated.value = false;
    };
    const openLogout = () => {
      ElMessageBox.confirm(
        '确认退出当前账号？',
        'Warning',
        {
          confirmButtonText: '是',
          cancelButtonText:'否',
          type:'Warning',
        }
      ).then(() => {
        logout()
      })
    }
    const logout = async () => {
      await user_logout_api().then(res => {
        useAuthStore().logout()
        cookies.removeAll()
        router.push('/login')
      })
    }
    return {
      dialogVisible,
      changePwdVisible,
      courseSelectVisible,
      closeAvatarEdits,
      closeChangePwd,
      closeCourseSelect,
      rotateAvatar,
      resetRotation,
      user,
      identity,
      openLogout
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