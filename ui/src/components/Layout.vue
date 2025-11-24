<template>
  <div class="common-layout">
    <aside class="sidebar">
      <nav>
        <ul>
          <li><router-link to="/EmbeddingsComponent">EmbeddingsComponent</router-link></li>
          <li><router-link to="/ModelDemoComponent">ModelDemoComponent</router-link></li>
        </ul>
      </nav>
    </aside>
    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
export default {
  name: 'CommonLayout',
};
</script>

<style scoped>
.common-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 200px;
  background-color: #f0f0f0;
  padding: 20px;
  border-right: 1px solid #ccc;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  margin-bottom: 10px;
}

.sidebar a {
  text-decoration: none;
  color: #333;
  font-weight: bold;
}

.sidebar a.router-link-active {
  color: #007bff;
}

.main-content {
  flex-grow: 1;
  padding: 20px;
  display: flex;
  flex-direction: column; /* Allow children to stack and take full width */
  /* Removed justify-content and align-items to allow full width */
}
</style>