<template>
  <div class="all">
    <div class="main">

      <!--左侧信息栏-->
      <div class="sideleft">
        <p style="font-size: 35px; font-weight: bold;color: #fdfbfb">智能组卷    智慧学习</p>
        <p style="font-size: 22px;color: #fdfbfb">大数据结合试题系统 让刷题更轻松</p>
        <div style="margin-top: 30px">
          <p>轻松模板录入，提高试题更新效率。</p>
          <p>打造线上线下数字一体化。</p>
          <p>手动组卷,自动生成,试题更加个性化。</p>
          <p>服务师生，携手共进。</p>
        </div>
      </div>

      <!--右侧登录界面-->
      <div class="sideright_login">
        <template>
          <Card class="cd">
            <div>
              <p class="headline" style="padding-top:60px;font-size: 30px;text-align: center">满分题库系统<br/>LOG IN</p>
            </div>
            <br>
            <Form ref="formInline" :model="formInline" :rules="ruleInline" inline>
              <FormItem prop="user">
                <Input type="text" v-model="formInline.user" placeholder="Username" class="in_text">
                  <Icon type="ios-person-outline" slot="prepend"></Icon>
                </Input>
              </FormItem>
              <br>
              <FormItem prop="password">
                <Input type="password" v-model="formInline.password" placeholder="Password" class="in_text">
                  <Icon type="ios-lock-outline" slot="prepend"></Icon>
                </Input>
              </FormItem>
              <br>
              <FormItem>
                <Button type="primary" @click="handleSubmit('formInline')">登录</Button>
              </FormItem>
            </Form>

          </Card>
        </template>
      </div>
    </div>
  </div>
</template>
<script>
  export default {
    name: "login",
    data() {
      return {
        formInline: {
          user: '',
          password: ''
        },
        ruleInline: {
          user: [
            {required: true, message: 'Please fill in the user name', trigger: 'blur'}
          ],
          password: [
            {required: true, message: 'Please fill in the password.', trigger: 'blur'},
            {type: 'string', min: 4, message: 'The password length cannot be less than 4 bits', trigger: 'blur'}
          ]
        }
      }
    },
    methods: {
      handleSubmit(name) {
        let that = this;
        this.$refs[name].validate((valid) => {
          if (valid) {
            $.ajax({
              url: that.$site + "api/login",
              dataType: "json",
              data: {
                name: this.formInline.user,
                psw: this.formInline.password
              },
              success: function (data) {
                if (data['res'] === "no") {
                  that.$Message.warning('用户名或密码错误');
                } else {
                  sessionStorage.setItem('per_name', that.formInline.user);
                  sessionStorage.setItem('identity', data['identity'])
                  that.$router.push("/");
                }
              }

            });
          } else {
            this.$Message.error('Fail!');
          }
        })
      },

    }
  }
</script>

<style scoped>
  .sideleft {
    color: #fdfbfb;
    width: 600px;
    height: 250px;
    float: left;
    padding: 100px 130px;
    text-align: left;
  }

  .sideleft p {
    padding: 8px 0;
    font-size: 16px;
    color: #c8cccf
  }

  .cd {
    width: 400px;
    height: 370px;
    background-color: rgba(255, 255, 255, 0.4);
    float: right;
    margin-right: 300px;
    margin-top: 120px;

  }
  .button>>>.ivu-btn ivu-btn-primary{
    background-color: #2c3e50;
  }



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
    padding-top: 200px;
    font-size: 50px;
  }

  .all {
    background-image: url("../assets/img/bg5.jpg");
    background-repeat: no-repeat;
    background-position: 50% 50%;
    background-size: 250vh;
    height: 100vh;
    font-family: "Microsoft YaHei" ! important;
  }

</style>
