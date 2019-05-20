import Vue from 'vue'
import Router from 'vue-router'
import login from '@/components/login'
import Test_Paper_Import from  '@/components/Test_Paper_Import'
import Test_Paper_Export_Byhands from  '@/components/Test_Paper_Export_Byhands'
import Test_Paper_Export_Mode from  '@/components/Test_Paper_Export_Mode'

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
    },
    {
      path: '/Test_Paper_Export_Byhands',
      name: 'Test_Paper_Export_Byhands',
      component: Test_Paper_Export_Byhands
    },
    {
      path: '/Test_Paper_Export_Mode',
      name: 'Test_Paper_Export_Mode',
      component: Test_Paper_Export_Mode
    }
  ]
})
