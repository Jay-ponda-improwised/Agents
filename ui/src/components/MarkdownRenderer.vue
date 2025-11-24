<template>
  <div class="markdown-renderer">
    <div v-if="markdownContent" v-html="renderedHtml"></div>
    <div v-else class="placeholder">
      No markdown content to render
    </div>
  </div>
</template>

<script>
import { marked } from 'marked';

export default {
  name: 'MarkdownRenderer',
  props: {
    markdownContent: {
      type: String,
      default: ''
    }
  },
  computed: {
    renderedHtml() {
      if (!this.markdownContent) return '';
      return marked(this.markdownContent);
    }
  }
};
</script>

<style scoped>
.markdown-renderer {
  text-align: left;
  padding: 10px;
}

.markdown-renderer :deep(h1) {
  font-size: 2em;
  margin: 0.67em 0;
}

.markdown-renderer :deep(h2) {
  font-size: 1.5em;
  margin: 0.83em 0;
}

.markdown-renderer :deep(h3) {
  font-size: 1.17em;
  margin: 1em 0;
}

.markdown-renderer :deep(p) {
  margin: 1em 0;
}

.markdown-renderer :deep(ul),
.markdown-renderer :deep(ol) {
  margin: 1em 0;
  padding-left: 40px;
}

.markdown-renderer :deep(li) {
  margin: 0.5em 0;
}

.markdown-renderer :deep(code) {
  background-color: #f4f4f4;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: monospace;
}

.markdown-renderer :deep(pre) {
  background-color: #f4f4f4;
  padding: 10px;
  border-radius: 5px;
  overflow-x: auto;
}

.markdown-renderer :deep(pre code) {
  background-color: transparent;
  padding: 0;
}

.markdown-renderer :deep(blockquote) {
  margin: 1em 0;
  padding: 0.5em 1em;
  border-left: 4px solid #ddd;
  background-color: #f9f9f9;
}

.markdown-renderer :deep(a) {
  color: #007bff;
  text-decoration: none;
}

.markdown-renderer :deep(a:hover) {
  text-decoration: underline;
}

.placeholder {
  color: #999;
  font-style: italic;
}
</style>