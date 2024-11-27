import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'element-plus/dist/index.css'
import axios from 'axios'
import moment from 'moment-timezone'

const timezone = 'Asia/Shanghai'
import * as echarts from 'echarts';

import locale from 'element-plus/es/locale/lang/zh-cn';
import ElementPlus from 'element-plus';

moment.tz.setDefault(timezone)
const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:3100',
});

// 添加请求拦截器
apiClient.interceptors.request.use((config) => {
    // 检查本地存储中是否存在token
    const token = localStorage.getItem('token');
    if (token) {
        // 如果存在token，则将其添加到headers中
        config.headers.Authorization = token;
    }
    return config;
});

const app = createApp(App)
app.config.globalProperties.$axios = apiClient
app.config.globalProperties.$moment = moment
app.config.globalProperties.$echarts = echarts;
app.use(store)
app.use(router)
app.use(ElementPlus, {locale});
app.mount('#app')
