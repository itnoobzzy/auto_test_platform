<template>
  <svg aria-hidden="true" class="el-icon-normal svg-icon" v-on="$listeners">
    <use :xlink:href="iconType" />
  </svg>
</template>

<script>
export default {
  name: 'SvgIcon',
  props: {
    type: {
      type: String,
      required: true
    }
  },
  computed: {
    iconType () {
      return `#icon-${this.type}`
    }
  }
}
</script>

<style>
.svg-icon {
  width: 1em;
  height: 1em;
  fill: currentColor;
  overflow: hidden;
  vertical-align: middle;
}
</style>
