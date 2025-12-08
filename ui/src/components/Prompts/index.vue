<template>
  <div class="prompts-demo">
    <div class="header">
      <h2 class="prompts-title">Prompts Demo</h2>
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
import Summarize from './Summarize.vue';
import SummaryV2 from './SummaryV2.vue';

const tabs = [
  { id: 'Summarize', name: 'Summarize Text', component: Summarize },
  { id: 'SummaryV2', name: 'Summary v2', component: SummaryV2 }
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
/* Styles are now centralized in assets/css/prompts.css */
</style>