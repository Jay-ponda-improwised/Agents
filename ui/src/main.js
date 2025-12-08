import './assets/main.css'
import './assets/css/layout.css'
import './assets/css/embeddings.css'
import './assets/css/prompts.css'
import './assets/css/response-time-display.css'
import 'vue-json-pretty/lib/styles.css';

import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

// Import components
import EmbeddingsComponent from './components/Embeddings/index.vue'
import ModelDemoComponent from './components/ModelDemoComponent.vue'
import PromptsComponent from './components/Prompts/index.vue'
import CommonLayout from './layout/Layout.vue' // Import the new layout
import HistoryComponent from './components/History.vue'

const routes = [
  {
    path: '/',
    component: CommonLayout,
    children: [
      { path: '/EmbeddingsComponent', component: EmbeddingsComponent },
      { path: '/ModelDemoComponent', component: ModelDemoComponent },
      { path: '/PromptsComponent', component: PromptsComponent },
      { path: '/History', component: HistoryComponent },
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