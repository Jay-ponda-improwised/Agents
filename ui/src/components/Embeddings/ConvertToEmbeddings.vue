<template>
  <div class="section">
    <h3 class="section-header">Convert Text to Embeddings</h3>
    <div class="form-group">
      <label for="textToConvert" class="form-label">Text:</label>
      <textarea id="textToConvert" v-model="textToConvert" placeholder="Enter text to convert to embeddings"
        class="textarea"></textarea>
    </div>

    <div class="action-row">
      <ResponseTimeDisplay :response-time="responseTimeConvertToEmbeddings" />
      <button @click="convertToEmbeddings" :disabled="loadingConvertToEmbeddings" class="btn">
        {{ loadingConvertToEmbeddings ? 'Converting...' : 'Convert' }}
      </button>
    </div>

    <div v-if="responseConvertToEmbeddings">
      <TruncatedTextDisplay :content="JSON.stringify(responseConvertToEmbeddings.embeddings, null, 2)"
        :max-lines="100" />
    </div>

    <div v-if="errorConvertToEmbeddings" class="error-section">
      <p class="error-text">Error: {{ errorConvertToEmbeddings }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import TruncatedTextDisplay from './TruncatedTextDisplay.vue';
import ResponseTimeDisplay from '../ResponseTimeDisplay.vue';

const textToConvert = ref('');
const responseConvertToEmbeddings = ref(null);
const errorConvertToEmbeddings = ref(null);
const loadingConvertToEmbeddings = ref(false);
const responseTimeConvertToEmbeddings = ref(null);

const convertToEmbeddings = async () => {
  if (!textToConvert.value.trim()) return;

  loadingConvertToEmbeddings.value = true;
  responseConvertToEmbeddings.value = null;
  errorConvertToEmbeddings.value = null;
  responseTimeConvertToEmbeddings.value = null;

  try {
    const apiUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:33001';
    const response = await fetch(`${apiUrl}/video-2/convert-to-embeddings?text=${encodeURIComponent(textToConvert.value)}`, {
      method: 'POST',
      credentials: 'include'
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || 'An error occurred');
    }
    responseConvertToEmbeddings.value = data;
    if (data.meta && data.meta.processTime) {
      responseTimeConvertToEmbeddings.value = data.meta.processTime;
    }
  } catch (err) {
    errorConvertToEmbeddings.value = err.message || 'An error occurred';
  } finally {
    loadingConvertToEmbeddings.value = false;
  }
};
</script>

<style>
/* Styles are now centralized in assets/css/common.css and assets/css/embeddings.css */
</style>