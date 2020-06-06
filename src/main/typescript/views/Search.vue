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
          <v-radio-group v-model="searchLanguage" label="Язык поиска" row>
            <v-radio label="Русский" value="RUSSIAN" />
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
            <v-col>
              <v-btn @click="showAttributesList = true">
                Признаки
              </v-btn>
            </v-col>
            <v-col>
              <v-btn @click="showExtraAttributesList = true">
                Доп. признаки
              </v-btn>
            </v-col>
          </v-row>
          <v-dialog
            v-model="showAttributesList"
            transition="dialog-bottom-transition"
            hide-overlay
            fullscreen
            @keydown.esc="showAttributesList = false"
          >
            <v-card>
              <v-toolbar elevation="0">
                <v-btn icon @click="showAttributesList = false">
                  <v-icon>mdi-close</v-icon>
                </v-btn>
                <v-toolbar-title>Признаки</v-toolbar-title>
                <v-spacer />
                <v-btn type="primary" @click="showAttributesList = false">
                  Снять все выделение
                </v-btn>
              </v-toolbar>
              <v-card flat>
                <v-card-text>
                  <v-container fluid>
                    <v-row>
                      <v-col cols="12" sm="4" md="4">
                        <v-checkbox
                          label="red"
                          color="red"
                          value="red"
                          hide-details
                        ></v-checkbox>
                        <v-checkbox
                          label="red darken-3"
                          color="red darken-3"
                          value="red darken-3"
                          hide-details
                        ></v-checkbox>
                      </v-col>
                      <v-col cols="12" sm="4" md="4">
                        <v-checkbox
                          label="indigo"
                          color="indigo"
                          value="indigo"
                          hide-details
                        ></v-checkbox>
                        <v-checkbox
                          label="indigo darken-3"
                          color="indigo darken-3"
                          value="indigo darken-3"
                          hide-details
                        ></v-checkbox>
                      </v-col>
                      <v-col cols="12" sm="4" md="4">
                        <v-checkbox
                          label="orange"
                          color="orange"
                          value="orange"
                          hide-details
                        ></v-checkbox>
                        <v-checkbox
                          label="orange darken-3"
                          color="orange darken-3"
                          value="orange darken-3"
                          hide-details
                        ></v-checkbox>
                      </v-col>
                    </v-row>

                    <v-row class="mt-12">
                      <v-col cols="12" sm="4" md="4">
                        <v-checkbox
                          label="primary"
                          color="primary"
                          value="primary"
                          hide-details
                        ></v-checkbox>
                        <v-checkbox
                          label="secondary"
                          color="secondary"
                          value="secondary"
                          hide-details
                        ></v-checkbox>
                      </v-col>
                      <v-col cols="12" sm="4" md="4">
                        <v-checkbox
                          label="success"
                          color="success"
                          value="success"
                          hide-details
                        ></v-checkbox>
                        <v-checkbox
                          label="info"
                          color="info"
                          value="info"
                          hide-details
                        ></v-checkbox>
                      </v-col>
                      <v-col cols="12" sm="4" md="4">
                        <v-checkbox
                          label="warning"
                          color="warning"
                          value="warning"
                          hide-details
                        ></v-checkbox>
                        <v-checkbox
                          label="error"
                          color="error"
                          value="error"
                          hide-details
                        ></v-checkbox>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card-text>
              </v-card>
            </v-card>
          </v-dialog>
          <v-dialog
            v-model="showExtraAttributesList"
            transition="dialog-bottom-transition"
            hide-overlay
            fullscreen
            @keydown.esc="showExtraAttributesList = false"
          >
            <v-card>
              <v-toolbar elevation="0">
                <v-btn icon @click="showExtraAttributesList = false">
                  <v-icon>mdi-close</v-icon>
                </v-btn>
                <v-toolbar-title>Доп. признаки</v-toolbar-title>
                <v-spacer />
                <v-btn type="primary" @click="showExtraAttributesList = false">
                  Снять все выделение
                </v-btn>
              </v-toolbar>
              <v-card flat>
                <v-card-text>
                  <v-container fluid>
                    <v-row>
                      <v-col cols="12" sm="4" md="4">
                        <v-checkbox
                          label="red"
                          color="red"
                          value="red"
                          hide-details
                        ></v-checkbox>
                        <v-checkbox
                          label="red darken-3"
                          color="red darken-3"
                          value="red darken-3"
                          hide-details
                        ></v-checkbox>
                      </v-col>
                      <v-col cols="12" sm="4" md="4">
                        <v-checkbox
                          label="indigo"
                          color="indigo"
                          value="indigo"
                          hide-details
                        ></v-checkbox>
                        <v-checkbox
                          label="indigo darken-3"
                          color="indigo darken-3"
                          value="indigo darken-3"
                          hide-details
                        ></v-checkbox>
                      </v-col>
                      <v-col cols="12" sm="4" md="4">
                        <v-checkbox
                          label="orange"
                          color="orange"
                          value="orange"
                          hide-details
                        ></v-checkbox>
                        <v-checkbox
                          label="orange darken-3"
                          color="orange darken-3"
                          value="orange darken-3"
                          hide-details
                        ></v-checkbox>
                      </v-col>
                    </v-row>

                    <v-row class="mt-12">
                      <v-col cols="12" sm="4" md="4">
                        <v-checkbox
                          label="primary"
                          color="primary"
                          value="primary"
                          hide-details
                        ></v-checkbox>
                        <v-checkbox
                          label="secondary"
                          color="secondary"
                          value="secondary"
                          hide-details
                        ></v-checkbox>
                      </v-col>
                      <v-col cols="12" sm="4" md="4">
                        <v-checkbox
                          label="success"
                          color="success"
                          value="success"
                          hide-details
                        ></v-checkbox>
                        <v-checkbox
                          label="info"
                          color="info"
                          value="info"
                          hide-details
                        ></v-checkbox>
                      </v-col>
                      <v-col cols="12" sm="4" md="4">
                        <v-checkbox
                          label="warning"
                          color="warning"
                          value="warning"
                          hide-details
                        ></v-checkbox>
                        <v-checkbox
                          label="error"
                          color="error"
                          value="error"
                          hide-details
                        ></v-checkbox>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card-text>
              </v-card>
            </v-card>
          </v-dialog>
        </v-tab-item>
      </v-tabs-items>
      <v-btn
        block
        color="primary"
        :loading="loading"
        :disabled="searchQuery.trim() === ''"
        @click="search(1)"
      >
        Поиск
      </v-btn>
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
  private extraAttributeList: string[] = [];

  private searchMode: SearchMode = SearchMode.FULL_TEXT;
  private searchLanguage: Language = "RUSSIAN";
  private searchTokenType: TokenType = "WORD";

  private showAttributesList = false;
  private showExtraAttributesList = false;

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
