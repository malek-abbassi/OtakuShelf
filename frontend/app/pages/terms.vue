<script setup lang="ts">
useSeoMeta({
  title: 'Terms of Service - OtakuShelf',
  description: 'Terms of Service for OtakuShelf anime tracking platform',
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
            Terms of Service
          </h1>
          <p class="mt-4 text-lg text-neutral-600 dark:text-neutral-400">
            Last updated: {{ lastUpdated }}
          </p>
        </div>

        <!-- Content -->
        <div class="prose prose-neutral max-w-none dark:prose-invert">
          <h2>Acceptance of Terms</h2>
          <p>
            By accessing and using OtakuShelf, you accept and agree to be bound by the terms and provision of this agreement.
          </p>

          <h2>Use License</h2>
          <p>
            Permission is granted to temporarily download one copy of OtakuShelf for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title, and under this license you may not:
          </p>
          <ul>
            <li>modify or copy the materials</li>
            <li>use the materials for any commercial purpose or for any public display</li>
            <li>attempt to reverse engineer any software contained on OtakuShelf</li>
            <li>remove any copyright or other proprietary notations from the materials</li>
          </ul>

          <h2>User Accounts</h2>
          <p>
            When you create an account with us, you must provide information that is accurate, complete, and current at all times. You are responsible for safeguarding the password and for keeping your account information current.
          </p>

          <h3>Account Responsibilities</h3>
          <ul>
            <li>You are responsible for maintaining the security of your account</li>
            <li>You must not share your account credentials</li>
            <li>You must notify us immediately of any unauthorized use</li>
            <li>You are responsible for all activities under your account</li>
          </ul>

          <h2>User Content</h2>
          <p>
            Our service allows you to post, link, store, share and otherwise make available certain information, text, graphics, or other material. You are responsible for the content that you post to the service.
          </p>

          <h3>Content Guidelines</h3>
          <ul>
            <li>Do not post illegal, harmful, or offensive content</li>
            <li>Respect intellectual property rights</li>
            <li>Do not spam or post repetitive content</li>
            <li>Be respectful to other users</li>
          </ul>

          <h2>Service Availability</h2>
          <p>
            We strive to keep OtakuShelf available 24/7, but we cannot guarantee uninterrupted service. We may need to suspend the service for maintenance or updates.
          </p>

          <h2>Prohibited Uses</h2>
          <p>
            You may not use our service:
          </p>
          <ul>
            <li>For any unlawful purpose or to solicit others to unlawful acts</li>
            <li>To violate any international, federal, provincial, or state regulations, rules, laws, or local ordinances</li>
            <li>To infringe upon or violate our intellectual property rights or the intellectual property rights of others</li>
            <li>To harass, abuse, insult, harm, defame, slander, disparage, intimidate, or discriminate</li>
            <li>To submit false or misleading information</li>
          </ul>

          <h2>Termination</h2>
          <p>
            We may terminate or suspend your account and bar access to the service immediately, without prior notice or liability, under our sole discretion, for any reason whatsoever including but not limited to a breach of the Terms.
          </p>

          <h2>Limitation of Liability</h2>
          <p>
            In no case shall OtakuShelf, nor its directors, employees, partners, agents, suppliers, or affiliates, be liable for any indirect, incidental, punitive, consequential, or similar damages that result from the use of or inability to use the service.
          </p>

          <h2>Changes to Terms</h2>
          <p>
            We reserve the right, at our sole discretion, to modify or replace these Terms at any time. If a revision is material, we will try to provide at least 30 days notice prior to any new terms taking effect.
          </p>

          <h2>Contact Information</h2>
          <p>
            If you have any questions about these Terms of Service, please contact us at:
            <a href="mailto:legal@otakushelf.com">legal@otakushelf.com</a>
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
