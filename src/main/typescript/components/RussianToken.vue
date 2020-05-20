<template>
  <v-menu :close-on-content-click="false">
    <template v-slot:activator="{ on }">
      <span :class="highlightStyle()" v-on="on">{{ token.text }}</span>
    </template>

    <v-list two-line>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>Исходный текст</v-list-item-title>
          <v-list-item-subtitle>{{ token.text }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>Лексема</v-list-item-title>
          <v-list-item-subtitle>
            {{ token.lexeme || "Отсутствует" }}
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>Атрибуты</v-list-item-title>
          <v-list-item-subtitle>
            {{ renderAttributes() }}
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>Доп. атрибуты</v-list-item-title>
          <v-list-item-subtitle>
            {{ renderExtraAttributes() }}
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

  renderAttributes(): string {
    return (
      this.token.attributes?.map(a => `${a.name} = ${a.value}`)?.join(", ") ||
      "Отсутствуют"
    );
  }

  renderExtraAttributes(): string {
    return this.token.extraAttributes?.join(", ") || "Отсутствуют";
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
}
.constant-yellow {
  background-color: yellow;
}
</style>
