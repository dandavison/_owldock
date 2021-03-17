<template>
  <section class="section">
    <p class="m-4 is-size-2">Initiate new work</p>
    <form>
      <b-field label="Employee first name">
        <b-input v-model="form.person.first_name"></b-input>
      </b-field>
      <b-field label="Employee surname">
        <b-input v-model="form.person.last_name"></b-input>
      </b-field>
      <!-- <b-field label="Nationality"
        ><b-input v-mode="form.person.nationality"></b-input
      ></b-field> -->
      <b-field label="Home country">
        <b-input v-model="form.person.home_country"></b-input>
      </b-field>
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
import { PersonImmigrationTaskSerializer } from "../api-types";

export default Vue.extend({
  data() {
    return {
      form: {
        person: {},
        case_type: "",
        current_status: "UNASSIGNED",
        host_country: "",
        progress: 0,
        service: "",
        target_entry_date: "",
      } as PersonImmigrationTaskSerializer,
    };
  },

  methods: {
    handleSubmit() {
      fetch("http://localhost:8000/api/person-immigration-tasks/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.form),
      });
    },
  },
});
</script>



    
