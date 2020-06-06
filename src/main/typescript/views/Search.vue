<template>
  <v-card>
    <v-card class="pa-3">
      <v-row>
        <v-col>
          <v-tabs v-model="searchMode">
            <v-tab key="0">Полнотекстовой поиск</v-tab>
            <v-tab key="1">Поиск по словоформам</v-tab>
          </v-tabs>
        </v-col>
        <v-col class="pa-md-4 mx-lg-auto">
          <v-radio-group v-model="searchLanguage" label="Язык поиска" row @change="attributeList.splice(0, attributeList.length)" >
            <v-radio label="Русский" value="RUSSIAN"  />
            <v-radio label="Японский" value="JAPANESE" />
          </v-radio-group>
        </v-col>
      </v-row>
      <v-tabs-items v-model="searchMode">
        <v-tab-item key="0" :transition="false" :reverse-transition="false">
          <v-text-field
            v-model="searchQuery"
            label="Слово или фраза"
            @click:clear="searchQuery = ''"
            @keydown.enter="search(1)"
          />
        </v-tab-item>
        <v-tab-item key="1" :transition="false" :reverse-transition="false">
          <v-text-field
            v-model="searchQuery"
            label="Слово или лексема"
            @click:clear="searchQuery = ''"
            @keydown.enter="search(1)"
          />
          <v-row>
            <v-col>
              <v-radio-group v-model="searchTokenType" label="Тип поиска" row>
                <v-radio label="Слово" value="WORD" />
                <v-radio label="Лексема" value="LEXEME" />
              </v-radio-group>
            </v-col>
          </v-row>
          <v-row v-for="item in attributeList" :key="attributeList.indexOf(item)">
            <v-col>
              <v-text-field
                    v-model="item.name"
                    dense
                    outlined
                    readonly
            ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                    v-model="item.value"
                    outlined
                    dense
                    readonly
            ></v-text-field></v-col>
            <v-col cols="1">
            <v-btn outlined color="red" class="mx-2" small fab
                   @click="attributeList.splice(attributeList.indexOf(item), 1)">
              <v-icon>mdi-minus-circle</v-icon>
            </v-btn>
            </v-col>
          </v-row>
          <v-row v-if="searchLanguage === 'JAPANESE'">
            <v-col>
              <v-autocomplete
                      v-model="attributePlaceholderName"
                      :items="attributeListNamesJa"
                      dense
                      outlined
                      label="Основной параметр"
              ></v-autocomplete>
            </v-col>
            <v-col>
              <v-autocomplete
                      v-model="attributePlaceholderValue"
                      :items="attributeListMapJa.get(attributePlaceholderName)"
                      outlined
                      dense
                      label="Значение параметра"
              ></v-autocomplete></v-col>
            <v-col cols="1">
              <v-btn :disabled="!(attributePlaceholderValue.length !== 0 && attributePlaceholderName.length !== 0)" outlined color="green" class="mx-2" small fab @click="attributeList.push({name: attributePlaceholderName,
              value: attributePlaceholderValue})">
                <v-icon>mdi-plus-circle</v-icon>
              </v-btn>
            </v-col>
          </v-row>
          <v-row v-if="searchLanguage === 'RUSSIAN'">
            <v-col>
              <v-autocomplete
                      v-model="attributePlaceholderName"
                      :items="attributeListNamesRu"
                      dense
                      outlined
                      label="Основной параметр"
              ></v-autocomplete>
            </v-col>
            <v-col>
              <v-autocomplete
                      v-model="attributePlaceholderValue"
                      :items="attributeListMapRu.get(attributePlaceholderName)"
                      outlined
                      dense
                      label="Значение параметра"
              ></v-autocomplete></v-col>
            <v-col cols="1">
              <v-btn :disabled="!(attributePlaceholderValue.length !== 0 && attributePlaceholderName.length !== 0)" outlined color="green" class="mx-2" small fab @click="attributeList.push({name: attributePlaceholderName,
              value: attributePlaceholderValue})">
                <v-icon>mdi-plus-circle</v-icon>
              </v-btn>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-autocomplete
                v-model="extraAttributeList"
                :items="[
                  'FamN',
                  'PersN',
                  'Human_name_or_family_name',
                  'Abbr',
                  'Content_word',
                  'Hiragana',
                  'Kanji',
                  'Katakana',
                  'Digits',
                  'unknown_reading',
                  'Progressive',
                  'unrecognized_symbols',
                  'Associated_content_word',
                  'Counting',
                  'To_supplement',
                  'Ender',
                  'Toponym',
                  'Address',
                  'Post',
                  'Organisation',
                  'Human_name'
                ]"
                outlined
                dense
                label="Дополнительные параметры"
                multiple
              ></v-autocomplete>
            </v-col>
          </v-row>
        </v-tab-item>
      </v-tabs-items>
      <v-row>
        <v-col cols="4"></v-col>
        <v-col cols="4">
      <v-btn
        block
        color="primary"
        :loading="loading"
        :disabled="searchQuery.trim() === ''"
        @click="search(1)"
      >
        <v-icon left class="mdi mdi-magnify"></v-icon>
        Поиск
      </v-btn>
        </v-col>
        <v-col cols="4"></v-col>
      </v-row>
    </v-card>

    <div v-if="searchResult !== null">
      <p>Всего результатов: {{ searchResult.totalCount }}</p>
      <p>Время запроса: {{ String(queryTime() / 1000.0) }} с</p>
      <v-btn
        block
        color="primary"
        :disabled="loading || results.length < 1"
        @click="downloadResults"
      >
        Скачать все результаты
      </v-btn>
      <sentence-pair-card
        v-for="result in results"
        :key="result.entryId + ',' + result.sentencePair.id"
        :result="result"
        :search-language="searchResult.request.language"
      />
    </div>

    <v-pagination
      :value="page"
      :length="numberOfPages()"
      :total-visible="7"
      :disabled="loading"
      @input="changePage"
    />

    <v-snackbar v-model="error">
      Не удалось обработать запрос
      <v-btn color="red" text @click="error = false">
        Скрыть
      </v-btn>
    </v-snackbar>
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";
import { Component, Watch } from "vue-property-decorator";
import {
  Attribute,
  Language,
  Result,
  SearchResult,
  TokenType
} from "@/backend/dto";
import { api } from "@/backend";
import { Dictionary } from "vue-router/types/router";
import SentencePairCard from "@/components/SentencePairCard.vue";
import { settingsModule } from "@/plugins/store/settings-module";

