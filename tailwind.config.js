module.exports = {
  future: {
    removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: true,
  },
  content: {
    enabled: false,
    content: ['./**/templates/*.html', './**/templates/**/*.html'],
  },
  theme: {
    extend: {
      animation: {
        "slide-bottom": "key-slide-bottom 0.5s cubic-bezier(0.250, 0.460, 0.450, 0.940)    both",
        "scale-up-ver-top": "scale-up-ver-top 0.5s cubic-bezier(0.390, 0.575, 0.565, 1.000)   both"
      },
      keyframes: {
        "key-slide-bottom": {
          "0%": {
            transform: "translateY(-100%)"
          },
          to: {
            transform: "translateY(0)"
          }
        },
       "scale-up-ver-top": {
         "0%": {
           transform: "scaleY(0.0)",
           "transform-origin": "100% 0%"
         },
         to: {
           transform: "scaleY(1)",
           "transform-origin": "100% 0%"
         }
       }
      }
    },
  },
  variants: {},
  plugins: [],
}
