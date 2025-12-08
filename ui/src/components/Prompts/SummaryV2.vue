<template>
  <div class="section">
    <h3 class="section-header">Text Summarization v2</h3>
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
      <div class="action-buttons">
        <button @click="submitForm" :disabled="isSubmitting || !isFormValid" class="btn">
          {{ isSubmitting ? 'Summarizing...' : 'Summarize' }}
        </button>
      </div>
    </div>

    <div v-if="error" class="error-section">
      <p class="error-text">Error: {{ error }}</p>
    </div>

    <div v-if="summaryResult" class="response-section">
      <div class="response-section-header">
        <h4 class="response-title">Summary Result:</h4>
        <div v-if="formData.responseFormat === 'MARKDOWN' || formData.responseFormat === 'JSON'" @click="togglePreview" title="Toggle Mode" class="mode-toggle-display">
          <span v-if="showPreview">Preview Mode</span>
          <span v-else>Normal View</span>
        </div>
      </div>
      <div class="summary-output">
        <div v-if="showPreview && (formData.responseFormat === 'MARKDOWN' || formData.responseFormat === 'JSON')" class="preview-container">
          <div class="preview-content">
            <MarkdownRenderer v-if="formData.responseFormat === 'MARKDOWN'" :markdown-content="previewProcessedResult" />
            <JsonRenderer v-if="formData.responseFormat === 'JSON'" :json-string="jsonProcessedResult" />
          </div>
        </div>
        <div v-else>
          <MarkdownRenderer :markdown-content="summaryResult" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue';
import MarkdownRenderer from '../MarkdownRenderer.vue';
import ResponseTimeDisplay from '../ResponseTimeDisplay.vue';
import JsonRenderer from '../JsonRenderer.vue';

const formData = reactive({
  content: '',
  responseLength: 'SHORT',
  responseFormat: 'PLAIN_TEXT'
});

const isSubmitting = ref(false);
const summaryResult = ref('');
const error = ref('');
const responseTime = ref(null);
const showPreview = ref(false);

const previewProcessedResult = computed(() => {
  if (formData.responseFormat === 'MARKDOWN' && summaryResult.value) {
    const codeBlockRegex = /```[\w-]*\n?([\s\S]*?)\n?```/;
    const match = summaryResult.value.trim().match(codeBlockRegex);
    if (match && match[1]) {
      return match[1].trim();
    }
  }
  return summaryResult.value;
});

const jsonProcessedResult = computed(() => {
  return summaryResult.value;
});

const togglePreview = () => {
  if (summaryResult.value) {
    showPreview.value = !showPreview.value;
  }
};

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

.action-buttons {
  display: flex;
  gap: 10px;
  align-items: center;
}

.response-section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  border-bottom: 1px solid var(--main-border);
  padding-bottom: 10px;
}

.response-title {
  margin: 0;
  color: var(--text-color);
  font-weight: 600;
}

.mode-toggle-display {
  cursor: pointer;
  padding: 5px 10px;
  border: 1px solid var(--main-border);
  border-radius: 4px;
  background-color: var(--button-secondary-bg);
  color: var(--text-color);
  font-size: 0.9em;
  transition: all 0.2s ease;
}

.mode-toggle-display:hover {
  background-color: var(--button-secondary-hover-bg);
  border-color: var(--button-border-hover);
}

.preview-container {
  border: 2px solid var(--button-primary-bg);
  border-radius: 6px;
  padding: 20px;
  background-color: rgba(14, 165, 233, 0.05);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Ensure consistent markdown rendering in both preview and normal modes */
.summary-output :deep(.markdown-renderer) {
  line-height: 1.6;
  background-color: transparent;
  padding: 10px 0;
}

.preview-content :deep(.markdown-renderer) {
  white-space: normal;
  line-height: 1.6;
}

/* Consistent styling for markdown elements in both modes */
.summary-output :deep(.markdown-renderer) :deep(h1),
.summary-output :deep(.markdown-renderer) :deep(h2),
.summary-output :deep(.markdown-renderer) :deep(h3),
.preview-content :deep(.markdown-renderer) :deep(h1),
.preview-content :deep(.markdown-renderer) :deep(h2),
.preview-content :deep(.markdown-renderer) :deep(h3) {
  margin-top: 1em;
  margin-bottom: 0.5em;
  line-height: 1.3;
}

.summary-output :deep(.markdown-renderer) :deep(h1),
.preview-content :deep(.markdown-renderer) :deep(h1) {
  font-size: 1.5em;
  font-weight: 600;
}

.summary-output :deep(.markdown-renderer) :deep(h2),
.preview-content :deep(.markdown-renderer) :deep(h2) {
  font-size: 1.3em;
  font-weight: 600;
}

.summary-output :deep(.markdown-renderer) :deep(h3),
.preview-content :deep(.markdown-renderer) :deep(h3) {
  font-size: 1.1em;
  font-weight: 600;
}

.summary-output :deep(.markdown-renderer) :deep(p),
.preview-content :deep(.markdown-renderer) :deep(p) {
  margin-top: 0.5em;
  margin-bottom: 0.5em;
}

.summary-output :deep(.markdown-renderer) :deep(strong),
.preview-content :deep(.markdown-renderer) :deep(strong) {
  font-weight: bold;
}

.summary-output :deep(.markdown-renderer) :deep(em),
.preview-content :deep(.markdown-renderer) :deep(em) {
  font-style: italic;
}
</style>