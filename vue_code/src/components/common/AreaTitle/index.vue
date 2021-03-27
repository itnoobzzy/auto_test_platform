<template>
    <div class="panel_title">{{ title }}</div>
</template>
<script>
export default {
  data () {
    return {
      data1: []
    }
  },
  props: {
    title: {
      type: String
    }
  },
  methods: {}
}
</script>
<style lang="scss" scoped>
.panel_title{
  font-size: 16px;
  color: #222;
  padding-left: 5px;
  line-height: 1;
  border-left: 3px solid #2e58f7;;
}
</style>
