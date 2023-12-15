<template>
    <div class="create-post-container">
      <form @submit.prevent="createPost" class="create-post-form">
        <div class="form-group">
          <input v-model="newPost.title" placeholder="标题" class="title-input" />
        </div>
        <div class="form-group">
          <md-editor v-model="newPost.content" placeholder="内容"></md-editor>
        </div>
        <button type="submit" class="submit-btn">发布</button>
      </form>
      <button @click="close" class="close-btn">关闭</button>
    </div>
  </template>
  <script>
  
  
  import MdEditor from "@/components/markdown/mdEditor.vue";
  export default {
    components: {
      MdEditor
    },
    data() {
      return {
        newPost: {
          title: '',
          content: '',
          author: 'gsj', 
          timestamp: null
        }
      };
    },
    methods: {
      createPost() {
        //API NEED
        console.log('POST CREATED', this.newPost);
  
        
        this.newPost.title = '';
        this.newPost.content = '';
        this.$emit('close');
      },
      close() {
        this.$emit('close');
      }
    }
  };
  </script>
  <style scoped>
  .create-post-container {
    padding: 20px;
    background: #f9f9f9;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  .create-post-form .form-group {
    margin-bottom: 20px;
  }
  
  .title-input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .submit-btn, .close-btn {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-right: 10px;
  }
  
  .submit-btn {
    background-color: #4CAF50;
    color: white;
  }
  
  .close-btn {
    background-color: #f44336;
    color: white;
  }
  </style>