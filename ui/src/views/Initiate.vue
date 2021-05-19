<template>
  <section class="section">
    <p class="m-4 is-size-2">Initiating</p>
    <p class="m-4 is-size-4">
      Owldock has two work-in-progress UIs related to initiation:
    </p>
    <ul>
      <li>
        <portal-zone-card
          link="/portal/assessment"
          buttonLabel="'Assessment'"
          buttonColor="#fff2cc"
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
          <router-link to="/portal/plan">Planning</router-link>
          section.
        </portal-zone-card>
      </li>
      <li>
        <portal-zone-card
          link="/portal/new-case"
          buttonLabel="'Create case'"
          buttonColor="#fff2cc"
        >
          <ol>
            <li>Select applicant</li>
            <li>Select Host country</li>
            <li>Select dates</li>
            <li>Select route</li>
            <li>Select provider</li>
            <li style="font-weight: bold">Confirm and initiate provider</li>
          </ol>
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
