<template>
  <div class="all">
    <el-row class="title">
      <p>满分题库系统</p>
    </el-row>
    <el-row>
      <el-input
        placeholder="请输入账号"
        v-model="per_name"
        clearable
        class="in_name">
      </el-input>
    </el-row>
    <el-row>
      <el-input
        placeholder="请输入密码"
        v-model="per_password"
        type="password"
        clearable
        class="in_pass">
      </el-input>
    </el-row>
    <el-row>
      <el-button round class="btn_login" @click="login_in">登陆</el-button>
    </el-row>
  </div>
</template>

<script>
  export default {
    name: "login",
    data() {
      return {
        per_name: '',
        per_password: ''
      }
    },
    methods: {
      login_in() {
        let that = this;
        $.ajax({
          url: that.$site + "api/login",
          dataType: "json",
          data: {
            name: this.per_name,
            psw: this.per_password
          },
          success: function (data) {
            if (data['res'] === "no") {
              that.$message({
                message: '用户名或密码错误',
                type: 'warning'
              });
            } else {
              that.$router.push({
                name: "home"
              });
              sessionStorage.setItem('per_name', that.per_name);
              sessionStorage.setItem('identity', data['identity'])
            }
          }
        })
      }
    }
  }
</script>

<style scoped>
  .in_name {
    width: 20vw;
    margin-top: 5vh;
  }

  .in_pass {
    width: 20vw;
    margin-top: 5vh;
  }

  .btn_login {
    margin-top: 2vh;
  }

  .title {
    padding-top: 23vh;
    font-size: 30px;
  }

  .all {
    background-image: url("../assets/img/bg.jpg");
    height: 97vh;
  }
</style>
