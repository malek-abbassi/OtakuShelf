// Global error handling composable

export type AppError = {
  message: string;
  code?: string | number;
  statusCode?: number;
  details?: any;
  retryable?: boolean;
  timestamp?: number;
};

export type ToastMessage = {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message?: string;
  duration?: number;
  action?: {
    label: string;
    handler: () => void;
  };
};

// Reactive state
const toasts = ref<ToastMessage[]>([]);
const isOnline = ref(true);
const networkErrors = ref<AppError[]>([]);

// Network status detection
function updateNetworkStatus() {
  isOnline.value = navigator.onLine;
}

if (typeof window !== 'undefined') {
  window.addEventListener('online', updateNetworkStatus);
  window.addEventListener('offline', updateNetworkStatus);
  updateNetworkStatus();
}

// Toast management
function removeToast(id: string) {
  const index = toasts.value.findIndex(toast => toast.id === id);
  if (index > -1) {
    toasts.value.splice(index, 1);
  }
}

function addToast(toast: Omit<ToastMessage, 'id'>) {
  const id = Date.now().toString();
  const newToast: ToastMessage = {
    id,
    duration: 5000,
    ...toast,
  };

  toasts.value.push(newToast);

  // Auto remove after duration
  if (newToast.duration && newToast.duration > 0) {
    setTimeout(() => {
      removeToast(id);
    }, newToast.duration);
  }

  return id;
}

function clearToasts() {
  toasts.value = [];
}

// Error handling utilities
function handleError(error: any, context?: string): AppError {
  console.error(`Error in ${context || 'unknown context'}:`, error);

  let appError: AppError;

  if (error instanceof Error) {
    appError = {
      message: error.message,
      details: error,
      timestamp: Date.now(),
    };
  }
  else if (typeof error === 'string') {
    appError = {
      message: error,
      timestamp: Date.now(),
    };
  }
  else if (error?.message) {
    appError = {
      message: error.message,
      code: error.code,
      statusCode: error.statusCode,
      details: error,
      timestamp: Date.now(),
    };
  }
  else {
    appError = {
      message: 'An unexpected error occurred',
      details: error,
      timestamp: Date.now(),
    };
  }

  // Check if it's a network error
  if (!isOnline.value || error?.code === 'NETWORK_ERROR' || error?.message?.includes('fetch')) {
    appError.retryable = true;
    networkErrors.value.push(appError);
  }

  return appError;
}

function showErrorToast(error: any, context?: string, action?: ToastMessage['action']) {
  const appError = handleError(error, context);

  addToast({
    type: 'error',
    title: 'Error',
    message: appError.message,
    action,
  });

  return appError;
}

function showSuccessToast(message: string, title = 'Success') {
  addToast({
    type: 'success',
    title,
    message,
  });
}

function showWarningToast(message: string, title = 'Warning') {
  addToast({
    type: 'warning',
    title,
    message,
  });
}

function showInfoToast(message: string, title = 'Info') {
  addToast({
    type: 'info',
    title,
    message,
  });
}

// Retry mechanism
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  baseDelay = 1000,
): Promise<T> {
  let lastError: any;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    }
    catch (error) {
      lastError = error;

      if (attempt < maxRetries - 1) {
        const delay = baseDelay * (2 ** attempt);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }

  throw lastError;
}

// Network error recovery
function clearNetworkErrors() {
  networkErrors.value = [];
}

const hasNetworkErrors = computed(() => networkErrors.value.length > 0);

// Export composable
export function useErrorHandler() {
  return {
    // State
    toasts: readonly(toasts),
    isOnline: readonly(isOnline),
    networkErrors: readonly(networkErrors),
    hasNetworkErrors,

    // Methods
    addToast,
    removeToast,
    clearToasts,
    handleError,
    showErrorToast,
    showSuccessToast,
    showWarningToast,
    showInfoToast,
    retryWithBackoff,
    clearNetworkErrors,
  };
}
