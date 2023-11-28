<template>
    <el-container class="card-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span> {{ item.course_id }}
          </span>
          <el-button class="button" text>Operation button</el-button>
        </div>
      </template>
      
      <div class="text item">
        {{ item.name }}
      </div>
    </el-card>
    </el-container>
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
  .card-container{
    display: flex;
    justify-content: center;
    align-items: center;
  }
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
    width: 90%;
    padding:5px;
    margin:10px;
  }
  </style>