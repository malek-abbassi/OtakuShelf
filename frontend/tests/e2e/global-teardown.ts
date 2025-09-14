// Global teardown for Playwright tests
async function globalTeardown() {
  // Any cleanup needed after all tests complete
  console.warn('✅ Test teardown completed');
}

export default globalTeardown;
