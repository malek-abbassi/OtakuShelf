// Theme utilities composable for OtakuShelf
export function useOtakuTheme() {
  const colorMode = useColorMode();

  // Theme-aware classes helper using semantic color aliases
  function getThemeClasses(lightClass: string, darkClass?: string) {
    return darkClass ? `${lightClass} dark:${darkClass}` : lightClass;
  }

  // Anime-themed gradients using theme aliases
  const animeGradients = {
    primary: 'bg-gradient-to-r from-primary-600 to-secondary-600 dark:from-primary-500 dark:to-secondary-500',
    secondary: 'bg-gradient-to-r from-accent-500 to-primary-600 dark:from-accent-400 dark:to-primary-500',
    hero: 'anime-gradient', // Uses the CSS class defined in main.css
    success: 'bg-gradient-to-r from-success-500 to-success-600',
    warning: 'bg-gradient-to-r from-warning-500 to-warning-600',
    error: 'bg-gradient-to-r from-error-500 to-error-600',
  };

  // Semantic color mappings using theme aliases
  const colors = {
    primary: 'primary',
    secondary: 'secondary',
    accent: 'accent',
    success: 'success',
    warning: 'warning',
    error: 'error',
    info: 'info',
    neutral: 'gray',
  };

  // Helper function to get semantic color classes
  function getColorClass(color: keyof typeof colors, shade = '500', prefix = 'text') {
    return `${prefix}-${colors[color]}-${shade} dark:${prefix}-${colors[color]}-${shade === '500' ? '400' : shade}`;
  }

  return {
    colorMode,
    getThemeClasses,
    animeGradients,
    colors,
    getColorClass,
  };
}
