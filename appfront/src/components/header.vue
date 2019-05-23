<template>
  <div style="background-color: ">
  <Menu mode="horizontal" :theme="theme1" active-name="1" >
    <MenuItem name="1" style="font-size: 15px">
      <Icon type="md-home"/>
      主页
    </MenuItem>
    <MenuItem name="2" style="font-size: 15px">
      <Icon type="ios-paper"/>
      试题导出
    </MenuItem>
    <MenuItem name="3" style="font-size: 15px">
      <Icon type="ios-paper"/>
      试题导入
    </MenuItem>


    <p style="text-align: right; margin-right: 30px">
      {{per_name}}，欢迎
    </p>

  </Menu>
    </div>
</template>

<script>
  export default {
    name: "my-header",
    data() {
      return{
        theme1:'light'
      }
      per_name = ''
    },
    mounted() {
      this.per_name = sessionStorage.getItem("per_name")
    }
  }
</script>

<style scoped>

</style>
