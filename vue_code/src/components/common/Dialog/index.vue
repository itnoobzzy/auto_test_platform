<template>
  <div class="dialog">
    <el-dialog :visible.sync="visible_flag" :top='top' :modal='modal' :width='`${dialog_width}px`' @close='closeDialog' :show-close='!!title'>
      <template slot="title">
        <div class="dialog__title" v-if="title">
          <AreaTitle :title="dialog_title" ></AreaTitle>
        </div>
        <div v-if="messageTitle" class="dialog__message_title">
          {{ messageTitle }}
        </div>
      </template>
      <div class="dialog__body">
        <slot name="con"></slot>
      </div>
      <template slot="footer">
        <slot name="footer"></slot>
      </template>
    </el-dialog>
  </div>
</template>
<script>
export default {
  props: {
    title: {
      type: String
    },
    visible: {
      type: Boolean,
      default: false
    },
    width: {
      type: String
    },
    messageTitle: {
      type: String
    },
    modal: {
      default: true,
      type: Boolean
    },
    top: {
      type: String
    }
  },
  data () {
    return {
      visible_flag: false,
      dialog_title: '',
      dialog_width: ''
    }
  },
  components: {
    AreaTitle: () => import('@/components/common/AreaTitle')
  },
  mounted () {},
  methods: {
    closeDialog () {
      this.$emit('closeDialog', false)
    },
    sureDialog () {
      this.$emit('sureDialog')
    }
  },
  watch: {
    visible: {
      handler(newValue, oldValue) {
        // console.log(newValue, oldValue)
        this.visible_flag = newValue
      },
      immediate: true
    },
    title: {
      handler(newValue, oldValue) {
        this.dialog_title = newValue
        // console.log('title',this.dialog_title)
      },
      immediate: true
    },
    width: {
      handler(newValue, oldValue) {
        this.dialog_width = newValue
        console.log('dialog_width',this.dialog_width)
      },
      immediate: true
    }
  }
}
</script>
<style lang="scss" scoped>
.dialog {
  &__title {
    padding: 15px 16px;
    background: rgba(46, 88, 247, 0.05);
  }
  &__body {
    padding: 24px 28px 0 28px;
  }
  &__message_title{
    font-size: 16px;
    padding: 14px 28px 0 28px;
  }

}
</style>
<style lang="scss">
.dialog {
  .el-dialog {
    border-radius: 8px;
    &__body,
    &__header,
    &__footer {
      padding: 0;
      margin-top: 1rem;
    }
    &__headerbtn {
      background: #dddddd;
      top: 15px;
      border-radius: 19px;
    }
    &__close {
      color: #fff;
      width: 19px;
      height: 19px;
      text-align: center;
      line-height: 19px;
    }
  }
  &__footer {
    padding: 30px 0;
    display: flex;
    align-items: center;
    justify-content: center;
    button{
      padding:12px 44px;
    }
  }
}
</style>
