<template>
  <div class="field has-addons" style="width: 100%">
    <p class="control" style="width: 100%">
      <b-field :label="label">
        <b-autocomplete
          ref="autocomplete"
          v-model="input"
          field="displayName"
          :data="filteredCandidates"
          @select="
            (providerContact) =>
              $emit('change:provider-contact', providerContact)
          "
          :openOnFocus="true"
          :keep-first="true"
          dropdown-position="bottom"
          max-height="100vh"
        >
          <template slot-scope="props">
            {{ props.option.displayName }}
          </template>
        </b-autocomplete>
      </b-field>
    </p>
  </div>
</template>

<script lang="ts">
import { inputMatchesString } from "@/utils";
import Vue, { PropType } from "vue";
import { ProcessSerializer, ProviderContactSerializer } from "../api-types";
import { dismissMobileKeyboardOnDropdownScroll } from "../componentUtils";
import { processIsNull } from "@/factories";

export default Vue.extend({
  props: { label: String, process: Object as PropType<ProcessSerializer> },

  data() {
    return {
      input: "",
      providerContacts: [] as ProviderContactSerializer[],
    };
  },

  created() {
    if (!processIsNull(this.process)) {
      this.fetchProviderContacts(this.process);
    }
  },

  mounted() {
    dismissMobileKeyboardOnDropdownScroll(this, "autocomplete");
  },

  watch: {
    process: function (
      value: ProcessSerializer,
      oldValue: ProcessSerializer
    ): void {
      console.log("process changed:", oldValue, "->", value);
      this.fetchProviderContacts(value);
    },
  },

  computed: {
    filteredCandidates(): ProviderContactSerializer[] {
      return this.providerContacts
        .filter((providerContact) =>
          inputMatchesString(this.input, displayName(providerContact))
        )
        .map((providerContact) => {
          return Object.assign(providerContact, {
            displayName: displayName(providerContact),
          });
        });
    },
  },

  methods: {
    fetchProviderContacts(process_: ProcessSerializer) {
      if (!process_.id) {
        // TODO: why?
        return;
      }
      fetch(
        `${process.env.VUE_APP_SERVER_URL}/api/client-contact/list-provider-contacts/?process_id=${process_.id}`
      )
        .then((resp) => resp.json())
        .then((data) => (this.providerContacts = data));
    },
  },
});

function displayName(providerContact: ProviderContactSerializer): string {
  return `${providerContact.user.first_name} ${providerContact.user.last_name} (${providerContact.provider.name})`;
}
</script>
