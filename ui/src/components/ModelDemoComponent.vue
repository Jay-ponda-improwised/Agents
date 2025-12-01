<template>
  <div class="section">
    <div class="header-row">
      <h2 class="section-header">Model Demo</h2>
      <button @click="submitQuestion" :disabled="loading" class="btn">
        {{ loading ? 'Loading...' : 'Submit' }}
      </button>
    </div>
    <div class="form-group">
      <label for="question" class="form-label">Question:</label>
      <input id="question" v-model="question" placeholder="Enter your question" @keyup.enter="submitQuestion"
        class="input" />
    </div>

    <div v-if="response" class="response-section">
      <ResponseTimeDisplay :response-time="responseTimeModelDemo" />
      <h3 class="response-section-header">Response:</h3>
      <div v-html="formattedResponse"></div>
    </div>

    <div v-if="error" class="error-section">
      <p class="error-text">Error: {{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { marked } from 'marked';
import ResponseTimeDisplay from './ResponseTimeDisplay.vue';

const question = ref('');
const response = ref(null);
const error = ref(null);
const loading = ref(false);
const responseTimeModelDemo = ref(null);

const formattedResponse = computed(() => {
  if (!response.value || !response.value.message) {
    return '';
  }
  let message = response.value.message;
  // If message is an object with a text property (like AIMessage), use that
  if (typeof message === 'object' && message.text) {
    message = message.text;
  }
  if (typeof message === 'string') {
    return marked(message);
  }
  if (typeof message === 'object') {
    const jsonString = '```json\n' + JSON.stringify(message, null, 2) + '\n```';
    return marked(jsonString);
  }
  return '';
});

const submitQuestion = async () => {
  if (!question.value.trim()) return;

  loading.value = true;
  response.value = null;
  error.value = null;
  responseTimeModelDemo.value = null;

  try {
    const apiUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:33001';
    const resp = await fetch(`${apiUrl}/video-1/?question=${encodeURIComponent(question.value)}`, {
      credentials: 'include'
    });
    const data = await resp.json();
    console.log(data.message);
    if (!resp.ok) {
      throw new Error(data.error || 'An error occurred');
    }
    response.value = data;
    if (data.meta && data.meta.processTime) {
      responseTimeModelDemo.value = data.meta.processTime;
    }
  } catch (err) {
    error.value = err.message || 'An error occurred';
  } finally {
    loading.value = false;
  }
};
</script>

<style>
/* Styles are now centralized in assets/css/common.css */
</style>