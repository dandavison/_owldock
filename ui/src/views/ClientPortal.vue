<template>
  <section class="section">
    <p class="m-4 is-size-2">
      {{ welcomeMessage() }}
    </p>
    <p class="m-4 is-size-4">What would you like to do next?</p>
    <ul>
      <li>
        <portal-zone-card
          link="/portal/plan"
          buttonLabel="Plan"
          buttonColor="#f8dcf7"
        >
          <ul>
            <li>Get general immigration information for a country</li>
            <li>Find out if a move needs a work permit</li>
            <li>See timelines and costs for different immigration options</li>
          </ul>
        </portal-zone-card>
      </li>
      <li>
        <portal-zone-card
          link="/portal/initiate"
          buttonLabel="Initiate"
          buttonColor="#fff2cc"
        >
          <ul>
            <li>Describe your move</li>
            <li>Select a route</li>
            <li>Initiate a provider</li>
            <li>Assign steps to different providers</li>
          </ul>
        </portal-zone-card>
      </li>
      <li>
        <portal-zone-card
          link="/portal/move"
          buttonLabel="Move"
          buttonColor="#e3efda"
        >
          <ul>
            <li>See live case status updates</li>
            <li>Exchange documents and information with providers</li>
            <li>See costs and approve invoices</li>
          </ul>
        </portal-zone-card>
      </li>
      <li>
        <portal-zone-card
          link="/portal/report"
          buttonLabel="Report"
          buttonColor="#deebf7"
        >
          <ul>
            <li>Access your data</li>
            <li>Get reports on initiated cases</li>
            <li>Get reports on assessments and queries</li>
            <li>Track document expiration dates</li>
          </ul>
        </portal-zone-card>
      </li>
    </ul>
  </section>
</template>

<script lang="ts">
import Vue from "vue";
import Cookies from "js-cookie";
import PortalZoneCard from "@/components/PortalZoneCard.vue";

export default Vue.extend({
  components: { PortalZoneCard },
  methods: {
    welcomeMessage(): string {
      const name = Cookies.get("first_name");
      if (name) {
        return `Hello ${name}, welcome to Owldock!`;
      } else {
        return `Hello, welcome to Owldock!`;
      }
    },
  },
});
</script>
