<template>
  <el-upload
   action="#"
   drag
   accept=".xls,.xlsx"
   :auto-upload="false"
   :limit="1"
   :file-list="file"
   :on-change="handleChange"
  >
    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
    <div class="el-upload__text">
      Drop file here or <em>click to upload</em>
    </div>
    <template #tip>
      <div class="el-upload__tip">
        支持xls、xlsx格式文件；文件大小不超过10M；excel内容按列依次为：学号、姓名，不需要表头，密码默认为学号
      </div>
    </template>
  </el-upload>
</template>

<script lang="ts">

import {ElMessage} from "element-plus";
import {UploadFilled} from "@element-plus/icons-vue";

export default {
  name: 'uploadFile',
  components: {UploadFilled},
  data() {
    return {
      file: []
    }
  },
  methods: {
    handleChange(uploadFile) {
      const isLt10M = uploadFile.size / 1024 / 1024 < 10
      if (!isLt10M) {
        ElMessage.error('上传文件大小不能超过 10MB！')
        return;
      }
      this.file = uploadFile
      this.$emit('file-uploaded', uploadFile);
    },
  }
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
