import path from 'path';
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: '../backend/src/public',
    emptyOutDir: true,
    sourcemap: process.env.NODE_ENV === 'development',
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path: string) => path.replace(/^\/api/, '')
      },
      '/docs': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path: string) => path.replace(/^\/docs/, '')
      }
    }
  }
})