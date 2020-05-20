<template>
  <div>
    <v-card-text v-if="entry !== null">
      <div>{{ entry.title.russian }} // {{ entry.url.russian }}</div>
      <div>{{ entry.title.japanese }} // {{ entry.url.japanese }}</div>
      <br />
      <div v-for="sp in entry.sentencePairs" :key="sp.id">
        <russian-token
          v-for="token in sp.russian.tokens"
          :key="sp.id + 'ru' + token.id"
          :token="token"
        />
        <br />
        <japanese-token
          v-for="token in sp.japanese.tokens"
          :key="sp.id + 'jap' + token.id"
          :token="token"
        />
        <hr />
      </div>
    </v-card-text>
    <div v-else-if="loading" class="text-center">
      <v-progress-circular indeterminate size="75" width="10" color="primary" />
    </div>
    <v-card-text v-else-if="error">Ошибка загрузки</v-card-text>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { Component } from "vue-property-decorator";
import { Entry } from "@/backend/dto";
import { api } from "@/backend";
import RussianToken from "@/components/RussianToken.vue";
import JapaneseToken from "@/components/JapaneseToken.vue";
@Component({
  components: { JapaneseToken, RussianToken }
})
export default class extends Vue {
  private entry: Entry | null = null;
  private loading: boolean = false;
  private error: boolean = false;

  async mounted() {
    const id = this.$route.params.id;
    try {
      this.loading = true;
      this.entry = await api.loadEntry(id);
    } catch (ignored) {
      this.error = true;
    } finally {
      this.loading = false;
    }
  }
}
</script>
