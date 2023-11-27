<template>
  <el-dialog
    title="编辑头像"
    :model-value="dialogVisible"
    :show-close="false"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    width="600px"
  >
    <div style="display: flex" class="avatar">
      <div class="avatar-left">
        <div v-show="!options.img">
          <el-upload
            ref="upload"
            action=""
            style="text-align: center;margin-bottom: 24px"
            :on-change="uploads"
            accept="image/png, image/jpeg, image/jpg"
            :show-file-list="false"
            :auto-upload="false">
            <el-button slot="trigger" size="small" type="primary" ref="uploadBtn">选择图片</el-button>
          </el-upload>
          <div>支持jpg、png格式的图片，大小不超过2M</div>
        </div>
        <div v-show="options.img" class="avatar-left-crop">
          <vueCropper
            class="crop-box"
            ref="cropper"
            :img="options.img"
            :can-scale="options.canScale"
            :autoCrop="options.autoCrop"
            :autoCropWidth="options.autoCropWidth"
            :autoCropHeight="options.autoCropHeight"
            :fixed="options.fixed"
            :fixed-number="options.fixedNumber"
            :fixedBox="options.fixedBox"
            :can-move="options.canMove"
            :canMoveBox="options.canMoveBox"
            :centerBox="options.centerBox"
            style="background-image:none"
            @realTime="realTime">
          </vueCropper>
          <p class="avatar-left-p">
            鼠标滚轮缩放控制图片显示大小，鼠标拖拽调整显示位置</p>
        </div>
      </div>
      <div class="avatar-right">
        <div class="avatar-right-div" v-for="item in previewsDiv" :style="item.style">
          <div v-show="options.img" :class="previews.div" class="avatar-right-previews" :style="item.zoomStyle">
            <img :src="previews.url" :style="previews.img">
          </div>
        </div>
        <div class="avatar-right-text">
          <el-button v-if="options.img" type="text" @click="uploadPreviews">重新上传</el-button>
          <span v-else>预览</span>
        </div>
      </div>
    </div>
    <span slot="footer" class="dialog-footer">
    <el-button @click="closeDialog">取 消</el-button>
    <el-button type="primary" @click="getCrop">确 定</el-button>
    </span>
  </el-dialog>
</template>

<script lang="ts">
import 'vue-cropper/dist/index.css' // 引入该样式才能显示截图框
import { VueCropper } from 'vue-cropper'
import {ElMessage} from "element-plus";
import {user_update_avatar_api} from "@/api/api.ts";
import useAuthStore from "@/store/user.ts";
export default {
  name: "avatarEdit",
  props: {
    dialogVisible: {
      type: Boolean,
      default: false
    }
  },
  components:{
    VueCropper
  },
  data() {
    return {
      //vueCropper组件 裁剪配置信息
      options: {
        img: '',  //原图文件
        canScale: true,  //图片允许滚轮缩放
        autoCrop: true,  //默认生成截图框
        autoCropWidth: 200,  //截图框宽度
        autoCropHeight: 200, //截图框高度
        fixed: true,  //固定截图框大小
        fixedNumber: [1, 1], //截图框的宽高比例
        fixedBox: true,      //固定截图框大小，不允许改变
        canMove: false,      //上传图片不可以移动
        canMoveBox: true,    //截图框能拖动
        centerBox: true,    //截图框被限制在图片里面
      },
      //实时预览图数据
      previews: {},
      //实时预览图样式
      previewsDiv: [
        //108px 预览样式
        {
          style: {
            width: '108px',
            height: '108px',
            margin: '0 auto'
          },
          zoomStyle: {
            zoom: 0.54
          }
        },
        //68px 预览样式
        {
          style: {
            width: '68px',
            height: '68px',
            margin: '27px auto'
          },
          zoomStyle: {
            zoom: 0.34
          }
        },
        //48px 预览样式
        {
          style: {
            width: '48px',
            height: '48px',
            margin: '0 auto'
          },
          zoomStyle: {
            zoom: 0.24
          }
        }
      ],
    }
  },

  methods: {
    //读取原图
    uploads(file) {
      const isIMAGE = file.raw.type === 'image/jpeg' || file.raw.type === 'image/png';
      const isLt2M = file.raw.size / 1024 / 1024 < 2;
      if (!isIMAGE) {
        ElMessage.warning("请选择 jpg、png 格式的图片" );
        return false;
      }
      if (!isLt2M) {
        ElMessage.warning("图片大小不能超过 2MB" );
        return false;
      }
      let reader = new FileReader();
      reader.readAsDataURL(file.raw);
      reader.onload = e => {
        this.options.img = e.target.result //base64
      }
    },
    //实时预览数据
    realTime(data) {
      this.previews = data
    },
    //重新上传
    uploadPreviews() {
      this.$refs.uploadBtn.$el.click()
    },
    //获取截图信息
    getCrop() {
      // 获取截图的 base64 数据
      // this.$refs.cropper.getCropData((data) => {
      //   console.log(data)
      // })
      // 获取截图的 blob 数据
      this.$refs.cropper.getCropBlob(async (data) => {
        const formData = new FormData()
        formData.append('avatar', data)
        await user_update_avatar_api(formData).then(res => {
          useAuthStore().setAvatar(res.data.url)
          console.log(res.data.url)
          location.reload()
          this.closeDialog()
        })
      })
    },
    //关闭弹框
    closeDialog() {
      //调用父组件关闭弹框方法 closeAvatarEdits()
      this.$parent.closeAvatarEdits()
      //重置 data 数据。(Object.assign是对象深复制  this.$data是组件内的数据对象 this.$options.data()是原始的数据)
      Object.assign(this.$data, this.$options.data())
    },
  }
}
</script>

<style lang="scss" scoped>

:deep(.el-dialog__header) {
  padding: 24px 0 11px 28px;
}

:deep(.el-dialog__title) {
  color: #333333;
}

:deep(.el-dialog__body) {
  padding: 0 28px;
}

:deep(.el-dialog__footer) {
  padding: 20px 28px;

  .el-button {
    width: 145px;
  }
}

.avatar {
  display: flex;

  .avatar-left {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 400px;
    height: 400px;
    background-color: #F0F2F5;
    margin-right: 10px;
    border-radius: 4px;

    .avatar-left-crop {
      width: 400px;
      height: 400px;
      position: relative;

      .crop-box {
        width: 100%;
        height: 100%;
        border-radius: 4px;
        overflow: hidden
      }

    }

    .avatar-left-p {
      text-align: center;
      width: 100%;
      position: absolute;
      bottom: 20px;
      color: #ffffff;
      font-size: 14px;
    }
  }

  .avatar-right {
    width: 150px;
    height: 400px;
    background-color: #F0F2F5;
    border-radius: 4px;
    padding: 16px 0;
    box-sizing: border-box;

    .avatar-right-div {
      border: 3px solid #ffffff;
      border-radius: 50%;
    }

    .avatar-right-previews {
      width: 200px;
      height: 200px;
      overflow: hidden;
      border-radius: 50%;
    }

    .avatar-right-text {
      text-align: center;
      margin-top: 50px;
      font-size: 14px;

      :deep(.el-button) {
        padding: 0;
      }

      span {
        color: #666666;
      }
    }
  }
}

</style>

