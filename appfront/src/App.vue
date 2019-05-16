<template>
    <Layout id="app">
      <Header/>
      <Content>
        <router-view/>
      </Content>
    </Layout>
</template>

<script>

import Header from  '@/components/header'
  export default {
    name: 'App',
    components:{
      Header
    }
  }
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }
</style>
