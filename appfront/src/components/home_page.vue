<template>
  <div class="all">
    <div class="main">

      <!--左侧信息栏-->
      <div class="sideleft">
        <p style="font-size: 37px; font-weight: bold;color: #fdfbfb">智能组卷    智慧学习</p>
        <p style="font-size: 22px;color: #fdfbfb">大数据结合试题系统 让刷题更轻松</p>
        <div style="margin-top: 30px">
          <p>轻松模板录入，提高试题更新效率。</p>
          <p>打造线上线下数字一体化。</p>
          <p>手动组卷,自动生成,试题更加个性化。</p>
          <p>服务师生，携手共进。</p>
        </div>
      </div>

      <!--右侧登录界面
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
        </template>-->

    </div>
  </div>
</template>

<script>
    export default {
        name: "home_page"
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
</style>
