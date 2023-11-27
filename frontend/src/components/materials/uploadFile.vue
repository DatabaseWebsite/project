<template>
  <el-upload
   class="upload-demo"
   action="#"
   multiple drag
   accept=".doc,.docx,.pdf,.ppt"
   :auto-upload="false"
   :limit="limitNum"
   :file-list="fileList"
   :on-exceed="handleExceed"
   :on-remove="handleRemove"
   :on-change="handleChange"
  >
    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
    <div class="el-upload__text">
      Drop file here or <em>click to upload</em>
    </div>
    <template #tip>
      <div class="el-upload__tip">
        支持doc, docx, pdf, ppt格式文件；文件大小不超过10M；最多上传{{limitNum}}个文件
      </div>
    </template>
  </el-upload>
  <el-button class="ml-3" type="primary" @click="submitUpload"> 上传课程资料 </el-button>
</template>

<script lang="ts">

import {ElMessage} from "element-plus";
import useAuthStore from "@/store/user.ts";
import {upload_materials_api} from "@/api/api.ts";
import {UploadFilled} from "@element-plus/icons-vue";

export default {
  name: 'uploadFile',
  components: {UploadFilled},
  data() {
    return {
      limitNum: 5,
      fileList: []
    }
  },
  methods: {
    handleExceed(file, uploadFiles) {
      ElMessage.warning('待上传文件数量超出限制，请分批次上传！')
    },
    handleChange(file, uploadFiles) {
      console.log(file.name)
      const isLt10M = file.size / 1024 / 1024 < 10
      if (!isLt10M) {
        ElMessage.error('上传文件大小不能超过 10MB！')
        return;
      }
      this.fileList = uploadFiles
    },
    handleRemove(file, uploadFiles) {
      this.fileList = uploadFiles
    },
    async submitUpload() {
      //判断是否有文件再上传
      if (this.fileList.length === 0) {
        return this.$message.warning('请选取文件后再上传')
      }
      // 下面的代码将创建一个空的FormData对象:
      const formData = new FormData()
      // 你可以使用FormData.append来添加键/值对到表单里面；
      this.fileList.forEach((file) => {
        formData.append(file.name, file.raw)
      })
      await upload_materials_api(formData).then(async res => {
        this.fileList = []
        await this.$parent.updateMaterials()
      })
    },
  },
}
</script>
<style lang="scss" scoped>
.previewDownload {
  margin-top: 80px;
  margin-left: 50px;
  display: flex;
  flex-direction: column;
}
</style>
