import { defineNuxtPlugin } from 'nuxt/app';
import SuperTokens from 'supertokens-web-js';
import EmailPassword from 'supertokens-web-js/recipe/emailpassword';
import Session from 'supertokens-web-js/recipe/session';

export default defineNuxtPlugin(() => {
  SuperTokens.init({
    appInfo: {
      appName: 'OtakuShelf',
      apiDomain: 'http://127.0.0.1:8000',
      apiBasePath: '/auth',
    },
    recipeList: [
      EmailPassword.init(),
      Session.init(),
    ],
  });
});
