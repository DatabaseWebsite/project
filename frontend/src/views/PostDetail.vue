<template>
    <div class="post-detail">
      <h2>{{ post.title }}</h2>
      <div class="post-meta">
        <span class="author">作者: {{ post.author }}</span>
        <span class="timestamp">{{ formatTimestamp(post.timestamp) }}</span>
      </div>
      <p>{{ post.content }}</p>
      <h3>回复:</h3>
      <div class="replies">
        <div v-for="reply in replies" :key="reply.id" class="reply">
          <div class="author">{{ reply.author }}</div>
          <div class="timestamp">{{ formatTimestamp(reply.timestamp) }}</div>
          <div class="content">{{ reply.content }}</div>
          <div v-if="reply.mentioned" class="mentioned">@{{ reply.mentioned }}</div>
        </div>
      </div>
    </div>
  </template>

<script>
export default {
  data() {
    return {
      post: {},
      replies: []
    };
  },
  created() {
    
    this.loadPost(this.$route.params.id); //API _ FUNCTION
  },
  methods: {
    formatTimestamp(timestamp) {
      return new Date(timestamp).toLocaleString();
    },
    loadPost(postId) {
      //API _ FUNCTION
      const data = {
        1: {
          title: 'database',
          content: 'too hard for me',
          author: 'gsj',
          timestamp: new Date('2023-01-01 10:00:00'),
          replies: [
            { id: 1, author: 'byc', timestamp: new Date(), content: 'too cai', mentioned: 'gsj' },
            
          ]
        },
        2: {
          title: 'compile',
          content: 'too ez',
          author: 'byc',
          timestamp: new Date('2023-01-02 11:00:00'),
          replies: [
            { id: 2, author: 'gsj', timestamp: new Date(), content: '666' },
            
          ]
        }
      };

      this.post = data[postId] || {};
      this.replies = this.post.replies || [];
    }
  }
};
</script>

<style scoped>
.post-detail {
  margin: 20px;
  padding: 20px;
  border: 1px solid #eee;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.post-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.author, .timestamp {
  color: #555;
  font-size: 0.9em;
}

.replies .reply {
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 4px;
}

.content {
  margin-top: 10px;
}

.mentioned {
  color: blue;
  font-style: italic;
}
</style>