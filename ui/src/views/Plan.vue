<template>
  <section class="section">
    <p class="m-4 is-size-2">Planning</p>
    <p class="m-4 is-size-4">
      Owldock has one work-in-progress UIs related to planning:
    </p>
    <ul>
      <li>
        <portal-zone-card
          link="/portal/assessment"
          buttonLabel="'Assessment'"
          buttonColor="#f8dcf7"
        >
          <ol>
            <li>Select host country</li>
            <li>
              Optionally enter applicant nationality, dates,
              contract/compensation info
            </li>
            <li style="font-weight: bold">
              Owldock will tell you which immigration routes match your move,
              and the steps that will be involved
            </li>
          </ol>
          Note that this UI is also listed in the
          <router-link to="/portal/initiate">Initiating</router-link>
          section.
        </portal-zone-card>
      </li>
    </ul>
  </section>
</template>

<script lang="ts">
import Vue from "vue";
import PortalZoneCard from "@/components/PortalZoneCard.vue";

export default Vue.extend({
  components: { PortalZoneCard },
});
</script>
