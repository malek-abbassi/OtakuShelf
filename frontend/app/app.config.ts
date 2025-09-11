export default defineAppConfig({
  ui: {
    // Primary brand color for OtakuShelf - anime/otaku themed
    primary: 'violet',

    // Gray color for neutral elements
    gray: 'neutral',

    // Custom theme strategy
    strategy: 'merge',

    // Custom semantic color mappings
    colors: {
      // Brand colors
      primary: 'violet',
      secondary: 'blue',
      accent: 'pink',

      // Semantic colors using aliases
      success: 'emerald',
      warning: 'amber',
      error: 'red',
      info: 'blue',

      // Neutral colors
      gray: 'neutral',
    },
  },
});
