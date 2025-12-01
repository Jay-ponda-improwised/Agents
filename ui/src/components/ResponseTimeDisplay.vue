<template>
  <div class="response-time-display" v-if="responseTime !== null && responseTime !== undefined">
    <span class="response-time-label">Response time:</span>
    <span class="response-time-value">{{ typeof responseTime === 'number' ? responseTime.toFixed(2) : responseTime }}s</span>
  </div>
</template>

<script setup>
defineProps({
  responseTime: {
    type: [Number, String],
    default: null
  }
});
</script>

<style scoped>
/* Styles are now centralized in assets/css/response-time-display.css */
</style>