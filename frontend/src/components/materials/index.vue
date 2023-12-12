<template>
  <div v-if="power" class="upload-box">
    <UploadMaterials/>
  </div>
  <div v-for="(item, index) in materialData">
    <div class="material-item">
      <div class="left-section">
        <div class="id">{{ index }}</div>
        <div class="name-time">
          <p class="name">{{ item.name }}</p>
          <p class="upload-time">{{ item.uploadTime }}</p>
        </div>
      </div>
      <div class="right-section">
        <icon-down-load :size="30" style="margin: 20px" @click="download(item.url, item.fileName)" />
        <el-popconfirm
          confirm-button-text="确定"
          cancel-button-text="取消"
          title="确定删除该资料吗？"
          @confirm="handleDelete(item.id)"
          style="margin: 20px"
        >
          <template #reference>
            <el-button v-if="power" type="text"><icon-delete :size="30" style="color:darkred"/></el-button>
          </template>
        </el-popconfirm>
      </div>
    </div>
    <el-divider style="margin: 0; padding: 0"/>
  </div>
</template>
<!--  课程资料页面-->

<script lang="ts">
import UploadMaterials from "@/components/materials/uploadMaterials.vue";
import useAuthStore from "@/store/user.ts";
import {del_material_api, get_materials_api} from "@/api/api.ts";
import {
  Download as IconDownLoad,
  Delete as IconDelete,
} from "@icon-park/vue-next";
import {saveAs} from "file-saver";

export default {
  name: "reference",
  components: {UploadMaterials, IconDownLoad, IconDelete},
  data() {
    return {
      materialData: [{
        id: 1,
        name: 'test',
        uploadTime: '2021-06-01',
        fileName: '2.png',
        url: "http://127.0.0.1:8000/media/avatars/2.png",
      },
      {
        id: 2,
        name: '2023词法分析辅助库',
        uploadTime: '2021-06-02',
        fileName: '2.png',
        url: "http://127.0.0.1:8000/media/avatars/2.png",
      }]
    }
  },
  methods: {
    download(fileUrl, fileName) {
      saveAs(fileUrl, fileName)
    },
    async getMaterials() {
      await get_materials_api().then(res => {
        this.materialData = res.data
      })
    },
    async handleDelete(id) {
      await del_material_api(id).then(res => {
        this.getMaterials()
      })
    }
  },
  computed: {
    power() {
      const use = useAuthStore()
      return use.getUser['identity'] === 'ADMIN' || use.getUser['identity'] === 'TEACHER' || use.getUser['identity'] === 'ASSISTANT'
    }
  },
  mounted() {

  }
}
</script>

<style lang="scss" scoped>
.upload-box {
  border-radius: 4px;
  padding: 30px;
  border: 1px solid var(--el-border-color);
  box-shadow: 12px 12px 2px 1px rgba(0, 0, 0, .2);
}
.material-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
}

.left-section {
  display: flex;
  align-items: center;
}

.id {
  font-family: "Microsoft YaHei",cursive;
  font-size: 24px;
  font-weight: bold;
  padding: 0;
  margin: 0 20px 0 20px;
}
.name {
  font-family: "Microsoft YaHei",cursive;
  font-size: 18px;
  font-weight: bold;
  padding: 0;
  margin: 10px 0 0 0;
  text-align: left;
}
.upload-time {
  font-family: "Times New Roman", Times, serif;
  font-size: 14px;
  color: gray;
  padding: 0;
  margin: 0 0 10px 0;
  text-align: left;
}
.name-time {
  display: flex;
  flex-direction: column;
}

.right-section {
  display: flex;
  text-align: right;
  align-items: center;
}
</style>
