<template>
  <v-menu :close-on-content-click="false" offset-y>
    <template v-slot:activator="{ on }">
      <span :class="highlightStyle()" v-on="on">{{ token.text }}</span>
    </template>

    <v-list v-if="token.lexeme != null" aria-multiline="true">
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
            {{ token.lexeme }}
            <v-chip class="ma-1" outlined color="secondary" small>
              <v-avatar left class="mdi mdi-note-text"></v-avatar>
              {{ renderMainAttributes() }}
            </v-chip>
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item
        v-if="renderAttributes() !== null || renderExtraAttributes() !== null"
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
            {{ token.text }}
          </v-list-item-title>
          <v-list-item-subtitle v-if="renderAttributes() !== null" three-line>
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
          <v-list-item-subtitle
            v-if="renderExtraAttributes() !== null"
            three-line
          >
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
import { RussianToken } from "@/backend/dto";

@Component
export default class extends Vue {
  @Prop()
  private readonly token!: RussianToken;
  @Prop()
  private readonly tokensIds!: number[] | null;

  renderAttributes(): Array<string> | null {
    const res = this.token.attributes
      ?.filter(a => a.name != "pos")
      .map(a => `${a.name} = ${a.value}`);
    if (res == null || res.length == 0) {
      return null;
    }
    return res;
  }

  renderMainAttributes(): string | null {
    const res = this.token.attributes
      ?.filter(a => a.name == "pos")
      .map(a => `${a.value}`);
    if (res == null || res[0] == null) {
      return null;
    }
    return res[0];
  }

  renderExtraAttributes(): Array<string> | null {
    if (this.token.extraAttributes?.length == 0) {
      return null;
    }
    return this.token.extraAttributes;
  }

  highlightStyle(): string {
    if (this.tokensIds == null) return "word-hover";

    return this.tokensIds.indexOf(this.token.id) === -1
      ? "word-hover"
      : "constant-yellow";
  }
}
</script>

<style lang="scss">
.word-hover:hover {
  background-color: yellow;
  color: black;
}
.constant-yellow {
  background-color: yellow;
  color: black;
}
</style>
