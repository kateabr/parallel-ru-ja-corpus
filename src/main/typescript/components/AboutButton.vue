<template>
  <v-btn depressed small color="primary" @click="$router.push('/about')">
    <v-icon left>mdi-information-outline</v-icon>
    О корпусе
  </v-btn>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class extends Vue {}
</script>
