/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.{html,js}",
    "./static/**/*.{html,js,css}"
  ],
  theme: {
    extend: {
      // ====== AURA WELLNESS GRADIENT ======
      backgroundImage: {
        'wellness': "linear-gradient(145deg, #89CFF0, #B0E0E6, #FFC0CB, #E6E6FA)"
      },

      // ====== CUSTOM ANIMATIONS ======
      keyframes: {
        softbreath: {
          '0%, 100%': { opacity: '1', transform: 'scale(1)' },
          '50%': { opacity: '0.80', transform: 'scale(1.05)' }
        },
        floatbutton: {
          '0%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-3px)' },
          '100%': { transform: 'translateY(0)' }
        },
        aura: {
          '0%,100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
      },
      animation: {
        softbreath: 'softbreath 4s ease-in-out infinite',
        floatbutton: 'floatbutton 2.5s ease-in-out infinite',
        aura: 'aura 12s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}
