// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import './icons'
import ElementUI from 'element-ui'
import '../theme/index.css'
import Vuex from 'vuex'
import axios from 'axios'
import echarts from 'echarts'
Vue.use(Vuex)
Vue.use(ElementUI)

Vue.config.productionTip = false
Vue.prototype.$echarts = echarts
Vue.prototype.$axios = axios

// 输出方法
export default function request (req) {
  // axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

  axios.defaults.withCredentials = true
  const service = axios.create({
    baseURL: process.env.NODE_ENV === 'production' ? '/' : '',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  service.defaults.withCredentials = true
  let url = req.url
  let method = req.method
  let data = req.data
  return new Promise((resolve, reject) => {
    const options = {
      url,
      method
    }
    if (method.toLowerCase() === 'get') {
      options.params = data
    } else {
      options.data = data
    }
    service(options)
      .then(res => {
        resolve(res)
      })
      .catch(error => {
        reject(error)
      })
  })
}

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
