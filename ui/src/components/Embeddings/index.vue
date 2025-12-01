<template>
  <div class="embeddings-demo">
    <div class="header">
      <h2 class="embeddings-title">Embeddings Demo</h2>
      <div class="tabs">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="{ 'tab-button': true, 'active': activeTab === tab.id }"
        >
          {{ tab.name }}
        </button>
      </div>
    </div>

    <div class="tab-content">
      <keep-alive>
        <component :is="activeComponent" />
      </keep-alive>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import ConvertToEmbeddings from './ConvertToEmbeddings.vue';
import GetEmbeddingsFromDocuments from './GetEmbeddingsFromDocuments.vue';
import EmbeddingsSearch from './EmbeddingsSearch.vue';

const tabs = [
  { id: 'ConvertToEmbeddings', name: 'Convert To Embeddings', component: ConvertToEmbeddings },
  { id: 'GetEmbeddingsFromDocuments', name: 'Get Embeddings From Documents', component: GetEmbeddingsFromDocuments },
  { id: 'EmbeddingsSearch', name: 'Embeddings Search', component: EmbeddingsSearch }
];

const router = useRouter();
const route = useRoute();
const activeTab = ref('');

const activeComponent = computed(() => {
  const tab = tabs.find(t => t.id === activeTab.value);
  return tab ? tab.component : null;
});

onMounted(() => {
  const tabFromQuery = route.query.tab;
  if (tabs.some(t => t.id === tabFromQuery)) {
    activeTab.value = tabFromQuery;
  } else if (tabs.length > 0) {
    activeTab.value = tabs[0].id;
  }
});

watch(activeTab, (newTab) => {
  if (newTab && route.query.tab !== newTab) {
    router.push({ query: { tab: newTab } });
  }
});

watch(() => route.query.tab, (newTab) => {
  if (newTab && tabs.some(t => t.id === newTab) && activeTab.value !== newTab) {
    activeTab.value = newTab;
  } else if (!newTab && tabs.length > 0) {
    // Handle case where query is removed
    activeTab.value = tabs[0].id;
  }
});
</script>

<style>
/* Styles are now centralized in assets/css/embeddings.css */
</style>