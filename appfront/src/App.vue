<template>
  <Layout id="app">
    <my-header v-if="this.$route.path != '/'&&this.$route.path != '/login'"/>
    <Content>
      <router-view/>
    </Content>
  </Layout>
</template>

<script>
import MyHeader from "@/components/header";
export default {
  name: "App",
  components: {
    MyHeader
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#app,
html,
body{
  height: 100%;
}
</style>
