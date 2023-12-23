<template>
  <el-timeline>
    <el-timeline-item
      v-for="(item, index) in arr2"
      :timestamp="displayTime(item.date)"
      placement="top"
    >
      <el-collapse v-model="activeID" accordion>
        <el-collapse-item :name="index">
          <template #title>
            <div class="header">
              <span style="font-size: 18px; font-weight: bold;display: flex; align-items: center;">{{item.title}}</span>
              <div v-if="identity" style="display: flex; margin-left: 3vw; align-items: center;">
                <icon-edit :size="20" style="margin-right: 2vw; color: cornflowerblue" @click.stop="editVisible=true; handleEdit(item)"/>
                <icon-delete :size="20" style="color: cornflowerblue" @click.stop="handleDelete(item)"/>
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
      <el-button type="primary" @click="submit">确认修改</el-button>
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
export default {
  name: "announcement",
  components: {MdEditor, MdPreview, announceForm, IconEdit, IconDelete},
  data() {
    return {
      arr2:[
          {title:'gaosj', date: new Date(), content:'hello'},
          {title:'bianyc', date: new Date(), content:'good'},
          {title:'chengqj', date: new Date(), content:'great'}
      ],
      text: '',
      activeID: 0,
      editVisible: false,
      editItem: {},
    }
  },
  methods: {
    identity() {
      const user = useAuthStore()
      return user.getUser['identify'] !== 'STUDENT'
    },
    displayTime(date: Date) {
      return date.toLocaleString().replaceAll('/', '-')
    },
    submit() {

    },
    handleEdit(item) {
      this.editItem = item;
    },
    handleDelete(item) {

    }
  }
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>