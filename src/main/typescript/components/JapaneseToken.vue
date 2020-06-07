<template>
  <v-menu :close-on-content-click="false" offset-y>
    <template v-slot:activator="{ on }">
      <ruby
        ><rb :class="highlightStyle()" v-on="on">{{ token.text }}</rb>
        <rt>{{ displayFurigana(token) }}</rt></ruby
      >
    </template>

    <v-list v-if="token.lexeme !== null" aria-multiline="true">
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>
            <v-chip
              class="ma-1 pl-sm-1 pr-sm-1"
              outlined
              color="secondary"
              x-small
            >
              <div class="mdi mdi-chevron-right"></div>
            </v-chip>
            {{ token.lexeme }} 〖{{ displayLexeme(token) }}〗
            <v-chip class="ma-1" outlined color="secondary" small>
              <v-avatar left class="mdi mdi-note-text"></v-avatar>
              {{ renderMainAttributes() }}
            </v-chip>
            <v-chip
              v-if="renderReadingType(token) != null"
              class="ma-1"
              outlined
              color="secondary"
              small
            >
              <v-avatar left>
                読
              </v-avatar>
              {{ renderReadingType(token) }}
            </v-chip>
          </v-list-item-title>
          <v-list-item-subtitle>
            <div v-if="token.translation !== null">
              <div v-html="token.translation"></div>
            </div>
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-list-item
        v-if="renderAttributes() !== null || renderExtraAttributes() != null"
        three-line
      >
        <v-list-item-content>
          <v-list-item-title>
            <v-chip
              class="ma-1 pl-sm-1 pr-sm-1"
              outlined
              color="secondary"
              x-small
            >
              <div class="mdi mdi-chevron-down"></div>
            </v-chip>
            {{ token.text }} 〖{{ displayReading(token) }}〗</v-list-item-title
          >
          <v-list-item-subtitle v-if="renderAttributes() !== null">
            <v-chip
              v-for="item in renderAttributes()"
              :key="item"
              class="ma-1"
              outlined
              color="secondary"
              small
            >
              <v-avatar left class="mdi mdi-tag-text"></v-avatar>
              {{ item }}
            </v-chip>
          </v-list-item-subtitle>
          <v-list-item-subtitle v-if="renderExtraAttributes() !== null">
            <v-chip
              v-for="item in renderExtraAttributes()"
              :key="item"
              class="ma-1"
              outlined
              color="secondary"
              small
            >
              <v-avatar left class="mdi mdi-tag-text-outline"></v-avatar>
              {{ item }}
            </v-chip>
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { JapaneseToken } from "@/backend/dto";
import { settingsModule } from "@/plugins/store/settings-module";

@Component
export default class extends Vue {
  @Prop()
  private readonly token!: JapaneseToken;
  @Prop()
  private readonly tokensIds!: number[] | null;

  private settingsStore = settingsModule.context(this.$store);

  renderMainAttributes(): string | null {
    const type = this.token.attributes?.filter(e => e.name == "type");
    const pos = this.token.attributes?.filter(e => e.name == "pos");

    if (type == null || type.length == 0) {
      if (pos != null) {
        return pos[0].value;
      }
    } else {
      if (pos != null) {
        return type[0].value + " " + pos[0].value;
      }
    }
    return null;
  }

  renderAttributes(): Array<string> | null {
    const res = this.token.attributes
      ?.filter(
        a =>
          a.name !== "romaji_reading" &&
          a.name !== "category" &&
          a.name !== "domain" &&
          a.name !== "lexeme_reading" &&
          a.name !== "romanized_lexeme_reading" &&
          a.name !== "type" &&
          a.name !== "pos" &&
          a.name !== "reading_type"
      )
      .map(a => `${a.name} = ${a.value}`);
    if (res == null) {
      return null;
    }
    return res;
  }

  renderExtraAttributes(): Array<string> | null {
    return this.token.extraAttributes;
  }

  highlightStyle(): string {
    if (this.tokensIds == null) return "word-hover";

    return this.tokensIds.indexOf(this.token.id) === -1
      ? "word-hover"
      : "constant-yellow";
  }

  displayFurigana(token: JapaneseToken): string | null {
    if (!this.settingsStore.getters.isFurigana) {
      return null;
    }
    return this.displayReading(token);
  }

  renderReadingType(token: JapaneseToken): string | null {
    const rt = token.attributes?.filter(a => a.name == "reading_type");
    if (rt == null || rt[0] == null) {
      return null;
    } else {
      return rt[0].value;
    }
  }

  displayReading(token: JapaneseToken): string | null {
    if (token.reading !== null) {
      if (token.extraAttributes?.indexOf("unknown_reading") != -1) {
        return "?";
      }
      const readingType = this.settingsStore.getters.reading;
      if (readingType == "Hiragana") {
        return token.reading;
      } else {
        const attrs = token.attributes;
        const reading = attrs?.filter(e => e.name == "romaji_reading")[0];
        return reading?.value ?? null;
      }
    } else {
      return null;
    }
  }

  displayLexeme(token: JapaneseToken): string | null {
    if (token.reading !== null) {
      if (token.extraAttributes?.indexOf("unknown_reading") != -1) {
        return "?";
      }
      const readingType = this.settingsStore.getters.reading;
      if (readingType == "Hiragana") {
        const reading = token?.attributes?.filter(
          e => e.name == "lexeme_reading"
        )[0];
        return reading?.value ?? null;
      } else {
        const reading = token?.attributes?.filter(
          e => e.name == "romanized_lexeme_reading"
        )[0];
        return reading?.value ?? null;
      }
    } else {
      return null;
    }
  }
}
</script>

<style lang="scss" scoped>
.word-hover:hover {
  background-color: yellow;
  color: black;
}
.constant-yellow {
  background-color: yellow;
  color: black;
}
</style>
