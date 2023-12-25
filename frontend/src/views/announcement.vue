<template>
  
  <el-button type="primary" class="create-button" @click = "CreateVisible=true">新建公告</el-button>
  <el-timeline>
    <el-timeline-item
      v-for="(item, index) in arr2"
      :timestamp="displayTime(item.create_time)"
      placement="top" class="timeline-item"
    >
      <el-collapse v-model="activeID" accordion>
        <el-collapse-item :name="index">
          <template #title>
            <div class="header">
              
              <span style="font-size: 18px; font-weight: bold;display: flex; align-items: center;">{{item.title}}</span>
                
              <div v-if="identity" style="display: flex; margin-left: 3vw; align-items: center;">
                <icon-edit :size="20" style="margin-right: 2vw; color: cornflowerblue" @click.stop="handleEdit(item)"/>
                <icon-delete :size="20" style="color: cornflowerblue" @click.stop="confirmDelete(item)"/>
              </div> 
            </div>
          </template>
          <div style="margin: 5px; border-radius: 10px; box-shadow: rgba(0, 0, 0, 0.02) 0px 1px 3px 0px, rgba(27, 31, 35, 0.15) 0px 0px 0px 1px;">
            <md-preview :text="item.content"/>
          </div>
        </el-collapse-item>
      </el-collapse>
    </el-timeline-item>
  </el-timeline>
  <el-dialog v-model="editVisible" title="编辑公告" width="70%">
    <div>
      <span style="font-size: 18px; font-weight: bold;">标题</span>
      <el-input v-model="editItem['title']" placeholder="请输入标题" style="margin-bottom: 10px;"/>
    </div>
    <md-editor v-model="editItem['content']"/>
    <div style="margin-top: 3vh">
      <el-button type="primary" @click="submitEdit">确认修改</el-button>
    </div>
  </el-dialog>
  <el-dialog v-model="CreateVisible" title="新建公告" width="70%">
    <div>
      <span style="font-size: 18px; font-weight: bold;">标题</span>
      <el-input v-model="createItem['title']" placeholder="请输入标题" style="margin-bottom: 10px;"/>
    </div>
    <md-editor v-model="createItem['content']"/>
    <div style="margin-top: 3vh">
      <el-button type="primary" @click="submitCreate">确认新建</el-button>
    </div>
  </el-dialog>
</template>

<script lang="ts">
import {
  Edit as IconEdit,
  Delete as IconDelete,
} from "@icon-park/vue-next";
import announceForm from "@/components/announce/announceForm.vue";
import MdPreview from "@/components/markdown/mdPreview.vue";
import useAuthStore from "@/store/user.ts";
import MdEditor from "@/components/markdown/mdEditor.vue";
import { ElMessageBox } from 'element-plus';
import {create_notice_api,delete_notice_api,notice_list_api} from '@/api/api.ts';
export default {
  name: "announcement",
  components: {MdEditor, MdPreview, announceForm, IconEdit, IconDelete},
  data() {
    return {
      arr2:[],
      text: '',
      activeID: 0,
      editVisible: false,
      CreateVisible : false,
      editItem: {},
      createItem:{}
    }
  },
  mounted() {
      console.log("mounted start");
      this.loadNotices();
  },
  methods: {
    
    identity() {
      const user = useAuthStore()
      return user.getUser['identify'] !== 'STUDENT'
    },
    course_id() {
      const user = useAuthStore()
      return user.getUser['course_id'];
    },
    displayTime(dateStr: String) {
      const date = new Date(dateStr);
      console.log(date.toLocaleString('zh-CN', {
    hour12: false,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  }).replaceAll('/', '-'))
  return date.toLocaleString('zh-CN', {
    hour12: false,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  }).replaceAll('/', '-');
    },
    submitEdit() {
      // TODO AWAIT EDIT()
      this.editVisible=false; 
    },
    async submitCreate() {
      console.log("submit enter",this.createItem['title'],this.createItem['content']);
      await create_notice_api(this.createItem['title'],this.createItem['content']);
      this.createVisible=false; 
      this.loadNotices();
    },
    handleEdit(item) {
      this.editVisible=true; 
      this.editItem = item;
    },
    confirmDelete(item) {
      ElMessageBox.confirm(
        '确认要删除这条信息么',
        '提示',
        {
          confirmButtonText: '确认',
          cancelButtonText: '取消',
          type: 'warning',
        }
      ).then(() => {
        this.handleDelete(item);
      }).catch(() => {
        // 处理取消操作或关闭 MessageBox
      });
    },
    async handleDelete(item) {
      try {
        console.log('信息已删除', item.id);
        await delete_notice_api(item.notice_id);
        //this.arr2 = this.arr2.filter((post) => post.id !== item.id);
      } catch (error) {
        console.error('删除信息失败', error);
      }
    },
    async loadNotices() {
      console.log("loadNotices start");
      try {
        const response = await notice_list_api();
        console.log("loadNotices success",response);
        this.arr2 = response.data.result  ; // Assuming the API response structure
      } catch (error) {
        console.error('Failed to load notices:', error);
      }
    },
  }
}
</script>

<style scoped>
.create-button {
  position: fixed;
  top:  80px;
  right:80px;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.timeline-item{
  margin-top: 10px;
}
</style>