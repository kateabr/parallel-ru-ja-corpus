<template>
  <v-app>
    <the-app-bar />
    <v-content>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-content>
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import TheAppBar from "@/components/TheAppBar.vue";
import { Component } from "vue-property-decorator";

@Component({ components: { TheAppBar } })
export default class extends Vue {}
</script>
