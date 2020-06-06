<template>
  <v-card outlined class="mt-3">
    <div class="pl-6 pr-6 pt-4">
    <russian-token
      v-for="token in result.sentencePair.russian.tokens"
      :key="result.sentencePair.id + 'ru' + token.id"
      :token="token"
      :tokens-ids="russianTokens()"
    />
    </div>
    <br />
    <div class="pl-6 pr-6">
    <japanese-token
      v-for="token in result.sentencePair.japanese.tokens"
      :key="result.sentencePair.id + 'ja' + token.id"
      :token="token"
      :tokens-ids="japaneseTokens()"
    />
    </div>
    <br />
    <div class="pb-2 pr-3">
    <v-row dense no-gutters>
      <v-spacer />
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn icon color="primary" v-on="on" @click="openSourceText()">
            <v-icon>mdi-script-text-outline</v-icon>
          </v-btn>
        </template>
        <span>Полный текст</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn icon color="primary" v-on="on" @click="openRussianSource()">
            RU
          </v-btn>
        </template>
        <span>Русский источник</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn icon color="primary" v-on="on" @click="openJapaneseSource()">
            JA
          </v-btn>
        </template>
        <span>Японский источник</span>
      </v-tooltip>
    </v-row>
    </div>
  </v-card>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { Language, Result } from "@/backend/dto";
import RussianToken from "@/components/RussianToken.vue";
import JapaneseToken from "@/components/JapaneseToken.vue";
@Component({
  components: { JapaneseToken, RussianToken }
})
export default class extends Vue {
  @Prop()
  private readonly result!: Result;
  @Prop()
  private readonly searchLanguage!: Language;

  openSourceText() {
    window.open(`/entry/${this.result.entryId}`, "_blank");
  }

  openJapaneseSource() {
    window.open(this.result.entryUrl.japanese, "_blank");
  }

  openRussianSource() {
    window.open(this.result.entryUrl.russian, "_blank");
  }

  russianTokens(): number[] {
    return this.searchLanguage === "RUSSIAN"
      ? this.result.tokenIds == null
        ? []
        : this.result.tokenIds
      : [];
  }
  japaneseTokens(): number[] | null {
    return this.searchLanguage === "JAPANESE"
      ? this.result.tokenIds == null
        ? null
        : this.result.tokenIds
      : null;
  }
}
</script>
