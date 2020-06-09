<template>
  <div>
    <v-card-text v-if="entry !== null">
        <v-row>
          <v-col cols="10">
            <div>
              <a target="_blank" :href="entry.url.russian">
                {{ entry.title.russian }}
              </a>
            </div>
            <div>
              <a target="_blank" :href="entry.url.japanese">
                {{ entry.title.japanese }}
              </a>
            </div>
          </v-col>
          <v-col align-self="center">
            <v-btn block color="primary" :loading="loading" :disabled="loading" @click="downloadEntry(entry.id)">
              <v-icon left>mdi-download</v-icon>
              Скачать
            </v-btn>
          </v-col>
        </v-row>
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

  downloadEntry(id: string) {
    let url = api.loadEntryUrl(id);
    window.open(url);
  }
}
</script>
