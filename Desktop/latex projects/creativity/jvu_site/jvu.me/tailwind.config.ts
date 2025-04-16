import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        'custom-gray': '#222222',
      },
      backgroundImage: {
        'dot-pattern': 'radial-gradient(circle, #888888 0.5px, transparent 0.5px)',
      },
      backgroundSize: {
        'dot-pattern': '5px 5px',
      },
      fontSize: {
        '2xs': '0.70rem',
        '3xs': '0.55rem',
      },
      animation: {
        'pokemon-pixel-move': 'pokemon-pixel-move 0.8s steps(2, end) infinite',
        'pulse-gentle': 'pulse-gentle 3s ease-in-out infinite',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        'pokemon-pixel-move': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-2px)' },
        },
        'pulse-gentle': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.7' },
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-5px)' },
        },
      },
      letterSpacing: {
        'very-tight': '-0.025em',
      },
      transitionProperty: {
        'height': 'height',
        'spacing': 'margin, padding',
      },
    },
  },
  plugins: [],
};

export default config;
