<template>
  <section class="section">
    <form>
      <b-field label="Host country">
        <b-input v-model="form.host_country"></b-input>
      </b-field>
      <b-field label="Target entry date">
        <b-input v-model="form.target_entry_date"></b-input>
      </b-field>
      <b-field label="Case type">
        <b-input v-model="form.case_type"></b-input>
      </b-field>
      <!-- <b-field label="End date of assignment"><b-input></b-input></b-field> -->
      <b-field label="Service required">
        <b-input v-model="form.service"></b-input>
      </b-field>
      <div class="field is-grouped">
        <div class="control">
          <button class="button is-link" @click="handleSubmit">Submit</button>
        </div>
        <div class="control">
          <button class="button is-link is-light">Cancel</button>
        </div>
      </div>
    </form>
  </section>
</template>

<script lang="ts">
import Vue from "vue";
import Cookies from "js-cookie";
import { CaseSerializer } from "../api-types";

export default Vue.extend({
  props: { employeeId: Number },

  data() {
    return {
      form: {
        employee: this.employeeId,
        case_type: "",
        current_status: "UNASSIGNED",
        host_country: "",
        progress: 0,
        service: "",
        target_entry_date: "",
      } as CaseSerializer,
    };
  },

  methods: {
    handleSubmit() {
      const headers = {
        "Content-Type": "application/json",
      } as any;
      const csrf_token = Cookies.get("csrftoken");
      if (csrf_token) {
        headers["X-CSRFToken"] = csrf_token;
      }

      fetch(`${process.env.VUE_APP_SERVER_URL}/api/cases/`, {
        method: "POST",
        headers,
        body: JSON.stringify(this.form),
      });
    },
  },
});
</script>



    
