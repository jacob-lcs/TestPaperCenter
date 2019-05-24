
<template>
  <div>
    <Menu mode="horizontal" :theme="theme1" active-name="1">
      <MenuItem name="1" style="font-size: 15px" to="/">
        <Icon type="md-home"/>
        主页
      </MenuItem>
      <MenuItem name="2" style="font-size: 15px" to="/Test_Paper_Export_Mode">
        <Icon type="ios-paper"/>
        试题导出
      </MenuItem>
      <MenuItem name="3" style="font-size: 15px" to="/Test_Paper_Import">
        <Icon type="ios-paper"/>
        试题导入
      </MenuItem>


      <p style="text-align: right; margin-right: 30px; cursor: pointer" @click="quit_login">
        <Poptip trigger="hover" content="点击退出登录" placement="left">
          {{per_name}}，欢迎
        </Poptip>
      </p>


    </Menu>
  </div>
</template>

<script>
  export default {
    name: "my-header",
    data() {
      return {
        theme1: 'light',
        per_name: ''
      }
    },
    methods:{
      quit_login(){
        sessionStorage.clear();
        this.$router.push('/login')
      }
    },
    mounted() {
      this.per_name = sessionStorage.getItem("per_name")
    }
  }
</script>

<style scoped>
</style>
