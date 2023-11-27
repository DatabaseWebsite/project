<template>
  <div v-if="canUpload" class="upload-box">
    <UploadFile/>
  </div>
  <div v-for="(item) in materialData">
    <div class="material-item">
      <div class="left-section">
        <div class="id">{{ item.id }}</div>
        <div class="name-time">
          <p class="name">{{ item.name }}</p>
          <p class="upload-time">{{ item.uploadTime }}</p>
        </div>
      </div>
      <div class="right-section">
        <icon-down-load :size="30" @click="download(item.url, item.name)" />
      </div>
    </div>
    <el-divider style="margin: 0; padding: 0"/>
  </div>
</template>
<!--  课程资料页面-->

<script lang="ts">
import UploadFile from "@/components/materials/uploadFile.vue";
import useAuthStore from "@/store/user.ts";
import {computed, inject, onMounted, reactive, ref, toRefs} from "vue";
import {get_materials_api} from "@/api/api.ts";
import {
  Download as IconDownLoad,
} from "@icon-park/vue-next";

export default {
  name: "reference",
  components: {UploadFile, IconDownLoad},
  methods: {
    download(fileUrl, fileName) {
      const a = document.createElement('a')
      a.href = fileUrl
      a.download = fileName
      a.style.display = 'none'
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
    }
  },
  setup(_props) {
    const use = useAuthStore()
    const canUpload = ref(computed(() => {
      console.log(use.getUser['identity'])
      return use.getUser['identity'] === 'TEACHER' || use.getUser['identity'] === 'ASSISTANT'
    }))

    // interface MaterialItem {
    //   name: string,
    //   uploadTime: string
    //   url: string
    // }
    const materialData = reactive<Record<string, Record<string, string>>>({
      '1': {
        id: '1',
        name: 'test',
        uploadTime: '2021-06-01',
        url: '',
      },
      '2': {
        id: '2',
        name: '2023词法分析辅助库',
        uploadTime: '2021-06-02',
        url: '',
      },
      '3': {
        id: '2',
        name: '2023词法分析辅助库',
        uploadTime: '2021-06-02',
        url: '',
      },
      '4': {
        id: '2',
        name: '2023词法分析辅助库',
        uploadTime: '2021-06-02',
        url: '',
      },
      '5': {
        id: '2',
        name: '2023词法分析辅助库',
        uploadTime: '2021-06-02',
        url: '',
      },
      '6': {
        id: '2',
        name: '2023词法分析辅助库',
        uploadTime: '2021-06-02',
        url: '',
      }
    })
    const materialDataRef = ref(toRefs(materialData))
    const updateMaterials = async () => {
      let res = await get_materials_api()
      materialData.value = res.data
    }
    onMounted(async () => {
      console.log('mounted')
      // await updateMaterials()
    })
    return {
      canUpload,
      materialData,
      updateMaterials
    }
  },
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
  text-align: right;
}
</style>
