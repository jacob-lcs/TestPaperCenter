// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import VueResource from 'vue-resource'
import axios from "axios";
import iView from 'iview';
import 'iview/dist/styles/iview.css';

Vue.use(VueResource);
Vue.use(iView);
Vue.config.productionTip = false;

Vue.prototype.$axios = axios;
Vue.prototype.$site = 'http://127.0.0.1:8000/';

/* eslint-disable no-new */
new Vue({
  el: "#app",
  router,
  components: {App},
  template: "<App/>"
});
