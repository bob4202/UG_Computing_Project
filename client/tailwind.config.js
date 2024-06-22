/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {
      keyframes: {
        slidein: {
          from: {
            opacity: "0",
            transform: "translateY(-10px)",
          },
          to: {
            opacity: "1",
            transform: "translateY(0)",
          },
        },
      },
      animation: {
        slidein300: "slidein 1s ease 300ms",
        slidein500: "slidein 1s ease 500ms",
        slidein700: "slidein 1s ease 700ms",
        slidefromleft: {
          variants: {
            hidden: {
              opacity: 0,
              x: 1300,
            },
            visible: {
              opacity: 1,
              x: 0,
            },
            exit: {
              opacity: 0,
              x: 1300,
            },
          },
          initial: "hidden",
          animate: "visible",
          exit: "exit",
          transition: { duration: 1.5 },
        },
      },
      fontFamily: {
        roboto: ["Roboto Mono", "monospace"],
      },
    },
  },
  plugins: [],
};
