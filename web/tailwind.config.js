/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        space: {
          bg: "#0B1220",
          surface1: "#121C2F",
          surface2: "#1A2740",
        },
        accent: {
          cyan: "#22D3EE",
          violet: "#8B5CF6",
        },
        verdict: {
          ac: "#22C55E",
          wa: "#EF4444",
          tle: "#F59E0B",
        },
        diff: {
          easy: "#34D399",
          medium: "#FBBF24",
          hard: "#F472B6",
        }
      },
    },
  },
  plugins: [],
}
