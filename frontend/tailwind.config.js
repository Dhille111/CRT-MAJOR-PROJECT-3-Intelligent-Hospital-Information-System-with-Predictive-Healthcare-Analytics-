/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      colors: {
        brand: {
          50: "#f0fbf9",
          100: "#dbf4ef",
          200: "#b7e9df",
          300: "#86d7c7",
          400: "#54beab",
          500: "#269683",
          600: "#1b7a6a",
          700: "#166456",
          800: "#125146",
          900: "#0e3e36",
        },
        medical: {
          50: "#f4f8fd",
          100: "#e7effb",
          200: "#cde0f7",
          300: "#a2c4f1",
          400: "#6fa3e8",
          500: "#4382dc",
          600: "#3164b3",
          700: "#275193",
          800: "#1d3e71",
          900: "#152c50",
        },
        emerald: {
          50: "#f0fdf4",
          100: "#dcfce7",
          200: "#bbf7d0",
          300: "#86efac",
          400: "#4ade80",
          500: "#22c55e",
          600: "#16a34a",
          700: "#15803d",
          800: "#166534",
          900: "#14532d",
        },
        ink: {
          50: "#f8faf9",
          100: "#edf2f1",
          200: "#d9e3e1",
          300: "#b9c9c5",
          400: "#8c9f9a",
          500: "#667671",
          600: "#4c5b57",
          700: "#35423f",
          800: "#24312e",
          900: "#15201e",
        },
      },
      boxShadow: {
        soft: "0 24px 72px rgba(19, 32, 30, 0.08)",
        glow: "0 0 0 1px rgba(255,255,255,0.7), 0 18px 48px rgba(19, 32, 30, 0.10)",
      },
      backgroundImage: {
        "hero-radial":
          "radial-gradient(circle at top left, rgba(38, 150, 131, 0.12), transparent 26%), radial-gradient(circle at top right, rgba(67, 130, 220, 0.08), transparent 24%), radial-gradient(circle at bottom left, rgba(84, 190, 171, 0.08), transparent 28%)",
      },
      keyframes: {
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-10px)" },
        },
        fadeUp: {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
      animation: {
        float: "float 8s ease-in-out infinite",
        fadeUp: "fadeUp 0.5s ease-out both",
      },
    },
  },
  plugins: [],
};
