<template>
  <el-upload
    class="upload-demo"
    action="#"
    drag
    :accept="accept"
    :auto-upload="false"
    :limit='1'
    :file-list="submitFile"
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
        支持{{accept}}格式文件；文件大小不超过{{fileSize}}M；单文件
      </div>
    </template>
  </el-upload>
</template>

<script lang="ts">
import {UploadFilled} from "@element-plus/icons-vue";
import {ElMessage} from "element-plus";

export default {
  name: "uploadFile",
  components: {UploadFilled},
  props: {
    fileType: {
      type: Array,
      default: () => ['.doc', '.docx', '.pdf', '.ppt', '.txt', '.xls','.xlsx', '.zip', '.rar'],
    },
    fileSize: {
      type: Number,
      default: () => 20,
    },
    submitFile: {
      default: []
    }
  },
  data() {
    return {
      accept: '',
    }
  },
  methods: {
    handleExceed() {
      ElMessage.warning('待上传文件数量超出限制，请分批次上传！')
    },
    handleChange(file, uploadFiles) {
      this.$emit('update:submitFile', uploadFiles)
    },
    handleRemove() {
      this.$emit('update:submitFile', '')
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
        const isLt = file.size / 1024 / 1024 < this.fileSize;
        if (!isLt) {
          ElMessage.error(`上传文件大小不能超过 ${this.fileSize} MB!`);
          return false;
        }
      }
      return true;
    }
  },
  created() {
    this.fileType.forEach(el => {
      this.accept += el + ','
    })
    this.fileType.slice(0, this.fileType.length - 2)
  }
}
</script>

<style scoped>

</style>