@Component({
  components: { SentencePairCard }
})
export default class extends Vue {
  private readonly settingsStore = settingsModule.context(this.$store);

  private searchResult: SearchResult | null = null;
  private results: Result[] = [];

  private page = 1;
  private itemsPerPage = this.settingsStore.getters.itemsPerPage;

  private searchQuery: string = "";
  private regex: boolean = false;
  private attributeList: Attribute[] = [];
  private attributeListNamesJa: string[] = ['pos', 'type'];
  private attributeListMapJa: Map<string, string[]> = new Map<string, string[]>([
                  ['pos', ['Noun', 'Verb']],
                  ['type', ['Common', 'Toponym', 'Human_name']]
          ]);
  private attributeListNamesRu: string[] = ['pos'];
  private attributeListMapRu: Map<string, string[]> = new Map<string, string[]>([
                  ['pos', ['Noun', 'Verb']]
          ]);
  private extraAttributeList: string[] = [];

  private searchMode: SearchMode = SearchMode.FULL_TEXT;
  private searchLanguage: Language = "RUSSIAN";
  private searchTokenType: TokenType = "WORD";

  private attributePlaceholderName = '';
  private attributePlaceholderValue = '';

  private loading = false;
  private error = false;

  async search(page: number) {
    this.page = page;

    this.updateUrlQuery();

    try {
      this.requestStarted();

      switch (this.searchMode) {
        case SearchMode.FULL_TEXT:
          this.searchResult = await api.fullTextSearch(
            this.searchQuery,
            this.searchLanguage,
            this.regex,
            this.offset(),
            this.itemsPerPage
          );
          break;
        case SearchMode.WORD_FORM:
          this.searchResult = await api.tokenSearch(
            this.searchQuery,
            this.searchLanguage,
            this.searchTokenType,
            this.attributeList,
            this.extraAttributeList,
            this.offset(),
            this.itemsPerPage
          );
          break;
      }
    } catch (e) {
      this.requestErrored(e);
    } finally {
      this.requestEnded();
    }
  }

