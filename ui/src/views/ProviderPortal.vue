<template>
  <section class="section">
    <p class="m-4 is-size-2">
      {{ welcomeMessage() }}
    </p>
    <ul>
      <li>
        <router-link to="/cases">
          <b-button class="is-large m-4" style="background-color: #f8dcf7">
            View active cases
          </b-button>
        </router-link>
      </li>
    </ul>
  </section>
</template>

<script lang="ts">
import Vue from "vue";
import Cookies from "js-cookie";

export default Vue.extend({
  methods: {
    welcomeMessage(): string {
      const name = Cookies.get("first_name");
      if (name) {
        return `Hello ${name}, welcome to your dashboard!`;
      } else {
        return `Hello, welcome to your dashboard!`;
      }
    },
  },
});
</script>
