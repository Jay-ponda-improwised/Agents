import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  define: {
    global: 'globalThis',
  },
  optimizeDeps: {
    esbuildOptions: {
      define: {
        global: 'globalThis',
      },
      plugins: [
        {
          name: 'fix-crypto',
          setup(build) {
            build.onResolve({ filter: /^crypto$/ }, args => {
              return { path: args.path, namespace: 'crypto-ns' }
            })
            build.onLoad({ filter: /.*/, namespace: 'crypto-ns' }, () => {
              return {
                contents: `
                  export const randomUUID = () => {
                    if (typeof window !== 'undefined' && window.crypto && window.crypto.randomUUID) {
                      return window.crypto.randomUUID();
                    }
                    // Fallback implementation for environments without crypto.randomUUID
                    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
                      const r = Math.random() * 16 | 0;
                      const v = c === 'x' ? r : (r & 0x3 | 0x8);
                      return v.toString(16);
                    });
                  };
                  export default { randomUUID };
                `,
                loader: 'js'
              }
            })
          }
        }
      ]
    }
  }
})