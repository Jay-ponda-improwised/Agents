<template>
  <div class="truncated-text-display">
    <pre>{{ displayContent }}</pre>
    <div class="content-actions">
      <div class="action-buttons">
        <button
          v-if="isTruncated"
          @click="toggleShowAllContent"
          class="toggle-button"
        >
          {{ displayMode === 'showAll' ? 'Show Less' : 'Show All' }}
        </button>

        <button
          v-if="isTruncated && displayMode !== 'showAll'"
          @click="toggleCollapseFirstLast"
          class="toggle-button"
        >
          {{ displayMode === 'collapseFirstLast' ? 'Expand' : 'Collapse (First/Last)' }}
        </button>
      </div>

      <div class="pagination-controls" v-if="isTruncated && displayMode === 'paginate'">
        <button
          @click="prevPage"
          class="pagination-button"
          :disabled="currentPage === 0"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
        </button>
        <span class="page-info" v-if="isTruncated">
          Page {{ currentPage + 1 }} of {{ totalPages }}
        </span>
        <button
          @click="nextPage"
          class="pagination-button"
          :disabled="currentPage === totalPages - 1"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
        </button>
      </div>

      <div class="copy-container">
        <span
          class="copy-icon"
          @click="copyToClipboard"
          :class="{ copied: isCopied }"
          aria-label="Copy to clipboard"
          role="button"
          tabindex="0"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-clipboard">
            <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
            <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
          </svg>
        </span>
        <span v-if="isCopied" class="copy-feedback">Copied!</span>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, onMounted } from 'vue';

const props = defineProps({
  content: {
    type: String,
    required: true
  },
  maxLines: {
    type: Number,
    default: 100
  },
  collapseLineCount: { // New prop
    type: Number,
    default: 5
  }
});

const displayMode = ref('showAll'); // Can be 'showAll', 'collapseFirstLast', 'paginate'
const isTruncated = ref(false);

const isCopied = ref(false);
const currentPage = ref(0);
const lines = ref([]);

const totalPages = computed(() => {
  return Math.ceil(lines.value.length / props.maxLines);
});

const displayContent = computed(() => {
  if (displayMode.value === 'showAll') {
    return props.content;
  }

  // Handle 'collapseFirstLast' mode
  if (displayMode.value === 'collapseFirstLast') {
    if (lines.value.length <= props.collapseLineCount * 2 + 1) { // +1 for ellipsis line
      return props.content; // If content is too short to collapse meaningfully, show all
    }
    const firstLines = lines.value.slice(0, props.collapseLineCount);
    const lastLines = lines.value.slice(-props.collapseLineCount);
    return firstLines.join('\n') + '\n...\n' + lastLines.join('\n');
  }

  // Default to 'paginate' mode
  const start = currentPage.value * props.maxLines;
  const end = start + props.maxLines;
  return lines.value.slice(start, end).join('\n');
});

const toggleShowAllContent = () => {
  if (displayMode.value === 'showAll') {
    displayMode.value = 'paginate';
  } else {
    displayMode.value = 'showAll';
  }
  currentPage.value = 0; // Reset pagination when changing mode
};

const toggleCollapseFirstLast = () => {
  if (displayMode.value === 'collapseFirstLast') {
    displayMode.value = 'paginate'; // Switch back to paginate if expanding
  } else {
    displayMode.value = 'collapseFirstLast'; // Switch to collapse first/last
  }
  currentPage.value = 0; // Reset pagination when changing mode
};

const nextPage = () => {
  if (currentPage.value < totalPages.value - 1) {
    currentPage.value++;
  }
};

const prevPage = () => {
  if (currentPage.value > 0) {
    currentPage.value--;
  }
};

const copyToClipboard = () => {
  navigator.clipboard.writeText(props.content)
    .then(() => {
      isCopied.value = true;
      setTimeout(() => {
        isCopied.value = false;
      }, 2000); // Revert after 2 seconds
    })
    .catch(err => {
      console.error('Failed to copy content: ', err);
      // Optionally provide error feedback to the user
    });
};

const checkIfTruncated = () => {
  lines.value = props.content.split('\n');
  if (lines.value.length > props.maxLines) {
    isTruncated.value = true;
    displayMode.value = 'paginate'; // Default to paginate if truncated
  } else {
    isTruncated.value = false;
    displayMode.value = 'showAll'; // Default to showAll if not truncated
  }
};

onMounted(() => {
  checkIfTruncated();
});
</script>

<style>
/* Styles are now centralized in assets/css/embeddings.css */
</style>