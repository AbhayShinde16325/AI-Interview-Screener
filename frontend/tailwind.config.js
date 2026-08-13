/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        // Single restrained accent — a trustworthy job-board blue.
        brand: {
          50: '#f0f5ff',
          100: '#e0eafd',
          200: '#c2d5fb',
          300: '#94b8f7',
          400: '#5f92f0',
          500: '#3b6fe8',
          600: '#2a55d6',
          700: '#2343b4',
          800: '#223b90',
          900: '#213673',
        },
        // Near-black ink for text and dark surfaces.
        ink: {
          50: '#f5f6f8',
          100: '#eceef2',
          200: '#d4d9e1',
          300: '#aeb6c5',
          400: '#818ca1',
          500: '#5f6b80',
          600: '#4a5466',
          700: '#3c4453',
          800: '#252b36',
          900: '#12161d',
        },
      },
      fontFamily: {
        sans: [
          'Inter',
          'ui-sans-serif',
          'system-ui',
          '-apple-system',
          'Segoe UI',
          'Roboto',
          'Helvetica',
          'Arial',
          'sans-serif',
        ],
      },
      boxShadow: {
        card: '0 1px 2px 0 rgb(18 22 29 / 0.05)',
        pop: '0 8px 24px -8px rgb(18 22 29 / 0.18)',
      },
      maxWidth: {
        page: '72rem', // 1152px — comfortable reading width
      },
    },
  },
  plugins: [],
}
