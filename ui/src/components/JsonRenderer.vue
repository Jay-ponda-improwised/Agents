<template>
  <div class="json-renderer">
    <vue-json-pretty
      :data="parsedJson"
      :deep="3"
      showLine
      showDoubleQuotes
      showIcon
      editable
    />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import VueJsonPretty from 'vue-json-pretty';
import '../assets/css/json-pretty.css';

const props = defineProps({
  jsonString: {
    type: String,
    required: true,
  },
});

const extractedJsonString = computed(() => {
  const markdownJsonRegex = /```json\s*([\s\S]*?)\s*```/;
  const match = props.jsonString.match(markdownJsonRegex);
  return match ? match[1] : props.jsonString;
});

const parsedJson = computed(() => {
  try {
    return JSON.parse(extractedJsonString.value);
  } catch (e) {
    return {
      error: "Invalid JSON format",
      details: e.message,
      originalInput: props.jsonString,
    };
  }
});
</script>

<style scoped>
.json-renderer {
  text-align: left;
  /* Add any specific styling for the JsonRenderer container */
}
</style>