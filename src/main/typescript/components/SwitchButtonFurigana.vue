<template>
  <v-btn icon @click="furigana = !furigana">
    <ruby
      ><rt>{{
        furigana
          ? this.settingsStore.getters.reading === "Hiragana"
            ? "あ"
            : "a"
          : ""
      }}</rt
      >ア</ruby
    >
  </v-btn>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { Reading, settingsModule } from "@/plugins/store/settings-module";

@Component
export default class extends Vue {
  private settingsStore = settingsModule.context(this.$store);

  set furigana(value: boolean) {
    this.settingsStore.actions.setFurigana(value);
  }

  get furigana() {
    return this.settingsStore.getters.isFurigana;
  }
}
</script>
