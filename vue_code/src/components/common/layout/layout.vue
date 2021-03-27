<template>
  <div class="layout">
    <template v-if="!$route.meta.noLayout">
      <PageHeader ></PageHeader>
      <TagsBar></TagsBar>
      <div class="layout__main">
        <router-view></router-view>
      </div>
    </template>
    <template v-else>
        <router-view></router-view>
    </template>
  </div>
</template>

<script>

export default {
  components: {
    PageHeader: () => import('@/components/layout/PageHeader/index'),
    TagsBar: () => import('@/components/layout/TagsBar/index')
  },
  data () {
    return {}
  }
}
</script>
<style lang="scss" scoped>
.layout{
  height: 100vh;
  &__main{
    padding: 23px 45px 0 45px;
  }
}
</style>