  async downloadResults() {
    try {
      this.requestStarted();

      let url: string;
      switch (this.searchMode) {
        case SearchMode.FULL_TEXT:
          url = api.fullTextSearchDownloadUrl(
            this.searchQuery,
            this.searchLanguage,
            this.regex
          );
          break;
        case SearchMode.WORD_FORM:
          url = api.tokenSearchDownloadUrl(
            this.searchQuery,
            this.searchLanguage,
            this.searchTokenType,
            this.attributeList,
            this.extraAttributeList
          );
          break;
      }
      window.open(url, "_blank");
    } catch (e) {
      this.requestErrored(e);
    } finally {
      this.requestEnded();
    }
  }

  updateUrlQuery() {
    this.$router
      .push({
        name: "search",
        query: this.paramsToQuery()
      })
      .catch(reason => {
        // vue-router will throw NavigationDuplicated if the route is the same, do nothing
        if (reason.name === "NavigationDuplicated") {
          /* ignored */
        } else {
          console.log("Unexpected error during route navigation: " + reason);
        }
      });
  }

  @Watch("searchResult")
  queryTime(): number {
    if (this.searchResult === null) {
      return 0;
    }
    return this.searchResult.request.elapsedTime;
  }

  @Watch("searchResult")
  onSearchResultUpdate() {
    if (this.searchResult === null) return;
    this.results = this.searchResult.results;
  }

  changePage(page: number) {
    this.search(page);
  }

  numberOfPages(): number {
    if (this.searchResult === null) return 1;
    return Math.ceil(this.searchResult.totalCount / this.itemsPerPage);
  }

  offset(): number {
    return (this.page - 1) * this.itemsPerPage;
  }

  requestStarted() {
    this.loading = true;
  }

  requestEnded() {
    this.loading = false;
  }

  requestErrored(e: Error) {
    console.log("Search error: " + e);
    this.error = true;
  }

  paramsToQuery(): Dictionary<string | (string | null)[] | null | undefined> {
    const query: Dictionary<string | (string | null)[] | null | undefined> = {};

    query.searchQuery = this.searchQuery;
    query.searchLanguage = this.searchLanguage;
    query.searchMode = this.searchMode.toString();
    query.searchTokenType = this.searchTokenType;
    query.attributeList = JSON.stringify(this.attributeList);
    query.extraAttributeList = JSON.stringify(this.extraAttributeList);
    query.offset = this.offset().toString();
    query.limit = this.itemsPerPage.toString();

    return query;
  }

  created() {
    // map every known query parameter to UI

    const query = this.$route.query;
    this.searchQuery = (query.searchQuery as string) || this.searchQuery;
    this.searchLanguage =
      (query.searchLanguage as Language) || this.searchLanguage;
    this.searchMode =
      (Number(query.searchMode) as SearchMode) || this.searchMode;
    this.searchTokenType =
      (query.searchTokenType as TokenType) || this.searchTokenType;

    if (query.attributeList) {
      try {
        this.attributeList = JSON.parse(query.attributeList as string);
        // eslint-disable-next-line no-empty
      } catch (ignored) {}
    }
    if (query.extraAttributeList) {
      try {
        this.extraAttributeList = JSON.parse(
          query.extraAttributeList as string
        );
        // eslint-disable-next-line no-empty
      } catch (ignored) {}
    }

    this.itemsPerPage = Number(query.limit as string) || this.itemsPerPage;
    if (query.offset) {
      const offset = Number(query.offset as string) || 1;
      this.page = Math.floor(offset / this.itemsPerPage) + 1 || this.page;
    }
  }

  mounted() {
    const query = this.$route.query;
    if (query.searchQuery == null) return;
    this.search(this.page);
  }
}

enum SearchMode {
  FULL_TEXT = 0,
  WORD_FORM = 1
}
</script>
