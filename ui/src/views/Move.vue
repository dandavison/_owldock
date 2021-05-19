<template>
  <section class="section">
    <p class="m-4 is-size-2">Moving</p>
    <p class="m-4 is-size-4">
      Owldock has one work-in-progress UI related to working with in-progress
      moves:
    </p>
    <ul>
      <li>
        <portal-zone-card
          link="/portal/cases"
          buttonLabel="My cases"
          buttonColor="#e3efda"
        >
          <ul>
            <li>
              View a table displaying summary information for each of your cases
            </li>
            <li>
              Click on a case to
              <ul>
                <li>View case status</li>
                <li>Change case status</li>
                <li>Change providers</li>
                <li>Exchange documents with provider</li>
              </ul>
            </li>
          </ul>
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
