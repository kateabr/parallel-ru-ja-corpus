<template>
  <v-btn icon @click="reading = !reading">
    {{ reading ? "あ" : "A" }}
  </v-btn>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { settingsModule } from "@/plugins/store/settings-module";

@Component
export default class extends Vue {
  private settingsStore = settingsModule.context(this.$store);

  get reading() {
    return this.settingsStore.getters.isHiragana;
  }

  set reading(value: boolean) {
    this.settingsStore.actions.setReading(value ? "Hiragana" : "Romaji");
  }
}
</script>
