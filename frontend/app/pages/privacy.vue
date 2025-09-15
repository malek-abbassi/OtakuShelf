<script setup lang="ts">
useSeoMeta({
  title: 'Privacy Policy - OtakuShelf',
  description: 'Privacy Policy for OtakuShelf anime tracking platform',
});

const lastUpdated = 'January 2024';
</script>

<template>
  <div class="min-h-screen bg-white dark:bg-neutral-950">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div class="space-y-8">
        <!-- Header -->
        <div class="text-center">
          <h1 class="text-4xl font-bold text-neutral-900 dark:text-white">
            Privacy Policy
          </h1>
          <p class="mt-4 text-lg text-neutral-600 dark:text-neutral-400">
            Last updated: {{ lastUpdated }}
          </p>
        </div>

        <!-- Content -->
        <div class="prose prose-neutral max-w-none dark:prose-invert">
          <h2>Information We Collect</h2>
          <p>
            At OtakuShelf, we collect information to provide better services to our users. We collect information in the following ways:
          </p>

          <h3>Information you give us</h3>
          <ul>
            <li>Account information such as username and email address</li>
            <li>Profile information and preferences</li>
            <li>Watchlist data and anime ratings</li>
            <li>Communications with us</li>
          </ul>

          <h3>Information we get from your use of our services</h3>
          <ul>
            <li>Device information</li>
            <li>Log information</li>
            <li>Location information</li>
            <li>Cookies and similar technologies</li>
          </ul>

          <h2>How We Use Information</h2>
          <p>
            We use the information we collect to:
          </p>
          <ul>
            <li>Provide, maintain, and improve our services</li>
            <li>Develop new features and services</li>
            <li>Provide personalized recommendations</li>
            <li>Communicate with you about services and features</li>
            <li>Protect against fraud and abuse</li>
          </ul>

          <h2>Information Sharing</h2>
          <p>
            We do not share personal information with companies, organizations, or individuals outside of OtakuShelf except in the following cases:
          </p>
          <ul>
            <li>With your consent</li>
            <li>For external processing by trusted partners</li>
            <li>For legal reasons</li>
          </ul>

          <h2>Data Security</h2>
          <p>
            We work hard to protect OtakuShelf and our users from unauthorized access to or unauthorized alteration, disclosure, or destruction of information we hold.
          </p>

          <h2>Data Retention</h2>
          <p>
            We retain personal data for as long as necessary to provide our services and for legitimate and essential business purposes.
          </p>

          <h2>Your Rights</h2>
          <p>
            You have the right to:
          </p>
          <ul>
            <li>Access your personal data</li>
            <li>Correct inaccurate data</li>
            <li>Request deletion of your data</li>
            <li>Object to processing of your data</li>
            <li>Data portability</li>
          </ul>

          <h2>Contact Us</h2>
          <p>
            If you have questions about this Privacy Policy, please contact us at:
            <a href="mailto:privacy@otakushelf.com">privacy@otakushelf.com</a>
          </p>
        </div>

        <!-- Back to home -->
        <div class="text-center pt-8">
          <UButton
            to="/"
            variant="outline"
            color="neutral"
            icon="i-heroicons-arrow-left"
          >
            Back to Home
          </UButton>
        </div>
      </div>
    </div>
  </div>
</template>
