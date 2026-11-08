import {createApp} from 'vue';
import App from './App.vue';
import ProductRegistration from '../../../product-registration/frontend/ProductRegistration.vue';
createApp(location.pathname === '/products/new' ? ProductRegistration : App).mount('#app');
