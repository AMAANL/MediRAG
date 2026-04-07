/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          900: '#0A2342',
        },
        teal: {
          600: '#0D9488',
        }
      }
    },
  },
  plugins: [],
}
