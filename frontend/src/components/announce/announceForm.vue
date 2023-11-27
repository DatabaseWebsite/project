<template>
  <el-card class="box-card">
    <template #header>
      <div class="card-header">
        <span> {{ item.title }}
        </span>
        <el-button class="button" text>Operation button</el-button>
      </div>
    </template>
    
    <div class="text item">
      {{ item.content }}
    </div>
  </el-card>
</template>

<script lang="ts">


export default {
  name: 'announceForm',
  props: {
    item: Object
  
  },
  data() {
    return {
      
      text: '',
      ritem: ''
    }
  },
  mounted() {
    // 在生命周期钩子中更新子组件的数据
    
    this.ritem = this.item;
  },
  methods: {
    submit() {

    }
  }
  
};
</script>
<style scoped>
/* form */
/*:deep(.el-form-item__label)  {*/
/*  color: white; !* 设置字体颜色为白色 *!*/
/*}*/
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
  width: 1500px;
}
</style>