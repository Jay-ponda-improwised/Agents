import { ref, watch } from 'vue'

const isDark = ref(false)

// Check for saved theme preference or OS preference
if (typeof window !== 'undefined') {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme) {
    isDark.value = savedTheme === 'dark'
  } else {
    // Check OS preference
    isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
  }
}

// Apply theme class to document
watch(isDark, (newVal) => {
  if (typeof document !== 'undefined') {
    if (newVal) {
      document.documentElement.classList.add('dark')
      localStorage.setItem('theme', 'dark')
    } else {
      document.documentElement.classList.remove('dark')
      localStorage.setItem('theme', 'light')
    }
  }
}, { immediate: true })

export function useTheme() {
  const toggleDark = () => {
    isDark.value = !isDark.value
  }

  return {
    isDark,
    toggleDark
  }
}