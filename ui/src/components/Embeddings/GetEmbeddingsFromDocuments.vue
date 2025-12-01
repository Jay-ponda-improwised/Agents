<template>
  <div class="section">
    <div class="header-row">
      <h3 class="section-header">Get Embeddings from Documents</h3>
      <button @click="getEmbeddingsFromDocuments" :disabled="loadingGetEmbeddingsFromDocuments" class="btn">
        {{ loadingGetEmbeddingsFromDocuments ? 'Processing...' : 'Process Documents' }}
      </button>
    </div>
    <div class="form-group">
      <label class="form-label">Documents (one per line):</label>
      <textarea
        v-model="documentsText"
        placeholder="Enter documents, one per line"
        rows="4"
        class="textarea"
      ></textarea>
    </div>

    <div v-if="responseGetEmbeddingsFromDocuments">
      <ResponseTimeDisplay :response-time="responseTimeGetEmbeddingsFromDocuments" />
      <TruncatedTextDisplay :content="JSON.stringify(responseGetEmbeddingsFromDocuments.document_embeddings, null, 2)" :max-lines="100" />
    </div>

    <div v-if="errorGetEmbeddingsFromDocuments" class="error-section">
      <p class="error-text">Error: {{ errorGetEmbeddingsFromDocuments }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import TruncatedTextDisplay from './TruncatedTextDisplay.vue';
import ResponseTimeDisplay from '../ResponseTimeDisplay.vue';

const documentsText = ref('');
const responseGetEmbeddingsFromDocuments = ref(null);
const errorGetEmbeddingsFromDocuments = ref(null);
const loadingGetEmbeddingsFromDocuments = ref(false);
const responseTimeGetEmbeddingsFromDocuments = ref(null);

const getEmbeddingsFromDocuments = async () => {
  const documents = documentsText.value.split('\n').filter(d => d.trim());
  if (documents.length === 0) return;

  loadingGetEmbeddingsFromDocuments.value = true;
  responseGetEmbeddingsFromDocuments.value = null;
  errorGetEmbeddingsFromDocuments.value = null;
  responseTimeGetEmbeddingsFromDocuments.value = null;

  try {
    const apiUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:33001';
    const response = await fetch(`${apiUrl}/video-2/from-documents`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(documents),
      credentials: 'include'
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || 'An error occurred');
    }
    responseGetEmbeddingsFromDocuments.value = data;
    if (data.meta && data.meta.processTime) {
      responseTimeGetEmbeddingsFromDocuments.value = data.meta.processTime;
    }
  } catch (err) {
    errorGetEmbeddingsFromDocuments.value = err.message || 'An error occurred';
  } finally {
    loadingGetEmbeddingsFromDocuments.value = false;
  }
};
</script>

<style>
/* Styles are now centralized in assets/css/common.css and assets/css/embeddings.css */
</style>