import Vue from 'vue'
import Router from 'vue-router'
import login from '@/components/login'
import Test_Paper_Import from  '@/components/Test_Paper_Import'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'login',
      component: login
    },
    {
      path: '/Test_Paper_Import',
      name: 'Test_Paper_Import',
      component: Test_Paper_Import
    }
  ]
})
