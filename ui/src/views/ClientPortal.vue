<template>
  <section class="section">
    <p class="m-4 is-size-2">
      {{ welcomeMessage() }}
    </p>
    <p class="m-4 is-size-4">What would you like to do next?</p>
    <ul>
      <li>
        <router-link to="/portal/question">
          <b-button class="is-large m-4" style="background-color: #fff2cc">
            Ask a question
          </b-button>
        </router-link>
      </li>
      <li>
        <router-link to="/portal/new-case">
          <b-button class="is-large m-4" style="background-color: #deebf7">
            Initiate new work
          </b-button>
        </router-link>
      </li>
      <li>
        <router-link to="/portal/cases">
          <b-button class="is-large m-4" style="background-color: #f8dcf7">
            View active cases
          </b-button>
        </router-link>
      </li>
      <li>
        <router-link to="/portal/providers">
          <b-button class="is-large m-4" style="background-color: #f8dcf7">
            View providers
          </b-button>
        </router-link>
      </li>
      <li>
        <router-link to="/portal/my-data">
          <b-button class="is-large m-4" style="background-color: #e3efda">
            Access my data
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
