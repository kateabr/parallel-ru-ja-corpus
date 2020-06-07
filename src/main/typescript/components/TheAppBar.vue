<template>
  <v-app-bar app fixed color="primary" hide-on-scroll>
    <v-row id="logo-text" class="flex" @click="$router.push('/')">
      <v-col cols="1">
        <v-img class="right" src="../assets/logo_white.png" alt="logo" min-height="100%" min-width="100%" contain/>
      </v-col>
      <div class="col text-truncate">
      Параллельный Русско-Японский Корпус
      </div>
    </v-row>
    <v-spacer />
    <search-button />
    <about-button />
    <switch-button-furigana />
    <switch-button-reading />
    <!--<switch-button-locale />-->
    <switch-button-theme />
  </v-app-bar>
</template>

<script lang="ts">
import Vue from "vue";
import { Component } from "vue-property-decorator";
import SwitchButtonTheme from "@/components/SwitchButtonTheme.vue";
import SwitchButtonLocale from "@/components/SwitchButtonLocale.vue";
import AboutButton from "@/components/AboutButton.vue";
import SearchButton from "@/components/SearchButton.vue";
import SwitchButtonReading from "@/components/SwitchButtonReading.vue";
import SwitchButtonFurigana from "@/components/SwitchButtonFurigana.vue";

@Component({
  components: {
    SwitchButtonFurigana,
    SwitchButtonReading,
    SearchButton,
    AboutButton,
    SwitchButtonTheme,
    SwitchButtonLocale
  }
})
export default class extends Vue {}
</script>

<style>
#logo-text {
  cursor: pointer;
  font-size: 1.5em;
  font-weight: bold;
  color: white;
}
</style>
