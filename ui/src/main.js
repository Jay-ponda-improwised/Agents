import './assets/main.css'

import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

// Import components
import EmbeddingsComponent from './components/EmbeddingsComponent.vue'
import ModelDemoComponent from './components/ModelDemoComponent.vue'
import CommonLayout from './components/Layout.vue' // Import the new layout

const routes = [
  {
    path: '/',
    component: CommonLayout,
    children: [
      { path: '/EmbeddingsComponent', component: EmbeddingsComponent },
      { path: '/ModelDemoComponent', component: ModelDemoComponent },
      { path: '/', redirect: '/EmbeddingsComponent' } // Default route
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(App)
app.use(router)
app.mount('#app')