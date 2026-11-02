/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        roadvision: {
          sidebar: "#0B192C",
          sidebarHover: "#162842",
          sidebarActive: "#1C3558",
          cardBg: "#FFFFFF",
          pageBg: "#F8FAFC",
          accentOrange: "#F97316",
          accentBlue: "#0284C7",
          accentCyan: "#06B6D4",
          accentDark: "#1E293B",
          demoBannerBg: "#FEF3C7",
          demoBannerText: "#D97706",
          demoBannerBorder: "#FDE68A",
        }
      }
    },
  },
  plugins: [],
}
