import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

/**
 * Vite Configuration for Vercel Deployment
 * 
 * WHY THE MIME TYPE ERROR OCCURRED:
 * The original vercel.json used deprecated V2 configuration format with
 * "@vercel/static-build" builder. This caused Vercel to incorrectly detect
 * and serve Vite-built assets (/assets/*.js, /assets/*.css) with text/html
 * MIME type instead of application/javascript and text/css.
 * 
 * HOW THE FIX RESOLVES IT:
 * 1. No 'base' configuration ensures assets are served from root path
 * 2. Modern vercel.json uses 'buildCommand' and 'outputDirectory' explicitly
 * 3. Proper route rewrites ensure SPA routing works correctly
 * 4. Vercel's static file handling now correctly identifies MIME types
 * 
 * NOTE: Do NOT set base: "./" or base: "/something/" for Vercel root deployment
 * as this can cause asset path issues. Use base: "/" or omit base entirely.
 */
export default defineConfig({
  plugins: [react()],
  
  // Explicitly set base to root for Vercel deployment
  // This ensures assets are served from /assets/ not /something/assets/
  base: '/',
  
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
  
  build: {
    outDir: 'dist',
    sourcemap: true, // Enable sourcemaps for easier debugging
  },
})
