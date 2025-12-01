<template>
  <div class="section">
    <div class="header-row">
      <h3 class="section-header">Embeddings Search</h3>
      <button @click="performEmbeddingsSearch" :disabled="loadingEmbeddingsSearch" class="btn">
        {{ loadingEmbeddingsSearch ? 'Searching...' : 'Search' }}
      </button>
    </div>
    <div class="form-group">
      <label for="searchQuery" class="form-label">Query:</label>
      <input
        id="searchQuery"
        v-model="searchQuery"
        placeholder="Enter search query"
        class="input"
      />

      <label class="form-label">Documents to Search (one per line):</label>
      <textarea
        v-model="searchDocumentsText"
        placeholder="Enter documents to search, one per line (leave empty to use default)"
        rows="4"
        class="textarea"
      ></textarea>
    </div>

    <div v-if="responseEmbeddingsSearch">
      <ResponseTimeDisplay :response-time="responseTimeSearch" />
      <TruncatedTextDisplay :content="JSON.stringify(responseEmbeddingsSearch.search_results, null, 2)" :max-lines="100" />
    </div>

    <div v-if="errorEmbeddingsSearch" class="error-section">
      <p class="error-text">Error: {{ errorEmbeddingsSearch }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import TruncatedTextDisplay from './TruncatedTextDisplay.vue';
import ResponseTimeDisplay from '../ResponseTimeDisplay.vue';

const searchQuery = ref('');
const searchDocumentsText = ref('');
const responseEmbeddingsSearch = ref(null);
const errorEmbeddingsSearch = ref(null);
const loadingEmbeddingsSearch = ref(false);
const responseTimeSearch = ref(null);

const performEmbeddingsSearch = async () => {
  const documents = searchDocumentsText.value.split('\n').filter(d => d.trim());

  loadingEmbeddingsSearch.value = true;
  responseEmbeddingsSearch.value = null;
  errorEmbeddingsSearch.value = null;
  responseTimeSearch.value = null;

  try {
    const apiUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:33001';
    const response = await fetch(`${apiUrl}/video-2/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        query: searchQuery.value,
        documents
      }),
      credentials: 'include'
    });
    const data = await response.json();
    console.log("EmbeddingsSearch API Response Data:", data);
    if (!response.ok) {
      throw new Error(data.detail || 'An error occurred');
    }
    responseEmbeddingsSearch.value = data;
    if (data.meta && data.meta.processTime) {
      responseTimeSearch.value = data.meta.processTime;
      console.log("responseTimeSearch value:", responseTimeSearch.value);
    }
  } catch (err) {
    errorEmbeddingsSearch.value = err.message || 'An error occurred';
  } finally {
    loadingEmbeddingsSearch.value = false;
  }
};
</script>

<style>
/* Styles are now centralized in assets/css/common.css and assets/css/embeddings.css */
</style>