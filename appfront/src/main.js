// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import VueResource from 'vue-resource'
import axios from "axios";
import iView from 'iview';
import 'iview/dist/styles/iview.css';
import mavonEditor from 'mavon-editor'
import 'mavon-editor/dist/css/index.css'
import Bmob from "hydrogen-js-sdk";
// 初始化
Bmob.initialize("955782e687fff4b1a1b268d8b095c115", "7c4a7bb7ae959e2a295ea0f61adddb82");


// 挂载到全局使用
Vue.prototype.Bmob = Bmob;
Vue.use(mavonEditor);
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
