<template>
  <v-btn icon @click="furigana = !furigana">
    <ruby>
      <rt>
        {{ renderFurigana() }}
      </rt>
      ア
    </ruby>
  </v-btn>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { settingsModule } from "@/plugins/store/settings-module";

@Component
export default class extends Vue {
  private settingsStore = settingsModule.context(this.$store);

  set furigana(value: boolean) {
    this.settingsStore.actions.setFurigana(value);
  }

  get furigana() {
    return this.settingsStore.getters.isFurigana;
  }

  renderFurigana(): string {
    return this.furigana
      ? this.settingsStore.getters.reading === "Hiragana"
        ? "あ"
        : "a"
      : "";
  }
}
</script>
