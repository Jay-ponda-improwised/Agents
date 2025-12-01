<template>
  <div class="common-layout">
    <aside class="sidebar">
      <div class="sidebar-nav">
        <div class="nav-header">
          Index
          <ThemeToggle class="theme-toggle-sidebar" />
        </div>
        <nav>
          <ol>
            <li><router-link to="/ModelDemoComponent">ModelDemoComponent</router-link></li>
            <li><router-link to="/EmbeddingsComponent">EmbeddingsComponent</router-link></li>
          </ol>
        </nav>
      </div>
      <div class="sidebar-history">
        <router-link to="/History">History</router-link>
      </div>
    </aside>
    <main class="main-content" ref="mainContentRef">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ThemeToggle from './ThemeToggle.vue'

const mainContentRef = ref(null)
</script>

<style>
/* Styles are now centralized in assets/css/layout.css */
</style>