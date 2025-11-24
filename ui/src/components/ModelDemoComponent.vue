<template>
  <div class="model-demo">
    <h2>Model Demo</h2>
    <div class="input-section">
      <label for="question">Question:</label>
      <input 
        id="question" 
        v-model="question" 
        placeholder="Enter your question" 
        @keyup.enter="submitQuestion"
      />
      <button @click="submitQuestion" :disabled="loading">
        {{ loading ? 'Loading...' : 'Submit' }}
      </button>
    </div>
    
    <div v-if="response" class="response-section">
      <h3>Response:</h3>
      <div v-html="formattedResponse"></div>
    </div>
    
    <div v-if="error" class="error-section">
      <p class="error">Error: {{ error }}</p>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked';

export default {
  name: 'ModelDemoComponent',
  data() {
    return {
      question: '',
      response: null,
      error: null,
      loading: false
    };
  },
  computed: {
    formattedResponse() {
      if (!this.response || !this.response.message) {
        return '';
      }
      let message = this.response.message;
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
    }
  },
  methods: {
    async submitQuestion() {
      if (!this.question.trim()) return;
      
      this.loading = true;
      this.response = null;
      this.error = null;
      
      try {
        const apiUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:33001';
        const response = await fetch(`${apiUrl}/video-1/?question=${encodeURIComponent(this.question)}`, {
          credentials: 'include'
        });
        const data = await response.json();
        console.log(data.message);
        if (!response.ok) {
          throw new Error(data.error || 'An error occurred');
        }
        this.response = data;
      } catch (err) {
        this.error = err.message || 'An error occurred';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.model-demo {
  width: 100%; /* Ensure it takes full width of parent */
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-family: Arial, sans-serif;
}

.input-section {
  margin-bottom: 20px;
}

.input-section label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.input-section input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.input-section button {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.input-section button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.response-section {
  margin-top: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.error-section {
  margin-top: 20px;
  padding: 15px;
  background-color: #f8d7da;
  border-radius: 4px;
}

.error {
  color: #721c24;
  margin: 0;
}
</style>