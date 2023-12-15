<template>
  <el-container class="card-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span> {{ item.title }}</span>
          <el-button v-if="isTeacherOrAssistant" class="button" text @click="showOperationDialog = true">Operation button</el-button>
        </div>
      </template>
      
      <div class="text item">
        {{ item.content }}
      </div>
    </el-card>

    <el-dialog v-model="showOperationDialog" title="操作" width="60%">
      <div>
        <el-button type="danger" @click="deleteAnnounce">删除公告</el-button>
        <el-button type="primary" @click="editAnnounce">编辑公告</el-button>
      </div>
    </el-dialog>

    <el-button class="create-announce-btn" type="primary" @click="createAnnounceVisible = true">新建公告</el-button>

    <el-dialog v-model="createAnnounceVisible" title="新建公告" width="60%">
      <md-editor v-model="newAnnounceContent"></md-editor>
      <span slot="footer" class="dialog-footer">
        <el-button @click="createAnnounceVisible = false">取消</el-button>
        <el-button type="primary" @click="createAnnounce">创建公告</el-button>
      </span>
    </el-dialog>
    <el-dialog v-model="editAnnounceVisible" title="编辑公告" width="60%">
      <md-editor v-model="editAnnounceContent"></md-editor>
        <span slot="footer" class="dialog-footer">
          <el-button @click="editAnnounceVisible = false">取消</el-button>
          <el-button type="primary" @click="submitEditAnnounce">保存编辑</el-button>
        </span>
    </el-dialog>

  <!-- 删除公告确认对话框 -->
    <el-dialog v-model="deleteAnnounceVisible" title="确认删除" width="30%">
      <span>确定要删除这条公告吗？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteAnnounceVisible = false">取消</el-button>
        <el-button type="primary" @click="submitDeleteAnnounce">确认删除</el-button>
      </span>
    </el-dialog>
  </el-container>
</template>

<script lang="ts">
import { ref, defineProps } from 'vue';
import useAuthStore from "@/store/user.ts";  
export default {
  name: 'announceForm',
  props: {
    item: Object
  },
  data() {
    return {
      text: '',
      ritem: '',
      isTeacherOrAssistant: false, // 用户身份标识
      showOperationDialog: false, // 操作对话框显示状态
      createAnnounceVisible: false, // 新建公告对话框显示状态
      newAnnounceContent: '', // 新建公告内容
      editAnnounceVisible: false,
      deleteAnnounceVisible: false,
      editAnnounceContent: '',
      // 假设每个公告都有一个唯一的ID
      editingAnnounceId: null
    };
  },
  mounted() {
    this.ritem = this.item;
    // 假设有方法来判断当前用户是否为老师或助教
    const use = useAuthStore();
    
    this.isTeacherOrAssistant = use.getUser['identity'] === 'TEACHER' || use.getUser['identity'] === 'ASSISTANT' || use.getUser['identity'] === 'ADMIN' ;
    console.log("mounted", this.isTeacherOrAssistant,use.getUser['identity']);
  },
  methods: {
    editAnnounce() {
      this.editAnnounceVisible = true;
      this.editAnnounceContent = this.item.content; // 假设每个公告项都有content属性
      this.editingAnnounceId = this.item.id; // 假设每个公告项都有id属性
    },

    submitEditAnnounce() {
      console.log('编辑内容:', this.editAnnounceContent);
      // 在这里调用API来更新公告内容
      // 示例：updateAnnounceAPI(this.editingAnnounceId, this.editAnnounceContent);
      this.editAnnounceVisible = false;
    },

    deleteAnnounce() {
      this.deleteAnnounceVisible = true;
      this.editingAnnounceId = this.item.id;
    },

    submitDeleteAnnounce() {
      console.log('删除公告ID:', this.editingAnnounceId);
      // 在这里调用API来删除公告
      // 示例：deleteAnnounceAPI(this.editingAnnounceId);
      this.deleteAnnounceVisible = false;
    },

    createAnnounce() {
      console.log('新建公告内容:', this.newAnnounceContent);
      // 在这里调用API来创建新的公告
      // 示例：createAnnounceAPI(this.newAnnounceContent);
      this.createAnnounceVisible = false;
    }
  }
};
</script> 

<style scoped>
.card-container {
  display: flex;
  justify-content: center;
  align-items: center;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.text {
  font-size: 14px;
}
.item {
  margin-bottom: 18px;
}
.box-card {
  width: 90%;
  padding: 5px;
  margin: 10px;
}
.create-announce-btn {
  position: absolute;
  top: 10px;
  right: 10px;
}
</style>