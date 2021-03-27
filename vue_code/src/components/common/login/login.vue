<template>
  <div class="login">
    <div class="login__logo">
      <img src="~@/assets/images/pic/logo.png" alt=""/>
      智能测试库平台
    </div>
    <div class="login__box">
      <div class="login__box_head">
        <p><i class="icon_face"></i>HELLO！</p>
        <p class="welcome">欢迎来到智能测试库平台</p>
      </div>
      <el-form :model="form" class="login_form" :rules="rules" ref="form">
        <el-form-item prop="user">
          <el-input v-model="form.user" placeholder="账号"></el-input>
        </el-form-item>
        <el-form-item prop="pwd">
          <el-input v-model="form.pwd" placeholder="密码" type="password"></el-input>
        </el-form-item>
        <el-form-item prop="code">
          <el-input v-model="form.code" placeholder="请输入验证码" @keypress.enter="submit('form')"></el-input>
          <div class="rang_img">
            <span
              @click="changeCode"
            >{{ imagecode }}</span>
          </div>
        </el-form-item>
        <el-button type="primary" round class="login__btn" @click="submit('form')">登 录</el-button>
        <p></p>
        <el-button type="text" class="login__forget">忘记密码</el-button>
      </el-form>
    </div>
  </div>
</template>
<script>
  import api from "../../../service/api";
  import {setCookie} from "../../../service/cookie";

  export default {
    data() {
      let check_code = (result, value, callback) => {
        if (this.form.code.toLowerCase() !== this.imagecode.toLowerCase()) {
          callback(new Error('请正确输入验证码'))
        }
        callback()
      }
      return {
        form: {
          user: '',
          pwd: '',
          code: ''
        },
        rules: {
          user: [
            { required: true, message: '用户名不能为空', trigger: 'blur' }
          ],
          pwd: [
            { required: true, message: '密码不能为空', trigger: 'blur' }
          ],
          code: [
            { required: true, message: '验证码不能为空', trigger: 'blur' },
            {validator: check_code, trigger: 'change'},
          ],
        },
        imagecode: '',
        url_path: ""
      }
    },
    methods: {
      submit(form) {
        this.$refs[form].validate((valid) => {
          if (valid){
            let data = {
              user_name: this.form.user,
              user_password: this.form.pwd
            }
            api.login_out_api.login(data).then(response => {
              let res = response;
              console.log(res)
              if (res.status === 0) {
                this.url_path = res.info.cur_branch + "_";
                setCookie("url_path", this.url_path, 10000000 * 60);
                setCookie("user_role_id", res.info.user_role_id, 10000000 * 60);
                setCookie("user_id", res.info.user_id, 10000000 * 60);
                setCookie("user_token", res.info.token, 10000000 * 60);
                setCookie("user_name", res.info.user_name, 10000000 * 60);
                setCookie("product_name", res.info.product_name, 10000000 * 60);
                setCookie("menu_name_list", res.info.menu_name_list, 10000000 * 60);

                if (res.user_role_id === "6") {
                  this.$router.push({
                    path: "/show_operate_data",
                    data: {
                      user_id: res.info.user_id,
                      user_token: res.info.token
                    }
                  });
                } else if (res.user_role_id !== 6) {
                  this.$router.push({
                    path: "/home/" + res.info.cur_branch + "_" + "wholeProcess",
                    data: {
                      user_id: res.info.user_id,
                      user_token: res.info.token
                    }
                  })
                }
              } else if (res.status === 400) {
                this.$message.error("用户名或密码错误");
              }
            });
          }
        })
      },
      changeCode() {
        this.imagecode = "";
        this.createCode();
      },
      createCode() {
        let random = Array(
          0,
          1,
          2,
          3,
          4,
          5,
          6,
          7,
          8,
          9,
          "a",
          "b",
          "c",
          "d",
          "e",
          "f",
          "g",
          "h",
          "i",
          "j",
          "k",
          "l",
          "m",
          "n",
          "o",
          "p",
          "q",
          "r",
          "s",
          "t",
          "u",
          "v",
          "w",
          "x",
          "y",
          "z",
          "A",
          "B",
          "C",
          "D",
          "E",
          "F",
          "G",
          "H",
          "I",
          "J",
          "K",
          "L",
          "M",
          "N",
          "O",
          "P",
          "Q",
          "R",
          "S",
          "T",
          "U",
          "V",
          "W",
          "X",
          "Y",
          "Z"
        );
        for (let i = 0; i < 4; i++) {
          let index = Math.floor(Math.random() * 62);
          let val = random[index];
          if (val === "I") {
            val = "i"
          }
          else if (val === "l") {
            val = "L"
          }
          this.imagecode += val;
        }
      }
    },

    mounted() {
      this.createCode();
    }

  }
</script>
<style lang="scss" scoped>
  .login {
    width: 100vw;
    height: 100vh;
    padding: 26px 19px;
    background: url(~@/assets/images/bg/login_bg.png) no-repeat center center/100% auto;

    &__logo {
      display: flex;
      align-items: center;
      font-size: 16px;

      img {
        width: 34px;
        margin-right: 8px;
      }
    }

    &__box {
      box-sizing: border-box;
      color: #333;
      width: 460px;
      height: 530px;
      background: #ffffff;
      border-radius: 16px;
      box-shadow: 0px 0px 36px 0px rgba(0, 0, 0, 0.06);
      position: absolute;
      top: 126px;
      left: 60px;
      padding: 34px 30px;

      &_head {
        padding-left: 7px;

        p {
          display: flex;
          align-items: center;
          font-size: 45px;
          line-height: 1;
        }

        .welcome {
          font-size: 24px;
          margin-top: 11px;
        }

        .icon_face {
          display: block;
          width: 39px;
          height: 42px;
          margin-right: 15px;
          background: url(~@/assets/images/pic/face.png) no-repeat center center/100% 100%;
        }
      }
    }

    &__btn {
      width: 100%;
      margin-top: 50px;
      height: 56px;
      border-radius: 56px;
      font-size: 20px;
    }

    &__forget {
      color: #c5c5c5;
      font-size: 14px;
      float: right;
      display: block;
      margin-top: 20px;
    }
  }
</style>
<style lang="scss">
  .login_form {
    margin-top: 43px;

    .el-form-item {
      height: 56px;
      background: #f6f6f6;
      border: 1px solid #e5ecf2;
      border-radius: 32px;
      margin-bottom: 14px;

      .el-form-item__content {
        display: flex;
        align-items: center;
      }

      .el-input__inner {
        border: none;
        height: 56px;
        font-size: 14px;
        line-height: 56px;
        flex: 1;
        background: transparent;
      }

      .rang_img {
        color: #2e58f7;
        font-size: 25px;
        width: 90px;
        flex-shrink: 0;
      }
    }
  }
</style>
