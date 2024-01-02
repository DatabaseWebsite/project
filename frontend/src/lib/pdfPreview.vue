<template>
  <vue-office-pdf :src="pdf" @rendered="rendered"/>
</template>

<script lang="ts">
//引入VueOfficePdf组件
import VueOfficePdf from '@vue-office/pdf'

export default {
  name: "pdfPreview",
  components:{ VueOfficePdf },
  props:{
    pdf:{
      type:String,
      required:true
    }
  },
  methods:{
    rendered(){
      console.log("渲染完成")
    }
  }
}
</script>