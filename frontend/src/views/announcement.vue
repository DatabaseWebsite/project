<template>
    <div>
        <announceForm v-for="(item, index) in arr2" :item =item>

        </announceForm>
    </div>
    <div>
    <ul>
      <li v-for="(item, index) in arr2" :key="index">
        <announceForm title={{item}} content="hello">

        </announceForm>
      </li>
    </ul>
  </div>
</template>
  
<script>

  import announceForm from "@/components/announce/announceForm.vue";
  export default {
    name: "announcement",
    components: {announceForm},
    data() {
      return {
        arr2:[
            {title:'gaosj',content:'hello'},
            {title:'bianyc',content:'good'},
            {title:'chengqj',content:'great'}
        ],
        text: '',
      }
    },
    methods: {
      submit() {
  
      }
    }
  }
  </script>
  
  <style scoped>
  
  </style>