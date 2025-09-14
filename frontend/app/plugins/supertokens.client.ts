import { defineNuxtPlugin } from 'nuxt/app';
import SuperTokens from 'supertokens-web-js';
import EmailPassword from 'supertokens-web-js/recipe/emailpassword';
import Session from 'supertokens-web-js/recipe/session';

export default defineNuxtPlugin(() => {
  SuperTokens.init({
    appInfo: {
      appName: 'OtakuShelf',
      apiDomain: 'http://localhost:8000', // Explicitly use localhost
      apiBasePath: '/auth',
    },
    recipeList: [
      EmailPassword.init(),
      Session.init(),
    ],
  });
});
