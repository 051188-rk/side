import type { Config } from "tailwindcss"

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./app/**/*.{ts,tsx}",
    "./src/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Strict Dark Mode - Grayscale Only
        background: "#000000",
        surface: "#0A0A0A",
        border: "#1A1A1A",
        "text-primary": "#FFFFFF",
        "text-secondary": "#8A8A8A",
        "text-tertiary": "#4A4A4A",
      },
      fontFamily: {
        sans: ["var(--font-plus-jakarta-sans)", "system-ui", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      fontSize: {
        "xs": ["12px", { lineHeight: "1.4", letterSpacing: "0", fontWeight: "300" }],
        "sm": ["13px", { lineHeight: "1.4", letterSpacing: "0", fontWeight: "300" }],
        "base": ["13px", { lineHeight: "1.5", letterSpacing: "0", fontWeight: "400" }],
        "lg": ["14px", { lineHeight: "1.5", letterSpacing: "0", fontWeight: "400" }],
        "xl": ["16px", { lineHeight: "1.5", letterSpacing: "0", fontWeight: "400" }],
        "2xl": ["18px", { lineHeight: "1.4", letterSpacing: "0", fontWeight: "500" }],
        "3xl": ["24px", { lineHeight: "1.3", letterSpacing: "-0.5px", fontWeight: "500" }],
        "4xl": ["32px", { lineHeight: "1.2", letterSpacing: "-1px", fontWeight: "500" }],
      },
      borderRadius: {
        none: "0px",
        sm: "2px",
        DEFAULT: "0px",
      },
      spacing: {
        "1": "4px",
        "2": "8px",
        "3": "16px",
        "4": "24px",
        "5": "32px",
        "6": "48px",
        "7": "64px",
        "8": "96px",
      },
    },
  },
  plugins: [],
}

export default config
