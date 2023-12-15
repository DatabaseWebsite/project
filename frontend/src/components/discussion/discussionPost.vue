<template>
    <div @click="onClickPost" class="post-item">
      <h3>{{ post.title }}</h3>
      <p>{{ post.summary }}</p>
      <div>作者：{{ post.author }}</div>
      <div>发布时间：{{ post.timestamp }}</div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      post: Object
    },
    methods: {
      onClickPost() {
        this.$emit('click');
      }
    }
  };
  </script>
  
  <style scoped>
  .post-item {
    cursor: pointer;
  }
  
  .post-item h3 {
    margin-top: 0;
  }
  </style>