<template>
  <section class="section">
    <p class="m-4 is-size-2">Hello (Name), welcome to your dashboard!</p>
    <p class="m-4 is-size-4">What would you like to do next?</p>
    <ul>
      <li>
        <router-link to="/question">
          <b-button class="is-large m-4" style="background-color: #fff2cc">
            Ask a question
          </b-button>
        </router-link>
      </li>
      <li>
        <router-link to="/initiate-new-work">
          <b-button class="is-large m-4" style="background-color: #deebf7">
            Initiate new work
          </b-button>
        </router-link>
      </li>
      <li>
        <router-link to="/work-in-progress">
          <b-button class="is-large m-4" style="background-color: #f8dcf7">
            View work in progress
          </b-button>
        </router-link>
      </li>
      <li>
        <router-link to="/access-data">
          <b-button class="is-large m-4" style="background-color: #e3efda">
            Access data
          </b-button>
        </router-link>
      </li>
    </ul>
  </section>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({});
</script>
