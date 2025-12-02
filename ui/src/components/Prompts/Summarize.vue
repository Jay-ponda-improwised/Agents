<template>
  <div class="section">
    <h3 class="section-header">Text Summarization</h3>
    <div class="form-group">
      <label for="content" class="form-label">Content to Summarize (1-2000 characters):</label>
      <textarea id="content" v-model="formData.content" placeholder="Enter text to summarize..." :maxlength="2000"
        class="textarea"></textarea>
      <div class="char-count">{{ formData.content.length }}/2000 characters</div>
    </div>

    <div class="form-group">
      <label for="responseLength" class="form-label">Response Length:</label>
      <select id="responseLength" v-model="formData.responseLength" class="input">
        <option value="SHORT">SHORT (1 paragraph, 3-4 sentences, approx. 100 words)</option>
        <option value="MEDIUM">MEDIUM (2-3 paragraphs, 8-10 sentences, approx. 100-300 words)</option>
        <option value="LONG">LONG (6-7 paragraphs, 15-20 sentences, approx. 300-500 words)</option>
      </select>
    </div>

    <div class="form-group">
      <label for="responseFormat" class="form-label">Response Format:</label>
      <select id="responseFormat" v-model="formData.responseFormat" class="input">
        <option value="PLAIN_TEXT">Plain Text</option>
        <option value="MARKDOWN">Markdown</option>
        <option value="JSON">JSON</option>
        <option value="CODE">Code Snippet</option>
      </select>
    </div>

    <div class="action-row">
      <ResponseTimeDisplay :response-time="responseTime" />
      <button @click="submitForm" :disabled="isSubmitting || !isFormValid" class="btn">
        {{ isSubmitting ? 'Summarizing...' : 'Summarize' }}
      </button>
    </div>

    <div v-if="error" class="error-section">
      <p class="error-text">Error: {{ error }}</p>
    </div>

    <div v-if="summaryResult" class="response-section">
      <h4 class="response-section-header">Summary Result:</h4>
      <div class="summary-output">
        <MarkdownRenderer :markdown-content="summaryResult" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue';
import MarkdownRenderer from '../MarkdownRenderer.vue';
import ResponseTimeDisplay from '../ResponseTimeDisplay.vue';

const formData = reactive({
  content: '',
  responseLength: 'SHORT',
  responseFormat: 'PLAIN_TEXT'
});

const isSubmitting = ref(false);
const summaryResult = ref('');
const error = ref('');
const responseTime = ref(null);

const isFormValid = computed(() => {
  return formData.content.length > 0 && formData.content.length <= 2000;
});

const submitForm = async () => {
  if (!isFormValid.value) {
    error.value = 'Content must be between 1 and 2000 characters';
    return;
  }

  isSubmitting.value = true;
  summaryResult.value = '';
  error.value = '';
  responseTime.value = null;

  try {
    const apiUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:33001';
    const response = await fetch(`${apiUrl}/video-3/summarize`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        content: formData.content,
        responseLength: formData.responseLength,
        responseFormat: formData.responseFormat
      })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to summarize text');
    }

    const data = await response.json();
    summaryResult.value = data.summary;

    if (data.meta && data.meta.processTime) {
      responseTime.value = data.meta.processTime;
    }
  } catch (err) {
    console.error('Summarization error:', err);
    error.value = err.message || 'An error occurred while summarizing the text';
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
.char-count {
  text-align: right;
  font-size: 0.8em;
  color: var(--text-secondary);
  margin-top: 5px;
}

.summary-output :deep(pre) {
  background: var(--code-bg);
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
}

.summary-output :deep(code) {
  font-family: 'Courier New', monospace;
}
</style>