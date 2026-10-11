export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        paper: "var(--paper)",
        "paper-dim": "var(--paper-dim)",
        ink: "var(--ink)",
        "ink-soft": "var(--ink-soft)",
        rule: "var(--rule)",
        "rule-strong": "var(--rule-strong)",
        "risk-critical": "var(--risk-critical)",
        "risk-warning": "var(--risk-warning)",
        "risk-safe": "var(--risk-safe)",
        info: "var(--info)",
      },
      fontFamily: {
        serif: ["Fraunces", "serif"],
        sans: ["Public Sans", "-apple-system", "BlinkMacSystemFont", "sans-serif"],
        mono: ["ui-monospace", "SFMono-Regular", "Menlo", "Monaco", "Consolas", "monospace"],
      },
      borderRadius: {
        none: "0px",
        DEFAULT: "0px",
      },
      transitionTimingFunction: {
        editorial: "cubic-bezier(0.16, 1, 0.3, 1)",
      },
    },
  },
  plugins: [],
};
