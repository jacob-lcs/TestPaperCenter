<template>
  <div class="all">
    <p class="title">满分题库系统</p>
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
                  that.$router.push({
                    name: "home"
                  });
                  sessionStorage.setItem('per_name', that.per_name);
                  sessionStorage.setItem('identity', data['identity'])
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
    background-image: url("../assets/img/bg.jpg");
    height: 97vh;
  }

</style>
