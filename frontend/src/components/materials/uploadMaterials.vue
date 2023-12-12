<template>
  <el-upload
   class="upload-demo"
   action="#"
   multiple drag
   :accept="accept"
   :auto-upload="false"
   :limit="limitNum"
   :file-list="fileList"
   :on-exceed="handleExceed"
   :on-remove="handleRemove"
   :on-change="handleChange"
   :before-upload="handleBeforeUpload"
  >
    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
    <div class="el-upload__text">
      Drop file here or <em>click to upload</em>
    </div>
    <template #tip>
      <div class="el-upload__tip">
        支持doc, docx, pdf, ppt, txt, xls, xlsx格式文件；文件大小不超过10M；最多上传{{limitNum}}个文件
      </div>
    </template>
  </el-upload>
  <el-button type="primary" @click="submitUpload"> 上传课程资料 </el-button>
  <el-button type="info" @click="fileList = []"> 取消 </el-button>
</template>

<script lang="ts">

import {ElMessage} from "element-plus";
import {upload_materials_api} from "@/api/api.ts";
import {UploadFilled} from "@element-plus/icons-vue";

export default {
  name: 'uploadMaterials',
  components: {UploadFilled},
  data() {
    return {
      limitNum: 5,
      fileList: [],
      fileType: ['.doc', '.docx', '.pdf', '.ppt', '.txt', '.xls', '.xlsx', '.pptx'],
      accept: '',
    }
  },
  methods: {
    handleExceed(file, uploadFiles) {
      ElMessage.warning('待上传文件数量超出限制，请分批次上传！')
    },
    handleChange(file, uploadFiles) {
        this.fileList = uploadFiles
    },
    handleRemove(file, uploadFiles) {
      this.fileList = uploadFiles
    },
    handleBeforeUpload(file) {
      if (this.fileType) {
        let fileExtension = "";
        if (file.name.lastIndexOf(".") > -1) {
          fileExtension = file.name.slice(file.name.lastIndexOf("."));
        }
        const isTypeOk = this.fileType.some((type) => {
          if (file.type.indexOf(type) > -1) return true;
          return fileExtension && fileExtension.indexOf(type) > -1;

        });
        if (!isTypeOk) {
          ElMessage.error(`文件格式不正确, 请上传${this.fileType.join("/")}格式文件!`);
          return false;
        }
      }
      // 校检文件大小
      if (this.fileSize) {
        const isLt = file.size / 1024 / 1024 < 10;
        if (!isLt) {
          ElMessage.error(`上传文件大小不能超过 10 MB!`);
          return false;
        }
      }
      return true;
    },
    async submitUpload() {
      //判断是否有文件再上传
      if (this.fileList.length === 0) {
        return ElMessage.warning('请选取文件后再上传')
      }
      // 下面的代码将创建一个空的FormData对象:
      const formData = new FormData()
      // 你可以使用FormData.append来添加键/值对到表单里面；
      this.fileList.forEach((file) => {
        formData.append('files', file.raw)
      })
      await upload_materials_api(formData).then(async res => {
        this.fileList = []
        await this.$parent.getMaterials()
      })
    },
  },
  created() {
    this.fileType.forEach(el => {
      this.accept += el + ','
    })
    this.fileType.slice(0, this.fileType.length - 2)
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
