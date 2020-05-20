<template>
  <v-btn depressed small color="primary" @click="$router.push('/search')">
    <v-icon left>mdi-text-box-search-outline</v-icon>
    Поиск в корпусе
  </v-btn>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class extends Vue {}
</script>
