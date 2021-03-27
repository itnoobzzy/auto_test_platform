
import axios from 'axios'
// axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
axios.defaults.withCredentials = true
const service = axios.create({
  baseURL: '',
  headers: {
    'Content-Type': 'application/json',
  }
});
service.defaults.withCredentials=true

const baseURL =  '';

// 拦截异常响应

// axios.interceptors.response.use((response) => {
//     if (response.status === 0) {
//       // 如果请求errno不等于0，则弹出错误原因
//         return response;
//     }
//   }, (error) => {
//     if (!error.response) {
//       Notification.warning({
//         title: '抱歉',
//         message: `后端接口响应失败，请刷新浏览器重试。错误原因${error}`,
//         duration: 6000,
//       });
//       return Promise.resolve(error);
//     }
//     // 返回错误码,自行定义,根据项目需求和实际情况
//     // switch (error.response.status) {
//     //   case 401:
//     //     Notification.error({
//     //       title: '错误',
//     //       message: '登录信息过期，跳转登陆页401',
//     //       duration: 5000,
//     //     });
//     //     Cookie.remove('token');
//     //     router.replace('/');
//     //     break;
//     //   case 403:
//     //     Notification.error({
//     //       title: '错误',
//     //       message: '您没有权限进行此操作403',
//     //       duration: 5000,
//     //     });
//     //     break;
//     //   case 404:
//     //     Notification.error({
//     //       title: '错误',
//     //       message: '接口网址未找到404',
//     //       duration: 5000,
//     //     });
//     //     break;
//     //   default:
//     //     Notification.error({
//     //       title: '错误',
//     //       message: '未知错误',
//     //       duration: 5000,
//     //     });
//     //     return Promise.reject(error);
//     // }
//     return error;
//   });

// 输出方法
export default {
  request(url, data = {}, method = 'get') {
  return new Promise((resolve, reject) => {
    const options = {
      url,
      method
    };
    if (method.toLowerCase() === 'get') {
      options.params = data
    } else {
      options.data = data
      //console.log(data)
    }
    service(options)
      .then(res => {
        resolve(res.data)
      })
      .catch(error => {
        reject(error);
      })
  })
},
  get(url, params = {}) {
    return new Promise((resolve, reject) => {
      axios.get(baseURL + url, {params}).then(res => {
        resolve(res.data);
      }).catch(error => {
        reject(error);
      })
    })
  },
  post(url, params = {}) {
    return new Promise((resolve, reject) => {
      axios.post(baseURL + url, params).then(res => {
        resolve(res.data);
      }).catch(error => {
        reject(error);
        this.$message.error('系统异常，请联系管理员！')
      })
    })
  },
}


