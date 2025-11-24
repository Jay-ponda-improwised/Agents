<template>
  <div class="embeddings-demo">
    <h2>Embeddings Demo</h2>
    
    <!-- Convert to Embeddings Section -->
    <div class="section">
      <h3>Convert Text to Embeddings</h3>
      <div class="input-section">
        <label for="textToConvert">Text:</label>
        <textarea 
          id="textToConvert" 
          v-model="textToConvert" 
          placeholder="Enter text to convert to embeddings"
        ></textarea>
        <button @click="convertToEmbeddings" :disabled="loading.convertToEmbeddings">
          {{ loading.convertToEmbeddings ? 'Converting...' : 'Convert' }}
        </button>
      </div>
      
      <div v-if="responses.convertToEmbeddings" class="response-section">
        <h4>Embeddings:</h4>
        <pre>{{ JSON.stringify(responses.convertToEmbeddings.embeddings, null, 2) }}</pre>
      </div>
      
      <div v-if="errors.convertToEmbeddings" class="error-section">
        <p class="error">Error: {{ errors.convertToEmbeddings }}</p>
      </div>
    </div>
    
    <!-- From Documents Section -->
    <div class="section">
      <h3>Get Embeddings from Documents</h3>
      <div class="input-section">
        <label>Documents (one per line):</label>
        <textarea 
          v-model="documentsText" 
          placeholder="Enter documents, one per line"
          rows="4"
        ></textarea>
        <button @click="getEmbeddingsFromDocuments" :disabled="loading.getEmbeddingsFromDocuments">
          {{ loading.getEmbeddingsFromDocuments ? 'Processing...' : 'Process Documents' }}
        </button>
      </div>
      
      <div v-if="responses.getEmbeddingsFromDocuments" class="response-section">
        <h4>Document Embeddings:</h4>
        <pre>{{ JSON.stringify(responses.getEmbeddingsFromDocuments.document_embeddings, null, 2) }}</pre>
      </div>
      
      <div v-if="errors.getEmbeddingsFromDocuments" class="error-section">
        <p class="error">Error: {{ errors.getEmbeddingsFromDocuments }}</p>
      </div>
    </div>
    
    <!-- Search Section -->
    <div class="section">
      <h3>Embeddings Search</h3>
      <div class="input-section">
        <label for="searchQuery">Query:</label>
        <input 
          id="searchQuery" 
          v-model="searchQuery" 
          placeholder="Enter search query"
        />
        
        <label>Documents to Search (one per line):</label>
        <textarea 
          v-model="searchDocumentsText" 
          placeholder="Enter documents to search, one per line (leave empty to use default)"
          rows="4"
        ></textarea>
        
        <button @click="performEmbeddingsSearch" :disabled="loading.embeddingsSearch">
          {{ loading.embeddingsSearch ? 'Searching...' : 'Search' }}
        </button>
      </div>
      
      <div v-if="responses.embeddingsSearch" class="response-section">
        <h4>Search Results:</h4>
        <pre>{{ JSON.stringify(responses.embeddingsSearch.search_results, null, 2) }}</pre>
      </div>
      
      <div v-if="errors.embeddingsSearch" class="error-section">
        <p class="error">Error: {{ errors.embeddingsSearch }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EmbeddingsComponent',
  data() {
    return {
      textToConvert: '',
      documentsText: '',
      searchQuery: '',
      searchDocumentsText: '',
      
      responses: {
        convertToEmbeddings: null,
        getEmbeddingsFromDocuments: null,
        embeddingsSearch: null
      },
      
      errors: {
        convertToEmbeddings: null,
        getEmbeddingsFromDocuments: null,
        embeddingsSearch: null
      },
      
      loading: {
        convertToEmbeddings: false,
        getEmbeddingsFromDocuments: false,
        embeddingsSearch: false
      }
    };
  },
  methods: {
    async convertToEmbeddings() {
      if (!this.textToConvert.trim()) return;
      
      this.loading.convertToEmbeddings = true;
      this.responses.convertToEmbeddings = null;
      this.errors.convertToEmbeddings = null;
      
      try {
        const apiUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:33001';
        const response = await fetch(`${apiUrl}/video-2/convert-to-embeddings?text=${encodeURIComponent(this.textToConvert)}`, {
          method: 'POST',
          credentials: 'include'
        });
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.detail || 'An error occurred');
        }
        this.responses.convertToEmbeddings = data;
      } catch (err) {
        this.errors.convertToEmbeddings = err.message || 'An error occurred';
      } finally {
        this.loading.convertToEmbeddings = false;
      }
    },
    
    async getEmbeddingsFromDocuments() {
      const documents = this.documentsText.split('\n').filter(d => d.trim());
      if (documents.length === 0) return;
      
      this.loading.getEmbeddingsFromDocuments = true;
      this.responses.getEmbeddingsFromDocuments = null;
      this.errors.getEmbeddingsFromDocuments = null;
      
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
          console.log(data);
          console.log(response.status);
          console.log(response.statusText);
          console.log(response.headers);
          console.log(response.body);
          console.log(response.url);
          console.log(response.redirected);
          console.log(response.type);
          console.log(response.useFinalURL);
          throw new Error(data.detail || 'An error occurred');
        }
        this.responses.getEmbeddingsFromDocuments = data;
      } catch (err) {
        this.errors.getEmbeddingsFromDocuments = err.message || 'An error occurred';
      } finally {
        this.loading.getEmbeddingsFromDocuments = false;
      }
    },
    
    async performEmbeddingsSearch() {
      const documents = this.searchDocumentsText.split('\n').filter(d => d.trim());
      
      this.loading.embeddingsSearch = true;
      this.responses.embeddingsSearch = null;
      this.errors.embeddingsSearch = null;
      
      try {
        const apiUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:33001';
        const response = await fetch(`${apiUrl}/video-2/search`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            query: this.searchQuery,
            documents
          }),
          credentials: 'include'
        });
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.detail || 'An error occurred');
        }
        this.responses.embeddingsSearch = data;
      } catch (err) {
        this.errors.embeddingsSearch = err.message || 'An error occurred';
      } finally {
        this.loading.embeddingsSearch = false;
      }
    }
  }
};
</script>

<style scoped>
.embeddings-demo {
  width: 100%; /* Ensure it takes full width of parent */
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-family: Arial, sans-serif;
}

.section {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #eee;
  border-radius: 6px;
}

.section h3 {
  margin-top: 0;
  color: #333;
}

.input-section {
  margin-bottom: 15px;
}

.input-section label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.input-section input,
.input-section textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  margin-bottom: 10px;
  font-family: inherit;
}

.input-section textarea {
  resize: vertical;
}

.input-section button {
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
  margin-top: 15px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.response-section pre {
  white-space: pre-wrap;
  word-break: break-word;
  margin: 0;
  font-size: 0.9em;
}

.error-section {
  margin-top: 15px;
  padding: 15px;
  background-color: #f8d7da;
  border-radius: 4px;
}

.error {
  color: #721c24;
  margin: 0;
}
</style>