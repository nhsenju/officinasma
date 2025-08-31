/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        slate: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        },
        blue: {
          500: '#3b82f6',
          600: '#2563eb',
        },
        violet: {
          500: '#8b5cf6',
        },
        emerald: {
          500: '#10b981',
        },
        orange: {
          500: '#f97316',
        },
        purple: {
          500: '#8b5cf6',
        },
        cyan: {
          500: '#06b6d4',
        },
        red: {
          600: '#dc2626',
        },
        green: {
          100: '#dcfce7',
          800: '#166534',
        },
        yellow: {
          100: '#fef3c7',
          800: '#92400e',
        },
      },
      fontFamily: {
        sans: ['Open Sans', 'sans-serif'],
      },
      boxShadow: {
        'soft-xl': '0 20px 27px 0 rgba(0, 0, 0, 0.05)',
        'soft-2xl': '0 0.5rem 1.5rem 0.75rem rgba(0, 0, 0, 0.08)',
        'soft-3xl': '0 8px 26px 0 rgba(0, 0, 0, 0.15)',
      },
      borderRadius: {
        '2xl': '1rem',
      },
      spacing: {
        '19': '4.75rem',
        '68': '17rem',
      },
      zIndex: {
        '990': '990',
      },
    },
  },
  plugins: [],
}
