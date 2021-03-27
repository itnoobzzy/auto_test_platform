<template>
  <div class="card" :style="{height:height,marginTop:`${marginT}px`}">
      <h2 class="card__title">
        <p>{{ title }}</p>
        <slot name='extral'></slot>
      </h2>
      <slot name='body'></slot>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String
    },
    height: {
      type: String
    },
    marginT: {
      type: String
    }
  },
  data () {
    return {
    }
  }
}
</script>
<style lang="scss" scoped>
.card{
    padding: 5px 23px;
    background: #fff;
    border-radius: 9px;
    &__title{
        display: flex;
        align-items: center;
        justify-content: space-between;
        p{
          font-weight: normal;
          color: #222222;
          font-size: 18px;
          padding-left: 6px;
          line-height: 1;
          border-left: 3px solid #2e58f7;
        }
    }
}
</style>
